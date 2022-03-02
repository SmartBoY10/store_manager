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
    product = models.ManyToManyField(Product)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"


class Manual(models.Model):
    name = models.CharField(verbose_name="Справочник", max_length=50)
    brand = models.ManyToManyField(Brand)
    category = models.ManyToManyField(Category)
    product = models.ManyToManyField(Product)
    storage = models.ManyToManyField(Storage)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"