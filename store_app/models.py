from django.db import models

class Status(models.Model):
    status_type = models.CharField(verbose_name="Тип статуса", max_length=50)

    def __str__(self):
        return self.status_type
    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


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