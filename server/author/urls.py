from django.urls import path

from author import views

app_name = 'author'

urlpatterns = [
    path('create/', views.CreateAuthorView.as_view(), name='create'),
    path('auth/', views.AuthAuthorView.as_view(), name='auth'),
    path('<slug:pk>/', views.AuthorProfileView.as_view(), name = 'authors'),
]