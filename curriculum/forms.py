from django import forms
from .models import Comment, Reply, Lesson,Subject


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        # fields = ('standard','subject_id','name','slug','image','description')
        # fields = ('standard','subject_id','name','sem','image','description')
        fields = ('standard','name','sem','image','description')

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('lesson_id','name','position','video','ppt','Notes')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

        labels = {"body":"Anonymous "}

        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control', 'rows':4, 'cols':70, 'placeholder':"Enter Here"}),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('reply_body',)

        widgets = {
            'reply_body': forms.Textarea(attrs={'class':'form-control', 'rows':2, 'cols':10,'placeholder':"Enter Anonymously"}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ReplyForm, self).__init__(*args, **kwargs)
