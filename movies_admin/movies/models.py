import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class TimeStampMixin(models.Model):
    # auto_now_add автоматически выставит дату создания записи
    created = models.DateTimeField(auto_now_add=True)
    # auto_now изменятся при каждом обновлении записи
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        # Этот параметр указывает Django, что этот класс не является представлением таблицы
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(default=uuid.uuid4(), primary_key=True, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampMixin):
    def __str__(self):
        return self.name
    # Типичная модель в Django использует число в качестве id.
    # В таких ситуациях поле не описывается в модели.
    # Первым аргументом обычно идёт человекочитаемое название поля
    name = models.CharField('name', max_length=255)
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField('description', blank=True)

    class Meta:
        db_table = "content\".\"genre"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Person(UUIDMixin, TimeStampMixin):

    def __str__(self):
        return self.full_name

    full_name = models.TextField("full_name", blank=False)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = "Участник фильма"


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

    title = models.TextField()
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(blank=True, validators=[MinValueValidator(0),
                                                       MaxValueValidator(100)])
    type = models.CharField('type', choices=FilmWorkTypes.choices, max_length=10)
    genre = models.ManyToManyField(Genre, through="GenreFilmWork")
    persons = models.ManyToManyField(Person, through='PersonFilmWork')


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = "Жанры фильма"


class PersonFilmWork(UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = "Участники фильма"
