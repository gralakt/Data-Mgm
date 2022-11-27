from django.views.generic.list import ListView

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, summary_per_date

from django.db.models import Sum

class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        total = Expense.objects.aggregate(Sum('amount'))["amount__sum"]
        print(total)
        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            min_date = form.cleaned_data.get('min_date')
            max_date = form.cleaned_data.get('max_date')
            if name:
                queryset = queryset.filter(name__icontains=name)
            if min_date:
                queryset = queryset.filter(date__gte=min_date)
            if max_date:
                queryset = queryset.filter(date__lte=max_date)
            category = form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category__id__in=category)
            order = form.cleaned_data.get('order')
            if order:
                if order == "1":
                    queryset = queryset.order_by('-date')
                elif order == "2":
                    queryset = queryset.order_by('date')
                elif order == "3":
                    queryset = queryset.order_by('category')
                elif order == "4":
                    queryset = queryset.order_by('-category')

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            summary_per_date=summary_per_date(),
            total=total,
            **kwargs)

class CategoryListView(ListView):
    model = Category
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(
            expenses = Expense.objects.values('category').annotate(category_sum = Sum('amount'))
            .values('category__name','category_sum','category__id'),
            **kwargs)







