#developed by Leo4Bey
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Blog

def home(request):
    blogs = Blog.objects.all().order_by('-id')
    return render(request, "index.html", {'blogs': blogs})

def profile(request, user_name):
    user = get_object_or_404(User, username=user_name)

    blogs = Blog.objects.filter(owner_id=user.id).order_by('-id')

    data = {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "date_join": user.date_joined,
        "last_login": user.last_login,
        "blogs_count": blogs.count()
    }
    
    return render(request, 'profile.html', {'data': data, 'blogs': blogs})

@login_required
def create_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        owner = request.user.id
        username = request.user.username

        blog = Blog.objects.create(
            title=title,
            content=content,
            owner_id=owner
        )

        return redirect(reverse('profile', kwargs={'user_name': username}))
    
    return render(request, "create_blog.html")

@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, owner=request.user)
    
    if request.method == 'POST':
        blog.delete()
        return redirect(reverse('profile', kwargs={'user_name': request.user.username}))

    # GET isteği için basit bir onay sayfası render edebilirsin
    return render(request, 'delete_blog_confirmation.html', {'blog': blog})

def blog_detail(request, user_name, blog_id):
    blogs = Blog.objects.get(id=blog_id)
    return render(request, "blog_detail.html", {'blogs': blogs})

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        repassword = request.POST.get('re_pass')
        agreement = request.POST.get('agree-term')
        print(username)
        print(email)
        print(password)
        print(repassword)
        print(agreement)
        user_infos = {
            "username": username,
            "email": email,
            "password": password,
            "repassword": repassword,
            "agreement": agreement
        }
        allowed_chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','0','1','2','3','4','5','6','7','8','9','_']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'kayıtlı kullanıcı adı')
            return render(request, 'signup.html', {'user_infos': user_infos})
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Kayıtlı mail')
            return render(request, 'signup.html', {'user_infos': user_infos})
        elif password != repassword:
            messages.error(request, 'Şifreler uyuşmuyor')
            return render(request, 'signup.html', {'user_infos': user_infos})
        elif agreement != "on":
            messages.error(request, 'Kullanım şartlarını kabul etmelisiniz')
            return render(request, 'signup.html', {'user_infos': user_infos})
        elif len(username) > 32:
            messages.error(request, 'En fazla 32 karakterli bir kullanıcı adı yapabilirsin')
            return render(request, 'signup.html', {'user_infos': user_infos})
        elif len(password) > 64:
            messages.error(request, 'En fazla 64 karakterli bir şifre yapabilirsin')
            return render(request, 'signup.html', {'user_infos': user_infos})
        else:
            name_check = True
            for i in username:
                if i not in allowed_chars:
                    name_check = False
            if name_check == False:
                messages.error(request, 'Kullanıcı adında özel karakter kullanamazsınız')
                return render(request, 'signup.html', {'user_infos': user_infos})
            else:
                user = User.objects.create(
                    email=email,
                    username=username,
                    password=make_password(password)
                )
                loged_user = authenticate(request, username=username, password=password)
                login(request, loged_user)
                print("Kullanıcı kaydı başarılı")
                return redirect('home')
 
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('your_name')
        password = request.POST.get('your_pass')
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Hatalı kullanıcı adı ya da şifre')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

#developed by Leo4Bey