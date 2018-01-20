from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView, UpdateView

from .forms import UserPollForm
from .models import (
    get_happiness_stats, is_eligible_for_poll, update_poll_date,
    UserPollProfile
)


class IndexView(TemplateView):

    template_name = 'index.html'


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
    Othewise redirets to the results page.
    """

    def dispatch(self, request, *args, **kwargs):
        results_url = reverse('teamstats:results_view')
        poll_url = reverse('teamstats:userpoll_view')
        # Redirect is based of users ability to participate in a poll and
        # the page he is trying to access. If user is eligible and is trying to
        # access results page - he will be redirected to the poll page and
        # vice versa.
        redirection_table = {
            (True, results_url): redirect(poll_url),
            (False, poll_url): redirect(results_url)
        }

        eligibility = is_eligible_for_poll(self.request.user)
        # redirect according to the table or invoke super().dispatch if
        return redirection_table.get(
            (eligibility, request.path),
            super().dispatch(request, *args, **kwargs)
        )


class ResultsView(LoginRequiredMixin, PollRedirectorMixin, TemplateView):

    template_name = 'results.html'

    def get_login_url(self):
        return reverse('teamstats:login_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team, detailed, average = get_happiness_stats(self.request.user)
        if team:
            context['team'] = team.name
        context['detailed'] = detailed
        context['average'] = average
        return context


class UserPollView(LoginRequiredMixin, PollRedirectorMixin, UpdateView):

    template_name = 'poll.html'
    form_class = UserPollForm

    def get_login_url(self):
        return reverse('teamstats:login_view')

    def get_success_url(self):
        # poll was successfull, so we can save the date
        update_poll_date(self.request.user)
        return reverse('teamstats:results_view')

    def get_object(self, querryser=None):
        return UserPollProfile.objects.get(user=self.request.user)
