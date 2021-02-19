from django.urls import path

from inbox import views

app_name = 'inbox'

urlpatterns = [
    path('<uuid:inboxAuthorID>/inbox/', views.InboxView.as_view(), name='inbox')
]
