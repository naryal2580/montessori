from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class AssignmentQuestionForm(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=CKEditorUploadingWidget())
    subject = forms.ChoiceField(choices=[])
    due_date = forms.DateField(widget=forms.SelectDateWidget())
    question_file = forms.FileField()

    def __init__(self, subjects, *args, **kwargs):
        super(AssignmentQuestionForm, self).__init__(*args, **kwargs)
        self.fields['subject'].choices = [ (sub.pk, sub.name) for sub in subjects ]