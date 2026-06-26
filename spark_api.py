#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
科大讯飞星火大模型API封装
支持WebSocket连接、多轮对话、流式输出、模拟模式
"""

import hashlib
import base64
import hmac
import json
import time
import threading
from datetime import datetime
from typing import List, Dict, Optional, Generator, Any
import websocket
import ssl


class SparkAPI:
    """
    科大讯飞星火大模型API封装类
    支持WebSocket连接、多轮对话、流式输出
    """
    
    # 星火大模型API地址
    SPARK_URLS = {
        "v1.5": "ws://spark-api.xf-yun.com/v1.1/chat",
        "v2.0": "ws://spark-api.xf-yun.com/v2.1/chat",
        "v3.0": "ws://spark-api.xf-yun.com/v3.1/chat",
        "v3.5": "ws://spark-api.xf-yun.com/v3.5/chat",
        "v4.0": "ws://spark-api.xf-yun.com/v4.0/chat"
    }
    
    def __init__(
        self,
        app_id: str,
        api_key: str,
        api_secret: str,
        model_version: str = "v3.5",
        mock_mode: bool = False,
        max_retries: int = 3,
        timeout: int = 30
    ):
        """
        初始化SparkAPI
        
        Args:
            app_id: 应用ID
            api_key: API密钥
            api_secret: API密钥Secret
            model_version: 模型版本 (v1.5, v2.0, v3.0, v3.5, v4.0)
            mock_mode: 是否启用模拟模式
            max_retries: 最大重试次数
            timeout: 超时时间（秒）
        """
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.model_version = model_version
        self.mock_mode = mock_mode
        self.max_retries = max_retries
        self.timeout = timeout
        
        # WebSocket连接
        self.ws = None
        self.ws_url = self.SPARK_URLS.get(model_version, self.SPARK_URLS["v3.5"])
        
        # 响应数据
        self.response_text = ""
        self.response_done = False
        self.response_error = None
        
    def _create_auth_url(self) -> str:
        """
        生成鉴权URL
        
        Returns:
            带鉴权参数的WebSocket URL
        """
        # 获取当前时间戳
        now = datetime.now()
        date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
        
        # 拼接签名字符串
        signature_origin = f"host: spark-api.xf-yun.com\n"
        signature_origin += f"date: {date}\n"
        signature_origin += "GET /v3.5/chat HTTP/1.1"
        
        # 进行hmac-sha256签名
        signature_sha = hmac.new(
            self.api_secret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        
        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')
        
        authorization_origin = f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        
        # 拼接鉴权URL
        url = self.ws_url
        url += f"?authorization={authorization}"
        url += f"&date={date}"
        url += f"&host=spark-api.xf-yun.com"
        
        return url
    
    def _on_message(self, ws, message):
        """WebSocket消息回调"""
        try:
            data = json.loads(message)
            
            # 检查是否有错误
            if data.get("header", {}).get("code") != 0:
                self.response_error = data.get("header", {}).get("message", "未知错误")
                self.response_done = True
                return
            
            # 提取文本内容
            choices = data.get("payload", {}).get("choices", {})
            if choices and "text" in choices:
                for text_item in choices["text"]:
                    self.response_text += text_item.get("content", "")
            
            # 检查是否结束
            if data.get("header", {}).get("status") == 2:
                self.response_done = True
                
        except Exception as e:
            self.response_error = str(e)
            self.response_done = True
    
    def _on_error(self, ws, error):
        """WebSocket错误回调"""
        self.response_error = f"WebSocket错误: {str(error)}"
        self.response_done = True
    
    def _on_close(self, ws, close_status_code, close_msg):
        """WebSocket关闭回调"""
        self.response_done = True
    
    def _on_open(self, ws):
        """WebSocket打开回调"""
        pass
    
    def _send_request(self, ws, request_data: Dict):
        """
        发送请求数据
        
        Args:
            ws: WebSocket连接
            request_data: 请求数据
        """
        request_json = json.dumps(request_data)
        ws.send(request_json)
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.5,
        max_tokens: int = 4096,
        stream: bool = False
    ) -> Generator[str, None, None] or str:
        """
        多轮对话
        
        Args:
            messages: 对话历史，格式为 [{"role": "user", "content": "你好"}]
            temperature: 温度参数，控制随机性
            max_tokens: 最大生成token数
            stream: 是否流式输出
            
        Returns:
            如果stream=True，返回生成器；否则返回完整回复字符串
        """
        # 模拟模式
        if self.mock_mode:
            return self._mock_chat(messages, stream)
        
        # 构建请求数据
        request_data = {
            "header": {
                "app_id": self.app_id,
                "uid": "user_" + str(int(time.time()))
            },
            "parameter": {
                "chat": {
                    "domain": self._get_domain(),
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
            },
            "payload": {
                "message": {
                    "text": messages
                }
            }
        }
        
        # 重试逻辑
        for attempt in range(self.max_retries):
            try:
                # 重置响应状态
                self.response_text = ""
                self.response_done = False
                self.response_error = None
                
                # 创建WebSocket连接
                websocket.enableTrace(False)
                ws_url = self._create_auth_url()
                
                self.ws = websocket.WebSocketApp(
                    ws_url,
                    on_message=self._on_message,
                    on_error=self._on_error,
                    on_close=self._on_close,
                    on_open=self._on_open
                )
                
                # 在单独线程中发送请求
                def run_ws():
                    self._send_request(self.ws, request_data)
                    # 保持连接直到收到完整响应
                    while not self.response_done:
                        time.sleep(0.1)
                    self.ws.close()
                
                ws_thread = threading.Thread(target=run_ws)
                ws_thread.daemon = True
                ws_thread.start()
                
                # 等待响应
                start_time = time.time()
                while not self.response_done:
                    time.sleep(0.01)
                    if time.time() - start_time > self.timeout:
                        raise TimeoutError("请求超时")
                
                # 检查错误
                if self.response_error:
                    raise Exception(self.response_error)
                
                # 返回结果
                if stream:
                    # 流式输出：逐字符返回
                    for char in self.response_text:
                        yield char
                else:
                    return self.response_text
                    
            except Exception as e:
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                    continue
                else:
                    raise Exception(f"调用星火API失败（已重试{self.max_retries}次）: {str(e)}")
        
        return self.response_text if not stream else None
    
    def _get_domain(self) -> str:
        """
        根据模型版本获取domain参数
        
        Returns:
            domain字符串
        """
        domain_map = {
            "v1.5": "general",
            "v2.0": "generalv2",
            "v3.0": "generalv3",
            "v3.5": "generalv3.5",
            "v4.0": "4.0Ultra"
        }
        return domain_map.get(self.model_version, "generalv3.5")
    
    def _mock_chat(self, messages: List[Dict[str, str]], stream: bool) -> Generator[str, None, None] or str:
        """
        模拟模式：返回预设回复
        
        Args:
            messages: 对话历史
            stream: 是否流式输出
            
        Returns:
            模拟回复
        """
        # 获取最后一条用户消息
        user_message = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break
        
        # 根据输入内容生成不同的模拟回复
        mock_response = self._generate_mock_response(user_message)
        
        # 流式输出或完整返回
        if stream:
            for char in mock_response:
                yield char
        else:
            return mock_response
    
    def _generate_mock_response(self, user_message: str) -> str:
        """
        根据用户消息生成模拟回复
        
        Args:
            user_message: 用户消息
            
        Returns:
            模拟回复内容
        """
        # 关键词匹配，返回不同的模拟回复
        user_lower = user_message.lower()
        
        # 问候类
        if any(word in user_lower for word in ["你好", "hello", "hi", "您好"]):
            return "你好！我是讯飞星火大模型。很高兴为你提供帮助。有什么我可以为你解答的问题吗？"
        
        # 自我介绍
        elif any(word in user_lower for word in ["你是谁", "介绍自己", "你是什么"]):
            return "我是科大讯飞推出的星火认知大模型。我具备跨领域的知识和语言理解能力，可以进行多轮对话、逻辑推理、文本生成等任务。我很乐意帮助你解决问题！"
        
        # 编程相关
        elif any(word in user_lower for word in ["python", "代码", "编程", "程序", "函数", "class"]):
            return """这是一个很好的编程问题！让我为你提供一个示例代码：

