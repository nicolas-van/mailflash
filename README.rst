mailflash
=========

A simple python library to send emails.

With mailflash, sending mail can be as simple as this: ::

    from mailflash import Mail, Message

    mail = Mail()
    message = Message("Hello",
                      sender="from@example.com",
                      recipients=["to@example.com"])
    mail.send(message)

This basic example will work perfectly fine on a Unix machine with a local SMTP server with classic configuration. In
other cases you'll just have to configure your SMTP server.

Installing mailflash
--------------------

Install with ``pip`` or ``easy_install``::

    pip install mailflash

Configuring mailflash
---------------------

``mailflash`` is configured through the arguments passed to the constructor of the ``Mail`` class. Those arguments
can be coded explicitly in your program or come from a JSON configuration file, as example.

* ``server`` : default ``'localhost'``
* ``port`` : default ``25``
* ``use_tls`` : default ``False``
* ``use_ssl`` : default ``False``
* ``debug`` : default ``False``
* ``username`` : default ``None``
* ``password`` : default ``None``
* ``default_sender`` : default ``None``. When the value ``None`` is used mailflash will automatically detect the
  sender's email by using *current_user@current_machine_hostname*. Can also be a two-elements tuple, the first one being
  the name and the second one the email address.
* ``max_emails`` : default ``None``
* ``suppress`` : default ``False``

Emails are managed through a ``Mail`` instance::

    from mailflash import Mail, Message

    mail = Mail(default_sender="mysender@example.com")

In this case all emails are sent using the configuration values that
were passed to the ``Mail`` class constructor.

Alternatively you can set up your ``Mail`` instance later at configuration time, using the
``init_mail`` method::

    mail = Mail()

    mail.init_mail(default_sender="mysender@example.com")

Sending messages
----------------

To send a message first create a ``Message`` instance::

    msg = Message("Hello",
                  sender="from@example.com",
                  recipients=["to@example.com"])

You can set the recipient emails immediately, or individually::

    msg.recipients = ["you@example.com"]
    msg.add_recipient("somebodyelse@example.com")

Setting the ``sender`` is facultative. If not set, maiflash will use the ``default_sender`` configured in the ``Mail``
object.::

    msg = Message("Hello",
                  recipients=["to@example.com"])

If the ``sender`` is a two-element tuple, this will be split into name
and address::

    msg = Message("Hello",
                  sender=("Me", "me@example.com"))

    assert msg.sender == "Me <me@example.com>"

The message can contain a body and/or HTML::

    msg.body = "testing"
    msg.html = "<b>testing</b>"

Finally, to send the message, you use the ``Mail`` instance.::

    mail.send(msg)


Bulk emails
-----------

Usually in a web application you will be sending one or two emails per request. In certain situations
you might want to be able to send perhaps dozens or hundreds of emails in a single batch - probably in
an external process such as a command-line script or cronjob.

In that case you do things slightly differently::

    with mail.connect() as conn:
        for user in users:
            message = '...'
            subject = "hello, %s" % user.name
            msg = Message(recipients=[user.email],
                          body=message,
                          subject=subject)

            conn.send(msg)


The connection to your email host is kept alive and closed automatically once all the messages have been sent.

Some mail servers set a limit on the number of emails sent in a single connection. You can set the max amount
of emails to send before reconnecting by specifying the ``max_emails`` setting.

Attachments
-----------

Adding attachments is straightforward::

    with open("image.png") as fp:
        msg.attach("image.png", "image/png", fp.read())

Unit tests and suppressing emails
---------------------------------

When you are sending messages inside of unit tests, or in a development
environment, it's useful to be able to suppress email sending.

If the setting ``suppress`` is set to ``True``, emails will be
suppressed. Calling ``send()`` on your messages will not result in
any messages being actually sent.

However, it's still useful to keep track of emails that would have been
sent when you are writing unit tests.

In order to keep track of dispatched emails, use the ``record_messages``
method::

    with mail.record_messages() as outbox:

        mail.send_message(subject='testing',
                          body='test',
                          recipients=emails)

        assert len(outbox) == 1
        assert outbox[0].subject == "testing"

The ``outbox`` is a list of ``Message`` instances sent.

Header injection
----------------

To prevent `header injection <http://www.nyphp.org/PHundamentals/8_Preventing-Email-Header-Injection>`_ attempts to send
a message with newlines in the subject, sender or recipient addresses will result in a ``BadHeaderError``.

Signalling support
------------------

``mailflash`` provides signalling support through a ``email_dispatched`` signal. This is sent whenever an email is
dispatched (even if the email is not actually sent, i.e. in a testing environment).

A function connecting to the ``email_dispatched`` signal takes a ``Message`` instance as a first argument, and the
``Mail`` instance as an optional argument::

    def log_message(message, app):
        print(message.subject)

    email_dispatched.connect(log_message)

Rationale
---------

``mailflash`` is a fork of Flask-Mail ( https://github.com/mattupstate/flask-mail ). I needed a good library to send mails
that could easily be configured using a configuration file. Flask-Mail seemed good for that but I wanted to use it
outside of a web application. So I removed the dependency to Flask and created mailflash.
