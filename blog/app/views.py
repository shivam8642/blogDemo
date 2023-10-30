from django.shortcuts import render,redirect,HttpResponse
from .forms import Signup

from django.contrib.auth import login as auth_login, authenticate,logout as django_logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .models import Blog,Comment

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import EmailBlogForm,CommentForm
from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect('blog')
    else:
        return render(request,'index.html')

def signup(request):
    if request.method=="POST":
        form=Signup(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('/login')
    else:
        form=Signup()
    return render(request,'signup.html',{'obj':form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('blog') 
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def logout(request):
   django_logout(request)
   return redirect("login") 



@login_required()
def blog(request):
    blog_list=Blog.objects.all()
    paginator = Paginator(blog_list,5)  
    page = request.GET.get('page') 

    try:
        obj = paginator.page(page)
    except PageNotAnInteger:
        obj = paginator.page(1)  #
    except EmptyPage:
        obj = paginator.page(paginator.num_pages)  
        return HttpResponse("Page does not exist. This is the last page.")

    return render(request, 'blog.html', {'obj': obj})



@login_required()

def post_detail(request, id):
    post = Blog.objects.get(id=id)
    current_user=request.user
    blog_id = id
    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            name=request.POST['name']
            email=request.POST['email']
            body=request.POST['body']
            comment = Comment(blog_id=blog_id,author=current_user,name=name,email=email,body=body) 
            comment.save()  
            return redirect('post_detail',id=id)

    else:
        form=CommentForm()
    return render(request, 'detail.html', {'post': post,'form':form})

@login_required()
def share_post(request,id):
    blog = Blog.objects.get(id=id)

    if request.method == 'POST':
        form = EmailBlogForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['from_email']
            to_email = form.cleaned_data['to_email']
            message = form.cleaned_data['message']
            email_message = f"Hi {name}Check out this blog post:\n\nTitle: {blog.title}\nDetail: {blog.content}{message}"
            send_mail('Blog Sharing', email_message, from_email, [to_email], fail_silently=False)
            return redirect("send")

    else:
        form = EmailBlogForm()

    return render(request,'share_post.html',{'form':form})



