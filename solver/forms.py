from django import forms

class WordleSolverForm(forms.Form):
    guess = forms.CharField(widget=forms.Textarea, required=False)