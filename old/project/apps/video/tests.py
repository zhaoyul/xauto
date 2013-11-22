__test__ = {"doctest": """

>>> from models import Video
>>> from forms import VideoModelForm

>>> v = Video(title='Title', type='rating', youtube_id='abcde')
>>> v.youtube_url()
u'http://www.youtube.com/v/abcde'

>>> f = VideoModelForm()
>>> f.is_valid()
False

>>> f = VideoModelForm({'title': 'Title', 'type': 'rating'})
>>> f.is_valid()
False

>>> f.errors
{'youtube_id': [u'This field is required.']}

>>> f = VideoModelForm({'title': 'Title', 'type': 'rating', 'youtube_id': 'abcde'})
>>> f.is_valid()
False

>>> f.errors
{'youtube_id': [u'Invalid YouTube ID entered.']}

>>> f = VideoModelForm({'title': 'Title', 'type': 'rating', 'youtube_id': 'http://www.youtube.com/watch?v=_xHIjlQ6v'})
>>> f.is_valid()
False

>>> f = VideoModelForm({'title': 'Title', 'type': 'rating', 'youtube_id': 'http://www.youtube.com/watch?v=_xHIjlQ6vgU&feature=channel'})
>>> f.is_valid()
True

>>> f = VideoModelForm({'title': 'Title', 'type': 'rating', 'youtube_id': '_xHIjlQ6vgU'})
>>> f.is_valid()
True

"""}

