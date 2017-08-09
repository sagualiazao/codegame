from django.contrib import admin
from django.contrib.auth.models import Group
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
