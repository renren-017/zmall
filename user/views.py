from django.contrib.auth import views
from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from .utils import Util


def register(request):
    """Register new user"""
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            current_site = get_current_site(request).domain
            absolut_url = 'http://' + current_site
            email_body = 'Hi ' + form.cleaned_data['username'] + ' You successfully sign up on ' + absolut_url + \
                         '\nCome and make your first advertisement'
            data = {
                'email_body': email_body,
                'to_email': form.cleaned_data['email'],
                'email_subject': 'Verify your email',
            }
            Util.send_email(data)
            return redirect('home')
    else:
        form = SignupForm()
    context = {
        'form': form,
    }
    return render(request, 'registration/register.html', context)


@login_required
def logout_view(request):
    """Log out"""
    logout(request)
    return redirect('home')


class ChangePassword(views.PasswordChangeView):
    """Change password"""
    template_name = 'registration/password_change_form.html'


class PasswordChangeDone(views.PasswordChangeDoneView):
    """Change password done landing"""
    template_name = 'registration/password_change_done.html'

