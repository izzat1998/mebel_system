from datetime import datetime

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name


class Filial(models.Model):
    name = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'filial'


class Consultant(models.Model):
    name = models.CharField(max_length=255, blank=True, default="")
    image = models.ImageField(upload_to='images', blank=True, default='default.png')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'consultant'


class CustomerInformation(models.Model):
    # About Client
    name = models.CharField(max_length=255, blank=True, default="")
    phone_number = models.CharField(max_length=255, blank=True, default="")
    character = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=255, blank=True, default="")
    nuance = models.CharField(max_length=255, blank=True, default="")
    is_called = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
        db_table = 'customer_information'

    def __str__(self):
        return self.name


class Visited(models.Model):
    # About Furniture
    category = models.ManyToManyField(Category, blank=True, related_name='post_category')
    name_furniture = models.CharField(max_length=255, blank=True, default="")
    type_furniture = models.CharField(max_length=255, blank=True, default="")
    model_furniture = models.CharField(max_length=255, blank=True, default="")
    color = models.CharField(max_length=255, blank=True, default="")
    nuance = models.CharField(max_length=255, blank=True, default="нет")
    # About Time and Place
    date = models.DateField(blank=True, null=True)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE, max_length=255, related_name='post_filial', blank=True,
                               default="")
    other_shop = models.CharField(max_length=255, blank=True, default="")
    find_out = models.CharField(max_length=255, blank=True, default="")
    # Consultant
    consultant = models.ForeignKey(Consultant, on_delete=models.CASCADE, related_name='post_consultant')

    visitor = models.ForeignKey(CustomerInformation, on_delete=models.CASCADE, max_length=255, blank=True, null=True,
                                related_name='visitors')

    class Meta:
        ordering = ['date']
        db_table = 'visited'

    def __str__(self):
        return str(self.date)
