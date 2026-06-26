"""
基础智能体类模块

定义所有智能体的基类，提供通用的属性和方法。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import json
from datetime import datetime


class BaseAgent(ABC):
    """
    智能体基类

    所有具体智能体都应该继承这个类并实现 process() 方法。
    """

    def __init__(
        self,
        name: str,
        role: str,
        spark_api: Optional[Any] = None,
        memory: Optional[List[Dict]] = None
    ):
        """
        初始化智能体

        Args:
            name: 智能体名称
            role: 智能体角色描述
            spark_api: Spark API 客户端实例
            memory: 记忆列表，存储历史对话
        """
        self.name = name
        self.role = role
        self.spark_api = spark_api
        self.memory = memory or []

    def add_to_memory(self, message: Dict[str, Any]) -> None:
        """
        添加消息到记忆中

        Args:
            message: 消息字典，包含 role 和 content
        """
        self.memory.append(message)

    def clear_memory(self) -> None:
        """清空记忆"""
        self.memory = []

    def get_memory(self) -> List[Dict[str, Any]]:
        """
        获取记忆

        Returns:
            记忆列表
        """
        return self.memory

    def generate_prompt(self, input_data: Dict[str, Any]) -> str:
        """
        生成提示词

        Args:
            input_data: 输入数据字典

        Returns:
            生成的提示词字符串
        """
        # 基础提示词模板，子类应该重写这个方法
        prompt = f"""
你是一个{self.name}，角色是{self.role}。

请根据以下输入生成相应的输出：

输入数据：
{json.dumps(input_data, ensure_ascii=False, indent=2)}

请根据你的角色和专业知识和上述输入，生成高质量的输出。
"""
        return prompt

    @abstractmethod
    def process(self, input_data: Dict[str, Any], mock: bool = False) -> Dict[str, Any]:
        """
        处理输入数据并生成输出

        这是一个抽象方法，所有子类必须实现。

        Args:
            input_data: 输入数据字典
            mock: 是否使用模拟模式（不调用API，返回模拟数据）

        Returns:
            包含处理结果的字典
        """
        pass

    def _call_spark_api(self, prompt: str, temperature: float = 0.7) -> str:
        """
        调用 Spark API

        Args:
            prompt: 提示词
            temperature: 温度参数

        Returns:
            API 返回的文本内容
        """
        if self.spark_api is None:
            raise ValueError("Spark API 未初始化，请在创建智能体时提供 spark_api 参数")

        try:
            # 这里需要根据实际的 Spark API 客户端实现来调用
            # 假设 spark_api 有一个 chat() 方法
            response = self.spark_api.chat(prompt, temperature=temperature)
            return response
        except Exception as e:
            raise Exception(f"调用 Spark API 失败: {str(e)}")

    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        解析 JSON 格式的 API 响应

        Args:
            response: API 返回的字符串

        Returns:
            解析后的字典
        """
        try:
            # 尝试直接解析 JSON
            return json.loads(response)
        except json.JSONDecodeError:
            # 如果失败，尝试从文本中提取 JSON
            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    pass

            # 如果还是失败，返回原始文本
            return {"raw_response": response}

    def __str__(self) -> str:
        """返回智能体的字符串表示"""
        return f"{self.name} ({self.role})"

    def __repr__(self) -> str:
        """返回智能体的详细表示"""
        return f"BaseAgent(name='{self.name}', role='{self.role}')"
