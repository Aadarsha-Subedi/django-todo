from django.urls import path

from . import views

urlpatterns = [
    path("", views.signup, name="signup"),
    path("verify/", views.verify_signup, name="verify"),
    path("login/", views.login, name="login")
]
