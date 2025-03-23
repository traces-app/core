from rest_framework import serializers 
from api.models.fcm_token import FCMToken

class FCMTokenSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = FCMToken
        fields = ["token"]

    @staticmethod
    def get_user_tokens(user): 
        """Retrieves all FCM tokens for a specific user."""
        return list(FCMToken.objects.filter(user = user).values_list('token', flat=True))

    @staticmethod
    def get_all_tokens():
        return list(FCMToken.objects.values_list('token', flat=True))
    
    @staticmethod
    def add_user_token(user, token): 
        """Adds the token if not already registered.""" 
        if not FCMToken.objects.filter(user=user, token=token).exists(): 
            FCMToken.objects.create(user=user, token=token)

    @staticmethod
    def remove_user_token(user, token): 
        """Removes a token for a user."""
        deleted_count, _ = FCMToken.objects.filter(user=user, token=token).delete()

    @staticmethod
    def remove_token(token): 
        """Removes all records of a specific token"""
        deleted_count, _ = FCMToken.objects.filter(token=token).delete()

        return deleted_count




