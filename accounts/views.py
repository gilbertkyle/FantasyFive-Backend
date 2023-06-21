from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .serializers import UserSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from django_rest_passwordreset.signals import reset_password_token_created, post_password_reset

User = get_user_model()

# Create your views here.


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:

            data = request.data

            username = data['username']
            password = data['password']
            email = data.get('email', '')

            if User.objects.filter(username=username).exists():
                return Response({"error": "A User with that username already exists"}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            user.save()
            refresh = MyTokenObtainPairSerializer().get_token(user) # gets updated tokens with user info
            
            # final confirmation the user exists
            if User.objects.filter(username=username).exists():
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": 'Something went wrong when creating your account'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except:
            return Response({"error": "Something went wrong when creating your account 2"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoadUserView(APIView):
    # authentication_classes = ()

    def get(self, request, format=None):
        try:

            user = request.user
            user = UserSerializer(user)

            return Response(
                {'user': user.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when trying to load user'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'token': reset_password_token.key,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(
                reverse('password_reset:reset-password-confirm')),
            reset_password_token.key),
        'frontend_url': 'http://localhost:3000/account/password-set?token={}&username={}'.format(reset_password_token.key, reset_password_token.user.username),

    }

    # render email text
    email_html_message = render_to_string(
        'email/user_reset_password.html', context)
    email_plaintext_message = render_to_string(
        'email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="FantasyFive.club"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()


@receiver(post_password_reset)
def post_password_reset(sender, user, *args, **kwargs):
    print("password saved")


class UpdatePasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def patch(self, request, *args, **kwargs):
        body = request.data
        user = self.request.user
        if not user.check_password(body["oldPassword"]):
            raise ValidationError("invalid password")
        user.set_password(body["newPassword"])
        user.save()
        return Response(status=status.HTTP_200_OK)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer