from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView, UpdateView

from .forms import HappyUserCreationForm, UserPollForm
from .models import HappyTeamUser


class IndexView(TemplateView):

    template_name = 'index.html'


class UserRegistrationView(TemplateView):
    template_name = 'register.html'

    def post(self, request, *args, **kwargs):
        form = HappyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('teamstats:userpoll_view')
        else:
            return self.get(request, form=form)

    def get(self, request, *args, **kwargs):
        form = kwargs.pop('form', HappyUserCreationForm())
        return super().get(request, form=form, *args, **kwargs)


class UserLoginView(LoginView):

    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_redirect_url(self):
        return reverse('teamstats:results_view')


class UserLogoutView(LogoutView):

    next_page = '/'


class PollRedirectorMixin:
    """
    Redirects to poll page if the user is eligible.
    Othewise redirects to the results page.
    """

    def dispatch(self, request, *args, **kwargs):
        results_url = reverse('teamstats:results_view')
        poll_url = reverse('teamstats:userpoll_view')
        requested_page = request.path

        try:
            eligibility = self.request.user.is_eligible_for_poll
        except ObjectDoesNotExist:
            eligibility = False

        if eligibility:
            if requested_page == results_url:
                # user is eligible for poll but tries to access results
                return redirect(poll_url)
        else:
            if requested_page == poll_url:
                # user tries to access poll when uneligible
                return redirect(results_url)

        # redirection is not needed
        return super().dispatch(request, *args, **kwargs)


class ResultsView(LoginRequiredMixin, PollRedirectorMixin, TemplateView):

    template_name = 'results.html'

    def get_happiness_stats(self):
        """
        Returns breakdown on happines level and an average happiness as a tuple.
        If the user is in some team, stats are calculated for this team only. In
        the other case, stats are calculated for all users without a team.
        """
        try:
            team_or_none = self.request.user.team
        except ObjectDoesNotExist:
            team_or_none = None

        teammates = HappyTeamUser.objects.filter(team=team_or_none)
        average_happiness = teammates.aggregate(Avg('happiness'))['happiness__avg']
        detailed_happiness = [teammates.filter(happiness=i).count() for i in range(1, 6)]
        return (detailed_happiness, average_happiness, )

    def get_login_url(self):
        return reverse('teamstats:login_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        detailed, average = self.get_happiness_stats()
        detailed = [{'label': UserPollForm.HAPPINESS_CHOICES[x][1], 'value': detailed[x]} for x in range(5)]
        context['detailed'] = detailed
        context['average'] = average
        return context


class UserPollView(LoginRequiredMixin, PollRedirectorMixin, UpdateView):

    template_name = 'poll.html'
    form_class = UserPollForm

    def get_login_url(self):
        return reverse('teamstats:login_view')

    def get_success_url(self):
        return reverse('teamstats:results_view')

    def get_object(self, queryset=None):
        return self.request.user
