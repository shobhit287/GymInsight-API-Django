from . models import User
from . serializers import UserSerializer
def findOne(id):
    try:
        user = User.objects.get(user_id=id)
        userSerialized = UserSerializer(user)
        return {"user":userSerialized.data, "status": True, "code": 200}
    except User.DoesNotExist as e:
        return {"error": "User not found", "status": False, "code": 404}
    except Exception as e:
        return {"error": str(e), "status": False, "code": 500},

def findOneByRole(role):
    try:
        user = User.objects.get(role=role)
        userSerialized = UserSerializer(user)
        return {"user":userSerialized.data, "status": True, "code": 200}
    except User.DoesNotExist as e:
        return {"error": "User not found", "status": False, "code": 404}
    except Exception as e:
        return {"error": str(e), "status": False, "code": 500},


    