from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Import User UpdateForm, ProfileUpdatForm
from .forms import  UserUpdateForm, ProfileUpdateForm

# Create your views here.
@csrf_protect
def user_login(request):
    if request.POST:
        username = password = ''
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            print("User Login:  Username:" + username + '    Password:' + password)
            print(request.POST)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'base.html', {'message': 'Username or Password wrong!'})
    else:
        return render(request, '404.html')


def user_logout(request):
    logout(request)
    return redirect('/')


@csrf_protect
def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return render(request, 'login.html', {'message': 'Registered successfully, congratulations! Please login.'})
        else:
            return render(request, 'register.html', {'error': 'Invalid input!', 'form': UserCreationForm()})
    else:
        return render(request, "register.html", {'form': UserCreationForm()})


def loginForm(request):
    return render(request, 'Login.html')

# Update it here
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('/') # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)