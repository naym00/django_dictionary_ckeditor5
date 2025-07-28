from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from user import models as MODELS_USER
from user_auth import models as MODELS_AUTH
from settings import models as MODELS_SETT
from help.common.generic import ghelp

def user_register(request):
    html_path = 'dictionary/user_auth/register.html'
    context = {
        'title': 'Register',
        'user': request.user,
        'nav_links': {
            'auth': {
                'home': ghelp.nav_links(key='home', user=request.user),
                'view_passage': ghelp.nav_links(key='view_passage'),
                'add_passage': ghelp.nav_links(key='add_passage'),
                'words': ghelp.nav_links(key='words'),
                'word_details': ghelp.nav_links(key='word_details'),
            },
            'unauth': {
                'home': ghelp.nav_links(key='home'),
                'login': ghelp.nav_links(key='login'),
            }
        },
        'field': {
            'first_name': '',
            'last_name': '',
            'username': '',
            'email': '',
            'phone': '',
            'password': '',
            'confirm_password': '',
            'gender': ''
        },
        'error': {
            'username': None,
            'email': None,
            'phone': None,
            'password': None
            
        }
    }
    if request.method == "POST":
        first_name = request.POST.get('firstName')
        context['field']['first_name'] = first_name
        
        last_name = request.POST.get('lastName')
        context['field']['last_name'] = last_name
        
        username = request.POST.get('username')
        context['field']['username'] = username
        
        email = request.POST.get('email')
        context['field']['email'] = email
        
        phone = request.POST.get('phone')
        context['field']['phone'] = phone
        
        password = request.POST.get('password')
        context['field']['password'] = password
        
        confirm_password = request.POST.get('confirmPassword')
        context['field']['confirm_password'] = confirm_password
        
        gender = request.POST.get('gender')
        context['field']['gender'] = gender
        
        prepare_data = {
            'first_name': first_name,
            'last_name': last_name,
            'gender': gender
        }
        
        user = MODELS_USER.User.objects.filter(username=username)
        if user.exists():
            context['error']['username'] = f'User with this username({username}) is already exist.'
        else:
            prepare_data.update({'username': username})
            user = MODELS_USER.User.objects.filter(email=email)
            if user.exists():
                context['error']['email'] = f'User with this email({email}) is already exist.'
            else:
                prepare_data.update({'email': email})
                phone_flag = False
                if phone:
                    user = MODELS_USER.User.objects.filter(phone=phone)
                    if user.exists(): phone_flag = True
                if phone_flag:
                    context['error']['phone'] = f'User with this phone({phone}) is already exist.'
                else:
                    prepare_data.update({'phone': phone})
                    if password != confirm_password:
                        context['error']['password'] = f'Password doesn\'t match({password} & {confirm_password}).'
                    else:
                        prepare_data.update({'password': make_password(password)})
                        user = MODELS_USER.User.objects.create(**prepare_data)
                        login(request, user)
                        return redirect('home')
        
    return render(request, html_path, context=context)

def user_login(request):
    html_path = 'dictionary/user_auth/login.html'
    context = {
        'title': 'Register',
        'user': request.user,
        'nav_links': {
            'auth': {
                'home': ghelp.nav_links(key='home', user=request.user),
                'view_passage': ghelp.nav_links(key='view_passage'),
                'add_passage': ghelp.nav_links(key='add_passage'),
                'words': ghelp.nav_links(key='words'),
                'word_details': ghelp.nav_links(key='word_details'),
            },
            'unauth': {
                'home': ghelp.nav_links(key='home'),
                'register': ghelp.nav_links(key='register'),
                'forgot_password': ghelp.nav_links(key='forgot_password'),
            }
        },
        'field': {
            'username': '',
            'password': ''
        },
        'error': {
            'username': None,
            'password': None
        }
    }
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not MODELS_USER.User.objects.filter(username=username).exists():
            context['error']['username'] = 'Invalid Username'
            context['field']['username'] = username
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                context['error']['password'] = 'Invalid Password'
                context['field']['password'] = password
            else:
                if not user.is_superuser:
                    login(request, user)
                    return redirect('home')
    return render(request, html_path, context=context)

