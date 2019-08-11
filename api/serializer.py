from django.http import HttpResponse
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


class VisitedCreateSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    consultant = ConsultantSerializer()
    filial = FilialSerializer()

    class Meta:
        model = Visited
        fields = ['category', 'consultant', 'filial', 'name_furniture', 'type_furniture',
                  'model_furniture',
                  'color', 'nuance', 'date', 'other_shop',
                  'find_out']


class CustomerInformationCreateSerializer(serializers.ModelSerializer):
    visitors = VisitedCreateSerializer(many=True)

    class Meta:
        model = CustomerInformation
        fields = [
            'id',
            'name', 'phone_number', 'character', 'status', 'nuance',
            'is_called', 'visitors'
        ]

    def create(self, validated_data):
        tracks_data = validated_data.pop('visitors')
        c_i = CustomerInformation(**validated_data)
        phone_number= validated_data.pop('phone_number')
        print(phone_number)
        if  CustomerInformation.objects.get(phone_number=phone_number):
            print(phone_number)
            c_i=CustomerInformation.objects.get(phone_number=phone_number)
        c_i.save()
        cat_list = []
        for track_data in tracks_data:
            filial = Filial.objects.get(name=track_data.pop('filial')['name'])
            consultant = Consultant.objects.get(name=track_data.pop('consultant')['name'])
            categories = track_data.pop('category')
            for cat in categories:
                category_id=Category.objects.get(name=cat['name']).id
                cat_list.append(category_id)
            v = Visited.objects.create(visitor=c_i, filial=filial, consultant=consultant, **track_data)
            for item in cat_list:
                v.category.add(item)
            v.save()
        return c_i





class GetCountCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerInformation
        fields = [
            'category',
            'count',
        ]
