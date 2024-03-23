from django.contrib import admin

from profiles.models import User, Profile, Message, Task, Service

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(Task)
admin.site.register(Service)
