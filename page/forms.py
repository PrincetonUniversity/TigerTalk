from django import forms

from .models import Review

class HorizRadioSelect(forms.RadioSelect):
   template_name = 'page/horizontal_select.html'

class StarRating(forms.RadioSelect):
	template_name = 'star_ratings/widget_base.html'

class PostForm(forms.ModelForm):

    BIN_OPTIONS = (
	    (1, 'Yes'),
	    (0, 'No'),
    )

    STARS = (
    	(1, '1'),
    	(2, '2'),
    	(3, '3'),
    	(4, '4'),
    	(5, '5'),
    )

    fun = forms.ChoiceField(widget=HorizRadioSelect, choices=BIN_OPTIONS)
    meaningful = forms.ChoiceField(widget=HorizRadioSelect, choices=BIN_OPTIONS)
    stars = forms.ChoiceField(widget=HorizRadioSelect, choices=STARS)

    class Meta:
        model = Review
        fields = ('text', 'fun', 'meaningful', 'stars', 'CBI',)