from django import forms
from .models import Journal
from .forms import JournalForm

class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ('title', 'content', 'date')
