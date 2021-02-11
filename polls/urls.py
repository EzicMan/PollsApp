from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('vote/', views.vote, name='vote'),
    path('save/', views.save, name='save'),
    path('add/',views.add,name='add'),
    path('<int:question_id>/delete',views.delete, name='delete'),
    path('<int:question_id>/edit',views.edit, name='edit'),
]