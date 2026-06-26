"""
文档生成器模块

调用 document_agent 生成学习文档，并保存为 Markdown 文件。

支持模拟模式：无需真实 Agent，直接生成模拟文档内容。
"""

import os
import json
import logging
from typing import Optional, Dict, List
from pathlib import Path
from datetime import datetime

from ..config import config
from ..utils.file_exporter import FileExporter
from ..utils.safety_filter import SafetyFilter, FilterResult

logger = logging.getLogger(__name__)


class DocumentAgentMock:
    """
    文档智能体模拟实现
    
    在模拟模式下替代真实的 document_agent，
    根据主题生成结构化的 Markdown 学习文档。
    """

    # 模拟文档模板库
    _TEMPLATES = {
        "default": """# {title}

> 本文档由 A3 多智能体学习系统生成  
> 生成时间: {timestamp}  
> 学科领域: {subject}

## 第一章 概述

{overview}

## 第二章 核心概念

{concepts}

## 第三章 详细讲解

{details}

## 第四章 例题分析

{examples}

## 第五章 本章小结

{summary}

## 参考资料

{references}
""",
        "math": """# {title}

> 数学学科文档  
> 生成时间: {timestamp}

## 定义

{overview}

## 基本性质

{concepts}

## 定理与证明

{details}

## 典型例题

{examples}

## 习题

{summary}
""",
        "computer": """# {title}

> 计算机学科文档  
> 生成时间: {timestamp}

## 知识点概述

{overview}

## 核心概念

{concepts}

## 代码实现

{details}

## 示例分析

{examples}

## 扩展阅读

{summary}
""",
    }

    def generate(self, topic: str, subject: str = "default", **kwargs) -> str:
        """
        模拟生成文档内容
        
        参数:
            topic: 文档主题
            subject: 学科类型（影响文档结构）
            **kwargs: 其他生成参数
        
        返回:
            生成的 Markdown 格式文档内容
        """
        template = self._TEMPLATES.get(subject, self._TEMPLATES["default"])
        
        # 根据主题和学科生成各部分内容
        overview = self._gen_overview(topic, subject)
        concepts = self._gen_concepts(topic, subject)
        details = self._gen_details(topic, subject)
        examples = self._gen_examples(topic, subject)
        summary = self._gen_summary(topic, subject)
        references = self._gen_references(topic, subject)
        
        content = template.format(
            title=topic,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            subject=subject,
            overview=overview,
            concepts=concepts,
            details=details,
            examples=examples,
            summary=summary,
            references=references,
        )
        
        return content

    def _gen_overview(self, topic: str, subject: str) -> str:
        """生成概述部分"""
        return (
            f"本章介绍 **{topic}** 的基本概念和应用场景。\n\n"
            f"{topic} 是现代{subject}领域中的重要内容，"
            "掌握其基本原理对于深入理解相关知识体系具有重要意义。\n\n"
            f"通过学习本章内容，您将了解 {topic} 的基本定义、发展历程以及主要应用场景。"
        )

    def _gen_concepts(self, topic: str, subject: str) -> str:
        """生成核心概念部分"""
        return (
            f"### 1. {topic} 的定义\n\n"
            f"{topic} 是指在特定上下文中具有特定含义的概念或方法。\n\n"
            f"### 2. {topic} 的主要特征\n\n"
            "- 特征一：具有明确的定义边界\n"
            "- 特征二：可应用于实际问题解决\n"
            "- 特征三：与其他概念存在有机联系\n\n"
            f"### 3. {topic} 的分类\n\n"
            f"根据不同的标准，{topic} 可以分为以下几类：\n\n"
            "1. 基础类型\n"
            "2. 进阶类型\n"
            "3. 综合应用类型\n"
        )

    def _gen_details(self, topic: str, subject: str) -> str:
        """生成详细讲解部分"""
        if subject == "computer":
            return (
                f"下面通过代码示例来说明 {topic} 的具体实现。\n\n"
                "```python\n"
                f"# {topic} 示例代码\n"
                "def example_function():\n"
                '    """示例函数"""\n'
                "    print('Hello, World!')\n"
                "    return True\n\n"
                "example_function()\n"
                "```\n\n"
                "上述代码展示了基本概念的实现方式。"
            )
        return (
            f"### 深入理解 {topic}\n\n"
            f"在掌握了 {topic} 的基本概念之后，我们进一步探讨其内在原理。\n\n"
            "#### 原理分析\n\n"
            f"{topic} 的核心原理可以从以下几个方面理解：\n\n"
            "1. **基础理论**：支撑该概念的基本理论框架\n"
            "2. **实现方法**：具体的实现路径和方法\n"
            "3. **优化策略**：提高效率的常用策略\n"
        )

    def _gen_examples(self, topic: str, subject: str) -> str:
        """生成例题分析部分"""
        return (
            f"### 示例 1：{topic} 的基础应用\n\n"
            "**题目描述**：给定一个具体问题，使用 {topic} 的方法进行解决。\n\n"
            "**解题思路**：首先分析问题的核心要素，然后选择合适的 {topic} 方法。\n\n"
            "**解答过程**：\n\n"
            "1. 步骤一：问题建模\n"
            "2. 步骤二：方法选择\n"
            "3. 步骤三：求解计算\n"
            "4. 步骤四：结果验证\n\n"
            "**答案**：经过上述步骤，得到最终结果为...\n"
        )

    def _gen_summary(self, topic: str, subject: str) -> str:
        """生成本章小结部分"""
        return (
            f"本章主要介绍了 **{topic}** 的基本概念、核心原理和应用方法。\n\n"
            "**重点回顾**：\n\n"
            f"- 掌握了 {topic} 的基本定义\n"
            f"- 理解了 {topic} 的核心原理\n"
            "- 学会了应用方法进行问题解决\n\n"
            "**思考题**：\n\n"
            "1. {topic} 与其他相关概念的区别是什么？\n"
            "2. 如何在实际问题中选择合适的解决方法？\n"
        )

    def _gen_references(self, topic: str, subject: str) -> str:
        """生成参考资料部分"""
        return (
            "1. 相关教材章节\n"
            "2. 在线文档和教程\n"
            "3. 学术论文（如适用）\n"
        )


