from django.shortcuts import HttpResponse, redirect
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
User = get_user_model()

class ActivateUser(View):
    def get(self, request, uid, token):
        try:
            uid = urlsafe_base64_decode(uid).decode('utf-8')
            user = User.objects.get(id=uid)
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return HttpResponse("Your Account is Activated")
            else:
                return HttpResponse("Invalid ID")
        except User.DoesNotExist:
            return HttpResponse("User Doesn't Exist.")
        