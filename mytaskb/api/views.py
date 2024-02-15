from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.serializers import AuthTokenSerializer
from tasksapp.models import Task
from .serializers import TaskSerializer, RegistrarionSerializer
from knox.auth import AuthToken

@api_view(['GET'])
def get_data(request):
    task = Task.objects.all()
    serializer = TaskSerializer(task, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_data_detail(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def get_data_detail_by_status(request, status):
    valid_status = status.lower().capitalize()
    tasks = Task.objects.filter(status=valid_status)

    if tasks.exists():
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    else:
        return Response({"error": "No tasks found with the specified status"})


@api_view(['POST'])
def add_item(requset):
    serializer = TaskSerializer(data=requset.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def edit_item(requset, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data=requset.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_item(requset, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return Response(f'{pk} item successfully delete')


@api_view(['POST'])
def login_api(requset):
    serializer = AuthTokenSerializer(data=requset.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    _, token = AuthToken.objects.create(user)
    return Response({
        'user_info':{
            'username':user.username,
            'email':user.email
        },
        'token': token

    })

@api_view(['GET'])
def get_user_data(request):
    user = request.user

    if user.is_authenticated:
        return Response({
            'user_info': {
                'id': user.id,
                'usermane': user.username,
                'email': user.email
            },
        })
    return Response({'erroer': 'not authenticated'}, status=400)


@api_view(['POST'])
def register_api(request):
    serializer = RegistrarionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()
    _, token = AuthToken.objects.create(user)

    return Response({
        'user_info':{
            'id':user.id,
            'username': user.username,
            'email': user.email
        },
        token: token

    })

