from django.shortcuts import render
from .forms import SignUpForm
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.mail import send_mail
from sendmail1 import settings 

# Create your views here.

def user_signup(request):
    if request.method=='POST':
        fm=SignUpForm(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request,"Account has been Created Successfully...")
            return HttpResponseRedirect('/signin/')
    else:
        fm=SignUpForm()
    return render(request,'testapp/signup.html',{'fm':fm})

def user_signin(request):
    
    
    if not request.user.is_authenticated:
        if request.method=="POST":
            fm=AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data['username']
                password1=fm.cleaned_data['password']
                user=authenticate(username=uname,password=password1)
                if user is not None:
                    login(request,user)
                    fname=request.user.first_name
                    e=request.user.email
                    p= "Hello "+ fname
                    t=e
                    from_email=settings.EMAIL_HOST_USER
                    msg="i love u"
                    send_mail(
                            p,
                            msg,
                            from_email,
                            [t],
                            fail_silently=True,
                            )
                    messages.success(request,"Logged in successfully.")
                    return render(request,"testapp/signout.html",{'f':fname})
        else:
            fm=AuthenticationForm()
        return render(request,'testapp/signin.html',{'fm':fm})
    else:
        return HttpResponseRedirect("/signout/")

    
    

    

def user_signout(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request,'testapp/signout.html')
    else:
        return HttpResponseRedirect("/signin/")



