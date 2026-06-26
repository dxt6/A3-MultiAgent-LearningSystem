"""
资源规划智能体模块

根据学生画像和学习需求，规划学习资源和路径。
"""

import json
from typing import Dict, Any, List
from .base_agent import BaseAgent


class PlannerAgent(BaseAgent):
    """
    资源规划智能体

    根据学生画像和学习需求，规划学习资源、制定学习路径。
    """

    def __init__(self, spark_api: Any = None, memory: List[Dict] = None):
        """
        初始化资源规划智能体

        Args:
            spark_api: Spark API 客户端实例
            memory: 记忆列表
        """
        super().__init__(
            name="资源规划智能体",
            role="你是一个专业的学习路径规划师，擅长根据学生画像设计个性化的学习方案和资源配置",
            spark_api=spark_api,
            memory=memory
        )

    def generate_prompt(self, input_data: Dict[str, Any]) -> str:
        """
        生成资源规划的提示词

        Args:
            input_data: 包含学生画像和学习需求的字典

        Returns:
            提示词字符串
        """
        student_profile = input_data.get("student_profile", {})
        learning_topic = input_data.get("learning_topic", "")
        available_resources = input_data.get("available_resources", [])

        prompt = f"""
{self.role}

## 任务
根据学生的画像信息和学习需求，制定个性化的学习路径和资源规划方案。

## 输入信息
学习目标/主题：{learning_topic}

学生画像：
{json.dumps(student_profile, ensure_ascii=False, indent=2)}

可用资源：
{json.dumps(available_resources, ensure_ascii=False, indent=2) if available_resources else "根据需求自动生成合适的资源建议"}

## 输出要求
请输出严格的JSON格式，包含以下结构：

1. learning_path (学习路径): 分阶段的学习计划
2. resource_allocation (资源配置): 推荐的学习资源列表
3. time_schedule (时间安排): 每个阶段的时间安排
4. milestones (里程碑): 学习过程中的关键节点和检查点
5. assessment_methods (评估方法): 如何评估学习效果

## 输出格式
```json
{{
    "learning_path": [
        {{
            "stage": "阶段名称",
            "description": "阶段描述",
            "topics": ["知识点1", "知识点2"],
            "duration": "预计时长"
        }}
    ],
    "resource_allocation": [
        {{
            "type": "文档/视频/练习题/项目",
            "title": "资源标题",
            "description": "资源描述",
            "priority": "高/中/低",
            "estimated_time": "预计学习时间"
        }}
    ],
    "time_schedule": {{
        "total_duration": "总时长",
        "daily_commitment": "每日学习投入",
        "stages_timeline": []
    }},
    "milestones": [
        {{
            "name": "里程碑名称",
            "description": "达成标准",
            "check_method": "评估方式"
        }}
    ],
    "assessment_methods": [
        {{
            "type": "测试/项目/讨论",
            "description": "评估方法描述",
            "frequency": "频率"
        }}
    ]
}}
```

只输出JSON，不要输出其他内容。
"""
        return prompt

    def process(self, input_data: Dict[str, Any], mock: bool = False) -> Dict[str, Any]:
        """
        处理输入数据，生成学习规划

        Args:
            input_data: 输入数据字典
            mock: 是否使用模拟模式

        Returns:
            包含学习规划的字典
        """
        if mock:
            return self._generate_mock_plan()

        # 生成提示词
        prompt = self.generate_prompt(input_data)

        # 调用 API
        try:
            response = self._call_spark_api(prompt, temperature=0.5)
            result = self._parse_json_response(response)

            # 添加到记忆
            self.add_to_memory({
                "role": "user",
                "content": f"请为{input_data.get('learning_topic', '学习主题')}制定学习计划"
            })
            self.add_to_memory({
                "role": "assistant",
                "content": json.dumps(result, ensure_ascii=False)
            })

            return {
                "success": True,
                "plan": result,
                "raw_response": response
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "plan": self._generate_mock_plan()["plan"]
            }

    def _generate_mock_plan(self) -> Dict[str, Any]:
        """
        生成模拟的学习规划数据

        Returns:
            模拟的学习规划字典
        """
        mock_plan = {
            "learning_path": [
                {
                    "stage": "基础巩固阶段",
                    "description": "复习和巩固基础知识，填补知识漏洞",
                    "topics": ["基础概念", "核心语法", "常用工具"],
                    "duration": "2周"
                },
                {
                    "stage": "进阶学习阶段",
                    "description": "学习进阶知识，提升技能水平",
                    "topics": ["高级特性", "设计模式", "最佳实践"],
                    "duration": "3周"
                },
                {
                    "stage": "实战应用阶段",
                    "description": "通过项目实战应用所学知识",
                    "topics": ["项目规划", "代码实现", "测试部署"],
                    "duration": "4周"
                }
            ],
            "resource_allocation": [
                {
                    "type": "文档",
                    "title": "核心概念讲解文档",
                    "description": "详细讲解核心概念和基础知识",
                    "priority": "高",
                    "estimated_time": "3小时"
                },
                {
                    "type": "视频",
                    "title": "实战案例视频教程",
                    "description": "通过实战案例演示应用场景",
                    "priority": "高",
                    "estimated_time": "5小时"
                },
                {
                    "type": "练习题",
                    "title": "阶段性练习题库",
                    "description": "每个阶段配套的思考和实践题",
                    "priority": "中",
                    "estimated_time": "2小时"
                },
                {
                    "type": "项目",
                    "title": "综合实践项目",
                    "description": "综合运用所学知识的实践项目",
                    "priority": "高",
                    "estimated_time": "10小时"
                }
            ],
            "time_schedule": {
                "total_duration": "9周",
                "daily_commitment": "1-2小时",
                "stages_timeline": [
                    "第1-2周：基础巩固阶段",
                    "第3-5周：进阶学习阶段",
                    "第6-9周：实战应用阶段"
                ]
            },
            "milestones": [
                {
                    "name": "基础知识掌握",
                    "description": "能够熟练解释和应用基础概念",
                    "check_method": "基础知识测试（80分以上）"
                },
                {
                    "name": "进阶技能达成",
                    "description": "能够独立实现中等复杂度的功能",
                    "check_method": "编程实战测试"
                },
                {
                    "name": "综合应用能力",
                    "description": "完成综合实践项目并通过评审",
                    "check_method": "项目成果展示和代码评审"
                }
            ],
            "assessment_methods": [
                {
                    "type": "测试",
                    "description": "每个阶段结束进行知识测试",
                    "frequency": "每2周一次"
                },
                {
                    "type": "项目",
                    "description": "完成阶段性实践项目",
                    "frequency": "每个阶段一次"
                },
                {
                    "type": "讨论",
                    "description": "与导师或同学讨论学习心得",
                    "frequency": "每周一次"
                }
            ]
        }

        return {
            "success": True,
            "plan": mock_plan,
            "mock": True
        }

    def create_learning_plan(
        self,
        student_profile: Dict[str, Any],
        learning_topic: str,
        available_resources: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        创建学习计划的便捷方法

        Args:
            student_profile: 学生画像
            learning_topic: 学习主题
            available_resources: 可用资源列表

        Returns:
            学习计划字典
        """
        input_data = {
            "student_profile": student_profile,
            "learning_topic": learning_topic,
            "available_resources": available_resources or []
        }

        return self.process(input_data)
