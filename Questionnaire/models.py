from datetime import datetime

from django.db import models


class Category(models.Model):
    is_selled = models.BooleanField(default=False, blank=True)
    name = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return self.name


class NameFurniture(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Filial(models.Model):
    name = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return self.name


class Consultant(models.Model):
    name = models.CharField(max_length=255, blank=True, default="")
    image = models.ImageField(upload_to='images', blank=True, default='default.png')

    def __str__(self):
        return self.name


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
    @property
    def dates(self):
        dates=[]
        for visit in self.visitors.all():
            dates.append(visit.date)
        return dates

    @property
    def filials(self):
        filials=[]
        for visit in self.visitors.all():
            filials.append(visit.filial.name)
        return filials
    @property
    def categories(self):
        categories=[]
        for visit in self.visitors.all():
            for cat in visit.category.all():
                categories.append(cat)
        return categories
    @property
    def names_furnitures(self):
        name_furnitures=[]
        for visit in self.visitors.all():
            for nmf in visit.name_furniture.all():
                name_furnitures.append(nmf)
        return name_furnitures








    def __str__(self):
        return self.name


class Visited(models.Model):
    # About Furniture
    category = models.ManyToManyField(Category, blank=True, related_name='post_category')
    name_furniture = models.ManyToManyField(NameFurniture, blank=True, related_name='name_furnitures')
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
        ordering = ['id']

    def __str__(self):
        return str(self.date)
