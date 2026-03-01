from django.urls import path

from . import views


urlpatterns = [
    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("resend-verification", views.resend_verification_view, name="resend-verification"),
    path("verify/<uuid:token>", views.verify_email_view, name="verify-email"),
    path("me", views.me_view, name="me"),
]
