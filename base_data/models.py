from django.db import models


class Province(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, related_name="cities")

    class Meta:
        unique_together = ("name", "province")

    def __str__(self):
        return self.name + " (" + self.province.name + ")"


class JobCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, related_name="jobs")
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name + " (" + self.category.name + ")"
