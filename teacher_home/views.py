from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from assignment.models import AssignmentQuestion, AssignmentSubmission
from django.db.models import Count
from . import forms
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import get_object_or_404
class TeacherAssignmentDashboard(UserPassesTestMixin, LoginRequiredMixin, View):

    def test_func(self):
        return self.request.user.is_teacher

    def get(self, request):
        context = dict()
        assignments = AssignmentQuestion.objects.filter(
            subject__in=request.user.teacher.subject.all()).annotate(num=Count('assignmentsubmission'))
        context['assignments'] = assignments
        return render(request, "assignment_dash.html", context)


class AddAssignmentView(UserPassesTestMixin, LoginRequiredMixin, View):

    def test_func(self):
        return self.request.user.is_teacher

    def get(self, request):
        context = dict()
        subjects = request.user.teacher.subject.all()
        form = forms.AssignmentQuestionForm(subjects=subjects)
        context['form'] = form
        return render(request, "add_assignment.html", context)

    def post(self, request):
        subjects = request.user.teacher.subject.all()
        submitted_form = forms.AssignmentQuestionForm(
            subjects=subjects, data=request.POST, files=request.FILES)
        if submitted_form.is_valid():
            title = submitted_form.cleaned_data['title']
            description = submitted_form.cleaned_data['description']
            subject = submitted_form.cleaned_data['subject']
            due_date = submitted_form.cleaned_data['due_date']
            question_file = submitted_form.cleaned_data['question_file']
            given_by = self.request.user.teacher

            assignment = AssignmentQuestion(title=title, description=description, subject_id=int(subject),
                                            due_date=due_date, given_by=given_by, question_file=question_file)

            assignment.save()

            return redirect('teacher:assignment')


class SubmissionView(UserPassesTestMixin, LoginRequiredMixin, View):

    def test_func(self):
        return self.request.user.is_teacher

    def get(self, request, slug):
        context = dict()
        
        assignment = get_object_or_404(AssignmentQuestion, slug=slug,  subject__in=request.user.teacher.subject.all() )


        
        submissions = AssignmentSubmission.objects.filter(
            question__slug=slug, question__subject__in=request.user.teacher.subject.all())

        context['assignment'] = assignment

        context['subs'] = submissions

        return render(request, "submission_list.html", context)

@user_passes_test(test_func= lambda u: u.is_teacher)
@login_required
def delete_assignment(request, slug):
    assignment = get_object_or_404(AssignmentQuestion,  slug=slug, subject__in=request.user.teacher.subject.all() )
    assignment.question_file.delete()
    assignment.delete()

    return redirect("teacher:assignment")

