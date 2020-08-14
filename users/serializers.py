from rest_framework import serializers
from users.models import Users


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = (
            'user_id', 'first_name', 'last_name', 'address', 'street',
            'city', 'state', 'zip_code', 'user_type', 'parent_id'
        )
