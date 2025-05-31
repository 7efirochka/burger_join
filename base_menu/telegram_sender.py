"""
Module for sending order data to Telegram.
This will be used for integration with a Telegram bot that will confirm orders
and send data to a delivery channel.
"""

import json
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

def send_order_to_telegram(order_data):
    """
    Send order data to Telegram bot or channel.
    
    Args:
        order_data (dict): Dictionary containing order information
            {
                'order_id': int,
                'customer_name': str,
                'phone_number': str,
                'delivery_address': str,
                'total_price': float,
                'items': [
                    {
                        'name': str,
                        'price': float,
                        'quantity': int,
                        'total': float
                    },
                    ...
                ]
            }
    
    Returns:
        bool: True if message was sent successfully, False otherwise
    """
    try:
        # This will be replaced with actual API key when ready
        TELEGRAM_BOT_TOKEN = '-'
        TELEGRAM_CHAT_ID = '-'
        
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            logger.warning("Telegram integration not configured. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in settings.")
            return False
        
        # Format message for Telegram
        message = format_order_message(order_data)


        # Send message to Telegram
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        logger.info(f"Order #{order_data['order_id']} sent to Telegram successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to send order to Telegram: {str(e)}")
        return False

def format_order_message(order_data):
    """
    Format order data as HTML message for Telegram.
    
    Args:
        order_data (dict): Dictionary with order information
    
    Returns:
        str: Formatted message
    """
    # Header
    message = f"🍔 <b>НОВЫЙ ЗАКАЗ #{order_data['order_id']}</b> 🍔\n\n"
    
    # Customer info
    message += "<b>Информация о клиенте:</b>\n"
    message += f"👤 Имя: {order_data['customer_name']}\n"
    message += f"📱 Телефон: {order_data['phone_number']}\n"
    message += f"🏠 Адрес: {order_data['delivery_address']}\n\n"
    
    # Order items
    message += "<b>Товары:</b>\n"
    for item in order_data['items']:
        message += f"• {item['name']} x{item['quantity']} = {item['total']} ₽\n"
    
    # Total
    message += f"\n<b>Итого: {order_data['total_price']} ₽</b>\n"
    
    return message

# For future: webhook handler to receive order status updates from Telegram
def handle_telegram_webhook(request_data):
    """
    Handle incoming webhook from Telegram bot.
    This will be used to update order status when delivery staff confirms the order.
    
    Args:
        request_data (dict): Data received from webhook
    
    Returns:
        dict: Response data
    """
    # This is a placeholder for future implementation
    try:
        # Process webhook data
        # Update order status based on webhook data
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error processing Telegram webhook: {str(e)}")
        return {"status": "error", "message": str(e)}
