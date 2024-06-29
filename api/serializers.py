from rest_framework import serializers

from django.contrib.auth.models import User

from budget.models import Income,Expense

class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model=User

        fields=["id","username","email","password"]

        read_only_fields=["id"]

    #method overridig
    def create(self,validated_data):

        return User.objects.create_user(**validated_data)


class Incomeserializer(serializers.ModelSerializer):

    user_object=serializers.StringRelatedField(read_only=True)
    
    class Meta:

        model=Income

        fields="__all__"

        read_only_fields=["id","created_date","user_object"]


class ExpenseSerializer(serializers.ModelSerializer):

    user_object=serializers.StringRelatedField(read_only=True)

    class Meta:

        model=Expense

        fields="__all__"

        read_only_fields=["id","created_date","user_object"]


    
