"""
学生画像智能体模块

从对话历史中提取学生特征，输出JSON格式画像（6个维度）。
"""

import json
from typing import Dict, Any, List
from .base_agent import BaseAgent


class ProfileAgent(BaseAgent):
    """
    学生画像智能体

    从对话历史中提取学生特征，生成包含6个维度的学生画像。
    六个维度：
    1. 知识水平 (knowledge_level)
    2. 学习风格 (learning_style)
    3. 兴趣爱好 (interests)
    4. 学习目标 (learning_goals)
    5. 薄弱环节 (weaknesses)
    6. 学习进度 (learning_progress)
    """

    def __init__(self, spark_api: Any = None, memory: List[Dict] = None):
        """
        初始化学生画像智能体

        Args:
            spark_api: Spark API 客户端实例
            memory: 记忆列表
        """
        super().__init__(
            name="学生画像智能体",
            role="你是一个专业的教育分析师，擅长从对话中分析学生的学习特征，生成全面的学生画像",
            spark_api=spark_api,
            memory=memory
        )

    def generate_prompt(self, input_data: Dict[str, Any]) -> str:
        """
        生成学生画像分析的提示词

        Args:
            input_data: 包含对话历史的字典

        Returns:
            提示词字符串
        """
        conversation_history = input_data.get("conversation_history", "")
        student_input = input_data.get("student_input", "")

        prompt = f"""
{self.role}

## 任务
分析以下学生的学习特征，生成包含6个维度的学生画像。

## 输入信息
对话历史：
{conversation_history}

学生输入：
{student_input}

## 输出要求
请输出严格的JSON格式，包含以下6个维度：

1. knowledge_level (知识水平): 描述学生的当前知识水平，包括已掌握的知识点、理解深度等
2. learning_style (学习风格): 描述学生的学习风格，如视觉型、听觉型、动手实践型等
3. interests (兴趣爱好): 列出学生的兴趣领域和喜欢的学习内容
4. learning_goals (学习目标): 描述学生的学习目标和期望
5. weaknesses (薄弱环节): 指出学生的知识薄弱点和需要改进的地方
6. learning_progress (学习进度): 描述学生当前的学习进度和阶段性成果

## 输出格式
```json
{{
    "knowledge_level": {{
        "level": "初学者/中级/高级",
        "mastered_topics": [],
        "understanding_depth": ""
    }},
    "learning_style": {{
        "type": "",
        "preferences": []
    }},
    "interests": [],
    "learning_goals": [],
    "weaknesses": [],
    "learning_progress": {{
        "current_stage": "",
        "completed_topics": [],
        "next_steps": []
    }}
}}
```

只输出JSON，不要输出其他内容。
"""
        return prompt

    def process(self, input_data: Dict[str, Any], mock: bool = False) -> Dict[str, Any]:
        """
        处理输入数据，生成学生画像

        Args:
            input_data: 输入数据字典，包含对话历史
            mock: 是否使用模拟模式

        Returns:
            包含学生画像的字典
        """
        if mock:
            return self._generate_mock_profile()

        # 生成提示词
        prompt = self.generate_prompt(input_data)

        # 调用 API
        try:
            response = self._call_spark_api(prompt, temperature=0.3)
            result = self._parse_json_response(response)

            # 添加到记忆
            self.add_to_memory({
                "role": "user",
                "content": input_data.get("student_input", "")
            })
            self.add_to_memory({
                "role": "assistant",
                "content": json.dumps(result, ensure_ascii=False)
            })

            return {
                "success": True,
                "profile": result,
                "raw_response": response
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "profile": self._generate_mock_profile()["profile"]
            }

    def _generate_mock_profile(self) -> Dict[str, Any]:
        """
        生成模拟的学生画像数据

        Returns:
            模拟的学生画像字典
        """
        mock_profile = {
            "knowledge_level": {
                "level": "中级",
                "mastered_topics": ["基础语法", "数据类型", "控制流程"],
                "understanding_depth": "对基础概念有较好理解，能够独立完成简单编程任务"
            },
            "learning_style": {
                "type": "视觉型+动手实践型",
                "preferences": ["图表说明", "代码示例", "项目实践"]
            },
            "interests": ["Web开发", "人工智能", "游戏开发"],
            "learning_goals": ["掌握高级编程技巧", "完成一个完整的项目", "准备技术面试"],
            "weaknesses": ["算法思维", "系统设计", "调试技巧"],
            "learning_progress": {
                "current_stage": "进阶学习阶段",
                "completed_topics": ["Python基础", "面向对象编程", "常用库使用"],
                "next_steps": ["数据结构与算法", "Web框架学习", "数据库操作"]
            }
        }

        return {
            "success": True,
            "profile": mock_profile,
            "mock": True
        }

    def extract_profile_from_conversation(self, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        从对话历史中提取学生画像

        Args:
            conversation_history: 对话历史列表

        Returns:
            学生画像字典
        """
        input_data = {
            "conversation_history": "\n".join([
                f"{msg['role']}: {msg['content']}" for msg in conversation_history
            ]),
            "student_input": conversation_history[-1]['content'] if conversation_history else ""
        }

        return self.process(input_data)
