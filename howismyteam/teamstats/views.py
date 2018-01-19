from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView


class IndexView(TemplateView):

    template_name = 'index.html'


class UserLoginView(LoginView):

    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = reverse('teamstats:results_view')
        return context


class UserLogoutView(LogoutView):

    next_page = '/'


class ResultsView(TemplateView):

    template_name = 'results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # inject happiness stats here
        # mock data
        happiness = [5]*5
        average = 5
        context['detailed'] = happiness
        context['average'] = average
        return context


class UserPollView(TemplateView):
    """
    Dummie.
    """
    template_name = 'poll.html'