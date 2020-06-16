from django.urls import path
from . import views


urlpatterns = [
    path('singup', views.sign_up, name='signup'),
    path('login', views.log_in, name='login'),
    path('', views.get_all_lists),
    path('<int:sicklist_id>/', views.get_list, name='sicklist_by_id'),
    path('<int:sicklist_id>/create_record', views.create_record, name='create_record'),
]
