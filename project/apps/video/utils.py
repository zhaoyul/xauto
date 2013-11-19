from django.template.loader import render_to_string

def render_youtube_video_tag(youtube_url, style):
    template = 'video/%s.html' % style
    return render_to_string(template, {'youtube_url': youtube_url})
