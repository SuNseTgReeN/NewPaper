from django.forms import DateInput
from django_filters import FilterSet, ModelChoiceFilter, DateFilter, CharFilter

from .models import Category


class ProductFilter(FilterSet):
    # поиск по тэгу
    category = ModelChoiceFilter(
        field_name='postcategory__category_through',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label=''
    )
    # Поиск по дате создания поста (Ищет все посты ДО указанной даты)
    DateCreation = DateFilter(
        field_name='date_creation',
        lookup_expr='gte',
        label='Пост создан после:',
        widget=DateInput(attrs={'type': 'date'})
    )
    # поиск по названию
    Title = CharFilter(
        lookup_expr='icontains',
        label='Название поста',
    )

