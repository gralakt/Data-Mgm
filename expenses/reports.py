from collections import OrderedDict

from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from .models import Expense

def summary_per_category(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(category_name=Coalesce('category__name', Value('-')))
        .order_by()
        .values('category_name')
        .annotate(s=Sum('amount'))
        .values_list('category_name', 's')
    ))


def summary_per_date():
    return ([
        {'year': i[0], 'month': i[1], 'summary': i[2]}
         for i in Expense.objects
         .all()
         .values_list('date__year', 'date__month')
         .annotate(Sum('amount'))
         .order_by('date__year', 'date__month')
    ])
        
