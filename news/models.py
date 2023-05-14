from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_(
        'The user who becomes the author'))
    rating = models.SmallIntegerField(default=0, verbose_name=_('Authors rating'))

    def update_rating(self):
        postRat = self.post_set
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.author_user.comment_set
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return str(self.author_user)

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=_('Category'))
    subscribers = models.ManyToManyField(User, related_name='categories', verbose_name=_('Subscribers'))

    def __str__(self):
        return self.name.title()

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    ]
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_('Author'))
    category_type = models.CharField(
        max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE, verbose_name=_('Type of post'))
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_('Date creation'))
    post_category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128, verbose_name=_('Title'))
    text = models.TextField(verbose_name=_('Text'))
    rating = models.SmallIntegerField(default=0, verbose_name=_('Rating'))

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:128] + '...'

    def count(self):
        count = 0
        count += 1
        return count

    def __str__(self):
        return self.title.title()

    def get_absolute_url(self):
        return reverse('news:post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')


class PostCategory(models.Model):
    post_through = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_('Post'))
    category_through = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Category'))

    def __str__(self):
        return f' {self.post_through.title} | {self.category_through.name}'

    class Meta:
        verbose_name = _('Categories of post')
        verbose_name_plural = _('Categories of posts')


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_('Comment'))
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    text = models.TextField(verbose_name=_('Сomment text'))
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_('Date the comment was created'))
    rating = models.SmallIntegerField(default=0, verbose_name=_('Comment Rating'))

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.text.title()

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
