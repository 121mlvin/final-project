from django.urls import path
from . import views
from knox import views as knox_views

urlpatterns = [
    path('rest-data/', views.get_data),
    path('rest-data-detail/<str:pk>/', views.get_data_detail),
    path('rest-data/add/', views.add_item),
    path('rest-data/edit/<str:pk>/', views.edit_item),
    path('rest-data/delete/<str:pk>/', views.delete_item),
    path('rest-login/', views.login_api),
    path('rest-user/', views.get_user_data),
    path('rest-register/', views.register_api),
    path('rest-logout/', knox_views.LogoutView.as_view()),
    path('rest-data-by-status/<str:status>/', views.get_data_detail_by_status)



]
