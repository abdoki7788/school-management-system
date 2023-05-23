from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm, UserCreationForm as BaseUserCreationForm

User = get_user_model()


class UserCreationForm(BaseUserCreationForm):
    identity = forms.CharField(max_length=11, label="شناسه")

    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ('identity', 'full_name')

class UserChangeForm(BaseUserChangeForm):
    pass