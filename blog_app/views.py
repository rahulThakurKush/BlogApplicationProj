from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import blogdata, UserModel, Category, Comment
from django.contrib import messages
from django.core.paginator import Paginator
from .send_email import send_otp_email
from django.http import HttpResponseRedirect
import random
import string


def index(request):
    blogs = blogdata.objects.all()
    categories = Category.objects.all()
    p = Paginator(blogdata.objects.all(), 3)
    page = request.GET.get('page')
    blogs_list = p.get_page(page)

    return render(request, 'index.html', {'blogs': blogs, 'blogs_list': blogs_list, 'categories': categories})



def signup(request):
    # print(request,"===============================")
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        UserModel = get_user_model()
        if UserModel.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!')
        elif UserModel.objects.filter(email=email).exists():
            messages.error(request, 'E-mail already registered!')
        else:
            # Generate OTP
            otp = ''.join(random.choices(string.digits, k=6))
            print("======================>",otp)
            user = UserModel.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, password=password, otp=otp)
            user.set_password(password)   #set_password() important function
            user.save()   
            # Send OTP via email
            send_otp_email(email, otp)
            messages.success(request, 'An OTP has been sent to your email. Please verify your account.')
            return redirect('verify_otp') 

    return render(request, 'signup.html')


from django.urls import reverse

def verify_otp(request):
    if request.method == "POST":
        otp_entered = request.POST.get('otp')
        # Retrieve the user using the OTP value
        try:
            user = UserModel.objects.get(otp=otp_entered)
        except UserModel.DoesNotExist:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect(reverse('verify_otp'))  # Redirect back to OTP verification page

        # Check if the entered OTP matches the stored OTP and is not expired
        if user.is_otp_valid(otp_entered):
            user.is_verified = True
            user.save()
            messages.success(request, 'Your account has been verified successfully.')
            return redirect('user_login')  # Redirect to login page

        messages.error(request, 'Invalid OTP or OTP has expired. Please try again.')
        return redirect(reverse('verify_otp'))  # Redirect back to OTP verification page

    return render(request, 'verify_otp.html')


def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # Redirect to 'index' URL name if the user is authenticated
            return redirect('index')
        else:
            # If authentication fails, display an error message
            messages.error(request, 'Invalid email or password. Please try again.')
    
    # Render the login template regardless of whether it's a GET or POST request
    return render(request, 'login.html')



def user_dashboard(request):
    if request.method == "POST":
        title = request.POST.get('title')
        desc = request.POST.get('description')
        blogimg = request.FILES.get('blogimg')  # Use request.FILES to get the uploaded file
        blog_content = request.POST.get('blog_content')
        category_id = request.POST.get('category')
        category = Category.objects.get(pk=category_id) 
        # Create a new blogdata instance with the uploaded file
        blog = blogdata.objects.create(title=title, desc=desc, blogimg=blogimg, blog_content=blog_content, category=category)
        pk = blog.pk
        blog.save()
        return redirect('post_detail', pk=pk)

    categories = Category.objects.all()
    return render(request, 'contact.html', {'categories': categories})


def user_profile(request):
    pass
    return render(request, 'user_profile.html')



def blog_category(request):
        categories = Category.objects.all()
        return render(request, 'contact.html', {'categories': categories})


def my_blogs(request):
    try:
        blogs = blogdata.objects.all()
    except blogdata.DoesNotExist:
        return HttpResponse('Post not found')
    
    return render(request, 'my_blog_list.html', {'blogs': blogs})


def show_blog(request):
    blogs = blogdata.objects.all()
    return render(request, 'standard-fullwidth.html', {'blogs': blogs})


def post_detail(request, pk):

    blog = get_object_or_404(blogdata, id=pk)
    post = blogdata.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment_text = request.POST.get('comment')
        comment = Comment.objects.create(name=name, email=email, comment=comment_text, blog_post_id=pk)
        comment.save()
        messages.success(request, 'Your comment has been submitted successfully.')
        return redirect('post_detail',pk)  
    
    try:
        comments = Comment.objects.filter(blog_post=blog)
    except Comment.DoesNotExist:
        comments = Comment.objects.none()

    return render(request, 'post-image.html', {'blog': blog, 'comments': comments, 'post': post})



def category_detail(request, pk):

    categories = get_object_or_404(Category, id=pk)
    try:
        blogs = blogdata.objects.filter(category=categories)
    except blogdata.DoesNotExist:
        blogs = blogdata.objects.none()

    return render(request, 'category.html', {'categories': categories, 'blogs': blogs})




def like_post(request, pk):
    if request.user.is_authenticated:
            blog = blogdata.objects.get(id=pk)
            if request.user in blog.likes.all():
                # post.like_by.remove(request.user)
                pass
            else:
                blog.likes.add(request.user)
            return redirect('post_detail', pk=pk)

    else:
        return HttpResponse('You must be logged in to like or dislike the blog')



def dislike_post(request, pk):
    if request.user.is_authenticated:
        blog = blogdata.objects.get(id=pk)
        if request.user in blog.likes.all():
            blog.likes.remove(request.user)
        else:
            pass
        return redirect('post_detail', pk=pk)

    else:
        return HttpResponse('You must be logged in to like or dislike the blog')






