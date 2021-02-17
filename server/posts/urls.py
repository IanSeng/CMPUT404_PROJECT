from django.urls import path

from posts import views

app_name = 'posts'

urlpatterns = [
    path('<uuid:author_id>/posts/', views.CreatePostView.as_view(), name='create'),
    path('<uuid:author_id>/posts/<uuid:pk>', views.UpdatePostView.as_view(), name='view')
] 