"""
Формы приложения core.
ВКР-035: ContactMessageForm — форма обратной связи.
ВКР-036: LoginForm, RegisterForm — аутентификация и регистрация.
ВКР-038: ProjectCreateForm — создание заявки клиентом (F02).
"""

import re
from django import forms
from django.contrib.auth import authenticate, get_user_model
from .models import ContactMessage, Project, Service, Priority

User = get_user_model()

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


# ─── Константы: аутентификация (ВКР-036) ─────────────────────────────────────

USERNAME_MIN_LENGTH = 3
PASSWORD_MIN_LENGTH = 8

ERR_INVALID_CREDENTIALS = 'Неверный логин или пароль.'
ERR_ACCOUNT_INACTIVE    = 'Учётная запись отключена. Обратитесь к администратору.'
ERR_USERNAME_TOO_SHORT  = (
    f'Логин должен содержать не менее {USERNAME_MIN_LENGTH} символов.'
)
ERR_PASSWORD_TOO_SHORT  = (
    f'Пароль должен содержать не менее {PASSWORD_MIN_LENGTH} символов.'
)
ERR_PASSWORDS_MISMATCH  = 'Пароли не совпадают.'
ERR_USERNAME_EXISTS     = 'Пользователь с таким логином уже существует.'
ERR_EMAIL_EXISTS        = 'Пользователь с таким email уже зарегистрирован.'


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


# ─── Форма входа (ВКР-036) ───────────────────────────────────────────────────

class LoginForm(forms.Form):
    """
    Форма авторизации по username + password.
    authenticate() вызывается в clean() — не в view, чтобы держать логику в форме.
    """
    username = forms.CharField(
        label='Логин',
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ваш логин',
            'autocomplete': 'username',
        }),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'autocomplete': 'current-password',
        }),
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self._authenticated_user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get('username', '').strip()
        password = cleaned.get('password', '')

        if username and password:
            user = authenticate(self.request, username=username, password=password)
            if user is None:
                raise forms.ValidationError(ERR_INVALID_CREDENTIALS)
            if not user.is_active:
                raise forms.ValidationError(ERR_ACCOUNT_INACTIVE)
            self._authenticated_user = user
        return cleaned

    def get_user(self):
        return self._authenticated_user


# ─── Форма регистрации (ВКР-036) ─────────────────────────────────────────────

class RegisterForm(forms.ModelForm):
    """
    Форма регистрации нового пользователя с ролью client (F01).
    Пароль вводится дважды для подтверждения.
    """
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Не менее 8 символов',
            'autocomplete': 'new-password',
        }),
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Повторите пароль',
            'autocomplete': 'new-password',
        }),
    )

    class Meta:
        model  = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username':   forms.TextInput(attrs={
                'placeholder': 'Латинские буквы и цифры',
                'autocomplete': 'username',
            }),
            'email':      forms.EmailInput(attrs={
                'placeholder': 'ivan@example.com',
                'autocomplete': 'email',
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Иван',
                'autocomplete': 'given-name',
            }),
            'last_name':  forms.TextInput(attrs={
                'placeholder': 'Иванов',
                'autocomplete': 'family-name',
            }),
        }
        labels = {
            'username':   'Логин',
            'email':      'Email',
            'first_name': 'Имя',
            'last_name':  'Фамилия',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if len(username) < USERNAME_MIN_LENGTH:
            raise forms.ValidationError(ERR_USERNAME_TOO_SHORT)
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(ERR_USERNAME_EXISTS)
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(ERR_EMAIL_EXISTS)
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1', '')
        if len(password) < PASSWORD_MIN_LENGTH:
            raise forms.ValidationError(ERR_PASSWORD_TOO_SHORT)
        return password

    def clean(self):
        cleaned   = super().clean()
        password1 = cleaned.get('password1', '')
        password2 = cleaned.get('password2', '')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', ERR_PASSWORDS_MISMATCH)
        return cleaned

    def save(self, commit=True):
        """Сохраняет пользователя с хэшированным паролем."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


# ─── Форма создания заявки (ВКР-038) ─────────────────────────────────────────

TITLE_MIN_LENGTH = 5

ERR_TITLE_TOO_SHORT = (
    f'Тема заявки должна содержать не менее {TITLE_MIN_LENGTH} символов.'
)


class ProjectCreateForm(forms.ModelForm):
    """
    Форма создания новой заявки клиентом (F02).
    Поля user и status заполняются во view, не в форме.
    """

    class Meta:
        model  = Project
        fields = ['title', 'description', 'service', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Кратко опишите тему заявки',
                'autofocus': True,
            }),
            'description': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Подробно опишите задачу, проблему или вопрос…',
            }),
            'service': forms.Select(),
            'priority': forms.Select(),
        }
        labels = {
            'title':       'Тема заявки',
            'description': 'Описание',
            'service':     'Услуга',
            'priority':    'Приоритет',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Только активные услуги
        self.fields['service'].queryset = (
            Service.objects.filter(is_active=True).order_by('title')
        )
        self.fields['priority'].queryset = Priority.objects.all()
        # service и priority — обязательные
        self.fields['service'].empty_label  = '— Выберите услугу —'
        self.fields['priority'].empty_label = '— Выберите приоритет —'

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < TITLE_MIN_LENGTH:
            raise forms.ValidationError(ERR_TITLE_TOO_SHORT)
        return title
