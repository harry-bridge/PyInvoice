from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from invoice import models


class ProfileCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = models.Profile


class ProfileChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = models.Profile


class FileUploadForm(forms.Form):
    file_source = forms.FileField()


class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('invoice_logo', )
