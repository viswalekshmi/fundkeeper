from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response

from rest_framework.views import APIView

from api.serializers import UserSerializer

from rest_framework.viewsets import ModelViewSet

from rest_framework import authentication,permissions

from api.serializers import Incomeserializer,ExpenseSerializer

from api.permissions import OwnerOnly

from budget.models import Income,Expense

from django.utils import timezone

from django.db.models import Sum




class UserCreationView(APIView):

    def post(self,request,*args,**kwargs):

        serializer_instance=UserSerializer(data=request.data)#deserialization

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)
 

class IncomeViewSet(ModelViewSet):

    serializer_class=Incomeserializer

    queryset=Income.objects.all()

    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]

    # permission_classes=[permissions.IsAuthenticated]

    permission_classes=[OwnerOnly]

    def list(self,request,*args,**kwargs):

        qs=Income.objects.filter(user_object=request.user)

        serializer_instance=Incomeserializer(qs,many=True)

        return Response(data=serializer_instance.data)
    
    def perform_create(self, serializer):

        return serializer.save(user_object=self.request.user)
    
    
class IncomeSummaryView(APIView):

    permission_classes=[permissions.IsAuthenticated]

    # authentication_classes=[authentication.BasicAuthentication]

    authentication_classes=[authentication.TokenAuthentication]


    def get(self,request,*args,**kwargs):

        current_month=timezone.now().month

        current_year=timezone.now().year

        all_incomes=Income.objects.filter(

                        user_object=request.user,

                        created_date__month=current_month,

                        created_date__year=current_year
         )
        
        income_total=all_incomes.values("amount").aggregate(total=Sum("amount"))

        category_summary=all_incomes.values("category").annotate(totals=Sum("amount"))

        data={
            "income_total":income_total,

            "category_summary":category_summary
        }

        return Response (data=data)



class ExpenseViewSet(ModelViewSet):

    serializer_class=ExpenseSerializer

    queryset=Expense.objects.all()

    authentication_classes=[authentication.TokenAuthentication]

    # permission_classes=[permissions.IsAuthenticated]

    permission_classes=[OwnerOnly]

    def list(self, request, *args, **kwargs):

        queryset=Expense.objects.filter(user_object=request.user)

        serializer_instance=ExpenseSerializer(queryset,many=True)

        return Response(data=serializer_instance.data)
    

    # avoid not null constrains 
    def perform_create(self, serializer):

        return serializer.save(user_object=self.request.user)
    


class ExpenseSummaryView(APIView):

    permission_classes=[permissions.IsAuthenticated]

    # authentication_classes=[authentication.BasicAuthentication]

    
    authentication_classes=[authentication.TokenAuthentication]

    def get(self,request,*args,**kwargs):

        current_month=timezone.now().month

        current_year=timezone.now().year

        all_expense=Expense.objects.filter(

                        user_object=request.user,

                        created_date__month=current_month,

                        created_date__year=current_year
         )
        
        expense_total=all_expense.values("amount").aggregate(total=Sum("amount"))

        category_summary=all_expense.values("category").annotate(totals=Sum("amount"))

        priority_summary=all_expense.values("priority").annotate(total=Sum("amount"))

        data={
            "expense_total":expense_total,

            "category_summary":category_summary,

            "priority_summary":priority_summary
        }

        return Response (data=data)
    
    
    
    
