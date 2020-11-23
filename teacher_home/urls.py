from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    path('', views.TeacherAssignmentDashboard.as_view(), name='assignment'),
    path('/add', views.AddAssignmentView.as_view(), name='add_assignment'),
    path('/<str:slug>', views.SubmissionView.as_view(), name='submissions'),
    path('/<str:slug>/delete', views.delete_assignment, name='delete_assignment')
    
]
