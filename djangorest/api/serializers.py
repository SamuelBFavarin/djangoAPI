from rest_framework import serializers
from django.db.models import Max
from .models import User
from .models import Salary


class UserSerializer(serializers.ModelSerializer):

    salaries = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Salary.objects.all())

    avg_salary = serializers.ReadOnlyField()
    avg_discount = serializers.ReadOnlyField()
    lower_salary = serializers.ReadOnlyField()
    bigger_salary = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'name', 'cpf', 'date_birth',
                  'date_created', 'date_modified', 'salaries',
                  'avg_salary', 'avg_discount', 'lower_salary', 'bigger_salary')
        read_only_fields = ('date_created', 'date_modified',
                            'salaries', 'avg_salary', 'avg_discount',
                            'lower_salary', 'bigger_salary')


class SalarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Salary
        fields = ('id', 'value', 'discount', 'user',
                  'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')
