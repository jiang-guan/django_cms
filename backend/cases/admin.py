from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Case, NaturalPerson, LegalEntity, UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '用户角色'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'get_role')
    list_filter = ('userprofile__role',)

    def get_role(self, obj):
        try:
            return obj.userprofile.get_role_display()
        except UserProfile.DoesNotExist:
            return '未设置'
    get_role.short_description = '角色'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

class NaturalPersonInline(admin.TabularInline):
    model = NaturalPerson
    extra = 1

class LegalEntityInline(admin.TabularInline):
    model = LegalEntity
    extra = 1

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'status', 'created_at')
    list_filter = ('status', 'creator')
    search_fields = ('title', 'description')
    inlines = [NaturalPersonInline, LegalEntityInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            if request.user.userprofile.role == 'ADM':
                return qs
            return qs.filter(creator=request.user)
        except UserProfile.DoesNotExist:
            return qs.none()

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        if request.user.is_superuser:
            return True
        try:
            if request.user.userprofile.role == 'ADM':
                return True
            return obj.creator == request.user
        except UserProfile.DoesNotExist:
            return False

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return True

@admin.register(NaturalPerson)
class NaturalPersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'case', 'role', 'gender', 'phone_number')
    list_filter = ('role', 'gender', 'case')
    search_fields = ('name', 'id_number', 'phone_number')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            if request.user.userprofile.role == 'ADM':
                return qs
            return qs.filter(case__creator=request.user)
        except UserProfile.DoesNotExist:
            return qs.none()

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        if request.user.is_superuser:
            return True
        try:
            if request.user.userprofile.role == 'ADM':
                return True
            return obj.case.creator == request.user
        except UserProfile.DoesNotExist:
            return False

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return True

@admin.register(LegalEntity)
class LegalEntityAdmin(admin.ModelAdmin):
    list_display = ('name', 'case', 'role', 'entity_type', 'phone_number')
    list_filter = ('role', 'entity_type', 'case')
    search_fields = ('name', 'credit_code', 'phone_number')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            if request.user.userprofile.role == 'ADM':
                return qs
            return qs.filter(case__creator=request.user)
        except UserProfile.DoesNotExist:
            return qs.none()

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        if request.user.is_superuser:
            return True
        try:
            if request.user.userprofile.role == 'ADM':
                return True
            return obj.case.creator == request.user
        except UserProfile.DoesNotExist:
            return False

    def has_view_permission(self, request, boj=None):
        return True

    def has_add_permission(self, request):
        return True

# 重新注册 User 模型
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)