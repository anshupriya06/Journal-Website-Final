from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_editor = models.BooleanField(default=False)
    is_reviewer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'login_register'
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.email

class UserRegistration(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'login_register'

    def __str__(self):
        return self.email
class Journal(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey('UserRegistration', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class PaperSubmission(models.Model):
    PAPER_STATUS = (
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    )

    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=500)
    abstract = models.TextField()
    keywords = models.CharField(max_length=200)
    paper_file = models.FileField(upload_to='papers/')
    submitted_by = models.ForeignKey('UserRegistration', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=PAPER_STATUS, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'paper_submissions'

    def __str__(self):
        return f"{self.title} by {self.authors}"

class JoinMember(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    linkedin = models.URLField(max_length=200)
    scopus = models.CharField(max_length=100)
    orchid = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    class Meta:
        db_table = 'join_member'

    def __str__(self):
        return f"{self.username} - {self.email}"

class JoinEditor(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    linkedin = models.URLField(max_length=200)
    scopus = models.CharField(max_length=100)
    orchid = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    class Meta:
        db_table = 'join_editor'

    def __str__(self):
        return f"{self.username} - {self.email}"

class JoinReviewer(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    linkedin = models.URLField(max_length=200)
    scopus = models.CharField(max_length=100)
    orchid = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    area_of_specialization = models.CharField(max_length=200, default='Not Specified')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    class Meta:
        db_table = 'join_reviewer'

    def __str__(self):
        return f"{self.username} - {self.email}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='unread')

    class Meta:
        db_table = 'contact_queries'

    def __str__(self):
        return f"{self.name} - {self.subject}"
