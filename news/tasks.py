from django.conf import settings

from celery import shared_task
import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from news.models import Post, Category

today = datetime.datetime.now()
last_week = today - datetime.timedelta(days=7)


#############
# Еженедельная отправка писем
#############

def set_posts():  # Получаю посты и возвращаю их на выход
    posts = Post.objects.filter(date_creation__gte=last_week)
    return posts


def set_categories():  # Получаю категории постов, используя функцию set_posts()
    posts = set_posts()
    categories = set(posts.values_list('post_category__name', flat=True))  # тут опечатка 'post_catts.values_liegory__name'
    return categories


def set_subscribers():  # Получаю подписчиков определённых категорий, использую функцию set_categories()
    categories = set_categories()
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    return subscribers


@shared_task
def weekly_newsletter():  # Отправляю письма подписчикам категорий, каждую неделю, используя функцию set_subscribers()
    subscribers = set_subscribers()
    posts = set_posts()
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


#############
# Отправка писем при создании поста
#############

# Отправляю письма подписчикам категорий, используя функцию set_subscribers()
@shared_task
def send_notifications(preview, pk, title):
    subscribers = set_subscribers()
    html_context = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()
