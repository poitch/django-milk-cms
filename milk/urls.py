from django.urls import path
from django.views.generic import TemplateView
from milk import views

app_name = 'milk'
urlpatterns = [
    path('', views.index, name='post_index'),
    path('post/<uuid:id>', views.post, name='post'),
    path('post/edit/<uuid:id>', views.post_edit, name='post_edit'),
    path('post/delete/<uuid:id>', views.post_delete, name='post_delete'),
    path('post/create', views.post_create, name='post_create'),
    path('media', views.media, name='media_index'),
    path('media/add', views.add_media, name='media_add'),
    path('media/add_api', views.add_media_api, name='media_add_json'),
    path('media/delete/<uuid:id>', views.media_delete, name='media_delete'),
    
    path('pages', views.pages, name='pages'),
    path('pages/add', views.page_add, name='pages_add'),
    path('pages/edit/<uuid:id>', views.pages_edit, name='pages_edit'),
    path('pages/<uuid:id>', views.page, name='page'),
    path('pages/delete/<uuid:id>', views.pages_delete, name='pages_delete'),
]
