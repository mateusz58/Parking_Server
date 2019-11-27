from django.core.mail import EmailMessage
email = EmailMessage('Hello', 'World', to=['matp321@mail.com'])
email.send()