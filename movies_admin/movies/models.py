import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


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
    name = models.CharField(_('name'), max_length=255)
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')


class Person(UUIDMixin, TimeStampMixin):

    def __str__(self):
        return self.full_name

    full_name = models.TextField(_('description'), blank=False)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')


class FilmWork(UUIDMixin, TimeStampMixin):

    def __str__(self):
        return self.title

    class FilmWorkTypes(models.TextChoices):
        tv_show = _('tv_show')
        movie = _('movie')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Movie')
        verbose_name_plural = _('Movies')
        indexes = [
            models.Index(fields=['creation_date'], name='film_work_creation_date_idx'),
        ]

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
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _("Film's genres")
        constraints = [models.UniqueConstraint(fields=['film_work_id', 'genre_id'],
                                               name='film_work_genre_idx')]
        indexes = [
            models.Index(fields=['film_work'], name='film_work_fk_idx'),
            models.Index(fields=['genre'], name='genre_fk_idx'),

        ]


class PersonFilmWork(UUIDMixin):
    class PersonRoles(models.TextChoices):
        actor = _('actor')
        director = _('director')
        screenwriter = _('screenwriter')

    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(_('role'), choices=PersonRoles.choices, max_length=100)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        db_table = 'content\".\"person_film_work'
        verbose_name = _('Film crew')
