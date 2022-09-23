import requests
from django.conf import settings

def verify_recaptcha(token):
    data = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': token
    }
    r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
    success = r.json()["success"]
    return True 

