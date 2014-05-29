from sorl.thumbnail import get_thumbnail
from django.conf import settings


class ThumbMixin(object):
    image_field_name = 'image'

    def get_thumb(self, size):
        image = getattr(self, self.image_field_name)

        if image:
            try:
                img = get_thumbnail(image,
                                    size,
                                    crop='center',
                                    quality=99)
                return img.url
            except IOError:
                pass
            return image.url

        return u''

    def list_thumb_url(self):
        return self.get_thumb(settings.LIST_THUMBNAIL_SIZE)

    def photoviewer_url(self):
        return self.get_thumb(settings.PHOTOVIEWER_SIZE)

    def card_thumb_url(self):
        return self.get_thumb(settings.CARD_THUMBNAIL_SIZE)

    def hero_thumb_url(self):
        return self.get_thumb(settings.HERO_THUMBNAIL_SIZE)

    def admin_thumb_url(self):
        return self.get_thumb(settings.ADMIN_THUMBNAIL_SIZE)

    def small_thumb_url(self):
        return self.get_thumb(settings.SMALL_THUMBNAIL_SIZE)