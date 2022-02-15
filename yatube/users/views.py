from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class PasswordResetForm(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:password_reset_form')
    template_name = 'users/password_reset_form.html'
