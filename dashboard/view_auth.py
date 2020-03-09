from django.contrib.auth.views import LoginView
from django.shortcuts import reverse


class HappeningLoginView(LoginView):
    template_name = 'dashboard/login.html'
    redirect_authenticated_user = True
