from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile  # Import the UserProfile model


class CreateNewUser(UserCreationForm):
    email = forms.EmailField(required=True, label="", widget=forms.EmailInput(attrs={
        'placeholder': "Email"
    }))
    
    username = forms.CharField(required=True, label="", widget=forms.TextInput(attrs={
        'placeholder': "Username"
    }))
    
    full_name = forms.CharField(required=True, label="", widget=forms.TextInput(attrs={
        'placeholder': "Full Name"
    }))

    password1 = forms.CharField(required=True, label="", widget=forms.PasswordInput(attrs={
        'placeholder': "Password"
    }))
   
    password2 = forms.CharField(required=True, label="", widget=forms.PasswordInput(attrs={
        'placeholder': "Confirm Password"
    }))

    # Additional fields
    dob = forms.DateField(required=True, label="", widget=forms.DateInput(attrs={
        'type': 'date',
        'placeholder': "Date of Birth"
    }))
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = forms.ChoiceField(required=True, choices=GENDER_CHOICES, label="", widget=forms.Select(attrs={
        'placeholder': "Gender"
    }))

    class Meta:
        model = User
        fields = ('full_name', 'email', 'username', 'password1', 'password2', 'dob', 'gender')

    def save(self, commit=True):
        # Save the User instance first
        user = super().save(commit=commit)
        
        # Save the profile fields
        full_name = self.cleaned_data.get('full_name')
        dob = self.cleaned_data.get('dob')
        gender = self.cleaned_data.get('gender')
        

        # Create or update the UserProfile instance
        UserProfile.objects.update_or_create(
            user=user,
            defaults={'full_name':full_name, 'dob': dob, 'gender': gender}
        )
        
        return user

class EditProfile(forms.ModelForm):
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'style':'height:120px',
        'label':""
    }))
    class Meta:
        model = UserProfile
        exclude = ('user',)

