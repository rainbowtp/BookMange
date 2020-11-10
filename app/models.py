from django.db import models


# Create your models here.

class Publish(models.Model):
    name = models.CharField(max_length=32)

    city = models.CharField(max_length=32, null=True, default="不详")
    tel = models.CharField(max_length=32, null=True, default="不详")
    email = models.EmailField(max_length=32, null=True, default="不详")
    description = models.CharField(max_length=32, null=True, default="无")


class Category(models.Model):
    name = models.CharField(max_length=32)


class Author(models.Model):
    name = models.CharField(max_length=32)

    description = models.CharField(max_length=32, null=True, default="无")
    age = models.IntegerField(null=True, default=0)
    country = models.CharField(max_length=32, null=True, default="不详")
    postcode = models.CharField(max_length=7, null=True, default='不详')


class Book(models.Model):
    name = models.CharField(max_length=32)
    # 建立一对多关系
    publish = models.ForeignKey(to=Publish, to_field='id', on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(to=Category, to_field='id', on_delete=models.CASCADE, null=True)
    # 建立多对多关系
    author = models.ManyToManyField(to=Author)


class Comment(models.Model):
    user = models.CharField(max_length=32, null=True, default="未知")
    comments = models.CharField(max_length=64, null=True, default="无")
    data = models.DateField(auto_now=True)

    book = models.ForeignKey(to=Book, to_field='id', on_delete=models.CASCADE, null=True)
