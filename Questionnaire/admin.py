from django.contrib import admin

from CallCenter.models import CalCenterClient
from Questionnaire.models import CustomerInformation, Consultant, Category, Filial, Visited

admin.site.register(CustomerInformation)
admin.site.register(Consultant)
admin.site.register(Category)
admin.site.register(Filial)
admin.site.register(Visited)
admin.site.register(CalCenterClient)

