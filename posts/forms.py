from django import forms
from .models import Contact, Post, Comment


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
