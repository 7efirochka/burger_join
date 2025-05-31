from django.db import models

# Create your models here.
class Images(models.Model):
    name = models.CharField('Название продукта', max_length=60)
    structure = models.TextField('Ингредиенты продукта', max_length=400)
    img = models.ImageField(upload_to='main/static/main/img')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена продукта', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Carusel of products'
        verbose_name = 'Carusel of products'

