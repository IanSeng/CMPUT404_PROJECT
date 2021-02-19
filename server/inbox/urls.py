from django.urls import path

from inbox import views

app_name = 'inbox'

urlpatterns = [
    path('<uuid:author_id>/inbox/', views.InboxView.as_view(), name='inbox')
]
