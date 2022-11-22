from django.urls import path
from . import views

app_name = 'postings'

urlpatterns = [
    path('', views.index, name='index'),
    path('postings/', views.posting_list, name='posting_list'),
    path('posting/create/', views.posting_create, name='posting_create'),
    path('posting/<int:posting_id>/', views.posting_detail, name='posting_detail'),
    path('posting/<int:posting_id>/update/', views.posting_update, name='posting_update'),
    path('posting/<int:posting_id>/delete/', views.posting_delete, name='posting_delete'),
    path('posting/<int:posting_id>/comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
]
