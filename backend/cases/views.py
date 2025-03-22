from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from .models import Case, NaturalPerson, LegalEntity, UserProfile, UserRole
from .forms import CaseForm, NaturalPersonForm, LegalEntityForm, CaseReviewForm, UserProfileForm

def is_admin(user):
    try:
        return user.userprofile.role == UserRole.ADMIN
    except UserProfile.DoesNotExist:
        return False

@login_required
def case_list(request):
    if request.user.userprofile.role == UserRole.ADMIN:
        cases = Case.objects.all()
    else:
        cases = Case.objects.filter(creator=request.user)
    return render(request, 'cases/case_list.html', {'cases': cases})

@login_required
def case_create(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.creator = request.user
            case.save()
            messages.success(request, '案件创建成功！')
            return redirect('case_detail', pk=case.pk)
    else:
        form = CaseForm()
    return render(request, 'cases/case_form.html', {'form': form})

@login_required
def case_detail(request, pk):
    case = get_object_or_404(Case, pk=pk)
    if not is_admin(request.user) and case.creator != request.user:
        messages.error(request, '您没有权限查看此案件！')
        return redirect('case_list')
    
    natural_persons = case.natural_persons.all()
    legal_entities = case.legal_entities.all()
    return render(request, 'cases/case_detail.html', {
        'case': case,
        'natural_persons': natural_persons,
        'legal_entities': legal_entities
    })

@login_required
def add_natural_person(request, case_pk):
    case = get_object_or_404(Case, pk=case_pk)
    if not is_admin(request.user) and case.creator != request.user:
        messages.error(request, '您没有权限添加当事人！')
        return redirect('case_detail', pk=case_pk)
    
    if request.method == 'POST':
        form = NaturalPersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.case = case
            person.save()
            messages.success(request, '自然人添加成功！')
            return redirect('case_detail', pk=case_pk)
    else:
        form = NaturalPersonForm()
    return render(request, 'cases/person_form.html', {'form': form, 'case': case})

@login_required
def add_legal_entity(request, case_pk):
    case = get_object_or_404(Case, pk=case_pk)
    if not is_admin(request.user) and case.creator != request.user:
        messages.error(request, '您没有权限添加当事人！')
        return redirect('case_detail', pk=case_pk)
    
    if request.method == 'POST':
        form = LegalEntityForm(request.POST)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.case = case
            entity.save()
            messages.success(request, '法人添加成功！')
            return redirect('case_detail', pk=case_pk)
    else:
        form = LegalEntityForm()
    return render(request, 'cases/entity_form.html', {'form': form, 'case': case})

@login_required
@user_passes_test(is_admin)
def case_review(request, pk):
    case = get_object_or_404(Case, pk=pk)
    if request.method == 'POST':
        form = CaseReviewForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            if case.status == 'APV':
                messages.success(request, '案件已通过审核！')
            elif case.status == 'RJCT':
                messages.warning(request, '案件已拒绝！')
            return redirect('case_detail', pk=pk)
    else:
        form = CaseReviewForm(instance=case)
    return render(request, 'cases/case_review.html', {'form': form, 'case': case})

@login_required
def case_edit(request, pk):
    case = get_object_or_404(Case, pk=pk)
    if not is_admin(request.user) and case.creator != request.user:
        messages.error(request, '您没有权限编辑此案件！')
        return redirect('case_detail', pk=pk)
    
    if case.status == 'APV':
        messages.error(request, '已通过审核的案件不能修改！')
        return redirect('case_detail', pk=pk)
    
    if request.method == 'POST':
        form = CaseForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            messages.success(request, '案件更新成功！')
            return redirect('case_detail', pk=pk)
    else:
        form = CaseForm(instance=case)
    return render(request, 'cases/case_form.html', {'form': form})



