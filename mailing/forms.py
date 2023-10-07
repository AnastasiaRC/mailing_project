from django import forms
from mailing.models import Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, forms.ModelForm):
    """Для рассылок (создание/редакт)"""
    class Meta:
        model = Mailing
        exclude = ('author', )


class MailingManagerForm(StyleFormMixin, forms.ModelForm):
    """Для изменения статуса рассылки (менеджер) """
    class Meta:
        model = Mailing
        fields = ('status', )
