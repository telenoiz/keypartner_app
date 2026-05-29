"""
Формы приложения core.
ВКР-035: ContactMessageForm — форма обратной связи.
"""

import re
from django import forms
from .models import ContactMessage

# ─── Константы валидации ─────────────────────────────────────────────────────

# Минимальная длина текста обращения
MESSAGE_MIN_LENGTH = 10

# Regexp для проверки телефона: +7 (999) 123-45-67 или пусто
PHONE_REGEX = re.compile(r'^\+?[\d\s\-() ]{7,20}$')

# Сообщения об ошибках
ERR_MESSAGE_TOO_SHORT = (
    f'Текст обращения должен содержать не менее {MESSAGE_MIN_LENGTH} символов.'
)
ERR_PHONE_INVALID = (
    'Введите корректный номер телефона (например, +7 999 123-45-67).'
)


# ─── Форма ───────────────────────────────────────────────────────────────────

class ContactMessageForm(forms.ModelForm):
    """
    Форма обратной связи.
    Доступна анонимным и авторизованным пользователям (F02).
    Поле phone — необязательное.
    """

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Иван Иванов',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'ivan@example.com',
                'autocomplete': 'email',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+7 999 123-45-67',
                'autocomplete': 'tel',
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'Кратко опишите тему обращения',
            }),
            'message': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Подробно опишите ваш вопрос или предложение…',
            }),
        }
        labels = {
            'name':    'Ваше имя',
            'email':   'Email',
            'phone':   'Телефон',
            'subject': 'Тема',
            'message': 'Сообщение',
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if phone and not PHONE_REGEX.match(phone):
            raise forms.ValidationError(ERR_PHONE_INVALID)
        return phone

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < MESSAGE_MIN_LENGTH:
            raise forms.ValidationError(ERR_MESSAGE_TOO_SHORT)
        return message
