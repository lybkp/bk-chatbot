"""
TencentBlueKing is pleased to support the open source community by making
蓝鲸智云PaaS平台社区版 (BlueKing PaaSCommunity Edition) available.
Copyright (C) 2017-2018 THL A29 Limited,
a Tencent company. All rights reserved.
Licensed under the MIT License (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""


from django.utils.decorators import method_decorator

from common.drf.view_set import BaseManageViewSet
from common.http.request import get_request_biz_id
from src.manager.module_trigger.models import TriggerModel
from src.manager.module_trigger.proto.trigger import (
    ReqPostTriggerViewSerializer,
    ReqPutTriggerViewSerializer,
    TriggerViewSerializer,
    trigger_create_docs,
    trigger_delete_docs,
    trigger_list_docs,
    trigger_update_docs,
)


@method_decorator(name="list", decorator=trigger_list_docs)
@method_decorator(name="create", decorator=trigger_create_docs)
@method_decorator(name="update", decorator=trigger_update_docs)
@method_decorator(name="destroy", decorator=trigger_delete_docs)
class TriggerViewSet(BaseManageViewSet):
    queryset = TriggerModel.objects.all()
    serializer_class = TriggerViewSerializer
    create_serializer_class = ReqPostTriggerViewSerializer
    update_serializer_class = ReqPutTriggerViewSerializer
    filterset_class = TriggerModel.OpenApiFilter

    def list(self, request, *args, **kwargs):
        """
        查询触发器
        @param request:
        @param args:
        @param kwargs:
        @return:
        """
        request.query_params._mutable = True
        biz_id = request.payload.get("biz_id", None)
        if not biz_id:
            request.query_params["biz_id"] = get_request_biz_id(request)
        return super().list(self, request, *args, **kwargs)
