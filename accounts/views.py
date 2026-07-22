from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import StackKartLoginForm, StackKartRegisterForm
from .models import CustomerProfile


class StackKartLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = StackKartLoginForm
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)


class StackKartLogoutView(LogoutView):
    next_page = reverse_lazy('catalog:home')


def register(request):
    if request.user.is_authenticated:
        return redirect('catalog:home')

    if request.method == 'POST':
        form = StackKartRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            CustomerProfile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, 'Account created successfully. Welcome to StackKart!')
            return redirect('catalog:home')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = StackKartRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})
