from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Role(models.TextChoices):
    PLAINTIFF = 'PLT', 'Plaintiff'
    DEFENDANT = 'DEF', 'Defendant'
    THIRD_PARTY = 'TP', 'Third Party'

class Case(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=4,  # 调整为4以适应最长的选项
        choices=[
            ('PEN', 'Pending'),
            ('APV', 'Approved'),
            ('RJCT', 'Rejected')
        ],
        default='PEN'
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class NaturalPerson(models.Model):
    case = models.ForeignKey(Case, related_name='natural_persons', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=50)
    work_unit = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    domicile_address = models.CharField(max_length=255)
    usual_residence = models.CharField(max_length=255, blank=True, null=True)
    id_type = models.CharField(max_length=50)
    id_number = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=3, choices=Role.choices)

    def __str__(self):
        return self.name

class LegalEntity(models.Model):
    case = models.ForeignKey(Case, related_name='legal_entities', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    registration_place = models.CharField(max_length=255)
    legal_representative = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    credit_code = models.CharField(max_length=18, unique=True)
    entity_type = models.CharField(max_length=50)
    role = models.CharField(max_length=3, choices=Role.choices)

    def __str__(self):
        return self.name



