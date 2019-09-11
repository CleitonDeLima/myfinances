from django.db.models import Sum, Q, Count
from django.urls import reverse_lazy
from django.views import generic
from django_filters.views import FilterView

from core.filters import RecordFilter
from core.forms import RecordForm
from core.mixins import RedirectToRefererSuccessMixin
from core.models import Bill, Record


class HomeView(generic.TemplateView):
    template_name = 'core/home.html'
    extra_context = {
        'title': 'Meu financeiro'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_totals'] = Record.objects.aggregate(
            value_in=Sum('value', filter=Q(type=Record.IN)),
            value_out=Sum('value', filter=Q(type=Record.OUT)),
        )
        context['bill_totals'] = Bill.objects.aggregate(
            balance_total=Sum('balance')
        )

        return context


class BillListView(generic.ListView):
    extra_context = {
        'title': 'Contas'
    }
    template_name = 'core/bill_list.html'
    queryset = Bill.objects.annotate(
        expense_count=Count('records', filter=Q(records__type=Record.OUT)),
        income_count=Count('records', filter=Q(records__type=Record.IN)),
    )


class RecordListView(FilterView):
    class_text = ''
    template_name = 'core/record_list.html'
    ordering = ['-date']
    filterset_class = RecordFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total = self.object_list.aggregate(Sum('value'))['value__sum']

        context['total'] = total
        context['class_text'] = self.class_text

        return context


class ExpenseListView(RecordListView):
    extra_context = {
        'title': 'Despesas'
    }
    queryset = Record.objects.filter(
        type=Record.OUT
    ).select_related('category', 'bill')
    class_text = 'text-danger'


class IncomeListView(RecordListView):
    extra_context = {
        'title': 'Receitas'
    }
    queryset = Record.objects.filter(
        type=Record.IN
    ).select_related('category', 'bill')
    class_text = 'text-success'


class ExpenseCreateView(generic.CreateView):
    extra_context = {
        'title': 'Nova Despesa'
    }
    template_name = 'core/record_form.html'
    model = Record
    form_class = RecordForm
    success_url = reverse_lazy('core:expense-list')

    def form_valid(self, form):
        form.instance.type = Record.OUT
        return super().form_valid(form)


class IncomeCreateView(generic.CreateView):
    extra_context = {
        'title': 'Nova Receita'
    }
    template_name = 'core/record_form.html'
    model = Record
    form_class = RecordForm
    success_url = reverse_lazy('core:income-list')

    def form_valid(self, form):
        form.instance.type = Record.IN
        return super().form_valid(form)


class RecordDeleteView(RedirectToRefererSuccessMixin, generic.DeleteView):
    http_method_names = ['post']
    model = Record


home = HomeView.as_view()
bill_list = BillListView.as_view()
expense_list = ExpenseListView.as_view()
expense_create = ExpenseCreateView.as_view()
income_list = IncomeListView.as_view()
income_create = IncomeCreateView.as_view()
record_delete = RecordDeleteView.as_view()
