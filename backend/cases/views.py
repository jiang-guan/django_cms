from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CaseForm, NaturalPersonForm, LegalEntityForm
from .models import Case, NaturalPerson, LegalEntity

@login_required
def create_case(request):
    if request.method == 'POST':
        case_form = CaseForm(request.POST)
        natural_person_forms = [NaturalPersonForm(request.POST, prefix=f'np-{i}') for i in range(0, int(request.POST.get('natural_person_count', 0)))]
        legal_entity_forms = [LegalEntityForm(request.POST, prefix=f'le-{i}') for i in range(0, int(request.POST.get('legal_entity_count', 0)))]

        if case_form.is_valid():
            case = case_form.save(commit=False)
            case.creator = request.user
            case.save()

            for form in natural_person_forms:
                if form.is_valid():
                    natural_person = form.save(commit=False)
                    natural_person.case = case
                    natural_person.save()

            for form in legal_entity_forms:
                if form.is_valid():
                    legal_entity = form.save(commit=False)
                    legal_entity.case = case
                    legal_entity.save()

            return redirect('case_detail', pk=case.pk)
    else:
        case_form = CaseForm()
        natural_person_forms = [NaturalPersonForm(prefix=f'np-{i}') for i in range(0, 1)]  # 初始显示一个自然人表单
        legal_entity_forms = [LegalEntityForm(prefix=f'le-{i}') for i in range(0, 1)]     # 初始显示一个法人实体表单

    context = {
        'case_form': case_form,
        'natural_person_forms': natural_person_forms,
        'legal_entity_forms': legal_entity_forms,
    }
    return render(request, 'cases/create_case.html', context)



