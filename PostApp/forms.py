from django import forms
from .models import Post
class PostForm(forms.ModelForm):
    caption = forms.CharField(label="", widget=forms.Textarea(attrs={
        'style':'height:90px'
    }))
    
    image = forms.ImageField(label="", widget=forms.ClearableFileInput(attrs={
        'class': 'mb-2',
    }))
    class Meta:
        model = Post
        fields = ['caption', 'image',]
        