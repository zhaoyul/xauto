from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils import simplejson
from django.core.mail import mail_admins
from xauto.lib.utils import set_cookie

import sys
import string

LOCK_MODES = (
    'ACCESS SHARE',
    'ROW SHARE',
    'ROW EXCLUSIVE',
    'SHARE UPDATE EXCLUSIVE',
    'SHARE',
    'SHARE ROW EXCLUSIVE',
    'EXCLUSIVE',
    'ACCESS EXCLUSIVE',
)

def require_lock(model, lock):
    """
    Decorator for PostgreSQL's table-level lock functionality

    Example:
        @transaction.commit_on_success
        @require_lock(MyModel, 'ACCESS EXCLUSIVE')
        def myview(request)
            ...

    PostgreSQL's LOCK Documentation:
    http://www.postgresql.org/docs/8.3/interactive/sql-lock.html
    """
    def require_lock_decorator(view_func):
        def wrapper(*args, **kwargs):
            if lock not in LOCK_MODES:
                raise ValueError('%s is not a PostgreSQL supported lock mode.')
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute(
                'LOCK TABLE %s IN %s MODE' % (model._meta.db_table, lock)
            )
            return view_func(*args, **kwargs)
        return wrapper
    return require_lock_decorator

# django_template based on http://www.djangosnippets.org/snippets/596/

decorator_with_args = lambda decorator: lambda *args, **kwargs: lambda func: decorator(func, *args, **kwargs )

templates = {}

def django_template_to_string(request, variables, template):
    """
    usage:

    django_template_to_string(request, { 'title' : 'hello' }, "base.html")
    """
    device = getattr(request, 'device', '')
    cached = 'Template not cached'
    if not settings.DEBUG:
        temp = templates.get(template + device)
        cached = 'Template cached'
        if temp is None:
            temp = loader.get_template(template)
            templates[template + device] = temp

    else:
        temp = loader.get_template(template)

    c = RequestContext(request)
    c.update(variables)
    c['cached'] = cached
    return temp.render(c)

@decorator_with_args
def render_to(func, template=None):
    """
    usage:

    @render_to("moja_strona.html")
    def master_home(request):
        variables = { 'title' : "Hello World!" }
        return variables
    """
    def wrapper(request, *args, **kwargs):

        response = func(request, *args, **kwargs)

        # -- store in flash the last current form used ---
        try:

            arrayTemplate = string.split(template,'/')
            templateName = arrayTemplate[len(arrayTemplate)-1]
            currentForm = string.split(templateName,'.')[0]
        except:
            currentForm = template
        request.flash['html_form'] = currentForm

        if isinstance(response, HttpResponse):
            return response
        stringForm = django_template_to_string(request, response, template)
        return HttpResponse(stringForm)

    wrapper.__name__ = func.__name__
    wrapper.__dict__ = func.__dict__
    wrapper.__doc__ = func.__doc__
    return wrapper

@decorator_with_args
def render_to_cookies(func, template=None):
    """
    usage:

    @render_to("moja_strona.html")
    def master_home(request):
        variables = { 'title' : "Hello World!" }
        return variables
    """
    def wrapper(request, *args, **kwargs):

        try:
            (response, cookies)  = func(request, *args, **kwargs)
        except:
            response = func(request, *args, **kwargs)
            cookies = None

        # -- store in flash the last current form used ---
        try:

            arrayTemplate = string.split(template,'/')
            templateName = arrayTemplate[len(arrayTemplate)-1]
            currentForm = string.split(templateName,'.')[0]
        except:
            currentForm = template
        request.flash['html_form'] = currentForm

        if isinstance(response, HttpResponse):
            return response
        stringForm = django_template_to_string(request, response, template)
        responseHttp = HttpResponse(stringForm)
        if cookies:
            set_cookie(responseHttp, cookies['key'], cookies['value'])

        return responseHttp

    wrapper.__name__ = func.__name__
    wrapper.__dict__ = func.__dict__
    wrapper.__doc__ = func.__doc__
    return wrapper



