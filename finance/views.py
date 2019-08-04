from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, reverse

from finance.forms import FinanceRecordForm
from finance.models import FinanceRecord


# Create your views here.
@login_required
def index(request):
    if request.method == 'POST':
        form = FinanceRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            return redirect(reverse('finance:index'))
        else:
            context = {
                'form': form,
                'records': FinanceRecord.get_record(request.user)
            }
            return render(request, 'finance_info.html', context=context)
    else:
        records = FinanceRecord.get_record(request.user)
        paginator = Paginator(records, 5)
        page = request.GET.get('page')
        try:
            records = paginator.get_page(page)
        except PageNotAnInteger:
            records = paginator.get_page(1)
        except EmptyPage:
            records = paginator.get_page(paginator.num_pages)
        context = {
            'form': FinanceRecordForm(),
            'records': records
        }
        print(dir(records))
        return render(request, 'finance_info.html', context=context)