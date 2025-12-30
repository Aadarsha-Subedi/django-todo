from rest_framework import serializers

from signup.serializers import StrictFieldsSerializer

from .models import Todo
from signup.models import User

class CreateOrUpdateTodoSerializer(serializers.ModelSerializer, StrictFieldsSerializer):
    title = serializers.CharField(max_length=100,
                                  error_messages={
                                      "required": "Title is required.",
                                      "blank": "Title cannot be empty.",
                                      "max_length": "Title is too long."
                                  })
    description = serializers.CharField(max_length=500,
                                        error_messages={
                                            "required": "Title is required.",
                                            "blank": "Title cannot be empty.",
                                            "max_length": "Title is too long."
                                        })
    due_date = serializers.DateField(
        error_messages={
            "required": "Due date is required.",
            "invalid": "Enter a valid date in YYYY-MM-DD format."
        })
    is_completed = serializers.BooleanField(required=False, default=False)
    priority = serializers.ChoiceField(
        choices=Todo.PriorityChoices.choices,
        default=Todo.PriorityChoices.MEDIUM,
        error_messages={
            "invalid_choice": "Priority must be high, medium, or low."
        })

    class Meta:
        model = Todo
        fields = [
            "id",
            "title",
            "description",
            "due_date",
            "priority",
            "is_completed",
            "created_at",
            "updated_at",
        ]


class GetTodoSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="email.email", read_only=True)

    class Meta:
        model = Todo
        fields = [
            "id",
            "email",
            "title",
            "description",
            "due_date",
            "priority",
            "is_completed",
            "created_at",
            "updated_at",
        ]
