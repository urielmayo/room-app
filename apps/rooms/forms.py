from django import forms
from .models import Room


class RoomForm(forms.ModelForm):
    """Form definition for Room."""

    class Meta:
        """Meta definition for Roomform."""

        model = Room
        fields = ('name',)
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}
