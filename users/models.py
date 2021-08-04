from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class Subscription(models.Model):
    """ Подписка """

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='subscribed_to',
                             verbose_name='Подписчик')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='subscribed_by',
                               verbose_name='Автор')

    def __str__(self):
        return f'Подписка{self.user} на {self.author}'

    class Meta:
        unique_together = ['user', 'author']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Favorite(models.Model):
    """Избранные рецепты пользователя"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorite_subscriber"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favorite_recipe"
    )

    class Meta:
        unique_together = ["user", "recipe"]
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f"{self.user}-{self.recipe}"


class Purchases(models.Model):
    """Список покупок"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="purchases_subscriber")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="purchases_recipe")

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_entry_in_shop_list'
                                    )]
