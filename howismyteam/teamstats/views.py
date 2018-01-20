from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from django.views.generic import TemplateView, UpdateView

from .forms import UserPollForm
from .models import get_happiness_stats, UserPollProfile


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


class UserPollView(LoginRequiredMixin, UpdateView):

    template_name = 'poll.html'
    form_class = UserPollForm

    def get_login_url(self):
        return reverse('teamstats:login_view')

    def get_success_url(self):
        return reverse('teamstats:results_view')

    def get_object(self, querryser=None):
        return UserPollProfile.objects.get(user=self.request.user)
