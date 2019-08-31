from django.http import HttpResponse
from rest_framework import serializers

from CallCenter.models import CalCenterClient
from Questionnaire.models import Category, CustomerInformation, Visited, Consultant, Filial, NameFurniture


class CallContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalCenterClient
        fields = ['id', 'call_content', 'date_pub', ]


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
        fields = ['name', 'is_selled']


class NameFurnitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = NameFurniture
        fields = ['name', ]


class VisitedSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    name_furniture = NameFurnitureSerializer(many=True)
    consultant = ConsultantSerializer()
    filial = FilialSerializer()
    callers = CallContentSerializer(many=True)

    class Meta:
        model = Visited
        fields = ['id', 'category', 'consultant', 'filial', 'name_furniture',
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
    name_furniture = NameFurnitureSerializer(many=True)
    consultant = ConsultantSerializer()
    filial = FilialSerializer()

    class Meta:
        model = Visited
        fields = ['category', 'consultant', 'filial', 'name_furniture',
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
        name_furniture_list = []
        c_i = CustomerInformation(**validated_data)
        phone_number = validated_data.pop('phone_number')
        print(phone_number)
        # if  CustomerInformation.objects.get(phone_number=phone_number):
        #     print(phone_number)
        #     c_i=CustomerInformation.objects.get(phone_number=phone_number)
        c_i.save()
        cat_list = []
        for track_data in tracks_data:
            filial = Filial.objects.get(name=track_data.pop('filial')['name'])
            consultant = Consultant.objects.get(name=track_data.pop('consultant')['name'])
            categories = track_data.pop('category')
            name_furnitures = track_data.pop('name_furniture')
            for name_furniture in name_furnitures:
                name_furniture_id = NameFurniture.objects.create(name=name_furniture['name']).id
                name_furniture_list.append(name_furniture_id)
            for cat in categories:
                category_id = Category.objects.get(name=cat['name']).id
                cat_list.append(category_id)
            v = Visited.objects.create(visitor=c_i, filial=filial, consultant=consultant, **track_data)
            for item in cat_list:
                v.category.add(item)
            v.save()
            for namef in name_furniture_list:
                print(name_furniture_id)
                v.name_furniture.add(namef)
            v.save()
        return c_i


class CustomerInformationUpdateSerializer(serializers.ModelSerializer):
    visitors = VisitedSerializer(many=True)

    class Meta:
        model = CustomerInformation
        fields = [
            'id',
            'name', 'phone_number', 'character', 'status', 'nuance',
            'is_called', 'visitors'
        ]

    def update(self, instance, validated_data):
        category_id = []
        name_furniture_id = []
        visitors = validated_data.pop('visitors')
        b_list = ['visitors', ]
        for k, v in validated_data.items():
            if hasattr(instance, k):
                setattr(instance, k, v)
        instance.save()
        categories, consultants, filials, name_furnitures, callers = [], [], [], [], []

        for visitor in visitors:
            print(visitor.pop('date'))
            categories = visitor.pop('category')
            name_furnitures = visitor.pop('name_furniture')
            callers = visitor.pop('callers')
            for category in categories:
                id = Category.objects.get(name=category['name'])
                category_id.append(id)
            for name_furniture in name_furnitures:
                id = NameFurniture.objects.get(name=name_furniture['name'])
                name_furniture_id.append(id)
            filial = Filial.objects.get(name=visitor.pop('filial')['name'])
            consultant = Consultant.objects.get(name=visitor.pop('consultant')['name'])

            for visit in instance.visitors.all():
                visit.nuance = visitor.get('nuance',visit.nuance)
                visit.model_furniture=visitor.get('model_furniture',visit.model_furniture)
                visit.date = visitor.get('date',visit.date)
                visit.other_shop = visitor.get('other_shop', visit.other_shop)
                visit.find_out = visitor.get('find_out', visit.find_out)
                visit.filial = filial
                visit.consultant = consultant
                visit.category.clear()
                visit.name_furniture.clear()
                for category_id in category_id:
                    visit.category.add(category_id)
                    visit.save()
                for name_furniture_id in name_furniture_id:
                    visit.name_furniture.add(name_furniture_id)
                    visit.save()
        return instance


class GetCountCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerInformation
        fields = [
            'category',
            'count',
        ]


visitors = [
    {
        "id": 1,
        "categpry": [
            {
                "id"
            }
        ]
    }
]
