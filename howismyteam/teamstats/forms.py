from django import forms

from .models import UserPollProfile


class UserPollForm(forms.ModelForm):

    happiness = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=(
            (1, 'Unhappy'), (2, 'Rather unhappy'), (3, 'Neutral'),
            (4, 'Quite happy'), (5, 'Happy'),
        )
    )

    class Meta:
        model = UserPollProfile
        fields = ('happiness', )
