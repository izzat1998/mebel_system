from django.contrib import admin

from CallCenter.models import CalCenterClient
from Questionnaire.models import CustomerInformation, Consultant, Category, Filial, Visited, NameFurniture



class CIAdmin(admin.ModelAdmin):
    list_display = ['name','phone_number','character','status','dates','filials','categories','names_furnitures']
    list_display_links = ['name','dates']
    list_editable = ['phone_number','character','status']
admin.site.register(CustomerInformation,CIAdmin)
admin.site.register(Consultant)
admin.site.register(Category)
admin.site.register(Filial)
admin.site.register(Visited)
admin.site.register(CalCenterClient)
admin.site.register(NameFurniture)

