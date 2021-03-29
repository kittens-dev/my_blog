from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField


class FormWithCaptcha(UserCreationForm):
    
    def __init__(self, data=None):
        super(FormWithCaptcha, self).__init__(data)

    captcha = ReCaptchaField()