from django import forms
from .models import Expense, Category


class DateInput(forms.DateInput):
    input_type = 'date'

class ExpenseSearchForm(forms.ModelForm):
    CHOICES = [(category.id, category) 
               for category in Category.objects.all()]
    ORDER_CHOICES = (
        ("1", "Latest"),
        ("2", "Oldest"),
        ("3", "Category Up"),
        ("4", "Category Down"),
        )
    class Meta:
        model = Expense
        fields = ('name',)
    # name = forms.CharField(label='Your name')
    min_date = forms.DateField(label='From', widget=DateInput, required=False)
    max_date = forms.DateField(label='To', widget=DateInput, required=False)
    category = forms.MultipleChoiceField(choices=(CHOICES), widget=forms.CheckboxSelectMultiple, required=False)
    order = forms.ChoiceField(choices=ORDER_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
