from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User

# Create your views here.
def index (request):
    return render(request , 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('stay-signed-in')

        try:
            user = User.objects.get(email=email)
            user = authenticate(username=user.username, password=password)
            
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                messages.success(request, 'Login successful!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
        
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

def register(request):
    return render(request, 'register.html')

def editor(request):
    return render(request, 'editor_guidelines.html')

def reviewer(request):
    return render(request, 'reviewer_guidelines.html')

# def guidelines(request):
#     return render(request, 'guidelines.html')

def author_guidelines(request):
    return render(request, 'guidelines/author_guidelines.html')

def editor_guidelines(request):
    return render(request, 'guidelines/editor_guidelines.html')

def reviewer_guidelines(request):
    return render(request, 'guidelines/reviewer_guidelines.html')

def join_member(request):
    return render(request, 'join/join_member.html')

def join_editor(request):
    return render(request, 'join/join_editor.html')

def join_reviewer(request):
    return render(request, 'join/join_reviewer.html')

def submit_paper(request):
    return render(request, 'submit_paper.html')

def archives(request):
    return render(request, 'archives.html')
