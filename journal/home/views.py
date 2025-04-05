from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from .models import User, UserRegistration, PaperSubmission, JoinMember, JoinEditor, JoinReviewer, Contact
from django.contrib.auth.decorators import login_required
from social_django.utils import load_strategy
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
import os
from django.http import JsonResponse

# Create your views here.
def index (request):
    return render(request , 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            # Create contact entry
            contact = Contact.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            messages.success(request, 'Thank you! Your message has been submitted successfully.')
            return redirect('contact')

        except Exception as e:
            messages.error(request, f'Failed to submit message: {str(e)}')
            
    return render(request, 'contact.html')

def home(request):
    # Get username for display
    username = request.session.get('username')
    is_authenticated = request.session.get('is_authenticated', False)
    
    return render(request, 'index.html', {
        'username': username,
        'is_authenticated': is_authenticated
    })

def login_view(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email').lower()
            password = request.POST.get('password')

            try:
                user = UserRegistration.objects.get(email=email)
                if check_password(password, user.password):
                    # Store user info in session
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    request.session['is_authenticated'] = True
                    messages.success(request, 'Login successful!')
                    return redirect('home')  # Redirect to home page
                else:
                    messages.error(request, 'Invalid password')
            except UserRegistration.DoesNotExist:
                messages.error(request, 'Email not registered')

        except Exception as e:
            messages.error(request, f'Login failed: {str(e)}')

    return render(request, 'login.html')

def logout_view(request):
    # Clear all session data
    request.session.flush()
    messages.success(request, 'Logged out successfully')
    return redirect('/')

def register(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm-password')

            # Print debug information
            print(f"Received registration data - Username: {username}, Email: {email}")

            # Basic validation
            if not all([username, email, password, confirm_password]):
                messages.error(request, 'All fields are required')
                return render(request, 'register.html')

            # Check if email exists
            if UserRegistration.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered')
                return render(request, 'register.html')

            # Check password match
            if password != confirm_password:
                messages.error(request, 'Passwords do not match')
                return render(request, 'register.html')

            # Create new user
            user = UserRegistration.objects.create(
                username=username,
                email=email.lower(),
                password=make_password(password)  # Hash the password
            )

            print(f"User created successfully with ID: {user.id}")

            # Set session data
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['is_authenticated'] = True

            messages.success(request, f'Welcome {username}! Registration successful!')
            return redirect('home')  # Redirect to home page

        except Exception as e:
            print(f"Registration error: {str(e)}")
            messages.error(request, f'Registration failed: {str(e)}')

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
    if request.method == 'POST':
        try:
            member = JoinMember.objects.create(
                username=request.POST.get('username'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                linkedin=request.POST.get('linkedin'),
                scopus=request.POST.get('scopus'),
                orchid=request.POST.get('orchid'),
                designation=request.POST.get('designation'),
                qualification=request.POST.get('qualification')
            )
            messages.success(request, 'Application submitted successfully!')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Submission failed: {str(e)}')
    return render(request, 'join/join_member.html')

def join_editor(request):
    if request.method == 'POST':
        try:
            editor = JoinEditor.objects.create(
                username=request.POST.get('username'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                linkedin=request.POST.get('linkedin'),
                scopus=request.POST.get('scopus'),
                orchid=request.POST.get('orchid'),
                designation=request.POST.get('designation'),
                qualification=request.POST.get('qualification')
            )
            messages.success(request, 'Application submitted successfully!')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Submission failed: {str(e)}')
    return render(request, 'join/join_editor.html')

def join_reviewer(request):
    if request.method == 'POST':
        try:
            reviewer = JoinReviewer.objects.create(
                username=request.POST.get('username'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                linkedin=request.POST.get('linkedin'),
                scopus=request.POST.get('scopus'),
                orchid=request.POST.get('orchid'),
                designation=request.POST.get('designation'),
                qualification=request.POST.get('qualification'),
                area_of_specialization=request.POST.get('area_of_specialization')
            )
            messages.success(request, 'Application submitted successfully!')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Submission failed: {str(e)}')
    return render(request, 'join/join_reviewer.html')

def submit_paper(request):
    # Check if user is logged in
    if not request.session.get('is_authenticated'):
        messages.error(request, 'Please login to submit a paper')
        return redirect('login')

    if request.method == 'POST':
        try:
            # Get form data
            title = request.POST.get('title')
            authors = request.POST.get('authors')
            abstract = request.POST.get('abstract')
            keywords = request.POST.get('keywords')
            paper_file = request.FILES.get('paper_file')

            # Basic validation
            if not all([title, authors, abstract, keywords, paper_file]):
                messages.error(request, 'All fields are required')
                return render(request, 'submit_paper.html')

            # Get current user
            user_id = request.session.get('user_id')
            user = UserRegistration.objects.get(id=user_id)

            # Create paper submission
            paper = PaperSubmission.objects.create(
                title=title,
                authors=authors,
                abstract=abstract,
                keywords=keywords,
                paper_file=paper_file,
                submitted_by=user
            )

            messages.success(request, 'Paper submitted successfully!')
            return redirect('home')

        except Exception as e:
            messages.error(request, f'Submission failed: {str(e)}')

    return render(request, 'submit_paper.html')

def archives(request):
    return render(request, 'archives.html')

def google_callback(request):
    if request.user.is_authenticated:
        messages.success(request, 'Successfully logged in with Google!')
        return redirect('home')
    messages.error(request, 'Google login failed.')
    return redirect('login')

def profile(request):
    # Check if user is authenticated using session
    if not request.session.get('is_authenticated'):
        messages.warning(request, 'Please login to view your profile.')
        return redirect('login')
    
    try:
        user_id = request.session.get('user_id')
        user_data = UserRegistration.objects.get(id=user_id)
        user_articles = PaperSubmission.objects.filter(submitted_by=user_data).order_by('-submitted_at')
        context = {
            'user_data': user_data,
            'user_articles': user_articles,
        }
        return render(request, 'profile.html', context)
    except UserRegistration.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('home')

def update_profile_image(request):
    # Check if user is authenticated using session
    if not request.session.get('is_authenticated'):
        return JsonResponse({'success': False, 'error': 'Authentication required'})
    
    if request.method == 'POST' and request.FILES.get('profile_image'):
        try:
            user_id = request.session.get('user_id')
            user_data = UserRegistration.objects.get(id=user_id)
            user_data.profile_image = request.FILES['profile_image']
            user_data.save()
            return JsonResponse({'success': True})
        except UserRegistration.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User profile not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def edit_profile(request):
    # Check if user is authenticated using session
    if not request.session.get('is_authenticated'):
        messages.warning(request, 'Please login to edit your profile.')
        return redirect('login')
    
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            user_data = UserRegistration.objects.get(id=user_id)
            
            # Handle profile image upload
            if 'profile_image' in request.FILES:
                # Delete old profile image if it exists
                if user_data.profile_image:
                    if os.path.exists(user_data.profile_image.path):
                        os.remove(user_data.profile_image.path)
                
                # Save new profile image
                profile_image = request.FILES['profile_image']
                fs = FileSystemStorage()
                filename = fs.save(f'profile_images/{user_data.id}_{profile_image.name}', profile_image)
                user_data.profile_image = filename

            # Update user details
            user_data.username = request.POST.get('username')
            user_data.email = request.POST.get('email')
            
            # Save changes
            user_data.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
            
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
    
    # Get user data for the form
    user_id = request.session.get('user_id')
    user_data = UserRegistration.objects.get(id=user_id)
    return render(request, 'edit_profile.html', {'user_data': user_data})

def privacy_view(request):
    return render(request, 'privacy.html')

def terms_view(request):
    return render(request, 'terms.html')

def journals(request):
    # Get all submitted papers/journals
    submitted_papers = PaperSubmission.objects.all().order_by('-submitted_at')
    
    context = {
        'papers': submitted_papers
    }
    return render(request, 'journals.html', context)

def view_article(request, article_id):
    # Check if user is authenticated using session
    if not request.session.get('is_authenticated'):
        messages.warning(request, 'Please login to view article details.')
        return redirect('login')
    
    try:
        article = PaperSubmission.objects.get(id=article_id)
        # Check if the article belongs to the current user
        user_id = request.session.get('user_id')
        user_data = UserRegistration.objects.get(id=user_id)
        
        if article.submitted_by != user_data:
            messages.error(request, 'You do not have permission to view this article.')
            return redirect('profile')
        
        context = {
            'article': article,
            'user_data': user_data
        }
        return render(request, 'article_detail.html', context)
    except PaperSubmission.DoesNotExist:
        messages.error(request, 'Article not found.')
        return redirect('profile')
    except UserRegistration.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('home')
