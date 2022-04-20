""" app_base view """
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def home_view(request):
    """ View for Home page """
    context = {}
    return render(request, 'app_base/home.html', context)

def login_view(request):
    """ View for login page """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            user_group = request.user.groups.all()[0].name
            if user_group == 'admin': #ทุกรายการ
                return redirect('home')
            elif user_group == 'ent_officer':
                return redirect('dashboard-ent')
            elif user_group == 'ocsb_officer':
                return redirect('dashboard-ocsb')
            else:
                return redirect('home')
        else:
            messages.info(request, 'Username/Password ไม่ถูกต้อง')
            return redirect('login')

    context = {}
    return render(request, 'app_base/login.html', context)

def logout_view(request):
    """ View for logout """
    logout(request)
    return redirect('login')
