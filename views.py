from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages 

from django.contrib.auth import authenticate, login, logout
from Luckydicegame import settings
from django.core.mail import send_mail  
from django.contrib.sites.shortcuts import get_current_site 
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, send_mail

from django.shortcuts import render

from django.utils.crypto import get_random_string
from .models import PasswordResetToken 
from .forms import PasswordResetRequestForm
# authentication/views.py

from django.contrib.auth import views as auth_views

from django.contrib.auth.models import User


# Your views and other code here


# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):

    if request.method == "POST":
        # username = request.POST.get('username')
        username =request.POST['username']
        fname =request.POST['fname']
        lname =request.POST['lname']
        email =request.POST['email']
        pass1 =request.POST['pass1']
        pass2 =request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists. Please try a different username.")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email already Registered..!")
            return redirect('home')
        
        if len(username)>10:
            messages.error(request, "Username must be under 10 characters")

        if pass1 != pass2:
            messages.error(request, "Password didn't match..!")

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric..!")
            return redirect('home')
        

        myuser =User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False

        myuser.save()
        messages.success(request, "Your account has been successfully created. \n We have sent you a confirmation email. Please confirm your email to activate your account.")

        #Welcome Email

        subject = ("Welcome to LuckyDice! Get ready to embark on an exciting journey of luck and entertainment. Login now to discover a world of thrilling experiences and endless fun!")
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to LuckyDice!! \n Thank You for visiting our Website \n we have sent you a confirmation email, please confirm your email address in order to activate your account. \n\n Thank You "
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # email address Confirmation Email

        current_site = get_current_site(request)
        email_subject = "confirm your email @ Luckydice -Django login..!"
        message2 = render_to_string('email_confirmation.html',{
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': default_token_generator.make_token(myuser)

        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )  
        email.fail_silently = True
        email.send()

        return redirect('signin')

    return render(request, "authentication/signup.html")


def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "DiceApp/index.html", {'fname' : fname})
        else:
            messages.error(request, "Bad credintial..!")
            return redirect('home')
        
    return render(request, "authentication/signin.html") 


def signout(request):
    logout(request)
    messages.success(request, "Logged out Successfully..!")
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExits):
        myuser = None

    if myuser is not None and default_token_generator.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')
    



#forget password
def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()

            if user:
                token = get_random_string(length=32)
                PasswordResetToken.objects.update_or_create(user=user, defaults={'token': token})

                reset_link = request.build_absolute_uri(f'/reset-password/{token}')
                subject = 'Password Reset'
                message = f'Click the following link to reset your password:\n\n{reset_link}'

                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

            return render(request, 'authentication/password_reset_sent.html')

    else:
        form = PasswordResetRequestForm()

    return render(request, 'authentication/forgot_password.html', {'form': form})


# reset password

# authentication/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PasswordResetToken
from .forms import ResetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode

def reset_password(request, token):
    try:
        token_obj = PasswordResetToken.objects.get(token=token)
        user = token_obj.user
    except PasswordResetToken.DoesNotExist:
        messages.error(request, "Invalid or expired reset link.")
        return redirect('home')

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password reset successful. You can now sign in with your new password.")
                token_obj.delete()  # Remove the used token
                return redirect('password_reset_sucess')
            else:
                messages.error(request, "Passwords do not match.")
    else:
        form = ResetPasswordForm()

    return render(request, 'authentication/reset_password.html', {'form': form})


# Password reset sucess page
def password_reset_sucess(request):
    return render(request, "authentication/password_reset_success.html")