from django.shortcuts import render , redirect

from django.contrib.auth.models import User

from .forms import CreateUserForm , LoginForm , UpdateUserForm

from django.contrib.sites.shortcuts import get_current_site

from . token import user_tokenizer_generate

from django.template.loader import render_to_string

from django.utils.encoding import force_bytes, force_str

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode 

from django.contrib.auth.models import auth

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.contrib import messages


def index(request):

    return render(request, 'secureapp/index.html')




def register(request):

    form = CreateUserForm()

    if request.method == 'POST':

        form = CreateUserForm(request.POST)

        if form.is_valid():

           user = form.save()


           user.is_active = False

           user.save()

           #email verificaiton setup

           current_site = get_current_site(request)

           subject = 'Account verification email'

           message = render_to_string('secureapp/registration/email-verification.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': user_tokenizer_generate.make_token(user)
})

           user.email_user(subject=subject, message=message)          

           return redirect('email-verification-sent')
    
    context = {'form':form}

    return render(request, 'secureapp/registration/register.html', context=context)






def email_verification(request, uidb64, token):

    unique_id = force_str(urlsafe_base64_decode(uidb64))

    user = User.objects.get(pk=unique_id)

    #success

    if user and user_tokenizer_generate.check_token(user, token):

        user.is_active =  True

        user.save()

        return redirect('email-verification-success')
    

    
    else:

        return redirect('email-verification-failed')




def email_verification_sent(request):
    return render(request, 'secureapp/registration/email-verification-sent.html')

def email_verification_success(request):
    return render(request, 'secureapp/registration/email-verification-success.html')

def email_verification_failed(request):   
    return render(request, 'secureapp/registration/email-verification-failed.html')


@login_required(login_url='two_factor:login')

def user_logout(request):

    try :

        for key in list(request.session.keys()):

            if key == 'session_key':

                continue

            else :

                del request.session[key]

    except KeyError:

        pass

    messages.success(request, 'Logout success')

    return redirect('/')




@login_required(login_url='two_factor:login')

def dashboard(request):

    return render(request, 'secureapp/dashboard.html')




@login_required(login_url='two_factor:login')

def profile_management(request):

    user_form = UpdateUserForm(instance=request.user)

   
    if request.method == 'POST':

        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():

            user_form.save()

            return redirect('dashboard')
        
    
    

    context = {'user_form':user_form}

    return render(request, 'secureapp/profile-management.html', context=context)






@login_required(login_url='two_factor:login')

def delete_account(request):

    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':

        user.delete()

        return redirect('/')

    return render(request, 'secureapp/delete-account.html')



def account_locked(request):

    return render(request, 'secureapp/account-locked.html')


def signup_redirect(request):
    messages.error(request, "Something wrong here, it may be that you already have account!")
    return redirect('index')