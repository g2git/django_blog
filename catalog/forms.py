import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Comment

class CommentForm(forms.ModelForm):
    #comment = forms.CharField(help_text="Enter a comment about this blog post")

    # def clean_comment(self):
    #     data = self.cleaned_data['comment']

        # Remember to always return the cleaned data.
        # return data
    
    class Meta:
        model = Comment
        fields = ['content']
