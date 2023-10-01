from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "id",
            "item_id",
            "user",
            "user_email",
            "comment",
            "created_at",
        )
        read_only_fields = [
            "id",
            "created_at",
            "user",
        ]

    def get_user_email(self, obj):
        return obj.user.email
