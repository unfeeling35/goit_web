from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path('tag/<int:tag_id>/', views.quotes_by_tag, name='quotes_by_tag'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('add-quote/', views.add_quote, name='add_quote'),
    path('add-author/', views.add_author, name='add_author'),
]