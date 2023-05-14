from django.urls import path
from .views import PostList, PostDetail, SearchList, PostCreate, PostUpdate, PostDelete, upgrade_me, CategoryListView, \
    subscribe

app_name = 'news'

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('search/', SearchList.as_view(), name='search'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]
