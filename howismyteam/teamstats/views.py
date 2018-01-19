from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView

from .models import get_happiness_stats


class IndexView(TemplateView):

    template_name = 'index.html'


class UserLoginView(LoginView):

    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_redirect_url(self):
        return reverse('teamstats:results_view')


class UserLogoutView(LogoutView):

    next_page = '/'


class ResultsView(LoginRequiredMixin, TemplateView):

    template_name = 'results.html'

    def get_login_url(self):
        return reverse('teamstats:login_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        detailed, average = get_happiness_stats(self.request.user)
        context['detailed'] = detailed
        context['average'] = average
        return context


class UserPollView(LoginRequiredMixin, TemplateView):
    """
    Dummie.
    """
    template_name = 'poll.html'

    def get_login_url(self):
        return reverse('teamstats:login_view')
