from rest_framework import serializers
from ...models import Todo
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    """
    Make the object to a json to show the task with serializer
    """

    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        fields = [
            "id",
            "user",
            "title",
            "absolute_url",
            "completed",
            "created_date",
        ]
        read_only_fields = ["user"]

    def get_absolute_url(self, obj):
        """
        Make url for edit the task for each post
        """
        request = self.context.get("request")
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": obj.pk})

        if request:
            return request.build_absolute_uri(url)

        return url
