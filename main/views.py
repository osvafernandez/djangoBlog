from django.shortcuts import render, redirect
from .forms import RegistrationForm, PostForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from .models import Post


@login_required(login_url='/login')
def home(request):
    posts = Post.objects.all()
    if request.method == "POST":
        post_id = request.POST.get("post-id")
        post = Post.objects.filter(id=post_id).first()
        if post and (post.author == request.user or request.user.has_perm("main.delete_post")):
            post.delete()
    return render(request, "main/home.html", {'posts': posts})


@login_required(login_url='/login')
@permission_required("main.add_post", login_url="/login", raise_exception=True)
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/home')
    else:
        form = PostForm()

    return render(request, 'main/create_post.html', {'form': form})


def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/sign-up.html', {'form': form})
