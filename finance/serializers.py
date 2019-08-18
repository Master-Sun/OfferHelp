from rest_framework import serializers
from finance.models import FinanceRecord


# 定义serializer序列化列表页的数据，类似于form表单，form表单继承自forms.ModelForm
class FinanceSerializer(serializers.ModelSerializer):
    # 类似form表单，对某些特殊的字段进行处理
    # 处理外键相关的字段
    user = serializers.SlugRelatedField(
        # many=True,    多对多时添加此参数
        read_only=True,     # 只读接口
        slug_field='username'    # 对应外键中要展示的字段
    )
    # 格式化时间字段
    record_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    # 类似form表单，定义关联的模型以及列表页展示的字段
    class Meta:
        model = FinanceRecord
        # id字段用来获取详情页的数据
        fields = ['id', 'user', 'summary', 'record_time']


# 定义serializer序列化详情页的数据，继承自列表页的序列化器，然后重新定义展示的字段即可
class FinanceDetailSerializer(FinanceSerializer):
    class Meta:
        model = FinanceRecord
        fields = ['id', 'user', 'alipay_balance', 'wechat_balance', 'paycard_balance',
                  'huabei_debt', 'credit_debt', 'other', 'describe', 'summary', 'record_time']
