from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('delete/<int:note_id>/', views.delete_note, name='delete_note'),
    path('tags/', views.tag_list, name='tag_list'),
    re_path(r'^tags/(?P<tag_name>[\w-]+)/$', views.tag_detail, name='tag_detail'),
    path('tag-suggestions/', views.tag_suggestions, name='tag_suggestions'),
]
