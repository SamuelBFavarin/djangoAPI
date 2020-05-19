from django.db import models
from django.db.models import Avg, Max, Min
from django.core.validators import MinLengthValidator, MinValueValidator


class User(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)
    cpf = models.CharField(max_length=11, blank=False,
                           unique=True, validators=[MinLengthValidator(11)])
    date_birth = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.name)

    @property
    def lower_salary(self):
        return self.salaries.all().aggregate(Min('value')).get('value__min', 0.00)

    @property
    def bigger_salary(self):
        return self.salaries.all().aggregate(Max('value')).get('value__max', 0.00)

    @property
    def avg_salary(self):
        return self.salaries.all().aggregate(Avg('value')).get('value__avg', 0.00)

    @property
    def avg_discount(self):
        print(self.salaries.all().aggregate(Avg('discount')))
        return self.salaries.all().aggregate(Avg('discount')).get('discount__avg', 0.00)


class Salary(models.Model):
    value = models.FloatField(
        blank=False,
        validators=[MinValueValidator(0)])
    discount = models.FloatField(
        blank=False,
        validators=[MinValueValidator(0)])
    user = models.ForeignKey(
        User, related_name='salaries', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.value)
