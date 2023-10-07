from django import forms
from mailing.forms import StyleFormMixin
from message.models import Message


class MessageForm(StyleFormMixin, forms.ModelForm):
    """Для сообщений (создания/редакт)"""

    class Meta:
        model = Message
        exclude = ('author',)
