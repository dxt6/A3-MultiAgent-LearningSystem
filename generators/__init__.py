"""
生成器模块初始化

提供以下生成器：
1. DocumentGenerator  - 文档生成器（调用 document_agent 生成文档）
2. QuizGenerator      - 题目生成器（调用 quiz_agent 生成题目）
3. MindMapGenerator   - 思维导图生成器（调用 mindmap_agent 生成思维导图）
4. PathPlanner        - 学习路径规划器（根据学生画像规划学习路径）

所有生成器均支持模拟模式。
"""

from .document_gen import DocumentGenerator
from .quiz_gen import QuizGenerator
from .mindmap_gen import MindMapGenerator
from .path_planner import PathPlanner

__all__ = [
    "DocumentGenerator",
    "QuizGenerator",
    "MindMapGenerator",
    "PathPlanner",
]
