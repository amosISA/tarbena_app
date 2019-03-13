from django.contrib.auth.models import User
from django.db.models import Q


def get_users_by_permission_q(permission_name, include_superusers=True):
    """ Returns the Q object suitable for querying users by permission. If include_superusers
    is true (default) all superusers will be also included. Otherwise
    only users with explicitely set permissions will be included. """
    (appname, codename) = permission_name.split(".")

    query = \
        Q(user_permissions__codename=codename, user_permissions__content_type__app_label=appname) | \
        Q(groups__permissions__codename=codename, groups__permissions__content_type__app_label=appname)

    if include_superusers:
        query |= Q(is_superuser=True)

    # The above query may return multiple instances of User objects if user
    # has overlapping permissions. Hence we are using a nested query by unique
    # user ids.
    #return {'pk__in': User.objects.filter(query).distinct().values('pk')}
    return User.objects.filter(query).distinct()


def get_users_by_permission(permission_name, include_superusers=True):
    """ Returns the queryset of User objects with the given permission. Permission name
    is in the form appname.permission similar to the format
    required by django.contrib.auth.decorators.permission_required
    """
    return User.objects.filter(get_users_by_permission_q(permission_name, include_superusers))


"""
https://code.djangoproject.com/ticket/18763#comment:1

Example of use
In models:
    class MyModel:
        my_fk_field = models.ForeignKey(User, limit_choices_to=dict(is_active=True, \
            *get_users_by_permission_q("myapp.change_my_model", False)))

In views:
    users = get_users_by_permission("subvenciones.add_subvencion")

To list all permissions use this command in the console: 
    python manage.py get_all_permissions
"""