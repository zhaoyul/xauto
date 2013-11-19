from xauto.video.utils import render_youtube_video_tag

from django.template import Library, Node, Variable

from django.utils.safestring import mark_safe
from django.utils.html import escape

register = Library()

class YouTubeVideoNode(Node):
    "Display youtube video player."
    def __init__(self, youtube_url, style):
        self.youtube_url, self.style = Variable(youtube_url), style

    def render(self, context):
        youtube_url = self.youtube_url.resolve(context)
        return render_youtube_video_tag(youtube_url, self.style)

@register.tag
def youtube(parser, token):
    """
    Render a YouTube video player.
    
    Usage::
    
        {% youtube [youtube_url] [full|preview] %}
    """
    tokens = token.contents.split()
    if len(tokens) != 3:
        raise TemplateSyntaxError, "'%r' tag requires two variables." % tokens[0]

    style = tokens[2]
    if style[0] in ('"', "'") and style[0] == style[-1]:
        style = style[1:-1]

    return YouTubeVideoNode(tokens[1], style)
