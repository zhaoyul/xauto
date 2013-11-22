from urllib2 import urlopen, HTTPError
from django.utils import simplejson


class VideoHelperFactory(object):
    
    @staticmethod
    def get_helper(url):
        url = url.replace('http://', '').replace('https://', '')
        if 'www.youtube.com/' in url:
            video_id = url.replace('www.youtube.com/watch?v=', '').split('&', 1)[0]
            return YouTubeHelper(video_id)

        elif 'vimeo.com/' in url:
            video_id = url.replace('vimeo.com/', '').replace('/', '')
            return VimeoHelper(video_id)

        elif 'www.metacafe.com/' in url:
            video_id = url.replace('www.metacafe.com/watch/', '').split('/', 1)[0]
            return MetaCafeHelper(video_id)

        elif 'www.dailymotion.com/' in url:
            video_id = url.replace('www.dailymotion.com/video/', '')\
                          .replace('/', '').split('_', 1)[0].split('#', 1)[0]
            return DailyMotionHelper(video_id)

        else:
            return None


class VideoHelper(object):
    provider = ''
    video_id = ''
    
    def __init__(self, video_id):
        self.video_id = video_id
    
    @staticmethod
    def open_url(url):
        u = urlopen(url)
        result = u.read()
        u.close()
        return result

    def video_url_validation(self, url):
        return {'status': 0}

    def get_embed_url(self, url):
        raise NotImplementedError

    def get_thumbnail_link(self, url):
        raise NotImplementedError


class YouTubeHelper(VideoHelper):
    provider = 'youtube'

    def get_thumbnail_link(self):
        return 'http://img.youtube.com/vi/%s/0.jpg' % self.video_id

    def get_embed_url(self):
        return 'http://www.youtube.com/embed/%s?showinfo=0' % self.video_id

    def video_url_validation(self):
        status = 0
        message = None
        url = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2&alt=json' % self.video_id
        try:
            resp = VideoHelper.open_url(url)
        except (HTTPError, ValueError):
            status = 1
            message = 'Enter a valid URL.'
        else:
            image_data = simplejson.loads(resp)
            if 'media$rating' in image_data['entry']['media$group']:
                status = 1
                message = 'Adult content - URL blocked.'
        result = {'status': status}
        if message is not None:
            result['message'] = message
        return result


class VimeoHelper(VideoHelper):
    provider = 'vimeo'

    def get_thumbnail_link(self):
        resp = VideoHelper.open_url('http://vimeo.com/api/v2/video/%s.json' % self.video_id)
        image_data = simplejson.loads(resp)
        thumbnail_link = image_data[0].get('thumbnail_large', None)
        if thumbnail_link is None:
            thumbnail_link = image_data[0].get('thumbnail_medium')
        return thumbnail_link

    def get_embed_url(self):
        return 'http://player.vimeo.com/video/%s?portrait=0&amp;color=ffffff' % self.video_id

    def video_url_validation(self):
        status = 0
        message = None
        url = 'http://vimeo.com/' + self.video_id
        try:
            resp = VideoHelper.open_url(url)
        except (HTTPError, ValueError):
            status = 1
            message = 'Enter a valid URL.'
        else:
            if resp.find('<span class="badge_rating explicit">') != -1:
                status = 1
                message = 'Adult content - URL blocked.'
        result = {'status': status}
        if message is not None:
            result['message'] = message
        return result


class MetaCafeHelper(VideoHelper):
    provider = 'metacafe'

    def get_thumbnail_link(self):
        return 'http://s3.mcstatic.com/thumb/%s.jpg' % self.video_id

    def get_embed_url(self):
        return 'http://www.metacafe.com/embed/' + self.video_id

    def video_url_validation(self):
        status = 0
        message = None
        url = 'http://www.metacafe.com/api/item/' + self.video_id
        try:
            resp = VideoHelper.open_url(url)
        except (HTTPError, ValueError):
            status = 1
            message = 'Enter a valid URL.'
        else:
            if resp.find('<item>') == -1:
                status = 1
                message = 'Enter a valid URL.'
            else:
                if resp.find('<media:rating scheme="urn:simple">adult</media:rating>') != -1:
                    status = 1
                    message = 'Adult content - URL blocked.'
        result = {'status': status}
        if message is not None:
            result['message'] = message
        return result


class DailyMotionHelper(VideoHelper):
    provider = 'dailymotion'

    def get_thumbnail_link(self):
        return 'http://www.dailymotion.com/thumbnail/video/' + self.video_id

    def get_embed_url(self):
        return 'http://www.dailymotion.com/embed/video/' + self.video_id

    def video_url_validation(self):
        status = 0
        message = None
        url = 'https://api.dailymotion.com/videos?ids=%s&fields=explicit' % self.video_id
        try:
            resp = VideoHelper.open_url(url)
        except (HTTPError, ValueError):
            status = 1
            message = 'Enter a valid URL.'
        else:
            image_data = simplejson.loads(resp)
            if len(image_data['list']) == 0:
                status = 1
                message = 'Enter a valid URL.'
            else:
                if image_data['list'][0]['explicit']:
                    status = 1
                    message = 'Adult content - URL blocked.'
        result = {'status': status}
        if message is not None:
            result['message'] = message
        return result
