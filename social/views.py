from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, checkemail
import random
import string
import os
from django import forms
from django.conf import settings
from django.conf.urls.static import static
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Post, Users, Comments, Likes
from django.core.files.storage import FileSystemStorage


def index(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/home')
                else:
                    return render(request, 'social/index.html', {'error_message': 'Your account has been disabled'})
            else:
                return render(request, 'social/index.html', {'error_message': 'Invalid login'})
        return render(request, 'social/index.html')
    else:
        return redirect('home/')


def checkusername(request):
    if request.method == 'GET':
        username = request.GET['usernameTrue']
        if User.objects.filter(username=username).exists():
            return HttpResponse("OK")
        else:
            return HttpResponse("Username not found")


def home(request):
    if not request.user.is_authenticated:
        return render(request, 'social/index.html')
    else:
        return render(request, 'social/home.html')


def register(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            request.POST['username'],
            request.POST['email'],
            request.POST['password1'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
        )

        user.refresh_from_db()  # load the profile instance created by the signal
        userdata = ''.join(random.choices(
            string.ascii_letters + string.digits, k=16))
        os.mkdir(os.path.join(settings.MEDIA_ROOT, userdata))
        user.profile.userdata = userdata
        user.save()
        raw_password = request.POST['password1']
        user = authenticate(username=user.username, password=raw_password)
        login(request, user)
        return redirect('/home')
    else:
        form = SignUpForm()
    return render(request, 'social/register.html', {'form': form})


def UserLogout(request):
    logout(request)
    return redirect('social:index')


def forgotpassword(request):
    form = checkemail(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            print("hi")
    context = {
        "form": form,
    }
    return render(request, 'social/forgot.html', context)


'''
class HomeView(generic.ListView):
    template_name = 'social/home.html'
    context_object_name = 'all_posts'
    queryset = Post.objects.all().prefetch_related('added_by').order_by('-id')
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['all_users'] = Users.objects.all()
        # And so on for more models
        return context

class HomeView(generic.ListView):
    template_name = 'social/home.html'
    context_object_name = 'all_posts'

    def get_queryset(self):
        queryset = (Post.objects
                           .all()
                           .prefetch_related('added_by')
                           .order_by('-id'))
        return queryset
'''


def HomeView(request):
    all_posts = Post.objects.all().order_by('-id')
    context = {
        'all_posts': all_posts,
    }
    return render(request, 'social/home.html', context)


def like(request, pk):
    if request.method == 'POST':
        try:
            get_like = Likes.objects.get(user_liked=request.user, post_id=pk)
            Likes.objects.get(user_liked=request.user, post_id=pk).delete()
        except Likes.DoesNotExist:
            get_post = Post.objects.get(pk=pk)
            create_like = Likes.objects.create(
                user_liked=request.user, post_id=get_post)
        return HttpResponse('')
    else:
        raise Http404


def comment(request, pk):
    if request.method == 'POST':
        comment = request.POST['data']
        get_post = Post.objects.get(pk=pk)
        create_like = Comments.objects.create(
            comment=comment, posted_by=request.user, post_id=get_post)
        img = request.user.profile.userdata
        root = settings.MEDIA_URL
        fname = request.user.first_name.capitalize()
        lname = request.user.last_name.capitalize()
        return HttpResponse('<div class="comment-all"><div class="comment-all-body"><img src="' + root + '\\' + img + '\dp.jpg" height="25" style="border-radius: 50%;transform: translateY(5px);" alt=""><a href="" target="_blank">' + fname + " " + lname + " " + '</a><span>' + comment + '</span></div></div><br>')
    else:
        raise Http404


def post(request):
    if request.method == 'POST':
        text = request.POST['post']
        img = request.FILES['post-image']
        post_save = Post.objects.create(
            body=text, added_by=request.user)
        post_save.post_image.save(img.name, img)
        return redirect('/home/')
    else:
        raise Http404
