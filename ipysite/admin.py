import os

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.http import HttpResponse

from models import UserProfile, NoteBookServerAccessConfiguration


# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'
    

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    

class UserProfileAdmin(admin.ModelAdmin):
    list_display   = ('username', 'name', 'email', 'nbserver_port', 'nbserver_password', 'access_enabled' )
    
    actions = ['enable_nbserver_access', 'disable_nbserver_access']

    
    def _change_access(self, queryset, enable):
        for user_profile in queryset:
                user_profile.access_enabled = enable
                user_profile.save() 
                
    def enable_nbserver_access(self, request, queryset):
        """ Enable notebook server access the selected users"""
        self._change_access(queryset, enable=True)
    enable_nbserver_access.short_description = "Enable Notebook server access for selected users"

    def disable_nbserver_access(self, request, queryset):
        """ Disable notebook server access the selected users"""
        self._change_access(queryset, enable=False)
    disable_nbserver_access.short_description = "Disable Notebook server access for selected users"



class NoteBookServerAccessConfigurationAdmin(admin.ModelAdmin):
    actions = ['view_selected_file_contents', 'reset_access']
    list_display = ('input_file', 'used_for', 'applied_at')
    
    def __init__(self, *args, **kwargs):
        super(NoteBookServerAccessConfigurationAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )
    
    def view_selected_file_contents(self, request, queryset):
        """ Shows the contents of the Config files"""
        response = HttpResponse()
        content = []
        for config_file in queryset:
            content.append(config_file.input_file.read())
        response.content = content
        return response
    view_selected_file_contents.short_description = "View selected file contents (shows in another window)"
    
    def reset_access(self, request, queryset):    
        """ Disable all user access """
        profiles = UserProfile.objects.all()
        for profile in profiles:
            profile.access_enabled = False
            profile.save()
    reset_access.short_description = 'Disable all user access to Notebook servers (except staff)'

# Register models
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(NoteBookServerAccessConfiguration, NoteBookServerAccessConfigurationAdmin)
