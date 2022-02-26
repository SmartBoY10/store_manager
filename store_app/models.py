from django.db import models

class Status(models.Model):
    status_type = models.CharField(verbose_name="Тип статуса", max_length=50)

    def __str__(self):
        return self.status_type
    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class PayType(models.Model):
    pay_type = models.CharField(verbose_name="", max_length=25)

    def __str__(self):
        return self.pay_type
    class Meta:
        verbose_name = "Способ оплаты"
        verbose_name_plural = "Способы оплаты"

class Category(models.Model):
    name = models.CharField(verbose_name="Названия категории", max_length=100)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank = 
    True, null=True)
    description = models.TextField("Описание", null=True)
    url = models.SlugField(max_length=160, unique=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Brand(models.Model):
    name = models.CharField(verbose_name="Названия бренда", max_length=50)
    url = models.SlugField(max_length=160, unique=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"


class Product(models.Model):
    name = models.CharField(verbose_name="Название", max_length=150)
    short_name = models.CharField(verbose_name="Короткое название", max_length=50)
    description = models.TextField(verbose_name="Описание")
    price = models.PositiveIntegerField(verbose_name="Цена")
    discount = models.PositiveSmallIntegerField(verbose_name="Скидка в %")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, verbose_name="Бренд", on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    view_count = models.PositiveIntegerField(verbose_name="Кол-во просмотров")
    quantity = models.PositiveIntegerField(verbose_name="Кол-во в складе", default=0)
    url = models.SlugField(max_length=160, unique=True, null=True)

    def __str__(self):
        return self.name

    def after_discount(self):
        return self.price - (self.price * self.discount / 100)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Buyer(models.Model):
    session_id = models.CharField(verbose_name="Сессия ID", max_length=25)
    full_name = models.CharField(verbose_name="ФИО", max_length=100, blank=True)
    address = models.CharField(verbose_name="Адрес", max_length=100, blank=True)
    phone = models.CharField(verbose_name="Номер телефона", max_length=20, blank=True)
    city = models.CharField(verbose_name="Город", max_length=50, blank=True)
    pay_type = models.ForeignKey(PayType, verbose_name="Способ оплаты", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.session_id

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Cart(models.Model):
    buyer = models.ForeignKey(Buyer, verbose_name="Клиент", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class Order(models.Model):
    buyer = models.ForeignKey(Buyer, verbose_name="Клиент", on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(verbose_name="Кол-во продукта", default=1)
    cart = models.ForeignKey(Cart, verbose_name="Корзина", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Journal(models.Model):
    full_name = models.CharField(verbose_name="ФИО", max_length=100, blank=True)
    address = models.CharField(verbose_name="Адрес", max_length=100, blank=True)
    phone = models.CharField(verbose_name="Номер телефона", max_length=20, blank=True)
    pay_type = models.ForeignKey(PayType, verbose_name="Способ оплаты", on_delete=models.SET_NULL, null=True, blank=True)
    cart = models.ForeignKey(Cart, verbose_name="Корзина", on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(Status, verbose_name="Статус", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    served_at = models.DateTimeField(auto_now=True, verbose_name='Дата обслуживания')

    class Meta:
        verbose_name = "Журнал"
        verbose_name_plural = "Журналы"