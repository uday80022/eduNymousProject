from django.urls import path
from app_users import views


# app_name = 'app_users'
urlpatterns = [
    path('',views.HomeView.as_view(),name='index'),
    path('home/',views.home_view.as_view(),name='home'),
    path('register/', views.register, name='register'),
    path('explain/', views.secretkey, name='secretkey'),
    path('user_login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('contact/', views.ContactView.as_view(), name="contact"),
    path('report/', views.report, name='report'),
    path('changepassword/',views.change_password,name='change_password'),
    path('add-class/',views.add_class,name='add_class'),
]
