from django.contrib import admin
from django.conf import settings
from sorl.thumbnail.admin import AdminImageMixin

from models import MultiuploaderImage


class MultiuploaderImageAdmin(AdminImageMixin, admin.ModelAdmin):
    """
    """
    search_fields = ["filename", "key_data", "application", "is_inappropriate"]
    list_display = ["id", "event_image", "my_image_thumb", "image", "application", "userprofile", "event_date", "Flagged"]
    list_filter = ["userprofile", "event_date", "application", "is_irrelevant", "is_inappropriate",]
    #fields = ('filename', 'image', 'key_data', 'application',  'userprofile', 'upload_date', 'caption')

    def Flagged(self, obj):
        if obj.is_irrelevant or obj.is_inappropriate:
            return 'Flagged!'
        return ''

    def event_image(self, obj):
        """
        Thumbnail for admin panel
        """
        image_url = settings.DEFAULT_EVENT_IMAGE

        if obj.event_date:
            event = obj.event_date.event
            if bool(event.main_image):
                image_url = event.main_image.admin_thumb_url()

        return u'<img src="{}"/ width="50"  height="50">'.format(image_url)

    event_image.allow_tags = True

    def my_image_thumb(self, obj):
        image_url = obj.get_thumb(settings.ADMIN_THUMBNAIL_SIZE)
        return u'<img width="60" src="%s" />' % (image_url)
        # else:
        #     return "No Image"
        #my_image_thumb.short_description = 'My Thumbnail'
        #my_image_thumb.allow_tags = True

    my_image_thumb.allow_tags = True

admin.site.register(MultiuploaderImage, MultiuploaderImageAdmin)