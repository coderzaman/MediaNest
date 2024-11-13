from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from LoginApp.models import UserProfile, Follow
from PostApp.models import Post
from .forms import PostForm
# Create your views here.
@login_required
def home(request):
    form = PostForm()
    results = None  # Initialize results as None to control display in the template

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('PostApp:home')
    
    if request.method == "GET":
        search = request.GET.get('search', '').strip()
        if search: 
            results = UserProfile.objects.filter(full_name__contains=search).select_related('user')
    
    # Step 1: Get the list of users the current user is following
    following_user_ids = Follow.objects.filter(follower=request.user).values_list('following', flat=True)

    # Step 2: Query posts authored by any user in the `following_user_ids` list
    posts = Post.objects.filter(author__in=following_user_ids).select_related('author').order_by('-upload_date')

    
    return render(request, 'PostApp/home.html', context={'form': form, 'results': results, 'posts':posts})



