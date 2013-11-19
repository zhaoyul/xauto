from forms import YouTubePreviewForm
from utils import render_youtube_video_tag
from xauto.lib.decorators import json_view
from xauto.lib.utils import flatten_errors

@json_view
def preview(request):
    form = YouTubePreviewForm(request.GET)
    import time
    time.sleep(1)
    if form.is_valid():
        return {
            'html': render_youtube_video_tag(form.cleaned_data['youtube_url'], 'full'),
        }

    else:
        return {
            'result': 'error',
            'errors': flatten_errors(form.errors),
        }
