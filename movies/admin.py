from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Filmwork, Genre, GenreFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class RatingListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Рейтинг')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return (
            ('0', _('0-10')),
            ('1', _('10-20')),
            ('2', _('20-30')),
            ('3', _('30-40')),
            ('4', _('40-50')),
            ('5', _('50-60')),
            ('6', _('60-70')),
            ('7', _('70-80')),
            ('8', _('80-90')),
            ('9', _('90-100')),
        )

    def queryset(self, request, queryset):
        low_level = int(self.value()) * 10
        high_level = low_level + 10
        return queryset.filter(
            rating__gte=low_level,
            rating__lte=high_level,
        )


class TypeListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Тип')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        return (
            ('movie', _('Фильм')),
            ('show', _('Шоу')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'movie':
            return queryset.filter(type='movie')
        if self.value() == 'show':
            return queryset.filter(type='tv_show')


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline,)
    list_display = ('title', 'type', 'creation_date', 'rating')
    list_filter = (TypeListFilter, RatingListFilter)
    # Поиск по полям
    search_fields = ('title', 'description', 'id')
