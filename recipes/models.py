from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


User = get_user_model()


class IngredientUnit(models.TextChoices):
    GRAM = 'GRAM', 'г.'


class Tag(models.Model):
    """Теги"""

    name = models.CharField(max_length=50, verbose_name='Тег')
    slug = models.SlugField(max_length=160, unique=True)
    color = models.SlugField(verbose_name='Цвет тега')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'color'],
                name='unique_tag'
            )]

    def __str__(self):
        return f'{self.name}'


class RecipeManager(models.Manager):
    @staticmethod
    def tag_filter(tags):
        if tags:
            return Recipe.objects.filter(tags__slug__in=tags).distinct()
        return Recipe.objects.all()


class Recipe(models.Model):
    """Рецепты"""

    author = models.ForeignKey(User, related_name='author_recipes',
                               verbose_name='автор', on_delete=models.CASCADE)
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    image = models.ImageField('Картинка', upload_to='recipes/',
                              blank=True, null=True)
    description = models.TextField('Описание')
    ingredients = models.ManyToManyField(through='RecipeIngredient',
                                         to='Ingredient', blank=True)
    tags = models.ManyToManyField(Tag, related_name='recipes',
                                  blank=True, verbose_name='теги')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)], verbose_name='время приготовления')
    slug = models.SlugField(max_length=160, unique=True)
    pub_date = models.DateTimeField(verbose_name='дата публикации',
                                    auto_now_add=True,
                                    db_index=True)
    objects = RecipeManager()

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ингредиенты"""

    title = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    dimension = models.CharField(
        verbose_name='Единицы измерения',
        max_length=256,
    )

    def __str__(self):
        return f'{self.title} {self.dimension}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['title']
        db_table = 'recipes_ingredients'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, related_name='recipe_ingredients', on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = "ингредиент рецепта"
        verbose_name_plural = "ингредиенты рецепта"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_recipe_ingredient",
            )
        ]

    def __str__(self):
        name = (
            f"{self.ingredient.title} - {self.amount}"
        )
        return name
