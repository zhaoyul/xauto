from django import forms
import django.utils.copycompat as copy
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class MultiFileWidget(forms.Widget):
    needs_multipart_form = True
    
    def __init__(self, attrs=None):
        super(MultiFileWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        widget = forms.FileInput(self.build_attrs(attrs))
        return mark_safe(self.format_output([widget.render(name, None, self.build_attrs(attrs)),
                                             '<input style="margin: 5px 0;" type="button" value="Add another image" onclick="addImage();" /><div class="additional-images"></div>']))

    def value_from_datadict(self, data, files, name):
        if files:
            return files.getlist(name)
        return None

    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)


class MultiImageField(forms.ImageField):
    widget = MultiFileWidget()
    def __init__(self, fields=(), *args, **kwargs):
        super(MultiImageField, self).__init__(*args, **kwargs)
        for f in fields:
            f.required = False
        self.fields = fields

    def to_python(self, files):
        try:
            from PIL import Image
        except ImportError:
            import Image
        if files is None:
            return None
        for data in files:
            if hasattr(data, 'temporary_file_path'):
                file = data.temporary_file_path()
            else:
                if hasattr(data, 'read'):
                    file = StringIO(data.read())
                else:
                    file = StringIO(data['content'])
            try:
                trial_image = Image.open(file)
                trial_image.load()
                if hasattr(file, 'reset'):
                    file.reset()
                trial_image = Image.open(file)
                trial_image.verify()
            except ImportError:
                raise
            except Exception: # Python Imaging Library doesn't recognize it as an image
                raise ValidationError(self.error_messages['invalid_image'])
        return files