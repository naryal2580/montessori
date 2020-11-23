from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class AssignmentSubmissionForm(forms.Form):
    answer_text = forms.CharField(widget=CKEditorUploadingWidget(), required=False)
    answer_file = forms.FileField(label="Answer File", required=False)
