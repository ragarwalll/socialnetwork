from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'username', 'password1', 'password2', )


class checkemail(forms.Form):
    email = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Enter email', 'class': 'user'}))

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            raise forms.ValidationError('Email does not exists.')

        # A user was found with this as a username, raise an error.
