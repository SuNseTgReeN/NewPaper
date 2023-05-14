from django import forms
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'post_category',
            'title',
            'text',
            'category_type',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")
        if title is not None and len(title) < 20:
            raise ValidationError({
                "title": "Описание не может быть менее 20 символов."
            })

        if title[0].islower():
            raise ValidationError({
                "title": "Описание не может начинаться с маленькой буквы."
            })

        if text == title:
            raise ValidationError(
                "Описание не должно быть идентично тексту поста."
            )

        return cleaned_data


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
