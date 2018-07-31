# Email task when create/update subsidie
from celery import task
from django.core.mail import send_mail
from django.template import loader

@task
def subvencion_mention_email(user_username, name_subv, object, url, mail, email_list_users):
    """
    Task to send an e-mail notification when a user is
    mentioned in a subsidie.
    """
    html_message = loader.render_to_string(
        'subvenciones/email/subv_email_mention.html',
        {
            'name_actor': user_username,
            'name_subv': name_subv,
            'object': object,
            'url': url
        }
    )

    mail_sent = send_mail('Gestión de subvenciones',
              '',
              mail,
              email_list_users,  # recievers
              html_message=html_message
              )

    return mail_sent

@task
def subvencion_create_email(user_username, name_subv, object, url, mail, email_list_users):
    """
    Task to send an e-mail notification when a subsidie is
    successfully created.
    """
    html_message = loader.render_to_string(
        'subvenciones/email/subv_email_create.html',
        {
            'name_actor': user_username,
            'name_subv': name_subv,
            'object': object,
            'url': url
        }
    )

    mail_sent = send_mail('Gestión de subvenciones',
              '',
              mail,
              email_list_users,  # recievers
              html_message=html_message
              )

    return mail_sent

@task
def subvencion_edit_email(user_username, name_subv, object, url, mail, email_list_users):
    """
    Task to send an e-mail notification when a subsidie is
    successfully edited.
    """
    html_message = loader.render_to_string(
        'subvenciones/email/subv_email_edit.html',
        {
            'name_actor': user_username,
            'name_subv': name_subv,
            'object': object,
            'url': url
        }
    )

    mail_sent = send_mail('Gestión de subvenciones',
              '',
              mail,
              email_list_users,  # recievers
              html_message=html_message
              )

    return mail_sent