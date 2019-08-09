import json

from datetime import datetime, date, time, timedelta
import collections

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from Questionnaire.models import CustomerInformation, Category, Filial, Visited
from .serializer import CustomerInformationSerializer, GetCountCategorySerializer


# Create your views here.
class GetCustomerInformationApiView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = ''
    serializer_class = CustomerInformationSerializer
    authentication_classes = []

    def get_queryset(self):
        qs = CustomerInformation.objects.all()
        if(self.request.GET.get('from')!=None and self.request.GET.get('to')!=None):
            date_1=str(self.request.GET.get('from'))
            date_2 = str(self.request.GET.get('to'))
            qs = CustomerInformation.objects.filter(visitors__date__range=[date_1, date_2])
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(name__icontains=query) | Q(phone_number__icontains=query) | Q(category__name__icontains=query) | Q(
                    date=query) | Q(status__contains=query)).distinct()
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class GetCustomerDetail(generics.RetrieveAPIView):
    lookup_field = 'pk'
    serializer_class = CustomerInformationSerializer
    queryset = CustomerInformation.objects.all()


class GetCountCategoryApiView(generics.ListAPIView):
    lookup_field = ''
    serializer_class = GetCountCategorySerializer
    authentication_classes = []


class GetCategoryCount(APIView):
    def get(self, request):
        count = []
        category2 = []
        categories = Category.objects.all()
        for category in categories:
            category2.append(category.name)
            count.append(Visited.objects.filter(category=category).count())
        response = [{'category': t, 'count': s} for t, s in zip(category2, count)]
        return Response(response)


class GetWhileCategoryCount(APIView):
    def get(self, request):
        count = []
        category2 = []
        categories = Category.objects.all()
        category = str(self.request.GET.get('category'))
        category_list = category.split(',')
        date_1 = str(self.request.GET.get('from'))
        date_2 = str(self.request.GET.get('to'))
        if category == 'None':
            for caty in categories:
                counter = 0
                category2.append(str(caty))
                counter = Visited.objects.filter(category=caty,date__range=[date_1,date_2]).count()
                print(counter)
                count.append(counter)
                response = [{'category': t, 'count': s} for t, s in zip(category2, count)]
            return Response(response)
        else:

            for categ in categories:
                counter = 0
                for cat in category_list:
                    if str(categ) == cat:
                        category2.append(cat)
                        counter = Visited.objects.filter(category=categ,date__range=[date_1,date_2]).count()
                        count.append(counter)
            response = [{'category': t, 'count': s} for t, s in zip(category2, count)]
            return Response(response)


class getDateCount(APIView):
    def get(self, request):
        response = []
        counted_dates = []
        filial_list = str(self.request.GET.get('filial')).split(',')
        date_1 = str(self.request.GET.get('from'))
        date_2 = str(self.request.GET.get('to'))
        start = datetime.strptime(date_1, '%Y-%m-%d')
        end = datetime.strptime(date_2, '%Y-%m-%d')
        step = timedelta(days=1)
        while start <= end:
            counted_dates.append(start.date())
            start += step
        for filial_name in filial_list:
            count = []
            counter = -1
            index_list = []
            for date in counted_dates:
                filial = Filial.objects.get(name=filial_name)
                ci_dates = Visited.objects.filter(date__contains=date, filial_id=filial.id)
                counter = counter + 1
                if not ci_dates:
                    index_list.append(counter)

                for ci in ci_dates:
                    count.append(ci.date)
            counted_customer = (list(collections.Counter(count).values()))

            for index in index_list:
                counted_customer.insert(index, 0)
            print(counted_customer)
            dictionary = ([{'date': t, 'count': s} for t, s in zip(counted_dates, counted_customer)])
            response.append({filial_name: dictionary})
        return Response(response)


class TenDaysGetCount(APIView):
    def get(self, request):
        response = []
        counted_dates = []
        dates = []
        filial_list = ['Себзор', 'Хамза', 'Октепа']
        today = date.today()
        if (today.day >= 1 and today.day <= 10):
            step = timedelta(days=1)
            while today.day >= 1:
                dates.append(today)
                today -= step
        elif (today.day >= 11 and today.day <= 20):
            step = timedelta(days=1)
            while today.day >= 11:
                dates.append(today)
                today -= step
        elif (today.day >= 21 and today.day <= 31):
            step = timedelta(days=1)
            while today.day >= 21:
                dates.append(today)
                today -= step
        for filial_name in filial_list:
            count = []
            counter = -1
            index_list = []
            for dat in dates:
                filial = Filial.objects.get(name=filial_name)
                ci_dates = Visited.objects.filter(date__contains=dat, filial_id=filial.id)
                counter = counter + 1
                if not ci_dates:
                    index_list.append(counter)
                for ci in ci_dates:
                    count.append(ci.date)
            counted_customer = (list(collections.Counter(count).values()))
            for index in index_list:
                counted_customer.insert(index, 0)

            print(len(dates))
            print(len(counted_customer))
            dictionary = ([{'date': t, 'count': s} for t, s in zip(dates, counted_customer)])
            response.append({filial_name: dictionary})
        return Response(response)
