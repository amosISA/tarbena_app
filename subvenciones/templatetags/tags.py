from django import template
from django.contrib.auth.models import Group
import datetime

register = template.Library()

def has_group(user, group_name):
    """
    Check in template if user belongs to a specific group
    """
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

register.filter('has_group', has_group)

def htmlattributes(value, arg):
    """
    So that I can use this filter to add attributes to my elements in templates such as:
    {{ form.email|htmlattributes:"class : something, id: openid_identifier" }}
    So my input email now have a class=something and id=openid_identifier
    """
    attrs = value.field.widget.attrs

    data = arg.replace(' ', '')
    kvs = data.split(',')

    for string in kvs:
        kv = string.split(':')
        attrs[kv[0]] = kv[1]

    rendered = str(value)
    return rendered

register.filter('htmlattributes', htmlattributes)

# I use this for debugging objects into the templates
def debug_object_dump(var):
    return vars(var)

register.filter('debug_object_dump', debug_object_dump)

def days_until(value):
    """
    Returns number of days between value and today
    Example usage in template:
    {% load days_until %}
    {{ ending_time|daysuntil }}
    """
    today = datetime.date.today()
    try:
        diff = value - today
    except TypeError:
        # convert datetime.datetime to datetime.date
        diff = value.date() - today

    if diff.days > 1:
        return '{days}d'.format(days=diff.days)
    elif diff.days == 0:
        return 'expires today'
    elif diff.days < -2:
        return 'passed days'
    else:
        # Date is in the past; return expired message
        return 'expired'

register.filter('daysuntil', days_until)

def split_value(value):
    """
    If username is: Juan Pablo:
    this returns: JP
    """
    str_word = str(value)
    words = str_word.split()
    letters = [word[0] for word in words]
    return "".join(letters)

register.filter('split_value', split_value)


@register.filter
def truncatesmart(value, limit=80):
    """
    Truncates a string after a given number of chars keeping whole words.

    Usage:
        {{ string|truncatesmart }}
        {{ string|truncatesmart:50 }}
    """

    try:
        limit = int(limit)
    # invalid literal for int()
    except ValueError:
        # Fail silently.
        return value

    # Make sure it's unicode
    # python 3
    value = str(value)

    # python 2
    #value = unicode(value)

    # Return the string itself if length is smaller or equal to the limit
    if len(value) <= limit:
        return value

    # Cut the string
    value = value[:limit]

    # Break into words and remove the last
    words = value.split(' ')[:-1]

    # Join the words and return
    return ' '.join(words) + '...'