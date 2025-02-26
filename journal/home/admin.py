from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserRegistration, Journal, PaperSubmission, JoinMember, JoinEditor, JoinReviewer, Contact

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(UserRegistration)
admin.site.register(Journal)
admin.site.register(PaperSubmission)
admin.site.register(JoinMember)
admin.site.register(JoinEditor)
admin.site.register(JoinReviewer)
admin.site.register(Contact)