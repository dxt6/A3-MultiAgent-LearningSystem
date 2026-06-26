"""
文档生成智能体模块

生成Markdown格式的讲解文档（1500-2000字）。
"""

import json
from typing import Dict, Any, List
from .base_agent import BaseAgent


class DocumentAgent(BaseAgent):
    """
    文档生成智能体

    根据主题和学生画像，生成Markdown格式的讲解文档。
    文档长度：1500-2000字
    """

    def __init__(self, spark_api: Any = None, memory: List[Dict] = None):
        """
        初始化文档生成智能体

        Args:
            spark_api: Spark API 客户端实例
            memory: 记忆列表
        """
        super().__init__(
            name="文档生成智能体",
            role="你是一个专业的教育内容创作者，擅长编写清晰、易懂、结构化的学习文档",
            spark_api=spark_api,
            memory=memory
        )

    def generate_prompt(self, input_data: Dict[str, Any]) -> str:
        """
        生成文档创作的提示词

        Args:
            input_data: 包含主题和学生画像的字典

        Returns:
            提示词字符串
        """
        topic = input_data.get("topic", "")
        student_profile = input_data.get("student_profile", {})
        document_type = input_data.get("document_type", "讲解文档")
        target_length = input_data.get("target_length", "1500-2000字")

        prompt = f"""
{self.role}

## 任务
请生成一篇关于"{topic}"的{document_type}。

## 要求
1. 文档格式：Markdown
2. 文档长度：{target_length}
3. 语言风格：清晰、易懂、适合学生学习
4. 结构要求：
   - 标题（# 主标题）
   - 简介（简要介绍主题）
   - 多个章节（## 章节标题）
   - 代码示例（如适用，使用代码块）
   - 重点总结
   - 参考资料（可选）

## 学生画像
{json.dumps(student_profile, ensure_ascii=False, indent=2) if student_profile else "无特定画像，适合一般水平学生"}

## 写作要点
- 根据学生的知识水平和学习风格调整内容深度和讲解方式
- 使用恰当的比喻和实例帮助理解
- 重点概念使用**加粗**标识
- 适当使用列表、表格等结构化元素
- 确保逻辑清晰，循序渐进

## 输出格式
直接输出Markdown格式的文档内容，不要包含额外的解释或说明。
"""
        return prompt

    def process(self, input_data: Dict[str, Any], mock: bool = False) -> Dict[str, Any]:
        """
        处理输入数据，生成文档

        Args:
            input_data: 输入数据字典
            mock: 是否使用模拟模式

        Returns:
            包含生成文档的字典
        """
        if mock:
            return self._generate_mock_document(input_data)

        # 生成提示词
        prompt = self.generate_prompt(input_data)

        # 调用 API
        try:
            response = self._call_spark_api(prompt, temperature=0.7)
            document_content = response.strip()

            # 添加到记忆
            self.add_to_memory({
                "role": "user",
                "content": f"请生成关于{input_data.get('topic', '主题')}的文档"
            })
            self.add_to_memory({
                "role": "assistant",
                "content": document_content[:500] + "..."  # 只保存前500字符到记忆
            })

            return {
                "success": True,
                "document": document_content,
                "topic": input_data.get("topic", ""),
                "word_count": len(document_content),
                "raw_response": response
            }
        except Exception as e:
            mock_result = self._generate_mock_document(input_data)
            return {
                "success": False,
                "error": str(e),
                "document": mock_result["document"]
            }

    def _generate_mock_document(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成模拟的文档数据

        Args:
            input_data: 输入数据字典

        Returns:
            模拟的文档字典
        """
        topic = input_data.get("topic", "Python基础")

        mock_document = f"""# {topic} 学习文档

## 简介

本文档将详细介绍{topic}的核心概念和应用方法。无论你是初学者还是有一定基础的开发者，都可以通过本文档系统地学习相关知识。

## 第一章：基础概念

### 1.1 什么是{topic}？

{topic}是一个重要的技术主题，它在现代软件开发中扮演着关键角色。理解{topic}的基本概念是掌握该技术的基础。

**核心要点：**
- 概念一：基本定义和原理
- 概念二：应用场景和价值
- 概念三：与其他技术的关联

### 1.2 为什么学习{topic}？

学习{topic}有以下几个重要原因：

1. **实用性**：{topic}在实际开发中被广泛应用
2. **基础性**：掌握{topic}有助于理解更复杂的技术
3. **职业发展**：{topic}是许多高薪职位的必备技能

## 第二章：核心内容

### 2.1 主要特性

{topic}具有以下主要特性：

- **易学易用**：语法简洁，上手快
- **功能强大**：支持多种编程范式
- **生态丰富**：有大量的第三方库和工具

### 2.2 基本语法

以下是一些基本的语法示例：

```python
# 示例代码
def example_function():
    \"\"\"这是一个示例函数\"\"\"
    print("Hello, {topic}!")
    return True
```

### 2.3 常见用法

在实际应用中，{topic}通常用于：

1. 场景一：数据处理
2. 场景二：自动化脚本
3. 场景三：Web开发

## 第三章：实践应用

### 3.1 实战案例

让我们通过一个实际的案例来加深对{topic}的理解。

**案例背景：** 假设我们需要开发一个简单的数据分析工具。

**实现步骤：**
1. 需求分析
2. 设计方案
3. 编写代码
4. 测试调试
5. 部署上线

### 3.2 最佳实践

在使用{topic}时，建议遵循以下最佳实践：

- 保持代码简洁 readable
- 注重代码复用
- 写好注释和文档
- 定期进行代码审查

## 第四章：进阶技巧

### 4.1 高级特性

对于有一定基础的开发者，可以进一步学习以下高级特性：

- 特性一：高级用法
- 特性二：性能优化
- 特性三：设计模式应用

### 4.2 常见问题与解决方案

在学习过程中，可能会遇到以下常见问题：

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 问题1 | 原因说明 | 解决方案说明 |
| 问题2 | 原因说明 | 解决方案说明 |
| 问题3 | 原因说明 | 解决方案说明 |

## 总结

通过本文档的学习，你应该已经对{topic}有了比较全面的了解。建议在学习过程中：

- 多动手实践
- 积极参与社区讨论
- 阅读优秀的开源项目代码
- 持续关注技术发展趋势

## 参考资料

1. 官方文档
2. 经典教程
3. 优质博客
4. 开源项目

---

*本文档仅供学习使用，如有问题欢迎反馈。*
"""

        return {
            "success": True,
            "document": mock_document,
            "topic": topic,
            "word_count": len(mock_document),
            "mock": True
        }

    def generate_document(
        self,
        topic: str,
        student_profile: Dict[str, Any] = None,
        document_type: str = "讲解文档"
    ) -> Dict[str, Any]:
        """
        生成文档的便捷方法

        Args:
            topic: 文档主题
            student_profile: 学生画像
            document_type: 文档类型

        Returns:
            生成的文档字典
        """
        input_data = {
            "topic": topic,
            "student_profile": student_profile or {},
            "document_type": document_type
        }

        return self.process(input_data)
