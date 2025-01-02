# -*- coding: utf-8 -*-
from typing import Optional, Dict, Any
from pydantic import BaseModel
import requests
import curlparser


class CurlRequest(BaseModel):
    url: str
    method: str = 'GET'
    headers: Dict[str, str] = {}
    data: Optional[Any] = None
    cookies: Dict[str, str] = {}
    auth: Optional[tuple] = None
    verify: bool = False

    def __init__(self, **data):
        super().__init__(**data)
        # 移除空值和空白字符串
        self.headers = {
            k: v.strip() for k, v in self.headers.items()
            if v is not None and v.strip()
        }
        # 标准化 header 名称
        self.headers = {k.strip().title(): v for k, v in self.headers.items()}


class CurlConverter:
    def parse_curl(self, curl_command: str) -> CurlRequest:
        parsed = curlparser.parse(curl_command)

        request = CurlRequest(
            url=parsed.url,
            auth=parsed.auth,
            method=parsed.method,
            headers=parsed.header,
            data=parsed.data,
            cookies=self._extract_cookies(parsed.header)
        )

        if 'Authorization' in parsed.header:
            request.auth = self._extract_auth(parsed.header['Authorization'])

        return request

    def _extract_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        important_headers = {
            'Host', 'Referer', 'User-Agent',
            'Accept', 'Content-Type', 'Origin'
        }
        return {k: v for k, v in headers.items()
                if k in important_headers or k.startswith('X-')}

    def _extract_cookies(self, headers: Dict[str, str]) -> Dict[str, str]:
        if 'Cookie' not in headers:
            return {}
        return dict(c.split('=', 1) for c in headers['Cookie'].split('; '))

    def _extract_auth(self, auth_header: str) -> Optional[tuple]:
        if auth_header.startswith('Basic '):
            import base64
            decoded = base64.b64decode(auth_header[6:]).decode()
            return tuple(decoded.split(':', 1))
        return None

    def execute_request(self, request: CurlRequest) -> requests.Response:
        return requests.request(
            method=request.method,
            url=request.url,
            headers=request.headers,
            data=request.data,
            cookies=request.cookies,
            auth=request.auth,
            verify=request.verify,
        )


def convert_and_execute(curl_command: str) -> requests.Response:
    converter = CurlConverter()
    request = converter.parse_curl(curl_command)
    return converter.execute_request(request)


def write_event_details(event, output_file):
    """将事件详情写入文件并打印"""
    content = []

    # 基本信息
    content.append(f"内网IP: {event.get('IntranetIp', 'N/A')}")
    content.append(f"公网IP: {event.get('InternetIp', 'N/A')}")
    content.append(f"实例名: {event.get('InstanceName', 'N/A')}")

    # 详细信息
    content.append("\n详细信息:")
    for detail in event['Details']:
        content.append(f"{detail['NameDisplay']}: {detail['ValueDisplay']}")

    # 写入文件
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write('\n'.join(content))
        f.write('\n\n' + '-'*50 + '\n\n')

    # 打印到控制台
    print('\n'.join(content))
    print('\n' + '-'*50 + '\n')
