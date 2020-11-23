from django.urls import path
from . import views

app_name = "assignment"

urlpatterns = [
    path('', views.AssignmentView.as_view(), name="home"),
    path('/<str:slug>', views.AssignmentDetailView.as_view(), name="details"),
    path('/<str:question_slug>/add', views.SubmitAssignmentView.as_view(), name="submit_answer"),
    path('/deleteSubmission/<str:slug>', views.deleteAssignment, name='delete_submission')

]
