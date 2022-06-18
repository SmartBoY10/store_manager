from django.db import models
import jsonfield

class Status(models.Model):
    status_type = models.CharField(verbose_name="Тип статуса", max_length=50)

    def __str__(self):
        return self.status_type
    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class PayType(models.Model):
    pay_type = models.CharField(verbose_name="Способ оплаты", max_length=25)

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


class Storage(models.Model):
    name = models.CharField(verbose_name="Склад", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"


class Product(models.Model):
    name = models.CharField(verbose_name="Название", max_length=150)
    short_name = models.CharField(verbose_name="Короткое название", max_length=50)
    description = models.TextField(verbose_name="Описание")
    storege = models.ForeignKey(Storage, verbose_name="Склад", on_delete=models.SET_NULL, null=True)
    purchase_price_per_unit = models.PositiveIntegerField(verbose_name="Цена покупки(за единицу)", null=True)
    sale_price_per_unit = models.PositiveIntegerField(verbose_name="Цена продажи(за единицу)", null=True)
    # total_cost = models.PositiveIntegerField(verbose_name="Общая себестоимость продукта", default=0)
    # quantity = models.PositiveIntegerField(verbose_name="Кол-во в складе", default=0)
    discount = models.PositiveSmallIntegerField(verbose_name="Скидка в %", blank=True, null=True)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, verbose_name="Бренд", on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото', blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата публикации')
    view_count = models.PositiveIntegerField(verbose_name="Кол-во просмотров")
    quantity = models.PositiveIntegerField(verbose_name="Кол-во в складе", default=0)
    url = models.SlugField(max_length=160, unique=True, null=True)

    def __str__(self):
        return self.name

    def get_sale_price(self):
        if self.discount:
            return self.sale_price_per_unit - (self.sale_price_per_unit * self.discount / 100)
        else:
            return self.sale_price_per_unit

    def total_cost(self):
        return self.purchase_price_per_unit * self.quantity

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Buyer(models.Model):
    session_id = models.CharField(verbose_name="Сессия ID", max_length=50)

    def __str__(self):
        return self.session_id

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Cart(models.Model):
    buyer = models.ForeignKey(Buyer, verbose_name="Клиент", on_delete=models.CASCADE, null=True)

    # def __str__(self):
    #     return self.buyer

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class Order(models.Model):
    buyer = models.ForeignKey(Buyer, verbose_name="Клиент", on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(verbose_name="Кол-во продукта", default=1)
    total_price = models.PositiveIntegerField(verbose_name="Общая сумма", default=0)
    cart = models.ForeignKey(Cart, verbose_name="Корзина", on_delete=models.CASCADE, null=True)

    # def total_price(self):
    #     return int(self.quantity * self.product.get_sale_price)

    # def __str__(self):
    #     return self.buyer

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Journal(models.Model):
    full_name = models.CharField(verbose_name="ФИО", max_length=100, blank=True)
    address = models.CharField(verbose_name="Адрес", max_length=100, blank=True)
    phone = models.CharField(verbose_name="Номер телефона", max_length=20, blank=True)
    pay_type = models.ForeignKey(PayType, verbose_name="Способ оплаты", on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, verbose_name="Статус", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    served_at = models.DateTimeField(auto_now=True, verbose_name='Дата обслуживания')
    orders = jsonfield.JSONField()

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Журнал"
        verbose_name_plural = "Журналы"


class Purchase(models.Model):
    storage = models.ForeignKey(Storage, verbose_name="Склад", on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(verbose_name="Кол-во")
    date_of_purchase = models.DateTimeField(auto_now_add=True, verbose_name='Дата закупки', null=True)
    price_per_unit = models.IntegerField(verbose_name="Цена покупки за единицу")

    def __str__(self):
        return self.product.name

    def total_purchase_price(self):
        return self.price_per_unit * self.quantity

    class Meta:
        verbose_name = "Закупка"
        verbose_name_plural = "Закупки"


class Sale(models.Model):
    # storage = models.ForeignKey(Storage, verbose_name="Склад", on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(verbose_name="Кол-во")
    date_of_purchase = models.DateField(verbose_name='Дата продажи', null=True)
    purchase_price_per_unit = models.IntegerField(verbose_name="Цена закупки за единицу", null=True)
    sale_price_per_unit = models.IntegerField(verbose_name="Цена продажи за единицу")

    def __str__(self):
        return self.product.name

    def total_sale_price(self):
        return self.sale_price_per_unit * self.quantity

    def total_cost_of_product(self):
        return self.quantity * self.purchase_price_per_unit

    def profit(self):
        return (self.sale_price_per_unit * self.quantity) - (self.quantity * self.purchase_price_per_unit)

    class Meta:
        verbose_name = "Продажа"
        verbose_name_plural = "Продажи"