@decorator_with_args
def render_paginated_to(func, template=None):
    """
    A conversion of django.views.generic.object_list to a decorator

    usage:

    @render_paginated_to("moja_strona.html")
    def master_home(request):
        variables = {
             'object_list': items,
             'allow_empty': True,
             'paginate_by': 5 }
        return variables
    """
    def wrapper(request, *args, **kwargs):
        page = kwargs.pop('page', None)
        allow_empty = kwargs.pop('allow_empty', False)
        variables = func(request, *args, **kwargs)

        object_list = variables['object_list']
        paginate_by = int(request.GET.get('pref_search_pager', 0))
        if not paginate_by:
            paginate_by = variables.get('paginate_by', 10)

        paginator = Paginator(object_list, paginate_by, allow_empty_first_page=allow_empty)
        if not page:
            page = request.GET.get('page', '1')
        try:
            page = int(page)
        except ValueError:
            if page == 'last':
                page = paginator.num_pages
            else:
                # Page is not 'last', nor can it be converted to an int
                raise Http404

        try:
            objects = paginator.page(page)
        except InvalidPage:
            try:
                objects = paginator.page(paginator.num_pages)
            except EmptyPage:
                objects = None

        get = request.GET.copy()
        get.pop('page', None)
        get.pop('pgc', None)
        base_query_string = get.urlencode()

        variables.update({
            'objects': objects,
            'paginate_by': paginate_by,
            'page': page,
            'paginate_options': [5, 10, 25, 50, 100],
            'base_query_string': base_query_string,
            })
        string = django_template_to_string(request, variables, template)
        return HttpResponse(string)

    wrapper.__name__ = func.__name__
    wrapper.__dict__ = func.__dict__
    wrapper.__doc__ = func.__doc__
    return wrapper

def json_view(func):
    def wrap(request, *a, **kw):
        response = None
        try:
            response = func(request, *a, **kw)
            assert isinstance(response, dict)
            if 'result' not in response:
                response['result'] = 'ok'
        except Exception, e:
            # Mail the admins with the error
            exc_info = sys.exc_info()
            subject = 'JSON view error: %s' % request.path
            try:
                request_repr = repr(request)
            except:
                request_repr = 'Request repr() unavailable'
            import traceback
            message = 'Traceback:\n%s\n\nRequest:\n%s' % (
                '\n'.join(traceback.format_exception(*exc_info)),
                request_repr,
                )
            #mail_admins(subject, message, fail_silently=True)

            # Come what may, we're returning JSON.
            if hasattr(e, 'message'):
                msg = e.message
            else:
                msg = 'Internal error: ' + str(e)
            response = {'result': 'error',
                        'text': msg}

        cookies = []
        if 'cookies' in response:
            cookies = response['cookies']
            del response['cookies']

        json = simplejson.dumps(response)
        http_response = HttpResponse(json, content_type='application/json; charset=utf8')

        for cookie in cookies:
            http_response.set_cookie(**cookie)
        return http_response

    wrap.__name__ = func.__name__
    wrap.__dict__ = func.__dict__
    wrap.__doc__ = func.__doc__
    return wrap

def post_required(func):
    """
    Decorator that returns an error unless request.method == 'POST'.
    """
    def post_wrapper(request, *args, **kwds):
        if request.method != 'POST':
            return HttpResponse('This requires a POST request.', status=405)
        return func(request, *args, **kwds)

    post_wrapper.__name__ = func.__name__
    return post_wrapper

def ajax_required(func):
    """
    Decorator that returns an error unless request.is_ajax == True.
    """
    def post_wrapper(request, *args, **kwds):
        if not request.is_ajax():
            return HttpResponse('This requires an XMLHttpRequest request.', status=405)
        return func(request, *args, **kwds)

    post_wrapper.__name__ = func.__name__
    return post_wrapper


from django.template.loader import render_to_string

def json_post_view(func):
    """
    Decorate a view returning HttpResponse on GET and json data on POST.
    """
    def wrap(request, *a, **kw):

        method = request.method
        if request.method == 'GET' and not request.is_ajax():
            response = func(request, *a, **kw)
            if isinstance(response, unicode):
                response = HttpResponse(response)
            return response

        try:
            response = func(request, *a, **kw)
            if isinstance(response, unicode):
                response = {'html': response}
            assert isinstance(response, dict)
            if 'result' not in response:
                response['result'] = 'ok'
        except KeyboardInterrupt:
            # Allow keyboard interrupts through for debugging.
            raise
        except Exception, e:
            # Mail the admins with the error
            exc_info = sys.exc_info()
            subject = 'JSON view error: %s' % request.path
            try:
                request_repr = repr(request)
            except:
                request_repr = 'Request repr() unavailable'
            import traceback
            message = 'Traceback:\n%s\n\nRequest:\n%s' % (
                '\n'.join(traceback.format_exception(*exc_info)),
                request_repr,
                )
            mail_admins(subject, message, fail_silently=True)

            # Come what may, we're returning JSON.
            if hasattr(e, 'message'):
                msg = e.message
            else:
                msg = 'Internal error: ' + str(e)
            response = {'result': 'error',
                        'text': msg}

        cookies = []
        if 'cookies' in response:
            cookies = response['cookies']
            del response['cookies']

        json = simplejson.dumps(response)
        http_response = HttpResponse(json, content_type='application/json; charset=utf8')

        for cookie in cookies:
            http_response.set_cookie(**cookie)
        return http_response

    wrap.__name__ = func.__name__
    wrap.__dict__ = func.__dict__
    wrap.__doc__ = func.__doc__
    return wrap
