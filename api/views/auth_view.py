from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from firebase_admin import auth
from django.contrib.auth import get_user_model
from api.models.user import StandardUser, MerchantAdministrator, LogisticsAdministrator, Driver
from api.serializers.user_serializer import StandardUserSerializer, MerchantAdministratorSerializer, LogisticsAdministratorSerializer, DriverSerializer 
from rest_framework.decorators import api_view


User = get_user_model()
class Authenticate(TokenObtainPairView): 
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        firebase_token = request.data.get("firebase_token")
        user = None
        try: 
            if firebase_token: 
                user = self.firebase_login(request)
            elif email and password: 
                user = self.password_login(request)
            else:
                return Response({"detail": "Invalid request, provide credentials"}, status=status.HTTP_400_BAD_REQUEST)     
        except Exception as e: 
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        if user: 
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=status.HTTP_200_OK)
        else: 
            return Response({"detail": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
            

    def password_login(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        return authenticate(request, email=email, password=password)

    def firebase_login(self, request): 
        firebase_token = request.data.get("firebase_token")
        
        decoded_token = auth.verify_id_token(firebase_token)
        uid = decoded_token.get("uid")
        email = decoded_token.get("email", f"{uid}@firebase.com") # default if the email is missing

        return User.objects.get(email=email, firebase_uid=uid)


class CreateUserView(APIView): 
    def post(self, request, format=None):
        user_role = request.data.get("role")
        user=None

        try: 
            serializer = None
            match str(user_role).lower(): 
                case "standard": 
                    serializer = StandardUserSerializer(data=request.data)
                case "merchant": 
                    serializer = MerchantAdministratorSerializer(data=request.data)
                case "logistics": 
                    serializer = LogisticsAdministratorSerializer(data=request.data)
                case "driver": 
                    serializer = DriverSerializer(data=request.data)
                                    
            if serializer.is_valid(): 
                user = serializer.save()   
                if user: 
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                    }, status=status.HTTP_200_OK)
            else: 
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e: 
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
    """
        {
            "email": "info@lithika.me", 
            "password": "password", 

            "role": "standard",
            "first_name": "lithika",
            "last_name": "damnod", 
        }

        {
            "firebase_token": "token", 

            "role": "standard",
            "first_name": "lithika",
            "last_name": "damnod", 
        }

        {
            "role": "merchant",
            "business_name": "business_name",
            "description:" "description", 
        }

        {
            "role": "logistics",
            "logistics_name": "logistics_name",
            "description:" "description", 
        }

        {
            "role": "driver",
            "logistics_id": "e009ekjrelk8421341",
            "first_name": "something",
            "last_name" "something", 
        }
    """


from rest_framework.permissions import IsAuthenticated

class UserInfoView(APIView): 
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user 
        match str(user.role).lower(): 
            case "standard":  
                user = StandardUser.objects.get(id=user.id)
                serializer = StandardUserSerializer(user)
            case "merchant":  
                user = MerchantAdministrator.objects.get(id=user.id)
                serializer = MerchantAdministratorSerializer(user)
            case "logistics":  
                user = LogisticsAdministrator.objects.get(id=user.id)
                serializer = LogisticsAdministratorSerializer(user)
            case "driver":  
                user = Driver.objects.get(id=user.id)
                serializer = DriverSerializer(user)
        return Response(serializer.data)


@api_view(['GET'])
def check_email_availability(request): 
    email = request.GET.get('email', None)
    
    if not email: 
        return Response({'detail': 'Email parameter is required'})

    # check if the email is taken 
    email_exists = User.objects.filter(email=email).exists() 

    return Response({
        'availability': not email_exists,
        'detail':  'Email is available' if not email_exists else 'Email is already taken'
    })
