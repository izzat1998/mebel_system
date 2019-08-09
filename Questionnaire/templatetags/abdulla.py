from django import template

register = template.Library()
from Questionnaire.models import Category,Consultant


@register.simple_tag(name='category')
def get_Category():
    category = Category.objects.all()

    return category

@register.simple_tag(name='consultants')
def get_Consultant():
    consultant=Consultant.objects.all()

    return consultant