```python
def solve_problem(data):
    \"\"\"
    解决问题的主要函数
    \"\"\"
    # 数据处理
    processed_data = [x for x in data if x is not None]
    
    # 核心逻辑
    result = sum(processed_data) / len(processed_data) if processed_data else 0
    
    return result

# 使用示例
data = [1, 2, 3, 4, 5]
output = solve_problem(data)
print(f"结果是: {output}")
```

这个示例展示了如何处理数据并计算平均值。你可以根据自己的需求修改逻辑。"""
        
        # 数学问题
        elif any(word in user_lower for word in ["数学", "计算", "方程", "函数", "几何"]):
            return """这是一个有趣的数学问题！

让我为你详细解答：

**问题分析：**
首先需要理解题目的要求和给定条件。

**解题步骤：**
1. 列出已知条件
2. 建立数学模型
3. 求解方程/推导公式
4. 验证结果

**最终答案：**
根据计算，结果为：√(2π) ≈ 2.5066

如果你需要更详细的推导过程，请告诉我！"""
        
        # 写作相关
        elif any(word in user_lower for word in ["写作", "文章", "作文", "写", "创作"]):
            return """我很乐意帮你进行写作！

**写作建议：**

1. **明确主题**：首先确定你想要表达的核心观点
2. **结构清晰**：采用"总-分-总"的结构
3. **论据充分**：使用具体的数据、案例来支持观点
4. **语言优美**：注意修辞手法的运用

