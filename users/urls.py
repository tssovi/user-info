from django.urls import path

from users.views import UsersView


urlpatterns = [
    path('user/', UsersView.as_view(), name='user-info-api'),
]
