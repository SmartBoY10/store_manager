from django.db import models


class Brand(models.Model):
    name = models.CharField(verbose_name="Названия бренда", max_length=50)
    url = models.SlugField(max_length=160, unique=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"


class Category(models.Model):
    name = models.CharField(verbose_name="Названия категории", max_length=100)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank = 
    True, null=True)
    url = models.SlugField(max_length=160, unique=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    name = models.CharField(verbose_name="Название", max_length=150)
    price = models.PositiveIntegerField(verbose_name="Цена")
    discount = models.PositiveSmallIntegerField(verbose_name="Скидка в %")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, verbose_name="Бренд", on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(verbose_name="Кол-во в складе", default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    url = models.SlugField(max_length=160, unique=True, null=True)

    def __str__(self):
        return self.name

    def after_discount(self):
        return self.price - (self.price * self.discount / 100)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Storage(models.Model):
    name = models.CharField(verbose_name="Склад", max_length=50)
    product = models.ManyToManyField(Product, verbose_name="Продукты")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"


class Purchase(models.Model):
    storage = models.ForeignKey(Storage, verbose_name="Склад", on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(verbose_name="Кол-во")
    price_per_unit = models.IntegerField(verbose_name="Цена покупки за единицу")

    def __str__(self):
        return self.product.name

    def total_purchase_price(self):
        return self.price_per_unit * self.quantity

    class Meta:
        verbose_name = "Закупка"
        verbose_name_plural = "Закупки"


class Sale(models.Model):
    storage = models.ForeignKey(Storage, verbose_name="Склад", on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(verbose_name="Кол-во")
    price_per_unit = models.IntegerField(verbose_name="Цена продажи за единицу")

    def __str__(self):
        return self.product.name

    def total_sale_price(self):
        return self.price_per_unit * self.quantity

    class Meta:
        verbose_name = "Продажа"
        verbose_name_plural = "Продажи"