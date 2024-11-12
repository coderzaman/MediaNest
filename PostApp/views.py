from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm
# Create your views here.
@login_required
def home(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            print("Done")
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            
            return redirect('LoginApp:profile')
    
    return render(request, 'PostApp/home.html', context={'form':form})


# @login_required
# def create_post(request):
 
    
#     return render(request, 'PostApp/home.html', context={'form':form})