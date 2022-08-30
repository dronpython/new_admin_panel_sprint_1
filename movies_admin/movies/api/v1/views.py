from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.core.paginator import Paginator
from movies.models import FilmWork


class MoviesApiMixin:
    def get_queryset(self):
        query = FilmWork.objects.all().values("id", "title", "description", "creation_date")
        return query  # Сформированный QuerySet

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    model = FilmWork
    http_method_names = ['get']  # Список методов, которые реализует обработчик
    paginate_by = 5


    def get_queryset(self):
        query = FilmWork.objects.all().values("id", "title", "description", "creation_date")
        return query  # Сформированный QuerySet

    # def paginate_queryset(self, queryset, paginate_by):
    #     p = Paginator(queryset, paginate_by)
    #     return p, p.num_pages, queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        page = self.kwargs.get('page', 1)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)
        result = list(paginator.page(page).object_list)

        if paginator.page(page).has_next():
            next_page = paginator.page(page).next_page_number()
        else:
            next_page = page

        if paginator.page(page).has_previous():
            prev_page = paginator.page(page).previous_page_number()
        else:
            prev_page = page

        context = {
            'results': result,
            'count': len(result),
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
        context = {"results": data}
        return context

