from .utils import Util, token_generator
from .models import CustomUser
from .forms import SignupForm

from django.contrib.auth import views
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages


def register(request):
    """Register new user"""
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user = CustomUser.objects.get(email=form.cleaned_data['email'])
            user.is_active = False
            user.save()
            uid64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={
                'uid64': uid64,
                'token': token_generator.make_token(user, ),
            })
            activate_url = 'http://' + domain + link
            email_body = 'Hi ' + user.username + ' You successfully sign up on Bulletin Board' + \
                         '\nTo verify your account use this link bellow ' + activate_url
            data = {
                'email_body': email_body,
                'to_email': user.email,
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


class VerificationView(View):

    def get(self, request, uid64, token):
        try:
            id = force_text(urlsafe_base64_decode(uid64))
            user = CustomUser.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                messages.success(request, 'Account already activated')
                return redirect('login')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass
        return redirect('login')


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


@login_required
def private(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {
        'user': user,
    }
    return render(request, 'registration/private.html', context)
