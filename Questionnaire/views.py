from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from .models import CustomerInformation, Consultant, Category, Visited


class MainMenuView(View):
    def get(self, request):
        return render(request, 'Questionnaire/mainstatistics.html')


class ShopView(View):
    def get(self, request):
        customerInfo = CustomerInformation.objects.filter(visitors__callers=None)
        page = request.GET.get('page', 1)
        paginator = Paginator(customerInfo, 50)
        try:
            customerInfo = paginator.page(page)
        except PageNotAnInteger:
            customerInfo = paginator.page(1)
        except EmptyPage:
            customerInfo = paginator.page(paginator.num_pages)

        return render(request, 'Questionnaire/index.html', context={'posts': customerInfo})


class CategoryDetailView(View):
    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        print(category)
        return render(request, 'Questionnaire/category_detail.html', context={'category': category})


class ProfileDetailView(View):
    def get(self, request, pk):
        profile = Consultant.objects.get(pk=pk)
        posts = Visited.objects.filter(consultant=profile)
        return render(request, 'Questionnaire/profile_detail.html', context={'profile': profile, 'posts': posts})

class QuestionnaireView(View):
    def post(self,request):
        if request.POST.get('from') and request.POST.get('to'):
            fr = request.POST.get('from')
            to = request.POST.get('to')
            print(fr,to)
            post=CustomerInformation.objects.filter(visitors__date__range=[fr,to])
            print(post)
            page = request.GET.get('page', 1)
            paginator = Paginator(post, 50)
            try:
                post = paginator.page(page)
            except PageNotAnInteger:
                post = paginator.page(1)
            except EmptyPage:
                post = paginator.page(paginator.num_pages)
        else:
            post=CustomerInformation.objects.all()
            page = request.GET.get('page', 1)
            paginator = Paginator(post, 50)
            try:
                post = paginator.page(page)
            except PageNotAnInteger:
                post = paginator.page(1)
            except EmptyPage:
                post = paginator.page(paginator.num_pages)

        return render(request, 'Questionnaire/questionnaire.html', context={'post': post,
                                                                            })


    def get(self, request):
        post = CustomerInformation.objects.get_queryset().order_by('id')
        page = request.GET.get('page', 1)
        paginator = Paginator(post, 50)
        try:
            post = paginator.page(page)
        except PageNotAnInteger:
            post = paginator.page(1)
        except EmptyPage:
            post = paginator.page(paginator.num_pages)
        return render(request, 'Questionnaire/questionnaire.html', context={'post': post
                                                                            })
