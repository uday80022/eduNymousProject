from django.urls import path
from . import views

app_name='curriculum'
urlpatterns = [

    path('', views.StandardListView.as_view(), name='standard_list'),
    path('<slug:slug>', views.StandardLearningListView.as_view(), name='learning_list'),
    path('<slug:slug>/', views.SubjectListView.as_view(), name='subject_list'),
    path('<slug:slug>/create', views.SubjectCreateListView.as_view(), name='subject_create'),
    path('<str:standard>/<slug:slug>/', views.LessonListView.as_view(), name='lesson_list'),
    path('<str:standard>/<str:slug>/create/', views.LessonCreateView.as_view(),name='lesson_create'),
    path('<str:standard>/<str:subject>/<slug:slug>/', views.LessonDetailView.as_view(),name='lesson_detail'),
    # added  238a5d15bfcbb7c83b5b0f9addb11631
    path('<str:standard>/<str:subject>/<slug:slug>/form', views.LessonDetailView.as_view(),name='lesson_form'),
    # path('<str:standard>/<str:subject>/<slug:slug>/update/', views.LessonUpdateView.as_view(),name='lesson_update'),
    path('<str:standard>/<str:subject>/<slug:slug>/238a5d15bfcbb7c83b5b0f9addb11631/', views.LessonUpdateView.as_view(),name='lesson_update'),
    path('<str:standard>/<str:subject>/<slug:slug>/8b18058289f183aa28306883cb658b24/', views.LessonDeleteView.as_view(),name='lesson_delete'),

]
