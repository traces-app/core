from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.models.fcm_token import FCMToken
from api.serializers.fcm_token_serializer import FCMTokenSerializer

class FCMTokenView(APIView): 
    permission_classes = [IsAuthenticated]
    def get(self, request): 
        user = request.user
        tokens = FCMTokenSerializer.get_user_tokens(user)

        return Response({"tokens": tokens})

    def post(self, request, format=None): 
        token = request.data.get("token")
        user = request.user

        if not token: 
            return Response({"detail": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)        

        try: 
            FCMTokenSerializer.add_user_token(user, token)
            return Response({"detail": "FCM token successfully linked to your account"})

        except Exception as e: 
            return Response({"error": str(e)}, status=500)

    def delete(self, request):
        token = request.data.get("token")
        user = request.user

        if not token: 
            return Response({"detail": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)        
        try: 
            if FCMToken.objects.filter(user=user, token=token).exists(): 
                FCMTokenSerializer.remove_user_token(user, token)
                return Response({"detail": "FCM token successfully deleted"})
            else: 
                return Response({"detail": "Token not found or already deleted"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e: 
            return Response({"error": str(e)}, status=500)
