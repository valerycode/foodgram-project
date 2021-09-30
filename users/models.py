from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class SubscriptionManager(models.Manager):
    @staticmethod
    def subscriptions(user):
        return User.objects.filter(pk__in=Subscription.objects.filter(
            user=user).values_list('author', flat=True))


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='subscribed_to',
                             verbose_name='Подписчик')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='subscribed_by',
                               verbose_name='Автор')
    objects = SubscriptionManager()

    def __str__(self):
        return f'Подписка{self.user} на {self.author}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['author']
        constraints = [
            models.CheckConstraint(
                check=~models.Q(user=models.F("author")),
                name='user_is_not_author',
            ),
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription',
            )
        ]


class FavoriteManager(models.Manager):
    @staticmethod
    def favorite_recipe(user, tags):
        return Recipe.objects.tag_filter(tags).filter(
            pk__in=Favorite.objects.filter(
                user=user).values_list('recipe', flat=True))


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="favorite_subscriber",
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name="favorite_recipe",
        verbose_name='Рецепт')
    objects = FavoriteManager()

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_recipe_in_favorites'
                                    )]

    def __str__(self):
        return f"{self.user}-{self.recipe}"


class Purchase(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="purchases_subscriber",
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name="purchases_recipe",
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_entry_in_shop_list'
                                    )]
