# Email task when create/update subsidie
from celery import task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
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

@task
def subvencion_responsable_email(user_username, name_subv, object, url, mail, email_list_users):
    """
    Task to send an e-mail notification when a subsidie is
    assigned to someone.
    """
    html_message = loader.render_to_string(
        'subvenciones/email/subv_email_responsable.html',
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

# @periodic_task(
#     run_every=(crontab(minute='*/1')),
#     name="task_alert_changed_estado",
#     ignore_result=True
# )
import datetime
@task
def task_alert_changed_estado(object, name_subv, estado_subv, url, mail, email_list_users):
    """
    Alert System. The app sends and email to the superadmin users when
    the subsidie changes his state to "Cerrada a la espera de resolución (id=1)" and "Solicitada con detalles por definir (id=3)".
    """

    current_time = datetime.datetime.now()
    html_message = loader.render_to_string(
        'subvenciones/email/subv_email_alert_estado.html',
        {
            'name_subv': name_subv,
            'object': object,
            'url': url,
            'estado_subv': estado_subv
        }
    )

    mail_sent = send_mail('Gestión de subvenciones',
                          '',
                          mail,
                          email_list_users,  # recievers
                          html_message=html_message
                          )

    return mail_sent