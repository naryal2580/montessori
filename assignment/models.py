from django.db import models
from grade.models import Subject
from users.models import Student, Teacher
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
import uuid

class AssignmentQuestion(models.Model):
    slug = models.CharField(max_length=150, blank=True)
    title = models.CharField(max_length=255)
    description = RichTextUploadingField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    due_date = models.DateField(null=True, blank=True)
    given_date = models.DateField(auto_now=True)
    given_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    question_file = models.FileField(
        upload_to="assignments/", null=True, blank=True)
    # THOUGHT: MAYBE SELF WRITTEN DELETE METHOD

    def __str__(self):
        return f"{self.title} - {self.subject.name} - {self.subject.grade.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(AssignmentQuestion, self).save(*args, **kwargs)


class AssignmentSubmission(models.Model):

    slug = models.CharField(max_length=150, blank=True)
    question = models.ForeignKey(AssignmentQuestion, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submitted_at = models.DateField(auto_now=True)
    answer_text = RichTextUploadingField()
    answer_file = models.FileField(upload_to="answers/", null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.answer_text[:5]) + uuid.uuid4().hex
        super(AssignmentSubmission, self).save(*args, **kwargs)
