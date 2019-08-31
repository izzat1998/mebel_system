from datetime import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from CallCenter.models import CalCenterClient
from Questionnaire.models import CustomerInformation, Visited

#
# class GetCustomerInfo(ListView):
#     paginate_by = 10
#     context_object_name = 'posts'
#     template_name = 'CallCenter/call_center.html'
#
#     def get_queryset(self):
#         qs = CustomerInformation.objects.filter(is_called=False)
#         return qs
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['call_post'] = CalCenterClient.objects.distinct()
#         print(context['call_post'])
#         return context


class GetCustomerInfo(View):
    def get(self, request):
        post = CustomerInformation.objects.filter(is_called=False).distinct()
        page = request.GET.get('page', 1)
        paginator = Paginator(post, 10)
        try:
            post = paginator.page(page)
        except PageNotAnInteger:
            post = paginator.page(1)
        except EmptyPage:
            post = paginator.page(paginator.num_pages)

        post2 = CalCenterClient.objects.order_by('visitor__visitor_id')

        print(post2)
        print(post2)
        page = request.GET.get('page2', 1)
        paginator = Paginator(post2, 10)
        try:
            post2 = paginator.page(page)
        except PageNotAnInteger:
            post2 = paginator.page(1)
        except EmptyPage:
            post2 = paginator.page(paginator.num_pages)
        return render(request, 'CallCenter/call_center.html', context={'posts': post, 'call_post': post2})


class PostCallContent(View):
    def post(self, request, *args, **kwargs):
        call = request.POST.get('call_content')
        ci_id = request.POST.get('id')
        call_content = CalCenterClient.objects.create(call_content=call)
        post = Visited.objects.get(id=ci_id)
        call_content.visitor = post
        call_content.save()
        post.visitor.is_called = True
        post.visitor.save()
        post.save()
        return HttpResponseRedirect(reverse('call_center'))


class UpdateCallContent(View):
    def get(self,request, id):
        call_content=CalCenterClient.objects.get(id=id)
        call_content.call_content=request.GET.get('call_content')
        call_content.save()
        return HttpResponseRedirect(reverse('call_center'))
