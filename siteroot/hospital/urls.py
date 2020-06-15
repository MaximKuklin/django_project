from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_lists),
    path('<int:list_id>/', views.get_list, name='sicklist_by_id'),
    path('<int:blog_id>/create_record', views.create_record, name='create_record'),
]
