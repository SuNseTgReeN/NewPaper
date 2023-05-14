from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory
from modeltranslation.admin import TranslationAdmin


class AuthorAdmin(admin.ModelAdmin):
    model = Author
    list_display = ('author_user', 'rating')
    list_filter = ('author_user', 'rating')
    search_fields = ('author_user', 'rating')


class SubscribersInLine(admin.TabularInline):
    model = Category.subscribers.through


class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


class CategoryAdmin(TranslationAdmin):
    model = Category
    inlines = [
        SubscribersInLine, PostCategoryInline
    ]
    exclude = ('subscribers',)
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


class PostAdmin(TranslationAdmin):
    model = Post
    inlines = [
        PostCategoryInline
    ]
    list_display = ('title', 'date_creation', 'category_type', 'post_author', 'rating')
    list_filter = ('date_creation', 'category_type', 'post_author', 'rating')
    search_fields = ('title', 'category_type')


class CommentAdmin(TranslationAdmin):
    model = Comment
    list_display = ('comment_post', 'text', 'comment_user', 'date_creation', 'rating')
    list_filter = ('comment_post', 'text', 'comment_user', 'date_creation', 'rating')
    search_fields = ('comment_post', 'text', 'comment_user', 'date_creation', 'rating')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PostCategory)
