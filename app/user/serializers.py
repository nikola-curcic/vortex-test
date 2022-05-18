import logging
import os
import requests

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers, status


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

        hunter_url ='https://api.hunter.io/v2/email-verifier?email={}&api_key={}' \
                     .format(validated_data.get('email'), os.getenv('HUNTER_API_KEY'))
        r = requests.get(hunter_url)

        if not r.status_code == status.HTTP_200_OK:
            logger.info('Error while checking email address with external API...')
            raise serializers.ValidationError({'message': ['Error while confirming email address.']})

        if r.json().get('data').get('status') == 'invalid':
            logger.info('Supplied email address %s is not a valid one...', validated_data.get('email'))
            raise serializers.ValidationError({'email': ['This address is not valid.']})

        logger.info('Email validation process completed successfully...')

        if not validated_data.get('first_name'):
            logger.info('first_name is required...')
            raise serializers.ValidationError({'first_name': ['This field is required.']})

        if not validated_data.get('last_name'):
            logger.info('last_name is required...')
            raise serializers.ValidationError({'last_name': ['This field is required.']})

        return get_user_model().objects.create_user(**validated_data)


