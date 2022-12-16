from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, \
    SetPasswordForm
from django.contrib.auth.hashers import check_password
from django.utils import timezone

# from accounts.views import change_password
from core.utils import change_password_help_text

UserModel = get_user_model()


class DeleteProfileForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = UserModel
        fields = ('confirm_password',)
        # labels = {
        #     'confirm_password': 'Потвърждаване на паролата'
        # }

    def clean(self):
        cleaned_data = super(DeleteProfileForm, self).clean()
        confirm_password = cleaned_data.get('confirm_password')
        if not check_password(confirm_password, self.instance.password):
            self.add_error('confirm_password', 'Паролата на съвпада.')

    def save(self, commit=True):
        user = super(DeleteProfileForm, self).save(commit)
        user.last_login = timezone.now()
        if commit:
            self.instance.delete()

        return self.instance


class ConfirmPasswordForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(ConfirmPasswordForm, self).clean()
        confirm_password = cleaned_data.get('confirm_password')
        if not check_password(confirm_password, self.instance.password):
            self.add_error('confirm_password', 'Паролата не съвпада.')

    def save(self, commit=True):
        user = super(ConfirmPasswordForm, self).save(commit)
        user.last_login = timezone.now()
        if commit:
            user.save()
        return user


class UserCreateForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'username', 'email',
                  'building_code', 'password1', 'password2')


class AdminUserCreateForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'username', 'email',
                  'building_code', 'is_admin', 'admin_code',
                  'password1', 'password2')

        labels = {
            'is_admin': 'Аз съм домоуправител.'
        }


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'placeholder': 'Username'}
        )
        self.fields['password'].widget.attrs.update(
            {'placeholder': 'Password'}
    )

    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data['username']
        existing = UserModel.objects.filter(username=username).exists()
        if not existing:
            raise forms.ValidationError("Грешно потребителско име!")
        return username


class CustomPasswordChangeForm(PasswordChangeForm):
    error_messages = {
        **SetPasswordForm.error_messages,
        "password_incorrect": (
            "Паролата беше въведена грешно. Моля, опитайте отново."
        ),
    }
    old_password = forms.CharField(
        label=("Стара парола"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )

    new_password1 = forms.CharField(
        label=("Нова парола"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=change_password_help_text()
        # help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Потвърди новата парола",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

