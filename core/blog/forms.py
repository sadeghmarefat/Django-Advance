from django import forms
from .models import Contact, Post


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = '__all__'


class CreateForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ['image', 'author']
        widgets = {
            'published_at': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            )
        }