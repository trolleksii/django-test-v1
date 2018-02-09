from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView, UpdateView

from .forms import UserPollForm, CHOICES
from .models import get_happiness_stats, is_eligible_for_poll


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
    Othewise redirects to the results page.
    """

    def dispatch(self, request, *args, **kwargs):
        results_url = reverse('teamstats:results_view')
        poll_url = reverse('teamstats:userpoll_view')
        # Redirect is based on users ability to participate in a poll and
        # the page he is trying to access. If the user is eligible and is
        # trying to access results page - he will be redirected to the poll
        # page and vice versa.
        redirection_table = {
            (True, results_url): redirect(poll_url),
            (False, poll_url): redirect(results_url)
        }

        eligibility = is_eligible_for_poll(self.request.user)
        # redirect according to the table or invoke super().dispatch if
        # redirection is not needed.
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
        detailed, average = get_happiness_stats(self.request.user)
        detailed = [{'label': CHOICES[x][1], 'value': detailed[x]} for x in range(5)]
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
        return self.request.user.pollprofile
