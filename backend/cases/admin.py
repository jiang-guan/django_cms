from django.contrib import admin
from .models import Case, NaturalPerson, LegalEntity

admin.site.register(Case)
admin.site.register(NaturalPerson)
admin.site.register(LegalEntity)