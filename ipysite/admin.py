from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from models import UserProfile

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'
    

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    
    actions = ['enable_nbserver_access', 'disable_nbserver_access']
    
    
    def _change_access(self, queryset, enable):
        for obj in queryset:
            user_profiles = UserProfile.objects.filter(user=obj)
            if user_profiles:
                user_profile = user_profiles[0]
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


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
