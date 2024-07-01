# myapp/forms.py

from django import forms

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}), label='')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), label='')