def forgot_password(request):
    html_path = 'dictionary/user_auth/forgot_password.html'
    context = {
        'title': 'Forgot Password',
        'user': request.user,
        'nav_links': {
            'auth': {
                'home': ghelp.nav_links(key='home', user=request.user),
                'view_passage': ghelp.nav_links(key='view_passage'),
                'add_passage': ghelp.nav_links(key='add_passage'),
                'words': ghelp.nav_links(key='words'),
                'word_details': ghelp.nav_links(key='word_details'),
            },
            'unauth': {
                'home': ghelp.nav_links(key='home'),
                'login': ghelp.nav_links(key='login'),
                'register': ghelp.nav_links(key='register'),
            }
        },
        'field': {
            'email': ''
        },
        'error': {
            'email': None,
            'error': None
        }
    }
    settings = ghelp.get_settings(MODELS_SETT.Settings)
    if settings != None:
        if request.method == "POST":
            email = request.POST.get('email')
            user = MODELS_USER.User.objects.filter(email=email)
            if user.exists():
                subject = 'Forget Password(Dictionary)'
                otp = ghelp.get_unique_code()[-5:]
                message = f'This is your OTP: {otp}'
                recipient_list = [email]
                if ghelp.send_mail_including_attatchment(subject, message, recipient_list, attachments=[], email_from = None):
                    MODELS_AUTH.ForgotPassword.objects.create(
                        user=user.first(),
                        otp=otp
                    )
                    return redirect('set-password')
            else:
                context['error']['email'] = 'Invalid Email'
                context['field']['email'] = email
    else: context['error']['error'] = 'Settings is undone.'
    return render(request, html_path, context=context)

def set_new_password(request):
    html_path = 'dictionary/user_auth/set_new_password.html'
    context = {
        'title': 'Set Password',
        'user': request.user,
        'nav_links': {
            'auth': {
                'home': ghelp.nav_links(key='home', user=request.user),
                'view_passage': ghelp.nav_links(key='view_passage'),
                'add_passage': ghelp.nav_links(key='add_passage'),
                'words': ghelp.nav_links(key='words'),
                'word_details': ghelp.nav_links(key='word_details'),
            },
            'unauth': {
                'home': ghelp.nav_links(key='home'),
                'login': ghelp.nav_links(key='login'),
                'register': ghelp.nav_links(key='register'),
            }
        },
        'field': {
            'otp': '',
            'password': ''
        },
        'error': {
            'otp': None,
            'password': None,
            'error': None
        }
    }
    settings = ghelp.get_settings(MODELS_SETT.Settings)
    if settings != None:
        if request.method == "POST":
            otp = request.POST.get('otp')
            forgot_password = MODELS_AUTH.ForgotPassword.objects.filter(otp=otp)
            if forgot_password.exists():
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirmPassword')
                if password == confirm_password:
                    today_datetime = ghelp.get_today_datetime()
                    duration = ((today_datetime - forgot_password.first().created_at).seconds)/60
                    if duration<=settings.otp_validation_minutes:
                        user = forgot_password.first().user
                        user.set_password(password)

                        user.save()
                        forgot_password.delete()
                        
                        for item in MODELS_AUTH.ForgotPassword.objects.all():
                            duration = ((today_datetime - item.created_at).seconds)/60
                            if duration>settings.otp_validation_minutes: item.delete()
                        login(request, user)
                        return redirect('home')
                    else: context['error']['error'] = 'OTP is Expired.'
                else:
                    context['error']['password'] = f'Password doesn\'t match({password} & {confirm_password}).'
                    context['field']['password'] = password
            else:
                context['error']['otp'] = 'Invalid OTP'
                context['field']['otp'] = otp
    else: context['error']['error'] = 'Settings is undone.' 
    return render(request, html_path, context=context)

def user_logout(request):
    logout(request)
    return redirect('home')