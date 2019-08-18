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
        all_records = FinanceRecord.get_record(request.user)
        paginator = Paginator(all_records, 5)
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

        # values：返回的是包含字典的查询结果集(列表中嵌套字典)
        # values_list：返回包含元组的查询结果集
        # 当只查询一个字段时，可加上参数flat，得到的就是一个只有一层的查询结果集，不再有嵌套在内部的数据结构
        # 将查询结果集通过list构造器转为列表，可在前端echarts中直接使用花括号接受数据
        echarts_record_time = list(all_records.order_by('id').values_list('record_time', flat=True))
        echarts_summary = list(all_records.order_by('id').values_list('summary', flat=True))

        # 通过列表推导式将datetime类型的日期格式转为字符串，方便前端echarts进行展示
        echarts_record_time = [i.strftime('%Y-%m-%d') for i in echarts_record_time]

        context.update({
            'echarts_record_time': echarts_record_time,
            'echarts_summary': echarts_summary
        })
        return render(request, 'finance_info.html', context=context)