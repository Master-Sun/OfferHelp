from rest_framework import viewsets
from finance.serializers import FinanceSerializer, FinanceDetailSerializer
from finance.models import FinanceRecord


# 定义视图层的逻辑
class FinanceViewSet(viewsets.ReadOnlyModelViewSet):
    """文档说明：调用文档接口时可以看到"""
    # 指定序列化的类和数据
    serializer_class = FinanceSerializer
    queryset = FinanceRecord.objects.all()

    # 重写详情页的接口
    def retrieve(self, request, *args, **kwargs):
        # 改为详情页的序列化器
        self.serializer_class = FinanceDetailSerializer
        return  super().retrieve(request, *args, **kwargs)