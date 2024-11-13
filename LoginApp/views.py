from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import CreateNewUser, AuthenticationForm, EditProfile
from .models import UserProfile, Follow
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

    user_data = User.objects.select_related('user_profile').prefetch_related('post').get(pk=request.user.pk)
    user_posts = user_data.post.all()  # Retrieve all posts related to the user
    user_profile = user_data.user_profile  # Access the user’s profile directly

    
    context = {
        'form':form,
        'user_profile':user_profile,
        'user_posts': user_posts
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


@login_required
def other_users(request, username):
    other_user = User.objects.get(username=username)

    already_followed = Follow.objects.filter(follower=request.user, following=other_user)
    
    if other_user == request.user:
        return redirect('LoginApp:profile')
    
    user_profile = UserProfile.objects.select_related('user').get(user__username=username)
    return render(request, 'LoginApp/other_user.html', context={'user_profile': user_profile, 'already_followed':already_followed} )

@login_required
def follow(request, username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    
    already_followed = Follow.objects.filter(follower=follower_user, following= following_user)
    
    if not already_followed:
        follow_user = Follow(follower=follower_user, following= following_user)
        follow_user.save()
    return redirect("LoginApp:user_profile", username)

@login_required
def un_follow(request, username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower=follower_user, following= following_user)
    already_followed.delete()
    return redirect("LoginApp:user_profile", username)