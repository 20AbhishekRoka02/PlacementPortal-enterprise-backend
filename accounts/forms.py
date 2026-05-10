# accounts/forms.py

from allauth.account.forms import LoginForm


class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("CUSTOM LOGIN FORM LOADED")

        self.fields['login'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Enter your email',
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Enter your password',
        })

    def login(self, *args, **kwargs):
        return super().login(*args, **kwargs)