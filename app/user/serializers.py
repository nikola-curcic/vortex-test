from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        if not validated_data.get('first_name'):
            raise serializers.ValidationError({'first_name': ['This field is required.']})

        if not validated_data.get('last_name'):
            raise serializers.ValidationError({'last_name': ['This field is required.']})

        return get_user_model().objects.create_user(**validated_data)


