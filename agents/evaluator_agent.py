"""
质量评估智能体模块

评估资源质量，输出评分和改进建议。
"""

import json
from typing import Dict, Any, List
from .base_agent import BaseAgent


class EvaluatorAgent(BaseAgent):
    """
    质量评估智能体

    评估学习资源的质量，输出评分和改进建议。
    评估维度：内容质量、结构合理性、适用性、完整性、可操作性
    """

    def __init__(self, spark_api: Any = None, memory: List[Dict] = None):
        """
        初始化质量评估智能体

        Args:
            spark_api: Spark API 客户端实例
            memory: 记忆列表
        """
        super().__init__(
            name="质量评估智能体",
            role="你是一个专业的教育资源评估专家，擅长从多个维度评估学习资源的质量",
            spark_api=spark_api,
            memory=memory
        )

    def generate_prompt(self, input_data: Dict[str, Any]) -> str:
        """
        生成质量评估的提示词

        Args:
            input_data: 包含待评估资源和评估标准的字典

        Returns:
            提示词字符串
        """
        resource = input_data.get("resource", {})
        resource_type = input_data.get("resource_type", "文档")
        evaluation_criteria = input_data.get("evaluation_criteria", self._get_default_criteria())

        prompt = f"""
{self.role}

## 任务
请评估以下{resource_type}的质量，并给出评分和改进建议。

## 待评估资源
{json.dumps(resource, ensure_ascii=False, indent=2) if isinstance(resource, dict) else str(resource)}

## 评估维度
{evaluation_criteria}

## 输出要求
请输出严格的JSON格式，包含以下结构：

```json
{{
    "overall_score": 85,
    "dimension_scores": {{
        "内容质量": {{
            "score": 90,
            "comment": "内容准确、全面",
            "suggestions": ["建议1", "建议2"]
        }},
        "结构合理性": {{
            "score": 80,
            "comment": "结构清晰，但部分章节顺序可优化",
            "suggestions": ["建议1", "建议2"]
        }},
        "适用性": {{
            "score": 85,
            "comment": "适合目标学生群体",
            "suggestions": ["建议1", "建议2"]
        }},
        "完整性": {{
            "score": 80,
            "comment": "基本覆盖主要知识点",
            "suggestions": ["建议1", "建议2"]
        }},
        "可操作性": {{
            "score": 90,
            "comment": "实践指导性强",
            "suggestions": ["建议1", "建议2"]
        }}
    }},
    "strengths": ["优点1", "优点2", "优点3"],
    "weaknesses": ["不足1", "不足2"],
    "improvement_suggestions": ["改进建议1", "改进建议2", "改进建议3"],
    "summary": "总体评价总结"
}}
```

## 评分标准
- 90-100分：优秀
- 80-89分：良好
- 70-79分：中等
- 60-69分：及格
- 60分以下：需要改进

## 注意
只输出JSON，不要输出其他内容。
"""
        return prompt

    def _get_default_criteria(self) -> str:
        """
        获取默认的评估标准

        Returns:
            评估标准字符串
        """
        return """
1. 内容质量 (25%): 准确性、深度、前沿性
2. 结构合理性 (20%): 逻辑性、层次性、可读性
3. 适用性 (20%): 目标匹配度、难度适宜性
4. 完整性 (20%): 知识点覆盖、细节充实度
5. 可操作性 (15%): 实践指导、可执行性
"""

    def process(self, input_data: Dict[str, Any], mock: bool = False) -> Dict[str, Any]:
        """
        处理输入数据，评估资源质量

        Args:
            input_data: 输入数据字典
            mock: 是否使用模拟模式

        Returns:
            包含评估结果的字典
        """
        if mock:
            return self._generate_mock_evaluation(input_data)

        # 生成提示词
        prompt = self.generate_prompt(input_data)

        # 调用 API
        try:
            response = self._call_spark_api(prompt, temperature=0.3)
            result = self._parse_json_response(response)

            # 添加到记忆
            self.add_to_memory({
                "role": "user",
                "content": f"请评估{input_data.get('resource_type', '资源')}的质量"
            })
            self.add_to_memory({
                "role": "assistant",
                "content": f"评估完成，总分：{result.get('overall_score', 'N/A')}"
            })

            return {
                "success": True,
                "evaluation": result,
                "overall_score": result.get("overall_score"),
                "raw_response": response
            }
        except Exception as e:
            mock_result = self._generate_mock_evaluation(input_data)
            return {
                "success": False,
                "error": str(e),
                "evaluation": mock_result["evaluation"]
            }

    def _generate_mock_evaluation(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成模拟的评估数据

        Args:
            input_data: 输入数据字典

        Returns:
            模拟的评估字典
        """
        resource_type = input_data.get("resource_type", "文档")

        mock_evaluation = {
            "overall_score": 82,
            "dimension_scores": {
                "内容质量": {
                    "score": 85,
                    "comment": "内容准确，覆盖了主要知识点，但部分细节可以更深入",
                    "suggestions": [
                        "增加更多实际案例",
                        "补充最新的技术发展趋势"
                    ]
                },
                "结构合理性": {
                    "score": 80,
                    "comment": "整体结构清晰，章节安排合理，但部分内容顺序可以优化",
                    "suggestions": [
                        "调整第三章和第四章的顺序",
                        "增加章节之间的过渡说明"
                    ]
                },
                "适用性": {
                    "score": 88,
                    "comment": "非常适合目标学生群体，难度适中",
                    "suggestions": [
                        "增加针对不同水平学生的可选内容",
                        "提供预习和复习指导"
                    ]
                },
                "完整性": {
                    "score": 75,
                    "comment": "基本覆盖了主要知识点，但部分重要内容提及较少",
                    "suggestions": [
                        "补充高级主题的简要介绍",
                        "增加常见问题的解答部分"
                    ]
                },
                "可操作性": {
                    "score": 82,
                    "comment": "提供了实践指导，但部分步骤可以更详细",
                    "suggestions": [
                        "增加详细的代码示例",
                        "提供完整的实践项目流程"
                    ]
                }
            },
            "strengths": [
                "内容准确性高，知识点讲解清晰",
                "结构设计合理，易于学习导航",
                "适用性强，符合目标学生的学习需求"
            ],
            "weaknesses": [
                "部分高级内容深度不够",
                "缺少足够的学习评估和反馈机制",
                "实践环节的指导不够详细"
            ],
            "improvement_suggestions": [
                "增加进阶内容的深度和广度",
                "添加阶段性测试和自我评估题目",
                "提供更详细的实践项目指导和代码示例",
                "增加学习路径的个性化推荐功能",
                "补充更多真实应用场景的案例"
            ],
            "summary": f"该{resource_type}整体质量良好，内容准确、结构清晰，适合目标学生学习使用。主要优点在于内容的准确性和适用性，但在内容的深度、实践指导的详细程度方面还有提升空间。建议针对高级内容、学习评估和实践指导进行优化。"
        }

        return {
            "success": True,
            "evaluation": mock_evaluation,
            "overall_score": mock_evaluation["overall_score"],
            "mock": True
        }

    def evaluate_resource(
        self,
        resource: Any,
        resource_type: str = "文档",
        evaluation_criteria: str = None
    ) -> Dict[str, Any]:
        """
        评估资源的便捷方法

        Args:
            resource: 待评估的资源
            resource_type: 资源类型
            evaluation_criteria: 评估标准

        Returns:
            评估结果字典
        """
        input_data = {
            "resource": resource,
            "resource_type": resource_type,
            "evaluation_criteria": evaluation_criteria or self._get_default_criteria()
        }

        return self.process(input_data)

    def compare_resources(
        self,
        resources: List[Dict[str, Any]],
        resource_type: str = "文档"
    ) -> Dict[str, Any]:
        """
        比较多个资源的质量

        Args:
            resources: 待比较的资源列表
            resource_type: 资源类型

        Returns:
            比较结果字典
        """
        evaluations = []

        for i, resource in enumerate(resources):
            evaluation = self.evaluate_resource(resource, resource_type)
            evaluations.append({
                "resource_id": i,
                "evaluation": evaluation.get("evaluation")
            })

        # 生成比较报告
        comparison = {
            "resources_count": len(resources),
            "evaluations": evaluations,
            "best_resource": self._find_best_resource(evaluations),
            "comparison_summary": "比较完成"
        }

        return {
            "success": True,
            "comparison": comparison
        }

    def _find_best_resource(self, evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        找出评分最高的资源

        Args:
            evaluations: 评估列表

        Returns:
            最佳资源信息
        """
        best_score = -1
        best_id = -1

        for item in evaluations:
            evaluation = item.get("evaluation", {})
            score = evaluation.get("overall_score", 0)
            if score > best_score:
                best_score = score
                best_id = item.get("resource_id")

        return {
            "resource_id": best_id,
            "score": best_score
        }
