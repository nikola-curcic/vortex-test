import clearbit
import logging
import requests

from rest_framework import serializers, status

from app.settings import CLEARBIT_KEY, HUNTER_API_KEY, HUNTER_URL


logger = logging.getLogger(__name__)

clearbit.key = CLEARBIT_KEY

def check_email_valid(email):
    hunter_url = '{}{}&api_key={}' \
        .format(HUNTER_URL, email, HUNTER_API_KEY)
    r = requests.get(hunter_url)

    if not r.status_code == status.HTTP_200_OK:
        logger.info('Error while checking email address with external API...')
        raise serializers.ValidationError({'message': ['Error while confirming email address.']})

    if r.json().get('data').get('status') == 'invalid':
        logger.info('Supplied email address %s is not a valid one...', email)
        raise serializers.ValidationError({'email': ['This address is not valid.']})

    logger.info('Email validation process completed successfully...')

def get_clearbit_details(email):
    logger.info('Started getting additional data for user %s...', email)

    try:
        response = clearbit.Enrichment.find(email=email, stream=False)
        logger.info('Fetched data for user %s added to db...', email)
        if 'pending' in response:
            return None
        return response
    except:
        logger.info('Error while fetching data for user %s or data not present...', email)
        return None