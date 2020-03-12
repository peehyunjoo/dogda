from .models import oauth
from django import forms

class oauthForm(forms.ModelForm):
    class Meta:
        model = oauth
        fields = ('id', 'nickname','reg_date')