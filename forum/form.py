#coding:utf-8
from functools import reduce

from django import forms
from django.conf import settings
from captcha.fields import CaptchaField
from forum.models import Post, Comment
from user.models import User, Friend, Team

DJANGO_FORUM_APP_FILTER_PROFANE_WORDS = getattr(settings, 'DJANGO_FORUM_APP_FILTER_PROFANE_WORDS', False)

# class MessageForm(forms.ModelForm):
#     class Meta:
#         model = Message
#         fields = ('content', )



class PostForm(forms.ModelForm):

    content = forms.CharField(
        widget = forms.Textarea(attrs={'class': 'form-control', 'rows': '3'})
    )

    title = forms.CharField(
        widget = forms.TextInput(attrs={'class': 'form-control'})
    )

    captcha = CaptchaField(error_messages={'invalid': 'wrong validation code'})
    class Meta:
        model = Post
        fields = ('title', 'content')

    # def clean_body(self):
    #     body = self.cleaned_data["body"]
    #
    #     if DJANGO_FORUM_APP_FILTER_PROFANE_WORDS:
    #         profane_words = ProfaneWord.objects.all()
    #         bad_words = [w for w in profane_words if w.word in body.lower()]
    #
    #         if bad_words:
    #             raise forms.ValidationError(_("Bad words like '%s' are not allowed in posts.") % (
    #                 reduce(lambda x, y: "%s,%s" % (x, y), bad_words)))
    #
    #     return body

class CommentForm(forms.ModelForm):
    captcha = CaptchaField(error_messages={'invalid': 'wrong validation code'})
    class Meta:
        model = Comment
        fields = ('content', )