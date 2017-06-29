from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from invoice import models


class ProfileCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = models.Profile


class ProfileChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = models.Profile
