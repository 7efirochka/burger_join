from django.contrib import admin
from .models import Burgers, Hotdogs, Breakfasts, Drinks, Sauces, Snacks


admin.site.register(Breakfasts)
admin.site.register(Burgers)
admin.site.register(Drinks)
admin.site.register(Hotdogs)
admin.site.register(Sauces)
admin.site.register(Snacks)
