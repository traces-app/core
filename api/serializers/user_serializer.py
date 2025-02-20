from rest_framework import serializers
from api.models.user import StandardUser, MerchantAdministrator, LogisticsAdministrator, Driver
from api.utils import firebase 

class BaseUserSerializer(serializers.ModelSerializer):
    firebase_token = serializers.CharField(required=False, write_only=True)
    password = serializers.CharField(required=False, allow_null=True, allow_blank=True, write_only=True)
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)

    class Meta: 
        abstract = True

    def validate(self, attrs): 
        email = attrs.get("email")
        password = attrs.get("password")
        firebase_token = attrs.get("firebase_token")

        if not password and not firebase_token: 
            raise serializers.ValidationError({"password, firebase_token": "Either password or Firebase token is required."})

        if email and not password:
            raise serializers.ValidationError({"password": "Password is required when email is provided."})

        if password and not email:
            raise serializers.ValidationError({"email": "Email is required when password is provided."})

        if firebase_token: 
            firebase_uid, extracted_email = firebase.validateFirebaseToken(firebase_token) 
            email = extracted_email

            # check if the firebase uid is already associated with an account
            if StandardUser.objects.filter(firebase_uid=firebase_uid).exists():
                raise serializers.ValidationError({"firebase_token": "User with this Firebase UID already exists."})

            attrs["firebase_uid"] = firebase_uid
            attrs["email"] = extracted_email

        # check if the email is already associated with an account
        if StandardUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "User with this Email already exists."})
         
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        firebase_token = validated_data.pop('firebase_token', None)

        # create firebase user
        if not firebase_token and password: 
            if(not validated_data.get("firebase_uid", None)): 
                firebase_uid = firebase.createFirebaseUser(validated_data.get("email"), password)
                validated_data['firebase_uid'] = firebase_uid

        user = self.Meta.model(**validated_data)

        # hash password
        if not firebase_token and password: 
            user.set_password(password)

        user.save()
        return user


class StandardUserSerializer(BaseUserSerializer):
    # firebase_uid = serializers.CharField(read_only=True)
    class Meta(BaseUserSerializer.Meta): 
        model = StandardUser
        fields = ['role', 'id', 'email', 'password', 'firebase_token', 'first_name', 'last_name', 'creation_date']
        read_only_fields = ['id', 'creation_date']

class MerchantAdministratorSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta): 
        model = MerchantAdministrator
        fields = ['role', 'id', 'email', 'password', 'firebase_token', 'business_name', 'creation_date' ]
        read_only_fields = ['id', 'creation_date']

class LogisticsAdministratorSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta): 
        model = LogisticsAdministrator
        fields = ['role', 'id', 'email', 'password', 'firebase_token', 'logistics_name', 'creation_date', ]
        read_only_fields = ['id', 'creation_date']

class DriverSerializer(BaseUserSerializer):
    first_name = serializers.CharField(source='driver_first_name')
    last_name = serializers.CharField(source='driver_last_name')
    logistics_id = serializers.PrimaryKeyRelatedField(
        queryset=LogisticsAdministrator.objects.all(), 
        source="logistics_name"
    )

    class Meta(BaseUserSerializer.Meta): 
        model = Driver 
        fields = ['role', 'id', 'email', 'password', 'firebase_token', 'logistics_id', 'first_name', 'last_name', 'creation_date', ]
        read_only_fields = ['id', 'creation_date']
