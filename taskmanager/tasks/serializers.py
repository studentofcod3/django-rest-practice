from rest_framework import serializers
from tasks.models import Task, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField(
        help_text="A human readable value of whether or not the task has been completed"
    )
    summary = serializers.SerializerMethodField()
    # Nested serializers are useful when the consumer of the API 
    # needs to see both the task and its category in one request.
    # NOTE: This is only for read operations. For write operations we need to modify the create method
    category = CategorySerializer()
    category_name = serializers.CharField(source='category.name')
    # Customize created_at field using serializer DateTimeField to adjust format for easier reading.
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    task_title = serializers.CharField(
        source='title',
        max_length=200,
        help_text="Enter the title of the task",
        error_messages={"max_length": "The title must be under 200 characters."}
    )

    class Meta:
        model = Task
        fields = [
            'id', 
            'created_at',
            'task_title', 
            'description',
            'category',
            'is_completed',
            'summary',
            'category_name'
        ]
        read_only_fields = [
            'id',
            'created_at'
            'category_name'
        ]

    def get_summary(self, obj):
        return f"{obj.title} - Completed: {'Yes' if obj.completed else 'No'}"

    def get_is_completed(self, obj):
        """
        A more user-friendly string for the completed status of a task. 
        
        The custom is_completed field converts the boolean into a human-readable string.
        """
        return "Yes" if obj.completed else "No"
    
    def create(self, validated_data):
        # Related objects can be created together in a single API call.
        # Reduces the need for multiple requests and simplifies client-side code
        category_data = validated_data.pop('category')
        category = Category.objects.create(**category_data)
        task = Task.objects.create(category=category, **validated_data)
        return task

    def validate(self, data):
        # Can validate across entire object
        if data["is_completed"] == "Yes" and not data["description"]:
            raise serializers.ValidationError["Completed tasks must have a description"]
        return data
    
    def validate_description(self, value):
        if 'badword' in value:
            raise serializers.ValidationError("Description containts inappropriate content")
        return value
    

    
