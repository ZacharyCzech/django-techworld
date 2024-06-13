from django import forms
from .models import Customer, Product
from django_recaptcha.fields import ReCaptchaField


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='E-mail',
        max_length=255,
        error_messages={
            'required': 'To pole nie może być puste!',
            'invalid': 'Niepoprawny e-mail!'
        }
    )
    password = forms.CharField(
        label='Hasło',
        widget=forms.PasswordInput,
        error_messages={
            'required': 'To pole nie może być puste!'
        }
    )


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label='E-mail',
        max_length=255,
        error_messages={
            'required': 'To pole nie może być puste!',
            'invalid': 'Niepoprawny e-mail!'
        }
    )

    password = forms.CharField(
        label='Hasło',
        widget=forms.PasswordInput,
        error_messages={
            'required': 'To pole nie może być puste!'
        }
    )

    repeat_password = forms.CharField(
        label='Powtórz hasło',
        widget=forms.PasswordInput,
        error_messages={
            'required': 'To pole nie może być puste!'
        }
    )

    checkbox = forms.BooleanField(
        label='Akceptuję regulamin sklepu',
        error_messages={
            'required': 'Potwierdź akceptację regulaminu!'
        }
    )

    captcha = ReCaptchaField(
        error_messages={
            'required': 'Potwierdź swoją tożsamość!',
            'invalid': 'Niepoprawna weryfikacja CAPTCHA!'
        }
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError('Ten e-mail jest już zarejestrowany!')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError('Hasło musi mieć przynajmniej 6 znaków!')
        return password

    def clean_repeat_password(self):
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')
        if password != repeat_password:
            raise forms.ValidationError('Hasła muszą być takie same!')
        return repeat_password

    def clean_checkbox(self):
        checkbox = self.cleaned_data.get('checkbox')
        if not checkbox:
            raise forms.ValidationError('Potwierdź akceptację regulaminu!')
        return checkbox

    def save(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        customer = Customer.objects.create_user(email=email, password=password)
        return customer
