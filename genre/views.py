from django.contrib import messages
from django.contrib.auth.mixins import(LoginRequiredMixin,PermissionRequiredMixin)
from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from . models import Genre, GenreFellow


from posts.models import Post
from django.views import View
from django.shortcuts import render


class CreateGenre(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description")
    model = Genre


class SingleGenre(View):

    def get(self, request, *args, **kwargs):
        genre_opened = get_object_or_404(Genre,slug=self.kwargs.get("slug"))
        post_to_displayed = []
        for item in Post.objects.all():
            if str(item.genre) == str(genre_opened.name):
                post_to_displayed.append(item)
        return render(request, 'genre/genre_detail.html',
                      {'post_list': post_to_displayed, 'genre': genre_opened})



class ListGenre(generic.ListView):
    model = Genre


class JoinGenre(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("genre:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        genre = get_object_or_404(Genre,slug=self.kwargs.get("slug"))

        try:
            GenreFellow.objects.create(user=self.request.user,genre=genre)

        except IntegrityError:
            messages.warning(self.request,("Warning, already a fellow of {}".format(genre.name)))

        else:
            messages.success(self.request,"You are now a fellow of the {} genre.".format(genre.name))

        return super().get(request, *args, **kwargs)


class LeaveGenre(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("genre:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        try:
            fellowship = GenreFellow.objects.filter(
                user=self.request.user,
                genre__slug=self.kwargs.get("slug")
            ).get()
        except GenreFellow.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this genre because you aren't in it."
            )
        else:
            fellowship.delete()
            messages.success(
                self.request,
                "You have successfully left this genre."
            )
        return super().get(request, *args, **kwargs)
