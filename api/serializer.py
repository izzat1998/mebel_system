from rest_framework import serializers

from CallCenter.models import CalCenterClient
from Questionnaire.models import Category, CustomerInformation, Visited, Consultant, Filial


class CallContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalCenterClient
        fields = ['call_content', 'date_pub']


class FilialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filial
        fields = ['name']


class ConsultantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultant
        fields = ['name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', ]


class VisitedSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    consultant = ConsultantSerializer()
    filial = FilialSerializer()
    callers = CallContentSerializer(many=True)

    class Meta:
        model = Visited
        fields = ['category', 'consultant', 'filial', 'name_furniture', 'type_furniture',
                  'model_furniture',
                  'color', 'nuance', 'date', 'other_shop',
                  'find_out', 'callers']


class CustomerInformationSerializer(serializers.ModelSerializer):
    visitors = VisitedSerializer(many=True)

    class Meta:
        model = CustomerInformation
        fields = [
            'id',
            'name', 'phone_number', 'character', 'status', 'nuance',
            'is_called', 'visitors'
        ]


class GetCountCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerInformation
        fields = [
            'category',
            'count',
        ]
