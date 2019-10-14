import uuid

from django.db import models
from django.shortcuts import resolve_url
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase

from core.managers import BillQuerySet


class AppModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


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
    bill = models.ForeignKey('core.Bill', on_delete=models.CASCADE,
                             related_name='records')
    tags = TaggableManager(through=UUIDTaggedItem)

    class Meta:
        verbose_name = 'registro'
        verbose_name_plural = 'registros'

    def __str__(self):
        return f'{self.get_type_display()} - {self.value}'

    @cached_property
    def tag_list(self):
        return list(self.tags.all())

    def get_update_url(self):
        if self.type == self.IN:
            return resolve_url('income-update', self.id)

        return resolve_url('expense-update', self.id)

    def get_delete_url(self):
        if self.type == self.IN:
            return resolve_url('income-delete', self.id)

        return resolve_url('expense-delete', self.id)


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
    type = models.CharField(choices=TYPES, max_length=2)
    tags = TaggableManager(through=UUIDTaggedItem)

    objects = BillQuerySet.as_manager()

    class Meta:
        verbose_name = 'conta'
        verbose_name_plural = 'contas'

    def __str__(self):
        return self.name

    @cached_property
    def tag_list(self):
        return list(self.tags.all())
