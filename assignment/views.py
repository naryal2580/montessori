from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from assignment.models import AssignmentQuestion, AssignmentSubmission
from django.db.models import Count, Q
from . import models
from django.http import HttpResponse
from . import forms
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.http import Http404
class AssignmentView(UserPassesTestMixin, LoginRequiredMixin, View):

    def test_func(self):
        return self.request.user.is_student

    def get(self, request):

        context = {'page_title': "Assignments"}

        if request.user.is_student:
            assignments = AssignmentQuestion.objects.filter(subject__grade=request.user.student.grade).annotate(
                submitted=Count('assignmentsubmission', filter=Q(assignmentsubmission__student=request.user.student)))

            context['assignments'] = assignments

        return render(request, "assignment_list.html", context)


class AssignmentDetailView(UserPassesTestMixin, LoginRequiredMixin, View):

    def test_func(self):
        return self.request.user.is_student


    def get(self, request, slug):
        assignment = AssignmentQuestion.objects.filter(slug=slug, subject__grade=request.user.student.grade).first()
        if not assignment:
            raise Http404('Not found!')
        submitted = AssignmentSubmission.objects.filter(question=assignment, student=request.user.student).first()
        print(assignment.due_date)
        print(datetime.date(datetime.now()))
        return render(request, 'assignment_details.html', { 'assignment' : assignment, 'submission' : submitted, 'date' : datetime.date(datetime.now()) })

class SubmitAssignmentView(UserPassesTestMixin, LoginRequiredMixin, View):

    def test_func(self):
        return self.request.user.is_student

    def get(self, request, question_slug):

        current_assignment = AssignmentSubmission.objects.filter(question__slug=question_slug, student=request.user.student).first()
        if current_assignment:
            return HttpResponse(status=400)
        form = forms.AssignmentSubmissionForm()
        context = dict()
        context['form'] = form
        context['date'] = datetime.date(datetime.now())

        
        return render(request, "submit_assignment.html", context)

    def post(self, request, question_slug):
        current_assignment = AssignmentSubmission.objects.filter(question__slug=question_slug, student=request.user.student).first()
        if current_assignment:
            return HttpResponse(status=400)
        question = get_object_or_404(AssignmentQuestion, slug=question_slug)
        
        answer = forms.AssignmentSubmissionForm(request.POST, request.FILES)
        curr_date = datetime.date(datetime.now())
        due_date = question.due_date

        print(curr_date <= due_date)

        if answer.is_valid() and curr_date <= due_date:
            student = request.user.student;
            answer_file = answer.cleaned_data['answer_file']
            answer_text = answer.cleaned_data['answer_text']

            print(request)
            
            submission = AssignmentSubmission(question=question,student=student,answer_text=answer_text,answer_file=answer_file)
            submission.save()

            messages.add_message(request, 10, "Your Assignment has been submitted!");
            return redirect("assignment:details", slug=question_slug);

        else:
            return HttpResponse(status=401)

@user_passes_test(test_func=lambda u: u.is_student )
@login_required()
def deleteAssignment(request, slug):
    assignment = get_object_or_404(AssignmentSubmission, student=request.user.student, slug=slug )
    
    question_slug = assignment.question.slug
    if assignment.answer_file:
        assignment.answer_file.delete()
    assignment.delete();
    messages.add_message(request,level=33,message="Succesfully deleted!", extra_tags="alert-success");
    return redirect("assignment:details", slug=question_slug);
