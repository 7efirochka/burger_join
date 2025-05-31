from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse


class Product(models.Model):  # Абстрактная базовая модель
    name = models.CharField('Название продукта', max_length=60)
    structure = models.TextField('Ингредиенты продукта', max_length=400)
    img = models.ImageField(upload_to='base_menu/static/base_menu/img')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена продукта', default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Burgers(Product):  # Наследуемся от Product
    pass

class Breakfasts(Product):  # Наследуемся от Product
    pass


class Hotdogs(Product):  # Наследуемся от Product
    pass

class Snacks(Product):  # Наследуемся от Product
    pass

class Sauces(Product):  # Наследуемся от Product
    pass

class Drinks(Product):  # Наследуемся от Product
    pass

class CartItem(models.Model):
    """Элемент корзины, отображающий отдельный товар и его количество"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # Для хранения информации о типе продукта (Burgers, Drinks и т.д.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def get_total_price(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} шт."

class Order(models.Model):
    """Модель заказа"""
    STATUS_CHOICES = (
        ('pending', 'Ожидает обработки'),
        ('processing', 'В обработке'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменен'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=100, verbose_name='Имя')
    phone_number = models.CharField(max_length=20, verbose_name='Телефон')
    delivery_address = models.TextField(verbose_name='Адрес доставки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    notes = models.TextField(verbose_name='Примечания к заказу', blank=True, null=True)
    
    def __str__(self):
        return f"Заказ #{self.id} от {self.customer_name}"
    
    def get_absolute_url(self):
        return reverse('order_detail', args=[self.id])

class OrderItem(models.Model):
    """Элемент заказа, связывающий заказ с товарами"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.PositiveIntegerField(default=1)
    product_image = models.CharField(max_length=255, blank=True, null=True)
    
    def get_total_price(self):
        return self.product_price * self.quantity
    
    def __str__(self):
        return f"{self.product_name} ({self.quantity} шт.) в заказе #{self.order.id}"