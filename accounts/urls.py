from django.urls import path
from .views import RegisterView, LoadUserView, UpdatePasswordView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('user', LoadUserView.as_view()),
    path('update', UpdatePasswordView.as_view())
]
