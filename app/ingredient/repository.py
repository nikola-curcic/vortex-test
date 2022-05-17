import logging

from django.db import connection

from core.models import Ingredient

logger = logging.getLogger(__name__)


def list_ingredients_db():
    logger.info('Listing ingredients...')
    return Ingredient.objects.get_queryset()


def get_ingredient_db(id):
    logger.info('Logging ingredient id: %s...', id)
    return Ingredient.objects.get(id=id)


def query_most_used_ingredients_db():
    logger.info('Querying most used ingredients...')
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT ci.name, COUNT(*) AS number '
            'FROM core_recipe_ingredients crp '
            'LEFT JOIN core_ingredient ci '
            'ON ci.id = crp.ingredient_id '
            'GROUP BY ci.name '
            'ORDER BY number DESC '
            'LIMIT 5'
        )
        data = cursor.fetchall()

        return [{'name': d[0], 'number_of_recipes': d[1]} for d in data]

