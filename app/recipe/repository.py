import logging

from django.db.models import Count

from core.models import Recipe

logger = logging.getLogger(__name__)


def list_recipes_db():
    logger.info('Listing recipes...')
    return Recipe.objects.get_queryset()


def get_recipe_db(id):
    logger.info('Logging recipe id: %s...', id)
    return Recipe.objects.get(id=id)


def list_own_recipes_db(user):
    logger.info('Logging recipes for user id: %s...', user.id)
    return list(Recipe.objects.filter(user=user))


def rate_recipe_db(recipe, rating):
    logger.info('Logging recipes for recipe id: %s...', recipe.id)
    num_of_ratings = recipe.num_of_ratings + 1
    total_rating = recipe.total_rating + rating
    average_rating = total_rating / num_of_ratings
    recipe.total_rating = total_rating
    recipe.average_rating = average_rating
    recipe.num_of_ratings = num_of_ratings
    recipe.save()
    return recipe.id


def list_recipes_name_db(name):
    logger.info('Filtering recipes by name...')
    return Recipe.objects.filter(name__contains=name)


def list_recipes_text_db(text):
    logger.info('Filtering recipes by text...')
    return Recipe.objects.filter(text__contains=text)


def list_recipes_ingredients_db(ingredients):
    logger.info('Filtering recipes by ingredients...')

    return Recipe.objects.filter(ingredients__in=ingredients).\
            annotate(num_ingredients=Count('ingredients'))\
            .filter(num_ingredients=len(ingredients))


def list_recipes_max_min_ingredients_db(max, min):
    logger.info('Filtering recipes with max and min number of ingredients...')
    return Recipe.objects.filter(num_of_ingredients__lte=max,
                                 num_of_ingredients__gte=min)
