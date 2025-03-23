import firebase_admin
from firebase_admin import messaging
from api.models.fcm_token import FCMToken

class FCMService:
    """Handles sending FCM push notifications."""
    
    @staticmethod
    def send_notification(tokens, title, body, data=None):
        """
        Send an FCM notification to a single device.

        :param tokens: (list) List of FCM device tokens
        :param title: (str) Notification title
        :param body: (str) Notification body
        :param data: (dict) Optional data payload
        :return: (dict) Response from FCM
        """
        if not firebase_admin._apps:
            print("Firebase is NOT initialized.")
        else:
            print("Firebase is initialized.")

        if not tokens: 
            return {"success": False, "error": "No tokens provided"}

        try: 
            message = messaging.MulticastMessage(
                notification=messaging.Notification(title=title, body=body),
                tokens=tokens,
                data=data if data else {},
            )

            response = messaging.send_each_for_multicast(message)

            # get invalid tokens
            invalid_tokens = []
            for i, result in enumerate(response.responses):
                if not result.success:
                    invalid_tokens.append(tokens[i])

            # remove invalid tokens from the database
            if invalid_tokens:
                FCMToken.objects.filter(token__in=invalid_tokens).delete()

            return {
                "success": True,
                "success_count": response.success_count,
                "failure_count": response.failure_count,
                "removed_tokens": invalid_tokens
            }

        except Exception as e: 
            return {"success": False, "detail": str(e)}
