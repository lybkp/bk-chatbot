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
import json
import logging
import os

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
    TencentCloudSDKException,
)
from tencentcloud.tmt.v20180321 import models, tmt_client
from tencentcloud.nlp.v20190408 import nlp_client
from tencentcloud.nlp.v20190408 import models as nlp_models

TencentCloudSecretId = os.getenv("TENCENT_CLOUD_SECRET_ID", "")
TencentCloudSecretKey = os.getenv("TENCENT_CLOUD_SECRET_KEY", "")

logger = logging.getLogger("root")


class TencentCloudClient:
    def __init__(self):
        cred = credential.Credential(TencentCloudSecretId, TencentCloudSecretKey)
        self.client = tmt_client.TmtClient(cred, "ap-beijing")
        self.nlp_client = nlp_client.NlpClient(cred, "ap-guangzhou")

    def translate_text(self, source_text, target_type, source_type="zh"):
        """
        文本翻译
        @param source_text:
        @param target_type:
        @param source_type:
        @return:
        """
        try:
            req = models.TextTranslateRequest()
            params = {
                "SourceText": source_text,
                "Source": source_type,
                "Target": target_type,
                "ProjectId": 0,
            }
            req.from_json_string(json.dumps(params))
            resp = self.client.TextTranslate(req)
            result = json.loads(resp.to_json_string())
            return result["TargetText"]
        except TencentCloudSDKException as ex:
            logger.exception(ex)
            return source_text
        except Exception as ex:
            logger.exception(ex)
            return source_text

    def chat(self, chat_content):
        """
        闲聊
        @param chat_content:
        @return:
        """
        try:
            req = nlp_models.ChatBotRequest()
            params = {"Query": chat_content}
            req.from_json_string(json.dumps(params))
            resp = self.nlp_client.ChatBot(req)
            result = json.loads(resp.to_json_string())
            result.update({"result": True})
            return result
        except TencentCloudSDKException as ex:
            result = {"result": False, "message": str(ex)}
        except Exception as ex:
            result = {"result": False, "message": str(ex)}
        return result
