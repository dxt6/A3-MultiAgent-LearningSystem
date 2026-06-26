"""
题目生成智能体模块

生成练习题（JSON格式，包含题目、选项、答案、解析）。
"""

import json
from typing import Dict, Any, List
from .base_agent import BaseAgent


class QuizAgent(BaseAgent):
    """
    题目生成智能体

    根据主题和学生水平，生成练习题。
    输出JSON格式，包含题目、选项、答案、解析。
    """

    def __init__(self, spark_api: Any = None, memory: List[Dict] = None):
        """
        初始化题目生成智能体

        Args:
            spark_api: Spark API 客户端实例
            memory: 记忆列表
        """
        super().__init__(
            name="题目生成智能体",
            role="你是一个专业的题库编写专家，擅长根据知识点生成高质量的练习题",
            spark_api=spark_api,
            memory=memory
        )

    def generate_prompt(self, input_data: Dict[str, Any]) -> str:
        """
        生成题目创作的提示词

        Args:
            input_data: 包含主题和题目要求的字典

        Returns:
            提示词字符串
        """
        topic = input_data.get("topic", "")
        difficulty = input_data.get("difficulty", "中等")
        num_questions = input_data.get("num_questions", 5)
        question_types = input_data.get("question_types", ["选择题", "判断题", "简答题"])
        student_level = input_data.get("student_level", "中级")

        prompt = f"""
{self.role}

## 任务
请生成关于"{topic}"的练习题。

## 要求
1. 题目数量：{num_questions} 道
2. 难度等级：{difficulty}（简单/中等/困难）
3. 学生水平：{student_level}
4. 题目类型：{', '.join(question_types)}
5. 输出格式：严格的JSON格式

## 输出格式要求
请输出严格的JSON格式，包含以下结构：

```json
{{
    "topic": "{topic}",
    "difficulty": "{difficulty}",
    "questions": [
        {{
            "id": 1,
            "type": "选择题",
            "question": "题目内容",
            "options": ["A. 选项A", "B. 选项B", "C. 选项C", "D. 选项D"],
            "correct_answer": "A",
            "explanation": "详细解析",
            "tags": ["知识点标签"]
        }},
        {{
            "id": 2,
            "type": "判断题",
            "question": "题目内容",
            "correct_answer": true,
            "explanation": "详细解析",
            "tags": ["知识点标签"]
        }},
        {{
            "id": 3,
            "type": "简答题",
            "question": "题目内容",
            "reference_answer": "参考答案",
            "explanation": "详细解析",
            "tags": ["知识点标签"]
        }}
    ]
}}
```

## 题目质量要求
- 题目表述清晰、准确
- 选项设计合理（选择题）
- 答案正确无误
- 解析详细、易懂
- 难度符合指定等级
- 覆盖主要知识点

## 注意
只输出JSON，不要输出其他内容。
"""
        return prompt

    def process(self, input_data: Dict[str, Any], mock: bool = False) -> Dict[str, Any]:
        """
        处理输入数据，生成题目

        Args:
            input_data: 输入数据字典
            mock: 是否使用模拟模式

        Returns:
            包含生成题目的字典
        """
        if mock:
            return self._generate_mock_quiz(input_data)

        # 生成提示词
        prompt = self.generate_prompt(input_data)

        # 调用 API
        try:
            response = self._call_spark_api(prompt, temperature=0.5)
            result = self._parse_json_response(response)

            # 添加到记忆
            self.add_to_memory({
                "role": "user",
                "content": f"请生成关于{input_data.get('topic', '主题')}的练习题"
            })
            self.add_to_memory({
                "role": "assistant",
                "content": f"已生成{len(result.get('questions', []))}道练习题"
            })

            return {
                "success": True,
                "quiz": result,
                "question_count": len(result.get("questions", [])),
                "raw_response": response
            }
        except Exception as e:
            mock_result = self._generate_mock_quiz(input_data)
            return {
                "success": False,
                "error": str(e),
                "quiz": mock_result["quiz"]
            }

    def _generate_mock_quiz(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成模拟的题目数据

        Args:
            input_data: 输入数据字典

        Returns:
            模拟的题目字典
        """
        topic = input_data.get("topic", "Python基础")
        num_questions = input_data.get("num_questions", 5)
        difficulty = input_data.get("difficulty", "中等")

        # 根据题目数量生成模拟题目
        questions = []

        for i in range(1, min(num_questions + 1, 6)):  # 最多生成5道题的模拟数据
            if i <= 2:
                # 选择题
                question = {
                    "id": i,
                    "type": "选择题",
                    "question": f"关于{topic}，以下说法正确的是？",
                    "options": [
                        f"A. {topic}主要用于数据分析",
                        f"B. {topic}支持面向对象编程",
                        f"C. {topic}不能用于Web开发",
                        f"D. {topic}是一种编译型语言"
                    ],
                    "correct_answer": "B",
                    "explanation": f"{topic}确实支持面向对象编程。选项A、C、D的描述不准确。{topic}是一个功能丰富的技术主题，适用于多种应用场景。",
                    "tags": [topic, "基础概念", "特性"]
                }
            elif i == 3:
                # 判断题
                question = {
                    "id": i,
                    "type": "判断题",
                    "question": f"{topic}的学习不需要任何编程基础。",
                    "correct_answer": False,
                    "explanation": f"虽然{topic}相对易学，但具备一定的编程基础会更有助于理解其核心概念和应用场景。",
                    "tags": [topic, "学习要求"]
                }
            else:
                # 简答题
                question = {
                    "id": i,
                    "type": "简答题",
                    "question": f"请简述{topic}的主要应用场景。",
                    "reference_answer": f"{topic}的主要应用场景包括：1. 数据分析与处理；2. Web开发；3. 自动化脚本编写；4. 人工智能与机器学习；5. 科学计算。",
                    "explanation": f"回答时应涵盖{topic}的主要应用领域，并简要说明每个场景的特点。",
                    "tags": [topic, "应用场景", "综合理解"]
                }

            questions.append(question)

        mock_quiz = {
            "topic": topic,
            "difficulty": difficulty,
            "questions": questions
        }

        return {
            "success": True,
            "quiz": mock_quiz,
            "question_count": len(questions),
            "mock": True
        }

    def generate_quiz(
        self,
        topic: str,
        difficulty: str = "中等",
        num_questions: int = 5,
        question_types: List[str] = None
    ) -> Dict[str, Any]:
        """
        生成题目的便捷方法

        Args:
            topic: 题目主题
            difficulty: 难度等级
            num_questions: 题目数量
            question_types: 题目类型列表

        Returns:
            生成的题目字典
        """
        input_data = {
            "topic": topic,
            "difficulty": difficulty,
            "num_questions": num_questions,
            "question_types": question_types or ["选择题", "判断题", "简答题"],
            "student_level": "中级"
        }

        return self.process(input_data)

    def evaluate_answer(
        self,
        question: Dict[str, Any],
        user_answer: Any
    ) -> Dict[str, Any]:
        """
        评估用户的答案

        Args:
            question: 题目信息
            user_answer: 用户答案

        Returns:
            评估结果字典
        """
        question_type = question.get("type", "")

        if question_type == "选择题":
            is_correct = user_answer == question.get("correct_answer")
        elif question_type == "判断题":
            is_correct = user_answer == question.get("correct_answer")
        else:  # 简答题
            # 简答题需要更复杂的评估逻辑，这里简单处理
            is_correct = len(user_answer) > 10  # 假设答案长度大于10就算正确

        return {
            "question_id": question.get("id"),
            "question_type": question_type,
            "user_answer": user_answer,
            "correct_answer": question.get("correct_answer") or question.get("reference_answer"),
            "is_correct": is_correct,
            "explanation": question.get("explanation", "")
        }
