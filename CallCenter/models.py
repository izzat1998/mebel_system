from django.db import models

from Questionnaire.models import Visited


class CalCenterClient(models.Model):
    call_content = models.TextField(blank=True, default="", null=True)
    visitor = models.ForeignKey(Visited, blank=True, on_delete=models.CASCADE, null=True, related_name='callers')
    call_center_name = models.CharField(max_length=255, default='Хамида')
    date_pub = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.call_content
