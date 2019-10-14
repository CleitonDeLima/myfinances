from django.urls import reverse_lazy
from django.views import generic
from django_filters.views import FilterView

from core.filters import RecordFilter
from core.forms import RecordForm
from core.models import Record, Bill


class RecordFilterView(FilterView):
    template_name = 'record_list.html'
    ordering = ['-date', '-created_at']
    filterset_class = RecordFilter
    paginate_by = 30


class HomeView(generic.TemplateView):
    template_name = 'home.html'


class BillListView(generic.ListView):
    template_name = 'bill_list.html'
    queryset = Bill.objects.balance()


class BillCreateView(generic.CreateView):
    template_name = 'bill_form.html'
    fields = ['name', 'type', 'tags']
    model = Bill
    success_url = reverse_lazy('bill-list')


class BillUpdateView(generic.UpdateView):
    template_name = 'bill_form.html'
    fields = ['name', 'type', 'tags']
    model = Bill
    success_url = reverse_lazy('bill-list')


class ExpenseListView(RecordFilterView):
    extra_context = {'class_label': 'danger'}
    queryset = Record.objects.filter(
        type=Record.OUT
    ).prefetch_related('tags', 'bill')


class ExpenseCreateView(generic.CreateView):
    extra_context = {'header_title': 'Criar Despesa'}
    template_name = 'record_form.html'
    form_class = RecordForm
    queryset = Record.objects.filter(type=Record.OUT)
    success_url = reverse_lazy('expense-list')

    def form_valid(self, form):
        form.instance.type = Record.OUT

        return super().form_valid(form)


class ExpenseUpdateView(generic.UpdateView):
    extra_context = {'header_title': 'Editar Despesa'}
    template_name = 'record_form.html'
    form_class = RecordForm
    queryset = Record.objects.filter(type=Record.OUT)
    success_url = reverse_lazy('expense-list')


class ExpenseDeleteView(generic.DeleteView):
    http_method_names = ['post']
    queryset = Record.objects.filter(type=Record.OUT)
    success_url = reverse_lazy('expense-list')


class IncomeListView(RecordFilterView):
    extra_context = {'class_label': 'success'}
    queryset = Record.objects.filter(
        type=Record.IN
    ).prefetch_related('tags', 'bill')


class IncomeCreateView(generic.CreateView):
    extra_context = {'header_title': 'Criar Receita'}
    template_name = 'record_form.html'
    form_class = RecordForm
    queryset = Record.objects.filter(type=Record.IN)
    success_url = reverse_lazy('income-list')

    def form_valid(self, form):
        form.instance.type = Record.IN

        return super().form_valid(form)


class IncomeUpdateView(generic.UpdateView):
    extra_context = {'header_title': 'Editar Receita'}
    template_name = 'record_form.html'
    form_class = RecordForm
    queryset = Record.objects.filter(type=Record.IN)
    success_url = reverse_lazy('income-list')


class IncomeDeleteView(generic.DeleteView):
    http_method_names = ['post']
    queryset = Record.objects.filter(type=Record.IN)
    success_url = reverse_lazy('income-list')


home = HomeView.as_view()

bill_list = BillListView.as_view()
bill_create = BillCreateView.as_view()
bill_update = BillUpdateView.as_view()

expense_list = ExpenseListView.as_view()
expense_create = ExpenseCreateView.as_view()
expense_update = ExpenseUpdateView.as_view()
expense_delete = ExpenseDeleteView.as_view()

income_list = IncomeListView.as_view()
income_create = IncomeCreateView.as_view()
income_update = IncomeUpdateView.as_view()
income_delete = IncomeDeleteView.as_view()
