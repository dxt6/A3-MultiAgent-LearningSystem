"""
思维导图智能体模块

生成知识图谱数据（nodes和edges）。
"""

import json
from typing import Dict, Any, List
from .base_agent import BaseAgent


class MindMapAgent(BaseAgent):
    """
    思维导图智能体

    根据主题生成知识图谱数据，包含nodes（节点）和edges（边）。
    """

    def __init__(self, spark_api: Any = None, memory: List[Dict] = None):
        """
        初始化思维导图智能体

        Args:
            spark_api: Spark API 客户端实例
            memory: 记忆列表
        """
        super().__init__(
            name="思维导图智能体",
            role="你是一个知识图谱构建专家，擅长将知识点组织成结构化的思维导图",
            spark_api=spark_api,
            memory=memory
        )

    def generate_prompt(self, input_data: Dict[str, Any]) -> str:
        """
        生成思维导图创建的提示词

        Args:
            input_data: 包含主题和要求的字典

        Returns:
            提示词字符串
        """
        topic = input_data.get("topic", "")
        depth = input_data.get("depth", 3)
        include_details = input_data.get("include_details", True)

        prompt = f"""
{self.role}

## 任务
请为"{topic}"创建一个知识图谱（思维导图）。

## 要求
1. 主题：{topic}
2. 图谱深度：{depth} 层（从中心主题向外展开）
3. 包含详细信息：{"是" if include_details else "否"}
4. 输出格式：严格的JSON格式

## 输出格式要求
请输出严格的JSON格式，包含 nodes 和 edges 两个数组：

```json
{{
    "topic": "{topic}",
    "nodes": [
        {{
            "id": "node_1",
            "label": "节点名称",
            "type": "核心概念/主要分支/子主题",
            "description": "节点描述（可选）",
            "level": 0
        }}
    ],
    "edges": [
        {{
            "source": "node_1",
            "target": "node_2",
            "relation": "包含/依赖/相关"
        }}
    ]
}}
```

## 节点类型说明
- 核心概念 (level 0): 中心主题
- 主要分支 (level 1): 一级子主题
- 子主题 (level 2+): 更细分的主题

## 图谱质量要求
- 结构清晰，层次分明
- 覆盖主要知识点
- 节点之间的关系合理
- 适合用于学习导航

## 注意
只输出JSON，不要输出其他内容。
"""
        return prompt

    def process(self, input_data: Dict[str, Any], mock: bool = False) -> Dict[str, Any]:
        """
        处理输入数据，生成知识图谱

        Args:
            input_data: 输入数据字典
            mock: 是否使用模拟模式

        Returns:
            包含知识图谱的字典
        """
        if mock:
            return self._generate_mock_mindmap(input_data)

        # 生成提示词
        prompt = self.generate_prompt(input_data)

        # 调用 API
        try:
            response = self._call_spark_api(prompt, temperature=0.5)
            result = self._parse_json_response(response)

            # 添加到记忆
            self.add_to_memory({
                "role": "user",
                "content": f"请为{input_data.get('topic', '主题')}创建知识图谱"
            })
            self.add_to_memory({
                "role": "assistant",
                "content": f"已生成知识图谱，包含{len(result.get('nodes', []))}个节点和{len(result.get('edges', []))}条边"
            })

            return {
                "success": True,
                "mindmap": result,
                "node_count": len(result.get("nodes", [])),
                "edge_count": len(result.get("edges", [])),
                "raw_response": response
            }
        except Exception as e:
            mock_result = self._generate_mock_mindmap(input_data)
            return {
                "success": False,
                "error": str(e),
                "mindmap": mock_result["mindmap"]
            }

    def _generate_mock_mindmap(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成模拟的知识图谱数据

        Args:
            input_data: 输入数据字典

        Returns:
            模拟的知识图谱字典
        """
        topic = input_data.get("topic", "Python编程")

        mock_mindmap = {
            "topic": topic,
            "nodes": [
                {
                    "id": "node_0",
                    "label": topic,
                    "type": "核心概念",
                    "description": f"{topic}的完整知识体系",
                    "level": 0
                },
                {
                    "id": "node_1",
                    "label": "基础语法",
                    "type": "主要分支",
                    "description": "编程语言的基础语法规则",
                    "level": 1
                },
                {
                    "id": "node_2",
                    "label": "数据结构",
                    "type": "主要分支",
                    "description": "常用的数据结构类型",
                    "level": 1
                },
                {
                    "id": "node_3",
                    "label": "面向对象",
                    "type": "主要分支",
                    "description": "面向对象编程概念",
                    "level": 1
                },
                {
                    "id": "node_4",
                    "label": "标准库",
                    "type": "主要分支",
                    "description": "常用的标准库模块",
                    "level": 1
                },
                {
                    "id": "node_5",
                    "label": "变量与数据类型",
                    "type": "子主题",
                    "description": "变量的定义和各种数据类型",
                    "level": 2
                },
                {
                    "id": "node_6",
                    "label": "控制流程",
                    "type": "子主题",
                    "description": "条件判断和循环控制",
                    "level": 2
                },
                {
                    "id": "node_7",
                    "label": "函数",
                    "type": "子主题",
                    "description": "函数的定义和调用",
                    "level": 2
                },
                {
                    "id": "node_8",
                    "label": "列表",
                    "type": "子主题",
                    "description": "列表的创建和操作",
                    "level": 2
                },
                {
                    "id": "node_9",
                    "label": "字典",
                    "type": "子主题",
                    "description": "字典的创建和操作",
                    "level": 2
                },
                {
                    "id": "node_10",
                    "label": "类与对象",
                    "type": "子主题",
                    "description": "类的定义和对象的创建",
                    "level": 2
                }
            ],
            "edges": [
                {
                    "source": "node_0",
                    "target": "node_1",
                    "relation": "包含"
                },
                {
                    "source": "node_0",
                    "target": "node_2",
                    "relation": "包含"
                },
                {
                    "source": "node_0",
                    "target": "node_3",
                    "relation": "包含"
                },
                {
                    "source": "node_0",
                    "target": "node_4",
                    "relation": "包含"
                },
                {
                    "source": "node_1",
                    "target": "node_5",
                    "relation": "包含"
                },
                {
                    "source": "node_1",
                    "target": "node_6",
                    "relation": "包含"
                },
                {
                    "source": "node_1",
                    "target": "node_7",
                    "relation": "包含"
                },
                {
                    "source": "node_2",
                    "target": "node_8",
                    "relation": "包含"
                },
                {
                    "source": "node_2",
                    "target": "node_9",
                    "relation": "包含"
                },
                {
                    "source": "node_3",
                    "target": "node_10",
                    "relation": "包含"
                }
            ]
        }

        return {
            "success": True,
            "mindmap": mock_mindmap,
            "node_count": len(mock_mindmap["nodes"]),
            "edge_count": len(mock_mindmap["edges"]),
            "mock": True
        }

    def generate_mindmap(
        self,
        topic: str,
        depth: int = 3,
        include_details: bool = True
    ) -> Dict[str, Any]:
        """
        生成思维导图的便捷方法

        Args:
            topic: 主题
            depth: 图谱深度
            include_details: 是否包含详细信息

        Returns:
            生成的知识图谱字典
        """
        input_data = {
            "topic": topic,
            "depth": depth,
            "include_details": include_details
        }

        return self.process(input_data)

    def export_to_d3_format(self, mindmap_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        将知识图谱转换为D3.js可用的格式

        Args:
            mindmap_data: 知识图谱数据

        Returns:
            D3.js格式的字典
        """
        nodes = mindmap_data.get("nodes", [])
        edges = mindmap_data.get("edges", [])

        # 转换为D3格式
        d3_nodes = [{"id": node["id"], "name": node["label"], "group": node["level"]} for node in nodes]
        d3_links = [{"source": edge["source"], "target": edge["target"], "value": 1} for edge in edges]

        return {
            "nodes": d3_nodes,
            "links": d3_links
        }
