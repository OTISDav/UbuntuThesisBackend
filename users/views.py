from rest_framework import status
from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, update_session_auth_hash
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt
from .utils import send_verification_email  # ta fonction d'envoi mail
from django.contrib.auth.hashers import make_password
from .models import NotificationPreference, Profile
from .serializers import (
    RegisterSerializer,
    NotificationPreferenceSerializer,
    ProfileSerializer,
    ChangePasswordSerializer,
    UpdateProfileSerializer,
)

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    # def post(self, request):
    #     serializer = RegisterSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            try:
                send_verification_email(user, settings.FRONTEND_URL)
            except Exception as e:
                return Response({
                    "detail": "Compte créé mais email non envoyé.",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({"detail": "Compte créé. Un email d'activation a été envoyé."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    # def post(self, request):
    #     username = request.data.get('username')
    #     password = request.data.get('password')
    #     user = authenticate(username=username, password=password)
    #
    #     if user:
    #         refresh = RefreshToken.for_user(user)
    #         return Response({
    #             'refresh': str(refresh),
    #             'access': str(refresh.access_token),
    #         })
    #     return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if not user.is_verified:
                return Response({'error': 'Veuillez vérifier votre adresse email avant de vous connecter.'},
                                status=status.HTTP_403_FORBIDDEN)

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Identifiants invalides.'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetailView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        profile, created = Profile.objects.get_or_create(user=user)
        return profile


class NotificationPreferenceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        preference, _ = NotificationPreference.objects.get_or_create(user=request.user)
        serializer = NotificationPreferenceSerializer(preference)
        return Response(serializer.data)

    def post(self, request):
        preference, _ = NotificationPreference.objects.get_or_create(user=request.user)
        serializer = NotificationPreferenceSerializer(instance=preference, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
            update_session_auth_hash(request, request.user)  # Important pour garder l'utilisateur connecté
            return Response({'message': 'Mot de passe changé avec succès.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = UpdateProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(ProfileSerializer(profile).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()

# class AccountActivationView(APIView):
#     permission_classes = []
#
#     def get(self, request):
#         token = request.query_params.get('token')
#         if not token:
#             return render(request, 'activation_result.html', {'message': "Token manquant."})
#
#         try:
#             payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
#
#             if payload.get('type') != 'email_verification':
#                 return render(request, 'activation_result.html', {'message': "Token invalide."})
#
#             if payload.get('exp') < timezone.now().timestamp():
#                 return render(request, 'activation_result.html', {'message': "Lien expiré."})
#
#             user_id = payload.get('user_id')
#             user = User.objects.get(id=user_id)
#
#             if user.is_verified and user.is_active:
#                 return render(request, 'activation_result.html', {'message': "Compte déjà activé."})
#
#             user.is_verified = True
#             user.is_active = True
#             user.save()
#
#             return render(request, 'activation_result.html', {'message': "Compte activé, vous pouvez vous connecter."})
#
#         except jwt.ExpiredSignatureError:
#             return render(request, 'activation_result.html', {'message': "Lien expiré."})
#         except jwt.InvalidTokenError:
#             return render(request, 'activation_result.html', {'message': "Token invalide."})
#         except User.DoesNotExist:
#             return render(request, 'activation_result.html', {'message': "Utilisateur introuvable."})



class AccountActivationView(APIView):
    permission_classes = []

    def get(self, request):
        token = request.query_params.get('token')
        context = {}

        if not token:
            context['message'] = "Token manquant."
            return render(request, 'users/activation_result.html', context)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            if payload.get('type') != 'email_verification':
                context['message'] = "Token invalide."
                return render(request, 'users/activation_result.html', context)

            if payload.get('exp') < timezone.now().timestamp():
                context['message'] = "Lien expiré."
                return render(request, 'users/activation_result.html', context)

            user_id = payload.get('user_id')
            user = User.objects.get(id=user_id)

            if user.is_verified and user.is_active:
                context['message'] = "Compte déjà activé."
                return render(request, 'users/activation_result.html', context)

            user.is_verified = True
            user.is_active = True
            user.save()

            context['message'] = "Compte activé, vous pouvez vous connecter."
            return render(request, 'users/activation_result.html', context)

        except jwt.ExpiredSignatureError:
            context['message'] = "Lien expiré."
        except jwt.InvalidTokenError:
            context['message'] = "Token invalide."
        except User.DoesNotExist:
            context['message'] = "Utilisateur introuvable."

        return render(request, 'users/activation_result.html', context)