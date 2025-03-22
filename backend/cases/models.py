from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserRole(models.TextChoices):
    LAWYER = 'LAW', '律师'
    ADMIN = 'ADM', '管理员'

class Role(models.TextChoices):
    PLAINTIFF = 'PLT', '原告'
    DEFENDANT = 'DEF', '被告'
    THIRD_PARTY = 'TP', '第三人'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=3, choices=UserRole.choices, default=UserRole.LAWYER)
    phone = models.CharField(max_length=20, blank=True, null=True)
    office = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)

class Case(models.Model):
    title = models.CharField(max_length=255, verbose_name='案件标题')
    description = models.TextField(verbose_name='案件描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    status = models.CharField(
        max_length=4,
        choices=[
            ('PEN', '待审核'),
            ('APV', '已通过'),
            ('RJCT', '已拒绝')
        ],
        default='PEN',
        verbose_name='状态'
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='创建者')
    rejection_reason = models.TextField(blank=True, null=True, verbose_name='拒绝原因')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '案件'
        verbose_name_plural = '案件'

class NaturalPerson(models.Model):
    case = models.ForeignKey(Case, related_name='natural_persons', on_delete=models.CASCADE, verbose_name='所属案件')
    name = models.CharField(max_length=100, verbose_name='姓名')
    gender = models.CharField(max_length=1, choices=[('M', '男'), ('F', '女')], verbose_name='性别')
    date_of_birth = models.DateField(verbose_name='出生日期')
    ethnicity = models.CharField(max_length=50, verbose_name='民族')
    nationality = models.CharField(max_length=50, verbose_name='国籍')
    work_unit = models.CharField(max_length=255, blank=True, null=True, verbose_name='工作单位')
    position = models.CharField(max_length=100, blank=True, null=True, verbose_name='职务')
    phone_number = models.CharField(max_length=20, verbose_name='联系电话')
    domicile_address = models.CharField(max_length=255, verbose_name='住所地')
    usual_residence = models.CharField(max_length=255, blank=True, null=True, verbose_name='经常居住地')
    id_type = models.CharField(max_length=50, verbose_name='证件类型')
    id_number = models.CharField(max_length=50, unique=True, verbose_name='证件号码')
    role = models.CharField(max_length=3, choices=Role.choices, verbose_name='角色')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '自然人'
        verbose_name_plural = '自然人'

class LegalEntity(models.Model):
    case = models.ForeignKey(Case, related_name='legal_entities', on_delete=models.CASCADE, verbose_name='所属案件')
    name = models.CharField(max_length=255, verbose_name='名称')
    address = models.CharField(max_length=255, verbose_name='住所地')
    registration_place = models.CharField(max_length=255, verbose_name='注册地')
    legal_representative = models.CharField(max_length=100, verbose_name='法定代表人')
    position = models.CharField(max_length=100, verbose_name='职务')
    phone_number = models.CharField(max_length=20, verbose_name='联系电话')
    credit_code = models.CharField(max_length=18, unique=True, verbose_name='统一社会信用代码')
    entity_type = models.CharField(max_length=50, verbose_name='类型')
    role = models.CharField(max_length=3, choices=Role.choices, verbose_name='角色')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '法人'
        verbose_name_plural = '法人'



