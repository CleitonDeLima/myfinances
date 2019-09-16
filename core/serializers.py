from rest_framework import serializers

from core.models import Bill, Category, Record


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color']


class RecordSerializer(serializers.ModelSerializer):
    record_type = None
    bill = BillSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    bill_id = serializers.PrimaryKeyRelatedField(
        source='bill',
        queryset=Bill.objects.all(),
        write_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        source='category',
        queryset=Category.objects.all(),
        write_only=True
    )

    class Meta:
        model = Record
        fields = [
            'id', 'value', 'date', 'description', 'category', 'category_id',
            'bill', 'bill_id', 'observation'
        ]

    def save(self, **kwargs):
        return super().save(type=self.record_type, **kwargs)


class ExpenseSerializer(RecordSerializer):
    record_type = Record.OUT


class IncomeSerializer(RecordSerializer):
    record_type = Record.IN
