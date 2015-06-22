from django import forms

class PostForm(forms.Form):
    name = forms.CharField(max_length=30)
    short_name = forms.CharField(max_length=3)
    description = forms.CharField(max_length=40)
