from django.urls import path

from author import views

app_name = 'author'

urlpatterns = [
    path('create/', views.CreateAuthorView.as_view(), name='create')
]