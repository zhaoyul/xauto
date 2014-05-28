from django.contrib import admin

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    """
    """

    list_display = ('getEmail', 'getuserName', 'created', 'ip_location', 'city', 'country', )
    search_fields = ['name', 'city', 'country', 'about', 'user__first_name', 'user__last_name', 'user__email',]
    ordering = ('name', 'city' , 'country')
    list_per_page = 30
    list_filter = ['country']
    change_list_filter_template = "admin/filter_listing.html"

    def getuserName(self, obj):
        return '%s-%s' % (obj.user.first_name, obj.user.last_name)

    def getEmail(self, obj):
        return '%s' % (obj.user.email)


admin.site.register(UserProfile, UserProfileAdmin)