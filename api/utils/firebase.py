from firebase_admin import auth

def validateFirebaseToken(token): 
    decoded_token = auth.verify_id_token(token)
    firebase_uid = decoded_token.get("uid")
    email = decoded_token.get("email", f"{firebase_uid}@firebase.com") # default to "{firebase_uid}@firebase.com" if the email is missing

    return (firebase_uid, email)

def createFirebaseUser(email, password): 
    try: 
        user = auth.create_user(
            email = email, 
            password = password,
        )
        return user.uid
    except Exception as e: 
        print(f"Error creating user {str(e)}")
    