from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
import logging
from django.contrib import messages
from base_menu import telegram_sender



from .models import (
    Burgers, Breakfasts, Hotdogs, Snacks, Sauces, Drinks,
    CartItem, Order, OrderItem
)

logger = logging.getLogger('base_menu.views')

MODEL_MAPPING = {
    'burgers': Burgers,
    'breakfasts': Breakfasts,
    'hotdogs': Hotdogs,
    'snacks': Snacks,
    'sauces': Sauces,
    'drinks': Drinks,
}

def menu_view(request):
    # Получаем все товары корзины для текущего пользователя
    cart_items = []
    total_price = 0
    total_quantity = 0
    
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_quantity = sum(item.quantity for item in cart_items)
        total_price = sum(item.get_total_price() for item in cart_items)
    
    context = {
        'burgers': Burgers.objects.all(),
        'breakfasts': Breakfasts.objects.all(),
        'hotdogs': Hotdogs.objects.all(),
        'snacks': Snacks.objects.all(),
        'sauces': Sauces.objects.all(),
        'drinks': Drinks.objects.all(),
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_price': total_price,
    }
    return render(request, 'base_menu/menu.html', context)

def profile_view(request):
    return render(request, "base_menu/profile.html")

@require_POST
def cart_add(request):
    """Добавление товара в корзину"""
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': 'Пожалуйста, войдите или зарегистрируйтесь, чтобы добавлять товары в корзину.',
            'redirect': reverse('login')
        })
    
    data = json.loads(request.body)
    product_id = data.get('product_id')
    product_type = data.get('product_type', 'burgers')  # По умолчанию - бургеры
    
    # Получаем модель по типу продукта
    model = MODEL_MAPPING.get(product_type)
    if not model:
        return JsonResponse({'status': 'error', 'message': 'Неверный тип продукта'})
    
    # Получаем продукт
    try:
        product = model.objects.get(id=product_id)
    except model.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Продукт не найден'})
    
    # Получаем ContentType для модели
    content_type = ContentType.objects.get_for_model(model)
    
    # Проверяем, есть ли уже этот продукт в корзине
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=product_id,
        defaults={'quantity': 1}
    )
    
    # Если продукт уже есть в корзине, увеличиваем количество
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    # Получаем обновленные данные корзины
    cart_items = CartItem.objects.filter(user=request.user)
    total_quantity = sum(item.quantity for item in cart_items)
    total_price = sum(item.get_total_price() for item in cart_items)
    
    return JsonResponse({
        'status': 'success',
        'message': 'Товар добавлен в корзину',
        'cart_count': total_quantity,
        'cart_total': total_price,
        'product': {
            'name': product.name,
            'price': float(product.price),
            'image': product.img.url,
            'quantity': cart_item.quantity
        }
    })

@require_POST
def cart_change(request):
    """Изменение количества товара в корзине"""
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': 'Пожалуйста, войдите или зарегистрируйтесь, чтобы изменять корзину.',
            'redirect': reverse('login')
        })
    
    data = json.loads(request.body)
    cart_item_id = data.get('cart_item_id')
    action = data.get('action')  # 'increase' или 'decrease'
    
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
    except CartItem.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Товар в корзине не найден'})
    
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()
            return JsonResponse({
                'status': 'success',
                'message': 'Товар удален из корзины',
                'removed': True,
                'cart_item_id': cart_item_id
            })
    
    cart_item.save()
    
    # Обновляем данные корзины
    cart_items = CartItem.objects.filter(user=request.user)
    total_quantity = sum(item.quantity for item in cart_items)
    total_price = sum(item.get_total_price() for item in cart_items)
    
    return JsonResponse({
        'status': 'success',
        'message': 'Количество изменено',
        'cart_count': total_quantity,
        'cart_total': total_price,
        'item_quantity': cart_item.quantity if cart_item.id else 0,
        'item_total': float(cart_item.get_total_price()) if cart_item.id else 0
    })

@require_POST
def cart_remove(request):
    """Удаление товара из корзины"""
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': 'Пожалуйста, войдите или зарегистрируйтесь, чтобы управлять корзиной.',
            'redirect': reverse('login')
        })
    
    data = json.loads(request.body)
    cart_item_id = data.get('cart_item_id')
    
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        cart_item.delete()
    except CartItem.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Товар в корзине не найден'})
    
    # Обновляем данные корзины
    cart_items = CartItem.objects.filter(user=request.user)
    total_quantity = sum(item.quantity for item in cart_items)
    total_price = sum(item.get_total_price() for item in cart_items)
    
    return JsonResponse({
        'status': 'success',
        'message': 'Товар удален из корзины',
        'cart_count': total_quantity,
        'cart_total': total_price
    })

def cart_view(request):
    """Отображение страницы корзины"""
    if not request.user.is_authenticated:
        messages.warning(request, "Пожалуйста, войдите или зарегистрируйтесь, чтобы просматривать корзину.")
        return redirect('login')

    cart_items = CartItem.objects.filter(user=request.user)
    total_quantity = sum(item.quantity for item in cart_items)
    total_price = sum(item.get_total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_price': total_price
    }

    return render(request, 'base_menu/cart.html', context)

def checkout_view(request):
    """Страница оформления заказа"""
    if not request.user.is_authenticated:
        messages.warning(request, "Пожалуйста, войдите или зарегистрируйтесь, чтобы оформить заказ.")
        return redirect('login')
    
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        messages.warning(request, "Ваша корзина пуста. Добавьте товары в корзину, чтобы оформить заказ.")
        return redirect('menu')
    
    total_price = sum(item.get_total_price() for item in cart_items)
    
    if request.method == 'POST':
        # Создание заказа
        customer_name = request.POST.get('customer_name')
        phone_number = request.POST.get('phone_number')
        delivery_address = request.POST.get('delivery_address')
        notes = request.POST.get('notes', '')
        
        if not all([customer_name, phone_number, delivery_address]):
            messages.error(request, "Пожалуйста, заполните все обязательные поля.")
            return redirect('checkout')
        
        # Создаем заказ
        order = Order.objects.create(
            user=request.user,
            customer_name=customer_name,
            phone_number=phone_number,
            delivery_address=delivery_address,
            total_price=total_price,
            notes=notes
        )
        
        # Добавляем товары из корзины в заказ
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_name=cart_item.product.name,
                product_price=cart_item.product.price,
                quantity=cart_item.quantity,
                product_image=cart_item.product.img.url
            )
        
        # Очищаем корзину
        cart_items.delete()
        
        # Генерируем данные для передачи в Telegram
        telegram_data = {
            'order_id': order.id,
            'customer_name': order.customer_name,
            'phone_number': order.phone_number,
            'delivery_address': order.delivery_address,
            'total_price': float(order.total_price),
            'items': [
                {
                    'name': item.product_name,
                    'price': float(item.product_price),
                    'quantity': item.quantity,
                    'total': float(item.get_total_price())
                } for item in order.items.all()
            ]
        }
        
        # В будущем здесь будет передача данных в Telegram бот
        telegram_sender.send_order_to_telegram(telegram_data)
        
        messages.success(request, f"Заказ №{order.id} успешно оформлен! Мы свяжемся с вами в ближайшее время.")
        return redirect('order_confirmation', order_id=order.id)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'user': request.user
    }
    
    return render(request, 'base_menu/checkout.html', context)

def order_confirmation(request, order_id):
    """Страница подтверждения заказа"""
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        messages.error(request, "Заказ не найден.")
        return redirect('menu')
    
    context = {
        'order': order,
        'order_items': order.items.all()
    }
    
    return render(request, 'base_menu/order_confirmation.html', context)



