==========
Crontab
==========
The cron daemon is a long-running process that executes commands at specific dates and times. You can use this to schedule activities, either as one-time events or as recurring tasks.

Usage
-----
I use it for making a database backup. First I need to activate my virtualenvironment so I create a bash script like this:
::

    # backup.sh
    #!/bin/bash
    # Script - Backup my app
    source /home/admin/tarbena/bin/activate
    python /home/backup2.py

What I do here is activate my virtualenv and then I execute my python script that contains the command for generating the json with my data and send an email with the backup:
::

    import os
    import subprocess
    import smtplib
    import datetime
    import os.path as op
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.utils import COMMASPACE, formatdate
    from email import encoders

    def send_mail(send_from, send_to, subject, message, files=[],
                  server="smtp.gmail.com", port=587, username='myemail@gmail.com', password='myemailpassword',
                  use_tls=True):
        """Compose and send email with provided info and attachments.

        Args:
            send_from (str): from name
            send_to (str): to name
            subject (str): message title
            message (str): message body
            files (list[str]): list of file paths to be attached to email
            server (str): mail server host name
            port (int): port number
            username (str): server auth username
            password (str): server auth password
            use_tls (bool): use TLS mode
        """
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = send_to
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        msg.attach(MIMEText(message))

        for path in files:
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="{}"'.format(op.basename(path)))
            msg.attach(part)

        smtp = smtplib.SMTP(server, port)
        if use_tls:
            smtp.starttls()
        smtp.login(username, password)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.quit()

    my_file = "/home/subsidies.json"

    if os.path.exists(my_file):
            os.remove("/home/subsidies.json")

    subprocess.call(["python", "/home/admin/tarbena/src/manage.py", "dumpdata", "subvenciones", "--indent=2", "--output=/home/subsidies.json"])

    now = datetime.datetime.now()
    send_mail('agoraweb700@gmail.com', ", ".join(['amosisa700@gmail.com', 'jctarbena@gmail.com']), 'Tarbena app DB Backup', 'Tarbena app DB Backup a fecha de {0}'.format(now), ['/home/subsidies.json'])

.. note::
    To make email work I need to install email and don't name ur script like `email.py`. `pip install email`.
    Also give ur scripts permissions to be executed: `chmod ugo+x backup.sh (the same with backup2.py or do it by reference chmod --reference=backup.sh backup2.py)`.

Crontab commands
----------------
::

    crontab -e # it opens the editor and at the bottom you can add your task to repeat

    # you can add it like so
    */5 * * * * /home/backup.sh # it will repeat the script every 5mins

    crontab -l # to list your repeating scripts added

`Good page to calculate your repeating time: every monday, every 5mins, etc <https://crontab.guru/every-5-minutes>`_