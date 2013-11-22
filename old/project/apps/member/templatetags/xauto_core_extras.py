from django import template
from django.contrib.auth.forms import AuthenticationForm
from lib.utils import CheckNumeric

from xauto.member.views.userprofile import get_user_address, get_userprofile_reviews
from django.core.urlresolvers import reverse
from event.models import *
from member.models import *
from django.db.models import Q
from event.models import FeedbackRating, Event
from django.conf import settings

register = template.Library()

@register.inclusion_tag('partials/stars_view.html')
def star_rating(percentage, color, box_add_class=''):
    return {
        'percentage': percentage,
        'color': color,
        'box_add_class': box_add_class,
    }


@register.inclusion_tag('partials/menu_links.html')
def menu_links(active, user):
    menu = ({'name':'Home', 'link': reverse('home'), 'active': active == 'home', 'needlogin': False},
            {'name':'My xauto', 'link': reverse('dashboard'), 'active': active == 'service', 'needlogin': True},
            {'name':'Account', 'link': reverse('account'), 'active': active == 'account', 'needlogin': True},
            {'name':'Help', 'link': reverse('help'), 'active': active == 'help', 'needlogin': False}
           )
    return {'menu': menu, 'user': user}


@register.inclusion_tag('partials/categories_list_with_child.html')
def categories_list_childs(category):
    return {
        'categories': get_categories_with_parent(category)
    }

@register.inclusion_tag('partials/location_info.html', takes_context=True)
def user_location(context):
    return {'user_address': get_user_address(context['request'])}


@register.inclusion_tag('partials/located_near.html', takes_context=True)
def located_near(context):
    if context.get('located_near_override', False):
        return {'count': context.get('located_near_override', 0)}

    try:
        event_list = Event.objects.within_radius()
    except:
        count = 0
        return {'count': count}
    try:
        servicetypes, category, servicetype = get_services_and_category(int(context.get('servicetype_id', 0)), int(context.get('category_id', 0)))
        if servicetype:
            event_list = event_list.filter(Q(service_type=servicetype))
            count = event_list.count()
        elif category:
            count = get_events_count(category)
        else:
            raise Exception()
    except Exception:
        count = event_list.count()
    return {'count': count}


@register.inclusion_tag('partials/distance_value.html', takes_context=True)
def distance_value(context):
    request = context['request']
    return {'distance': request.session.get('filter_distance', 200)}


@register.inclusion_tag('partials/items_per_page.html', takes_context=True)
def items_per_page(context):
    request = context['request']
    url = request.get_full_path()
    path = url.split('?')
    if len(path) > 1:
        url_parse = path[1].split('&')
        path_parts = []
        for i, param in enumerate(url_parse):
            if not 'per_page=' in param:
                path_parts.append(param)
        url = '&'.join(path_parts)
        if len(path_parts):
            url = '%s?%s&' % (path[0], url)
        else:
            url = '%s?' % path[0]
    else:
        url += '?'
    return {'items_page': int(request.session.get('items_per_page', '5')),
            'pages_choice': (5, 10, 15, 20, 25, 50, 0,),
            'url': url}


@register.inclusion_tag('partials/profile_reviews.html')
def profile_reviews(user):
    return {'reviews': get_userprofile_reviews(user)}

@register.filter(name='hash')
def hash(value, arg):
    if arg:
        return value.as_widget(attrs={'class': "error-input" })
    else:
        return value.as_widget()

@register.filter(name='timedelta')
def timedelta(value):
    from datetime import datetime, timedelta
    # if not isinstance(value, timedelta):
    #     value = value - datetime.today()
    hours, remainder = divmod(value.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '%dd %dh %dmin' % (value.days, hours, minutes)

@register.inclusion_tag('partials/messages/messages_menu.html', takes_context=True)
def messages_menu(context, message):
    return {'m': message, 'modification': context['user'].id}
    #modification need to confuse user id in users lists

@register.inclusion_tag('partials/login_signup_box.html', takes_context=True)
def login_signup_menu(context):
    user = context['user']

    return {'menu': True, 'user': user}


@register.inclusion_tag('partials/login_signup_box.html', takes_context=True)
def login_signup_box(context):
    user = context['user']
    login_next_url = ''
    if user.is_anonymous():

        sign_up_form = signup_form(context['request'])

        login_form = AuthenticationForm(data=context['request'].POST if context['request'].path == '/login/' and context['request'].method == 'POST' else None)
        #raise Exception(context['request'].POST.get('username'))
        #import pdb; pdb.set_trace()
        if context['request'].GET.get('next', False):
            login_next_url = '?next=%s' % context['request'].GET.get('next', False)
        login_form.is_valid()
    else:
        sign_up_form = None
        login_form = None

    _username = context['request'].COOKIES.get('auto_fill_username', False)

    #login_form = AuthenticationForm( data=context['request'].POST)
    next_path = context['request'].GET.get('next', '')
    return {'menu': False, 'user': user, 'auto_fill_username': _username, 'login_next': login_next_url, 'signup_form': sign_up_form, 'login_form': login_form, 'c': context, 'next': next_path}



@register.filter()
def getFeedbackStatus(event, user):
    """
    get Feedback status
    """

    returnStatus = ""
    typeUser = ""

    if event:

        # -----------------------------------------------------------------
        # --- determine if current Logged user is a provide or Customer ---
        if event.author == user:
            typeUser = 'c'
        else:
            if event.current_active_bid:
                if event.current_active_bid.provider == user:
                    typeUser = 'p'

        # ----------------------------------------------------------------
        # --- for specific case try to check if feedback has been left ---
        if event.current_active_status == 'completed' and event.current_active_bid:
            if (event.current_active_bid.feedback_customer_left and typeUser == 'p') or (event.current_active_bid.feedback_provider_left and typeUser == 'c'):
                returnStatus = 'Feedback Left'
            else:
                returnStatus = 'No Feedback'

    return returnStatus




@register.filter()
def roundValue(value, decimal=1):
    """
    get number of Rating the user received
    """

    if CheckNumeric(value, wcheck='FLOAT') and CheckNumeric(decimal, wcheck='INT'):
        if value > settings.MINI_VALUE_ROUND or value == 0:
            return int(value)
        return round(value, int(decimal))
    return value


@register.filter()
def getuserRatingCount(user):
    """
    get number of Rating the user received
    """
    nbrRatings = FeedbackRating.active.filter(author=user).count()
    return nbrRatings

