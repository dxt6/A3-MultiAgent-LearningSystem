"""
思维导图生成器模块

调用 mindmap_agent 生成思维导图数据，并保存为多种格式。

支持模拟模式：无需真实 Agent，直接生成模拟思维导图数据。
支持导出格式：JSON（通用）、Markdown（文本表示）、SVG（需要额外依赖）。
"""

import os
import json
import logging
from typing import Optional, Dict, List, Any
from pathlib import Path
from datetime import datetime
from enum import Enum

from ..config import config
from ..utils.file_exporter import FileExporter
from ..utils.safety_filter import SafetyFilter, FilterResult
from ..utils.text_utils import MarkdownHelper

logger = logging.getLogger(__name__)


class MindMapFormat(str, Enum):
    """思维导图导出格式枚举"""
    JSON = "json"       # JSON 格式（通用数据）
    MARKDOWN = "md"     # Markdown 格式（文本大纲）
    MERMaid = "mermaid"  # Mermaid 格式（可渲染为图表）
    SVG = "svg"         # SVG 矢量图（需要额外依赖）


class MindMapAgentMock:
    """
    思维导图生成智能体模拟实现
    
    在模拟模式下替代真实的 mindmap_agent，
    根据主题生成结构化的思维导图数据。
    """

    def generate(
        self,
        topic: str,
        max_depth: int = 3,
        include_details: bool = True,
        **kwargs
    ) -> Dict:
        """
        模拟生成思维导图数据
        
        参数:
            topic: 思维导图主题
            max_depth: 最大深度（层级数）
            include_details: 是否包含详细说明
            **kwargs: 其他生成参数
        
        返回:
            思维导图数据（树形结构字典）
        """
        return {
            "topic": topic,
            "root": self._gen_node(topic, depth=0, max_depth=max_depth, include_details=include_details),
            "metadata": {
                "max_depth": max_depth,
                "include_details": include_details,
                "node_count": 0,  # 将在构建后计算
            },
        }

    def _gen_node(self, label: str, depth: int, max_depth: int, include_details: bool) -> Dict:
        """
        递归生成思维导图节点
        
        参数:
            label: 节点标签
            depth: 当前深度
            max_depth: 最大深度
            include_details: 是否包含详细说明
        
        返回:
            节点字典
        """
        node = {
            "id": label,
            "label": label,
            "children": [],
        }
        
        if include_details and depth == 0:
            node["details"] = f"关于 {label} 的详细思维导图"
        
        # 如果未达到最大深度，生成子节点
        if depth < max_depth:
            children_labels = self._get_children_labels(label, depth)
            for child_label in children_labels:
                child_node = self._gen_node(
                    label=child_label,
                    depth=depth + 1,
                    max_depth=max_depth,
                    include_details=include_details,
                )
                node["children"].append(child_node)
        
        return node

    def _get_children_labels(self, parent_label: str, depth: int) -> List[str]:
        """
        根据父节点标签生成子节点标签
        
        参数:
            parent_label: 父节点标签
            depth: 当前深度
        
        返回:
            子节点标签列表
        """
        # 根节点的子节点（一级主题）
        if depth == 0:
            return ["基本概念", "核心原理", "应用场景", "实例分析", "扩展阅读"]
        
        # 二级节点的子节点
        if depth == 1:
            if parent_label == "基本概念":
                return ["定义", "特点", "分类"]
            elif parent_label == "核心原理":
                return ["理论基础", "运行机制", "关键算法"]
            elif parent_label == "应用场景":
                return ["实际应用", "案例分析", "效果评估"]
            elif parent_label == "实例分析":
                return ["示例一", "示例二", "示例三"]
            elif parent_label == "扩展阅读":
                return ["相关文献", "进阶内容", "研究前沿"]
        
        # 三级节点的子节点（更深层级的内容）
        if depth == 2:
            return [f"{parent_label} - 要点1", f"{parent_label} - 要点2"]
        
        return []

    @staticmethod
    def count_nodes(mindmap_data: Dict) -> int:
        """计算思维导图的节点总数"""
        def _count(node: Dict) -> int:
            count = 1
            for child in node.get("children", []):
                count += _count(child)
            return count
        
        return _count(mindmap_data["root"])


