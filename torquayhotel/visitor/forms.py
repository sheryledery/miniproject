from django.contrib.auth.forms import UserCreationForm
from django import forms


class MyUserCreationForm(UserCreationForm):
    picture = forms.URLField()
    nickname = forms.CharField(max_length=30)

class AvailabilityForm(forms.Form):
    ROOM_CATEGORIES=(
        ('ST', 'STANDARD'),
        ('DEL', 'DELUXE'),
        ('SUI', 'SUITE'),
    )
    room_category = forms.ChoiceField(choices=ROOM_CATEGORIES, required=True)
    check_in = forms.DateField(required=True, input_formats=["%Y-%m-%d"])
    check_out = forms.DateField(required=True, input_formats=["%Y-%m-%d"])