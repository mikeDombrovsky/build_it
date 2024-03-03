from django.contrib import admin

from profiles.models import User, Profile, Message


# class UserAdmin(admin.ModelAdmin):
#     list_editable = ['verified']
#     list_display = ['username', 'email']
#
#
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['user', 'wallet', 'verified']


admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Message)
