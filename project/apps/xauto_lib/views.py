from xauto.lib.utils import flatten_errors

from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.edit import FormMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson as json

class BaseView(View):
    """
    A general-purpose class-based view.
    """
    def redirect(self, next):
        raise Exception
        return HttpResponseRedirect(next)

class JSONResponseMixin(object):
    """
    A mixin that provides the ability to respond in JSON.
    """
    def render_to_response(self, context):
        """
        Return a JSON response containing 'context' as payload.
        """
        return self.get_json_response(self.convert_context_to_json(context))

    def get_context_data(self, *args, **kwargs):
        context = super(JSONResponseMixin, self).get_context_data(*args, **kwargs)
        context['is_ajax'] = self.request.is_ajax()
        return context

    def get_json_response(self, content, **httpresponse_kwargs):
        """
        Construct a response object.
        """
        return HttpResponse(content,
                            content_type='text/plain; charset=utf8',
                            **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        """
        Convert the context dictionary into a JSON object.
        """
        #return self.get_response({
        #    'errors': flatten_errors(self.errors),
        #}, content_type='application/json; charset=utf8')
        if not context.has_key('result'):
            context['result'] = 'ok'
        if context.has_key('form'):
            context['form'] = context['form'].as_p()
        return json.dumps(context)

    def redirect(self, next):
        """
        Perform a redirect using a JSON response.
        """
        return self.render_to_response({'redirect_to': next})

class AdaptiveMixin(JSONResponseMixin, TemplateResponseMixin):
    """
    A mixin for a view that can respond in JSON or HTML.
    """
    valid_responses = {
        'GET': ['html', 'json'],
        'POST': ['html', 'json'],
    }

    def render_to_response(self, context, force_ajax=False, force_html=False):
        """
        Return an appropriate response for request type.
        """
        
        if (force_ajax or self.request.is_ajax()) and not force_html:
            return JSONResponseMixin.render_to_response(self, context)
        else:
            return TemplateResponseMixin.render_to_response(self, context)

    def redirect(self, next):
        """
        Perform a redirect in appropriate response type.
        """
        if self.request.is_ajax():
            return JSONResponseMixin.redirect(self, next)
        else:
            return HttpResponseRedirect(next)

class AdaptiveFormMixin(AdaptiveMixin, FormMixin):
    """
    A mixin providing form handling and adaptive JSON/HTML response.
    """
    def form_invalid(self, form):
        if self.request.is_ajax():
            ctx = {
                'result': 'error',
                'errors': flatten_errors(form.errors),
                'non_field_errors': form.non_field_errors(),
            }
        else:
            ctx = self.get_context_data(form=form)
        return self.render_to_response(ctx)

    def form_valid(self, form):
        self.object = form.save()
        return self.redirect(self.get_success_url())
