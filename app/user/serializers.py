import logging
import requests

from core.repository import check_email_valid
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        logger.info('Started email validation for %s...', validated_data.get('email'))

        check_email_valid(validated_data.get('email'))

        if not validated_data.get('first_name'):
            logger.info('first_name is required...')
            raise serializers.ValidationError({'first_name': ['This field is required.']})

        if not validated_data.get('last_name'):
            logger.info('last_name is required...')
            raise serializers.ValidationError({'last_name': ['This field is required.']})

        return get_user_model().objects.create_user(**validated_data)


