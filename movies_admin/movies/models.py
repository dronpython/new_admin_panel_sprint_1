import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


# Create your models here.
class TimeStampMixin(models.Model):
    # auto_now_add автоматически выставит дату создания записи
    created = models.DateTimeField(_("created"), auto_now_add=True)
    # auto_now изменятся при каждом обновлении записи
    modified = models.DateTimeField(_("modified"), auto_now=True)

    class Meta:
        # Этот параметр указывает Django, что этот класс не является представлением таблицы
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(_("id"), default=uuid.uuid4(), primary_key=True, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampMixin):
    def __str__(self):
        return self.name
    # Типичная модель в Django использует число в качестве id.
    # В таких ситуациях поле не описывается в модели.
    # Первым аргументом обычно идёт человекочитаемое название поля
    name = models.CharField(_('name'), max_length=255)
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        db_table = "content\".\"genre"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Person(UUIDMixin, TimeStampMixin):

    def __str__(self):
        return self.full_name

    full_name = models.TextField(_('description'), blank=False)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = 'Участник фильма'


# ToDo: add foreign keys
# ToDo: delete creation_date?
class FilmWork(UUIDMixin, TimeStampMixin):

    def __str__(self):
        return self.title

    class FilmWorkTypes(models.TextChoices):
        tv_show = 'tv_show'
        movie = 'movie'

    class Meta:
        db_table = "content\".\"film_work"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    title = models.TextField(_('title'), blank=False)
    description = models.TextField(_('description'), blank=True, null=True,)
    creation_date = models.DateTimeField(_('creation_date'), blank=True, null=True,)
    rating = models.FloatField(_('rating'),
                               blank=True,
                               validators=[MinValueValidator(0), MaxValueValidator(100)],
                               null=True)
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')
    type = models.CharField(_('type'), choices=FilmWorkTypes.choices, max_length=255)
    genre = models.ManyToManyField(Genre, through="GenreFilmWork")
    persons = models.ManyToManyField(Person, through='PersonFilmWork')


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = "Жанры фильма"


class PersonFilmWork(UUIDMixin):
    class PersonRoles(models.TextChoices):
        actor = 'actor'
        director = 'director'
        screenwriter = 'screenwriter'

    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField(_('role'), choices=PersonRoles.choices, max_length=100)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = 'Участники фильма'
