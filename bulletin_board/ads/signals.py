from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Ads, Response


@receiver(post_save, sender=Response)
def response_update(instance, **kwargs):
    if not instance.status:
        return
    email = instance.author.email
    subject = f'Ваш отклик принят'
    text_content = (
        f'Принят ваш отклик:\n'
        f'"{instance.text}"\n'
        f'Ссылка на статью: http://127.0.0.1{instance.get_absolute_url()}'
    )
    html_content = (
        f'Принят ваш отклик:<br>'
        f'<p>"{instance.text}"</p><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на статью</a>'
    )
    msg = EmailMultiAlternatives(subject, text_content, None, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(post_save, sender=Response)
def product_created(instance, created, **kwargs):
    if not created:
        return
    email = instance.ads.author.email
    subject = 'У вас новый отклик'
    text_content = (
        f'На вашу статью новый отклик: "{instance.text}"\n'
        f'Принять отклик: http://127.0.0.1:8000/responses/update/{instance.id}'
    )
    html_content = (
        f'На вашу статью новый отклик: "{instance.text}"<br>'
        f'<a href="http://127.0.0.1:8000/responses/update/{instance.id}">'
        f'Принять отклик</a>'
    )
    msg = EmailMultiAlternatives(subject, text_content, None, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(post_save, sender=Ads)
def product_created(instance, created, **kwargs):
    if not created:
        return
    emails = []
    emails.extend(User.objects.filter(
        subscriber__category=instance.category
    ).values_list('email', flat=True))
    subject = f'Новая статья в категории {instance.category}'
    text_content = (
        f'Статья: {instance.header}\n'
        f'Ссылка на статью: http://127.0.0.1{instance.get_absolute_url()}'
    )
    html_content = (
        f'Статья: {instance.header}<br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на статью</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
