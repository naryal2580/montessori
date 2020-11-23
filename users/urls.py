from django.urls import path
from . import views
from django.views.generic import TemplateView
app_name = "auth"

urlpatterns = [
    path('', views.LoginView.as_view(), name="login"),
    path('/logout', views.logout_view, name="logout" ),
    path("/profile", views.ProfileView.as_view(), name="student_profile")

]
