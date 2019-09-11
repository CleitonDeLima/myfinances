import uuid

from colorfield.fields import ColorField
from django.db import models
from django.utils import timezone


class AppModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Record(AppModel):
    IN = '1'
    OUT = '2'
    TYPES = [
        (IN, 'Entrada'),
        (OUT, 'Saída'),
    ]
    type = models.CharField(choices=TYPES, max_length=1)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True)
    category = models.ForeignKey('core.Category', on_delete=models.CASCADE)
    bill = models.ForeignKey('core.Bill', on_delete=models.CASCADE,
                             related_name='records')
    observation = models.TextField(blank=True)

    class Meta:
        verbose_name = 'registro'
        verbose_name_plural = 'registros'

    def __str__(self):
        return f'{self.get_type_display()} - {self.value}'

    def save(self, *args, **kwargs):
        if self.type == self.OUT:
            self.bill.decrease_balance(self.value)
        elif self.type == self.IN:
            self.bill.add_balance(self.value)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.type == Record.IN:
            self.bill.decrease_balance(self.value)
        else:
            self.bill.add_balance(self.value)

        return super().delete(*args, **kwargs)


class Category(AppModel):
    IN = '1'
    OUT = '2'
    TYPES = [
        (IN, 'Entrada'),
        (OUT, 'Saída'),
    ]
    type = models.CharField(choices=TYPES, max_length=1)
    name = models.CharField(max_length=30)
    color = ColorField(default='#FF0000')

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):
        return f'{self.name} - {self.get_type_display()}'


class Bill(AppModel):
    MONEY = '1'
    CURRENT_ACCOUNT = '2'
    INVESTMENTS = '3'
    OTHERS = '4'

    TYPES = [
        (MONEY, 'Dinheiro'),
        (CURRENT_ACCOUNT, 'Conta Corrente'),
        (INVESTMENTS, 'Investimentos'),
        (OTHERS, 'Outros'),
    ]
    name = models.CharField(max_length=30)
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    type = models.CharField(choices=TYPES, max_length=2)

    class Meta:
        verbose_name = 'conta'
        verbose_name_plural = 'contas'

    def __str__(self):
        return self.name

    def add_balance(self, value):
        self.balance += value
        self.save()

    def decrease_balance(self, value):
        self.balance -= value
        self.save()


class Transfer(AppModel):
    sender = models.ForeignKey('core.Bill', on_delete=models.CASCADE,
                               related_name='sender_transfers')
    receiver = models.ForeignKey('core.Bill', on_delete=models.CASCADE,
                                 related_name='receiver_transfers')
    value = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = 'transferência'
        verbose_name_plural = 'transferências'

    def __str__(self):
        return str(self.value)

    def save(self, *args, **kwargs):
        # atualiza valores em conta
        self.sender.decrease_balance(self.value)
        self.receiver.add_balance(self.value)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # atualiza valores em conta antes de excluir
        self.sender.add_balance(self.value)
        self.receiver.decrease_balance(self.value)

        super().delete(*args, **kwargs)
