from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm
from . models import Account
from faculty.models import Faculty
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from article.models import Article, ArticleReviewer


#for email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage



def register(request):
    print('this is being call')
    faculties = Faculty.objects.all()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            faculty = form.cleaned_data.get('faculty')
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            faculty_id = request.POST.get('faculty')
            faculty = Faculty.objects.get(id=faculty_id)
            user = Account.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                password = password
                        )
            
            

            user.phone_number = phone_number
            user.faculty = faculty
            user.save()
            messages.success(request,"Your account has been created successfully, please login below")
            mail_subject = 'Account Registration Notification'
            message = render_to_string('accounts/registrationEmail.html',{
                'user':user,
            })
            to_email = user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return redirect('login')

            #I will need to send account creation email here later

        else:
            print('form is not valid')
            messages.error(request, 'Error Creating your account, Please try again')
            
    else:
        form = RegistrationForm
   
    
    context= {
        'form':form,
        'faculties':faculties
    }
    return render(request, 'accounts/register.html', context)


#reveiwer-registration
def registerreviewer(request):
    print('I am being called')
    faculties = Faculty.objects.all()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
                        
            faculty_id = request.POST.get('faculty')
            faculty = get_object_or_404(Faculty, id=faculty_id)

            generated_username = email.split('@')[0]

            if Account.objects.filter(username=generated_username).exists():
                import uuid
                generated_username = f"{generated_username}_{uuid.uuid4().hex[:4]}"
            
            user = form.save(commit=False)
            user.username = generated_username
            user.email = email
            user.user_type = 'reviewer'
            user.phone_number = phone_number
            user.faculty = faculty
            user.set_password(form.cleaned_data['password'])
            user.save()
            #I will send registration successful email here

            mail_subject = 'Account Registration Notification'
            message = render_to_string('accounts/registrationEmailReviewer.html',{
                'user':user,
            })
            to_email = user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request,"Your account has been created successfully, please login below")
            return redirect('login')

            #I will need to send account creation email here later

        else:
            print('form is not valid')
            messages.error(request, 'Error Creating your account, Please try again')
            
    else:
        form = RegistrationForm
   
    
    context= {
        'form':form,
        'faculties':faculties
    }
    return render(request, 'accounts/register-reviewer.html', context)



def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                pass
                #I will check the type of user here and redirect accordingly
                #I will fetch the user's article here
                
            except:
                pass

            auth.login(request, user)
            messages.success(request, 'You are now logged in ')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Username/Password')
            return redirect('login')


    return render(request, 'accounts/login.html')



@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('login')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            #reset password email
            current_site = get_current_site(request)
            mail_subject = 'Password Reset Notification'
            message = render_to_string('accounts/passwordReset.html',{
                'user':user,
                'domain':current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset link has been sent to your email box')
            return redirect('login')
        else:
            messages.error(request, 'Account with the email provided does not exist')
            return redirect('forgotPassword')

    return render(request, 'accounts/forgotPassword.html')


def resetPassword_validate(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password'
                        )
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has expired')
        return redirect('login')
    


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk = uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password Reset Successfully')
            return redirect('login')

        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')
    


@login_required
def dashboard(request):
    if request.user.user_type == 'reviewer':
        assignments = ArticleReviewer.objects.filter(
            reviewer= request.user).select_related(
                'article').order_by('-id')
        approved = ArticleReviewer.objects.filter(
            reviewer=request.user,
            article__status = 'approved'
        ).select_related('article')
        approved = approved.count()

        rejected = ArticleReviewer.objects.filter(
            reviewer=request.user,
            article__status = 'rejected'
        ).select_related('article')
        rejected = rejected.count()

        pending = ArticleReviewer.objects.filter(
            reviewer=request.user,
            article__status = 'pending'
        ).select_related('article')
        pending = pending.count()


        articles = [a.article for a in assignments]
        assignment_count  = assignments.count()
        context = {
            'articles':articles,
            'assignment_count':assignment_count,
            'approved':approved,
            'rejected':rejected,
            'pending':pending

        }

        return render(request, 'accounts/reviewer/dashboard.html', context)
    
    elif request.user.user_type == 'admin':
        articles = Article.objects.filter(user__faculty = request.user.faculty).order_by('-submitted_at')

        totalapproved = Article.objects.filter(user__faculty =request.user.faculty).filter(status = 'approved').count()
        totalpending = Article.objects.filter(user__faculty =request.user.faculty).filter(status = 'pending').count()
        totalrejected = Article.objects.filter(user__faculty =request.user.faculty).filter(status = 'rejected').count()
        totalsubmitted  = articles.count()

        context = {
            'articles':articles,
             'totalsubmitted':totalsubmitted,
            'totalapproved':totalapproved,
            'totalpending':totalpending,
            'totalrejected':totalrejected
        }
        return render(request, 'accounts/admin/dashboard.html',context)
    else:
          
        totalapproved = Article.objects.filter(user=request.user).filter(status = 'approved').count()
        totalpending = Article.objects.filter(user=request.user).filter(status = 'pending').count()
        totalrejected = Article.objects.filter(user=request.user).filter(status = 'rejected').count()
        articles = Article.objects.filter(user =request.user).order_by('-submitted_at')
        totalsubmitted  = articles.count()
        context = {'articles':articles,
                'totalsubmitted':totalsubmitted,
                'totalapproved':totalapproved,
                'totalpending':totalpending,
                'totalrejected':totalrejected
                }
        return render(request, 'accounts/dashboard.html', context)