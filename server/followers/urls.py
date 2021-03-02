from django.urls import path

from followers import views

app_name = 'followers'

urlpatterns = [
    path('<slug:id>/followers/', views.FollowersView.as_view(), name='followers'),
    path('<slug:id>/followers/<slug:foreignId>/', views.FollowersModificationView.as_view(), name="followers modify")
]