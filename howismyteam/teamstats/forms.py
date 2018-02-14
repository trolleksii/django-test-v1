from django import forms

from .models import PollProfile


class UserPollForm(forms.ModelForm):

    HAPPINESS_CHOICES = (
        (1, 'Unhappy'), (2, 'Rather unhappy'), (3, 'Neutral'),
        (4, 'Quite happy'), (5, 'Happy'),
    )

    happiness = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=HAPPINESS_CHOICES
    )

    class Meta:
        model = PollProfile
        fields = ('happiness', )
