from django.contrib import admin
from .models import *

admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Storage)
admin.site.register(Purchase)
admin.site.register(Sale)