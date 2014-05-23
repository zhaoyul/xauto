from models import MultiuploaderImage
from django.contrib import admin
from sorl.thumbnail import default
ADMIN_THUMBS_SIZE = '60x60'
from sorl.thumbnail.admin import AdminImageMixin




class MultiuploaderImageAdmin(AdminImageMixin, admin.ModelAdmin):
    """
    """

    search_fields = ["filename", "key_data", "application", "is_inappropriate"]
    list_display = ["id", "EVENT_IMAGE", "filename", "image", "application", "userprofile", "event_date", "Flagged"]
    list_filter = ["userprofile", "event_date", "application", "is_irrelevant", "is_inappropriate",]
    #fields = ('filename', 'image', 'key_data', 'application',  'userprofile', 'upload_date', 'caption')

    def Flagged(self, obj):
        if obj.is_irrelevant or obj.is_inappropriate:
            return 'Flagged!'
        return ''

    def my_image_thumb(self, obj):
        if obj.image:
            thumb = default.backend.get_thumbnail(obj.image.file, ADMIN_THUMBS_SIZE)
            return u'<img width="%s" src="%s" />' % (thumb.width, thumb.url)
        else:
            return "No Image"
        #my_image_thumb.short_description = 'My Thumbnail'
        #my_image_thumb.allow_tags = True

admin.site.register(MultiuploaderImage, MultiuploaderImageAdmin)