class DocumentGenerator:
    """
    文档生成器
    
    负责调用 document_agent 生成学习文档，并进行安全过滤后保存为文件。
    
    属性:
        agent: 文档生成智能体实例
        exporter: 文件导出器实例
        safety_filter: 内容安全过滤器实例
        mock_mode: 是否使用模拟模式
    """

    def __init__(
        self,
        agent=None,
        output_dir: Optional[str] = None,
        mock_mode: Optional[bool] = None,
    ):
        """
        初始化文档生成器
        
        参数:
            agent: 文档生成智能体（为 None 时使用模拟 Agent）
            output_dir: 输出目录（为 None 时使用默认 exports/ 目录）
            mock_mode: 是否使用模拟模式（为 None 时读取全局配置）
        """
        self.mock_mode = mock_mode if mock_mode is not None else config.MOCK_MODE
        
        # 初始化 Agent（真实模式使用传入的 agent，模拟模式使用 Mock）
        if self.mock_mode or agent is None:
            self.agent = DocumentAgentMock()
            logger.info("文档生成器初始化完成（模拟模式）")
        else:
            self.agent = agent
            logger.info("文档生成器初始化完成（真实模式）")
        
        # 初始化导出器和安全过滤器
        self.exporter = FileExporter(output_dir)
        self.safety_filter = SafetyFilter()

    def generate(
        self,
        topic: str,
        subject: str = "default",
        filename: Optional[str] = None,
        export_formats: List[str] = None,
        **kwargs
    ) -> Dict:
        """
        生成文档并导出
        
        参数:
            topic: 文档主题
            subject: 学科领域
            filename: 导出文件名（为 None 时自动生成）
            export_formats: 导出格式列表（如 ["md", "pdf"]）
            **kwargs: 传递给 Agent 的其他参数
        
        返回:
            包含生成结果的字典：
            - success: 是否成功
            - filepath: 导出文件路径
            - content: 生成的文档内容
            - safety: 安全过滤结果
            - metadata: 元数据
        """
        # 1. 调用 Agent 生成文档内容
        logger.info(f"开始生成文档，主题: {topic}, 学科: {subject}")
        content = self.agent.generate(topic, subject, **kwargs)
        
        # 2. 内容安全过滤
        logger.info("进行内容安全过滤...")
        safety_result = self.safety_filter.filter(content, subject)
        
        if not safety_result.is_safe:
            logger.warning(
                f"内容安全检测未通过（评分: {safety_result.score}），"
                f"命中敏感词: {safety_result.matched_words}"
            )
            # 在模拟模式下，仍然继续生成，但记录警告
            if not self.mock_mode:
                return {
                    "success": False,
                    "error": "内容安全检测未通过",
                    "safety": safety_result.to_dict(),
                }
        
        # 3. 确定文件名
        if filename is None:
            # 使用主题生成安全的文件名
            safe_topic = "".join(c for c in topic if c.isalnum() or c in (" ", "-", "_")).strip()
            safe_topic = safe_topic.replace(" ", "_")[:50]  # 限制长度
            filename = f"doc_{safe_topic}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 4. 导出文件
        if export_formats is None:
            export_formats = ["md"]
        
        logger.info(f"导出文档为 {export_formats} 格式...")
        export_results = self.exporter.export(
            content=content,
            filename=filename,
            formats=export_formats,
            mock_mode=self.mock_mode,
            metadata={
                "title": topic,
                "subject": subject,
                "generated_at": datetime.now().isoformat(),
                "generator": "DocumentGenerator",
            },
        )
        
        # 5. 返回结果
        result = {
            "success": True,
            "filename": filename,
            "export_paths": {k: str(v) for k, v in export_results.items() if v is not None},
            "content": content,
            "content_length": len(content),
            "safety": safety_result.to_dict(),
            "topic": topic,
            "subject": subject,
            "generated_at": datetime.now().isoformat(),
        }
        
        logger.info(f"文档生成完成: {filename}")
        return result

    def batch_generate(
        self,
        topics: List[str],
        subject: str = "default",
        export_formats: List[str] = None,
        **kwargs
    ) -> List[Dict]:
        """
        批量生成多个主题的文档
        
        参数:
            topics: 主题列表
            subject: 学科领域
            export_formats: 导出格式列表
            **kwargs: 其他生成参数
        
        返回:
            生成结果列表
        """
        results = []
        for i, topic in enumerate(topics):
            logger.info(f"批量生成进度: {i+1}/{len(topics)} - {topic}")
            try:
                result = self.generate(
                    topic=topic,
                    subject=subject,
                    export_formats=export_formats,
                    **kwargs
                )
                results.append(result)
            except Exception as e:
                logger.error(f"生成文档失败（主题: {topic}）: {e}")
                results.append({
                    "success": False,
                    "topic": topic,
                    "error": str(e),
                })
        return results
