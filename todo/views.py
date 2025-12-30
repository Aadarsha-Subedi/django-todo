from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import CreateOrUpdateTodoSerializer, GetTodoSerializer

from .models import Todo

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    create_todo_serializer = CreateOrUpdateTodoSerializer(data=request.data)

    if not create_todo_serializer.is_valid():
        return Response(create_todo_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    new_todo = Todo.objects.create(
        email=request.user,
        title=create_todo_serializer.validated_data['title'],
        description=create_todo_serializer.validated_data['description'],
        due_date=create_todo_serializer.validated_data['due_date'],
        priority=create_todo_serializer.validated_data['priority'],
        is_completed=create_todo_serializer.validated_data['is_completed'])
    new_todo.save()

    serializer = CreateOrUpdateTodoSerializer(new_todo)

    return Response({
        "message":
        f"Task with title {create_todo_serializer.validated_data['title']} created successfully. ",
        "data": serializer.data
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_tasks(request):
    todos = Todo.objects.filter(email=request.user)
    serializer = GetTodoSerializer(todos, many=True)
    return Response(
        {
            "message": "All todos retrieved successfully.",
            "todos": serializer.data
        },
        status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_task(request, todo_id):
    try:
        todo = Todo.objects.filter(id=todo_id, email=request.user)
    except Todo.DoesNotExist:
        return Response({"message": "Todo not found."},
                        status=status.HTTP_404_NOT_FOUND)

    todo.delete()
    return Response({"message": "Todo deleted successfully."},
                    status=status.HTTP_204_NO_CONTENT)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_task(request, todo_id):
    update_todo_serializer = CreateOrUpdateTodoSerializer(data=request.data)

    if not update_todo_serializer.is_valid():
        return Response(update_todo_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    updated_count = Todo.objects.filter(id=todo_id, email=request.user).update(
        title=update_todo_serializer.validated_data['title'],
        description=update_todo_serializer.validated_data['description'],
        due_date=update_todo_serializer.validated_data['due_date'],
        priority=update_todo_serializer.validated_data['priority'],
        is_completed=update_todo_serializer.validated_data['is_completed'])

    if updated_count == 0:
        return Response({"message": "Todo not found."},
                    status=status.HTTP_404_NOT_FOUND)
    
    updated_todo = Todo.objects.filter(id=todo_id, email = request.user).get()
    serializer = CreateOrUpdateTodoSerializer(updated_todo)
    return Response({
        "message":
        f"Task with title {update_todo_serializer.validated_data['title']} created successfully. ",
        "data": serializer.data
    })
