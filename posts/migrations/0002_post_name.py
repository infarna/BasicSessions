# Generated by Django 3.0.6 on 2020-05-28 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='name',
            field=models.TextField(default='<django.db.models.fields.related.ForeignKey>1'),
        ),
    ]