**示例开头：**
"在当今快速发展的社会中，人工智能技术正在深刻改变着我们的生活方式。从智能助手到自动驾驶，从医疗诊断到教育培训，AI的应用已经渗透到各个领域..."

如果你有具体的写作需求，可以告诉我主题，我会帮你创作！"""
        
        # 翻译相关
        elif any(word in user_lower for word in ["翻译", "translate", "英文", "中文", "日语"]):
            return """我可以帮你进行翻译！

**翻译要点：**
1. 保持原文的意思和语气
2. 符合目标语言的表达习惯
3. 注意专业术语的准确性

**示例：**
- 中文："人工智能是未来科技发展的方向"
- 英文："Artificial intelligence is the direction of future technological development"
- 日文："人工知能は未来の技術発展の方向です"

请把需要翻译的内容发给我，我会为你提供准确的翻译！"""
        
        # 学习相关
        elif any(word in user_lower for word in ["学习", "复习", "考试", "知识点", "理解"]):
            return """关于学习，我有以下建议：

**高效学习方法：**

1. **费曼学习法**：尝试用简单的语言向别人解释概念
2. **间隔重复**：定期复习，加深记忆
3. **主动回忆**：而不是被动阅读
4. **建立知识图谱**：将知识点连接起来

**学习规划：**
- 每天固定时间学习
- 设定具体可达成的目标
- 及时总结和反思

如果你有具体的学科问题，欢迎随时问我！"""
        
        # 默认回复
        else:
            return f"""这是一个很有意思的问题！

关于"{user_message[:50]}..."，我的理解是：

这个问题涉及到多个方面的考量。让我从以下几个角度为你分析：

**1. 核心要点**
首先需要明确问题的本质和关键要素。

**2. 相关背景**
了解相关的上下文信息对于全面理解很重要。

**3. 解决方案**
基于以上分析，我建议采取以下方法：

- 方案A：直接解决问题
- 方案B：分步实施
- 方案C：寻求替代方案

**4. 总结**
综合考虑各种因素，我认为最合适的方法是...

如果你需要更详细的解答，或者有其他问题，请随时告诉我！"""
    
    def close(self):
        """关闭WebSocket连接"""
        if self.ws:
            self.ws.close()


# 便捷函数
def create_spark_client(
    app_id: str = None,
    api_key: str = None,
    api_secret: str = None,
    model_version: str = "v3.5",
    mock_mode: bool = False
) -> SparkAPI:
    """
    创建星火API客户端
    
    Args:
        app_id: 应用ID（如果不提供，从环境变量读取）
        api_key: API密钥（如果不提供，从环境变量读取）
        api_secret: API密钥Secret（如果不提供，从环境变量读取）
        model_version: 模型版本
        mock_mode: 是否启用模拟模式
        
    Returns:
        SparkAPI实例
    """
    import os
    
    # 从环境变量读取配置
    if not app_id:
        app_id = os.getenv("SPARK_APP_ID", "")
    if not api_key:
        api_key = os.getenv("SPARK_API_KEY", "")
    if not api_secret:
        api_secret = os.getenv("SPARK_API_SECRET", "")
    
    return SparkAPI(
        app_id=app_id,
        api_key=api_key,
        api_secret=api_secret,
        model_version=model_version,
        mock_mode=mock_mode
    )


# 示例用法
if __name__ == "__main__":
    # 示例1：使用模拟模式
    print("=== 示例1：模拟模式 ===")
    client = create_spark_client(mock_mode=True)
    
    # 非流式对话
    messages = [{"role": "user", "content": "你好，请介绍一下自己"}]
    response = client.chat(messages, stream=False)
    print(f"用户: {messages[0]['content']}")
    print(f"星火: {response}\n")
    
    # 流式对话
    print("=== 示例2：流式输出 ===")
    messages = [{"role": "user", "content": "请用Python写一个冒泡排序"}]
    print(f"用户: {messages[0]['content']}")
    print("星火: ", end="")
    for char in client.chat(messages, stream=True):
        print(char, end="", flush=True)
    print("\n")
    
    # 示例2：多轮对话
    print("=== 示例3：多轮对话 ===")
    conversation = []
    
    # 第一轮
    conversation.append({"role": "user", "content": "什么是机器学习？"})
    response = client.chat(conversation, stream=False)
    conversation.append({"role": "assistant", "content": response})
    print(f"用户: {conversation[0]['content']}")
    print(f"星火: {response}\n")
    
    # 第二轮
    conversation.append({"role": "user", "content": "能给我举几个应用的例子吗？"})
    response = client.chat(conversation, stream=False)
    print(f"用户: {conversation[-1]['content']}")
    print(f"星火: {response}\n")
    
    client.close()