class MindMapGenerator:
    """
    思维导图生成器
    
    负责调用 mindmap_agent 生成思维导图，并导出为多种格式。
    
    属性:
        agent: 思维导图生成智能体实例
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
        初始化思维导图生成器
        
        参数:
            agent: 思维导图生成智能体
            output_dir: 输出目录
            mock_mode: 是否使用模拟模式
        """
        self.mock_mode = mock_mode if mock_mode is not None else config.MOCK_MODE
        
        if self.mock_mode or agent is None:
            self.agent = MindMapAgentMock()
            logger.info("思维导图生成器初始化完成（模拟模式）")
        else:
            self.agent = agent
            logger.info("思维导图生成器初始化完成（真实模式）")
        
        self.exporter = FileExporter(output_dir)
        self.safety_filter = SafetyFilter()

    def generate(
        self,
        topic: str,
        max_depth: int = 3,
        include_details: bool = True,
        filename: Optional[str] = None,
        export_formats: List[str] = None,
        **kwargs
    ) -> Dict:
        """
        生成思维导图并导出
        
        参数:
            topic: 思维导图主题
            max_depth: 最大层级深度
            include_details: 是否包含详细说明
            filename: 导出文件名
            export_formats: 导出格式列表（["json", "md", "mermaid"]）
            **kwargs: 传递给 Agent 的其他参数
        
        返回:
            包含生成结果的字典
        """
        # 1. 调用 Agent 生成思维导图数据
        logger.info(f"开始生成思维导图，主题: {topic}, 最大深度: {max_depth}")
        mindmap_data = self.agent.generate(
            topic=topic,
            max_depth=max_depth,
            include_details=include_details,
            **kwargs
        )
        
        # 计算节点数
        node_count = MindMapAgentMock.count_nodes(mindmap_data)
        mindmap_data["metadata"]["node_count"] = node_count
        logger.info(f"思维导图生成完成，共 {node_count} 个节点")
        
        # 2. 内容安全过滤
        logger.info("进行内容安全过滤...")
        all_text = self._extract_text_from_mindmap(mindmap_data["root"])
        safety_result = self.safety_filter.filter(all_text, topic)
        
        if not safety_result.is_safe and not self.mock_mode:
            return {
                "success": False,
                "error": "思维导图内容安全检测未通过",
                "safety": safety_result.to_dict(),
            }
        
        # 3. 确定文件名
        if filename is None:
            safe_topic = "".join(c for c in topic if c.isalnum() or c in (" ", "-", "_")).strip()
            safe_topic = safe_topic.replace(" ", "_")[:50]
            filename = f"mindmap_{safe_topic}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 4. 导出为多种格式
        if export_formats is None:
            export_formats = ["json", "md"]
        
        export_results = {}
        
        for fmt in export_formats:
            fmt = fmt.lower().strip()
            try:
                if fmt == "json":
                    result = self.exporter.export(
                        content="",
                        filename=filename,
                        formats=["json"],
                        mock_mode=self.mock_mode,
                        data=mindmap_data,
                    )
                    export_results["json"] = result.get("json")
                
                elif fmt == "md":
                    md_content = self._to_markdown(mindmap_data["root"])
                    result = self.exporter.export(
                        content=md_content,
                        filename=f"{filename}_outline",
                        formats=["md"],
                        mock_mode=self.mock_mode,
                    )
                    export_results["md"] = result.get("md")
                
                elif fmt == "mermaid":
                    mermaid_code = self._to_mermaid(mindmap_data["root"], topic)
                    result = self.exporter.export(
                        content=mermaid_code,
                        filename=f"{filename}_mermaid",
                        formats=["md"],
                        mock_mode=self.mock_mode,
                        metadata={"format": "mermaid"},
                    )
                    export_results["mermaid"] = result.get("md")
                
                elif fmt == "svg":
                    # SVG 导出需要额外处理
                    logger.warning("SVG 导出需要额外依赖，当前生成 Mermaid 代码替代")
                    mermaid_code = self._to_mermaid(mindmap_data["root"], topic)
                    export_results["svg_placeholder"] = mermaid_code
                
                else:
                    logger.warning(f"不支持的导出格式: {fmt}")
            
            except Exception as e:
                logger.error(f"导出格式 {fmt} 失败: {e}")
                export_results[fmt] = None
        
        # 5. 返回结果
        result = {
            "success": True,
            "filename": filename,
            "export_paths": {k: str(v) for k, v in export_results.items() if v is not None},
            "node_count": node_count,
            "max_depth": max_depth,
            "mindmap_data": mindmap_data,
            "safety": safety_result.to_dict(),
            "topic": topic,
            "generated_at": datetime.now().isoformat(),
        }
        
        logger.info(f"思维导图生成完成: {filename}")
        return result

    def _extract_text_from_mindmap(self, node: Dict) -> str:
        """
        从思维导图中提取所有文本内容（用于安全过滤）
        
        参数:
            node: 思维导图节点
        
        返回:
            所有节点标签和详情的拼接文本
        """
        text = node.get("label", "") + " "
        if "details" in node:
            text += node["details"] + " "
        for child in node.get("children", []):
            text += self._extract_text_from_mindmap(child)
        return text

    def _to_markdown(self, node: Dict, level: int = 1) -> str:
        """
        将思维导图转换为 Markdown 大纲格式
        
        参数:
            node: 思维导图节点
            level: 当前层级
        
        返回:
            Markdown 格式的大纲文本
        """
        lines = []
        
        # 添加当前节点
        indent = "  " * (level - 1)
        lines.append(f"{indent}- **{node['label']}**")
        
        if "details" in node:
            lines.append(f"{indent}  > {node['details']}")
        
        # 递归处理子节点
        for child in node.get("children", []):
            child_md = self._to_markdown(child, level + 1)
            # 调整子节点的缩进
            for line in child_md.split("\n"):
                lines.append(line)
        
        return "\n".join(lines)

    def _to_mermaid(self, node: Dict, title: str) -> str:
        """
        将思维导图转换为 Mermaid 格式（可渲染为图表）
        
        参数:
            node: 思维导图根节点
            title: 图表标题
        
        返回:
            Mermaid 格式的文本
        """
        lines = ["```mermaid", "mindmap", f"  root(({title}))"]
        
        def _add_children(parent_id: str, children: List[Dict], indent: int = 2):
            for child in children:
                prefix = "  " * indent
                lines.append(f"{prefix}{child['label']}")
                if child.get("children"):
                    _add_children(child["id"], child["children"], indent + 1)
        
        _add_children("root", node.get("children", []))
        lines.append("```")
        
        return "\n".join(lines)

    def visualize(self, mindmap_data: Dict, output_path: Optional[str] = None) -> str:
        """
        生成思维导图的文本可视化（用于控制台打印）
        
        参数:
            mindmap_data: 思维导图数据
            output_path: 可选，保存到文件路径
        
        返回:
            文本可视化字符串
        """
        lines = [f"思维导图: {mindmap_data['topic']}", "=" * 50]
        
        def _print_node(node: Dict, prefix: str = "", is_last: bool = True):
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{node['label']}")
            
            children = node.get("children", [])
            for i, child in enumerate(children):
                child_prefix = prefix + ("    " if is_last else "│   ")
                _print_node(child, child_prefix, i == len(children) - 1)
        
        _print_node(mindmap_data["root"])
        
        result = "\n".join(lines)
        
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result)
        
        return result
