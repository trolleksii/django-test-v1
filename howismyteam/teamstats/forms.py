from re import sub

from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField

from .models import HappyTeamUser, Team


class HappyUserCreationForm(UserCreationForm):

    class Meta:
        model = HappyTeamUser
        fields = ('username', 'password1', 'password2', 'team')
        field_classes = {'username': UsernameField}

    add_new_team = forms.CharField(max_length=256, required=False)

    def clean(self):
        team = self.cleaned_data.get('team')
        new_team = self.cleaned_data.get('add_new_team')
        if team and new_team:
            raise forms.ValidationError('Please specify either Team or New Team!')
        elif new_team:
            # bring all team names to uniform look
            team_name = ' '.join([word.capitalize() for word in sub(r'[^\w\s\d\']', ' ', new_team).split()])
            team, created = Team.objects.get_or_create(name=team_name)
            self.cleaned_data['team'] = team
            self.cleaned_data.pop('add_new_team', None)
        return super().clean()

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.team = self.cleaned_data['team']
        if commit:
            user.save()
        return user


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
        model = HappyTeamUser
        fields = ('happiness', )
