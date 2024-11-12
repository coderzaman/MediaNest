from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import CreateNewUser, AuthenticationForm, EditProfile
from .models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from PostApp.forms import PostForm
from django.contrib.auth.models import User

# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('PostApp:home')
    
    form = CreateNewUser()
    registered = False    

    if request.method == "POST":
        form = CreateNewUser(data=request.POST)
        
        if form.is_valid():
            form.save()
            registered = True
            return redirect('LoginApp:signIn')
    return render(request, 'LoginApp/signup.html', context={'form': form, 'registered': registered})
  

def sign_in(request):
    
    if request.user.is_authenticated:
        return redirect('PostApp:home')
    
    form = AuthenticationForm()
    
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('PostApp:home')
    context = {'form':form}
    return render(request, 'LoginApp/signIn.html', context)

@login_required
def sign_out(request):
    logout(request)
    return redirect('LoginApp:signIn')

@login_required
def user_profile(request):
    user_details =  request.user.user_profile
    
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            print("Done")
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            
            return redirect('LoginApp:profile')

    user_post = User.objects.prefetch_related('post','user_profile').get(pk=request.user.pk)

    print(user_post)
    
    context = {
        'form':form,
        'user_details':user_details,
        'user_post': user_post
    }
    return render(request, 'LoginApp/user.html', context=context)


@login_required
def edit_profile(request):
    current_user = UserProfile.objects.get(user=request.user)
    form = EditProfile(instance=current_user)
    
    if request.method == "POST":
        form = EditProfile(request.POST, request.FILES, instance=current_user)
        
        if form.is_valid():
            form.save()
            form = EditProfile(instance=current_user)
            return redirect("LoginApp:profile")
    
    return render(request, 'LoginApp/profile.html', context={'form':form})