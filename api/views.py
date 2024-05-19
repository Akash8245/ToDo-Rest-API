from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UserSerializer,TaskSerializer
from .models import User,Task
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken

class Register(APIView):
    def post(self,request):
        searlizer = UserSerializer(data=request.data)
        data = {"message":"user created"}

        if searlizer.is_valid():
            searlizer.save()
        else:
            data = {"message":"User couldn't be created"}
        return Response(data)

class Login(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        data = {}

        if user is None:
            data = {"message":"User not Found !"}
            return Response(data , status=404)
        elif not check_password(password, user.password):
            data = {"message":"Incorrect Password"}
            return Response(data , status=401)
        else:
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            res = Response()
            res.set_cookie(key="access",value=token)

        return res
    
class getSetTask(APIView):
    def get(self,request):
        token = request.COOKIES.get('access')
        if not token:
            return Response({"message":"Unauthorized"})
        
        try :
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            tasks = Task.objects.filter(id=user_id)
            searlizer = TaskSerializer(tasks,many=True)
            return Response(searlizer.data)
        except:
            return Response({"message":"Unauthorized"})
        
    def post(self,request):
        token = request.COOKIES.get('access')
        if not token:
            return Response({"message":"Unauthorized"})
        
        try :
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = User.objects.get(pk=user_id)

            data = request.data
            data['user'] = user.id

            searlizer = TaskSerializer(data=data)
            if searlizer.is_valid():
                searlizer.save()
                return Response({"message":"Task added"})
            else:
                return Response({"message":"Invalid form of data"})
        except:
            return Response({"message":"Unauthorized"})
        
class updateTask(APIView):
    def post(self, request, pk):
        token = request.COOKIES.get('access')
        if not token:
            return Response({"message": "Unauthorized"}, status=401)
        
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = User.objects.get(pk=user_id)

            task = get_object_or_404(Task, pk=pk, user=user)

            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Data updated"}, status=200)
            return Response({"message": "Invalid data", "errors": serializer.errors}, status=400)
        except Exception as e:
            return Response({"message": "Couldn't update task", "error": str(e)}, status=500)

             
        
class deleteTask(APIView):
    def post(self,request,pk):
        token = request.COOKIES.get('access')
        if not token:
            return Response({"message":"Unauthorized 1"})
        
        try :
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = User.objects.get(pk=user_id)

            task = get_object_or_404(Task, pk=pk, user=user)
            task.delete()
            return Response({"message":"Task Deleted"})
            
        except:
            return Response({"message":"Unauthorized 2"})


