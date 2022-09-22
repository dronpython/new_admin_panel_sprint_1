from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.core.paginator import Paginator
from django.contrib.postgres.aggregates import ArrayAgg
from movies.models import FilmWork


class MoviesApiMixin:
    def get_queryset(self):
        query = FilmWork.objects.annotate(genres=ArrayAgg("genre__name", distinct=True),
                                          actors=ArrayAgg("persons__full_name",
                                                          distinct=True,
                                                          filter=Q(personfilmwork__role="actor")),
                                          directors=ArrayAgg("persons__full_name",
                                                             distinct=True,
                                                             filter=Q(personfilmwork__role="director")),
                                          writers=ArrayAgg("persons__full_name",
                                                           distinct=True,
                                                           filter=Q(personfilmwork__role="writer")
                                          )).values()
        return query

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    model = FilmWork
    http_method_names = ['get']  # Список методов, которые реализует обработчик
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        page = self.request.GET.get('page', 1)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)
        if page == "last":
            page = paginator.num_pages
        result = list(paginator.page(page).object_list)

        if paginator.page(page).has_next():
            next_page = paginator.page(page).next_page_number()
        else:
            next_page = None

        if paginator.page(page).has_previous():
            prev_page = paginator.page(page).previous_page_number()
        else:
            prev_page = None

        context = {
            'results': result,
            'count': len(queryset),
            'prev': prev_page,
            'next': next_page,
            'total_pages': paginator.num_pages
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseListView):

    def __init__(self):
        super(MoviesApiMixin).__init__()

    def get_context_data(self, **kwargs):
        uuid = self.kwargs.get('pk', None)  # получаем аргумент из ссылки
        data = self.get_queryset().get(id=uuid)
        return data
