# Generated by Django 3.2 on 2022-08-16 20:02

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FilmWork',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.UUID('1f7bc2fb-bf92-472e-8cc3-62b29bb85bf7'), editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('title', models.TextField(verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('creation_date', models.DateTimeField(blank=True, null=True, verbose_name='creation_date')),
                ('rating', models.FloatField(blank=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='rating')),
                ('file_path', models.FileField(blank=True, null=True, upload_to='movies/', verbose_name='file')),
                ('type', models.CharField(choices=[('tv_show', 'Tv Show'), ('movie', 'Movie')], max_length=255, verbose_name='type')),
            ],
            options={
                'verbose_name': 'Фильм',
                'verbose_name_plural': 'Фильмы',
                'db_table': 'content"."film_work',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.UUID('1f7bc2fb-bf92-472e-8cc3-62b29bb85bf7'), editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'db_table': 'content"."genre',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.UUID('1f7bc2fb-bf92-472e-8cc3-62b29bb85bf7'), editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('full_name', models.TextField(verbose_name='description')),
            ],
            options={
                'verbose_name': 'Участник фильма',
                'db_table': 'content"."person',
            },
        ),
        migrations.CreateModel(
            name='PersonFilmWork',
            fields=[
                ('id', models.UUIDField(default=uuid.UUID('1f7bc2fb-bf92-472e-8cc3-62b29bb85bf7'), editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('role', models.CharField(choices=[('actor', 'Actor'), ('director', 'Director'), ('screenwriter', 'Screenwriter')], max_length=100, verbose_name='role')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('film_work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.person')),
            ],
            options={
                'verbose_name': 'Участники фильма',
                'db_table': 'content"."person_film_work',
            },
        ),
        migrations.CreateModel(
            name='GenreFilmWork',
            fields=[
                ('id', models.UUIDField(default=uuid.UUID('1f7bc2fb-bf92-472e-8cc3-62b29bb85bf7'), editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('film_work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.genre')),
            ],
            options={
                'verbose_name': 'Жанры фильма',
                'db_table': 'content"."genre_film_work',
            },
        ),
        migrations.AddField(
            model_name='filmwork',
            name='genre',
            field=models.ManyToManyField(through='movies.GenreFilmWork', to='movies.Genre'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(through='movies.PersonFilmWork', to='movies.Person'),
        ),
    ]
