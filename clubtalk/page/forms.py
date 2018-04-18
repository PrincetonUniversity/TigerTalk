from django import forms

from .models import Review

FUN_OPTIONS = (
	(1, 'Yes'),
	(0, 'No'),
)

class PostForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('text', 'fun', 'meaningful', 'stars', 'CBI',)
        widgets = {
            'fun': forms.RadioSelect()
        }