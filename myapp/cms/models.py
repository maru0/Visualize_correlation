from django.db import models


# Create your models here.
class Category(models.Model):
    categories = models.CharField(max_length=50)

    def __str__(self):
        return self.categories


class Deviation(models.Model):
    data_name = models.CharField(max_length=50)

    def __str__(self):
        return self.data_name


class Sample(models.Model):
    cate_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    data_id = models.ForeignKey(Deviation, on_delete=models.CASCADE)

    def __str___(self):
        return self.date_id


class Prefecture(models.Model):
    prefecture = models.CharField(max_length=10)


class Alldata(models.Model):
    cate_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    static_id = models.ForeignKey(Deviation, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Prefecture, on_delete=models.CASCADE)
    data1 = models.FloatField()
    data2 = models.FloatField()
    hensa = models.FloatField()
