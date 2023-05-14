from .models import Category, Post, Comment
from modeltranslation.translator import register, TranslationOptions


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('post_author', 'category_type', 'date_creation', 'post_category', 'title', 'text')


@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ('comment_post', 'comment_user', 'text', 'date_creation')
