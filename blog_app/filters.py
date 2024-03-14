import django_filters
from .models import blogdata


# class BlogDataFilter(django_filters.FilterSet):
#     search = django_filters.CharFilter(method='custom_search')

#     class Meta:
#         model = blogdata
#         fields = []

#     def custom_search(self, queryset, name, value):
#         return queryset.filter(
#             models.Q(title__icontains=value) |
#             models.Q(publication_date__icontains=value) |
#             models.Q(category__name__icontains=value)
#         ).distinct()



class BlogDataFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    likes = django_filters.CharFilter(field_name='likes__username', lookup_expr='icontains')
    publication_date = django_filters.DateFilter(field_name='publication_date', lookup_expr='exact')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    class Meta:
        model = blogdata
        fields = ['title', 'likes', 'publication_date', 'category']


