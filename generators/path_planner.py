"""
学习路径规划器模块

根据学生画像（知识水平、学习目标、学习偏好等）规划个性化的学习路径。

无需调用外部 Agent，基于规则和知识图谱进行规划。
支持模拟模式：使用模拟的学生画像和课程内容进行演示。
"""

import os
import json
import logging
from typing import Optional, Dict, List, Any
from pathlib import Path
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


class ProficiencyLevel(str, Enum):
    """熟练度等级枚举"""
    BEGINNER = "beginner"       # 入门
    ELEMENTARY = "elementary"   # 初级
    INTERMEDIATE = "intermediate"  # 中级
    ADVANCED = "advanced"      # 高级
    EXPERT = "expert"           # 专家


class LearningGoal(str, Enum):
    """学习目标枚举"""
    FOUNDATION = "foundation"   # 打基础
    EXAM = "exam"               # 备考
    PROJECT = "project"         # 做项目
    CAREER = "career"           # 职业发展
    HOBBY = "hobby"             # 兴趣学习


@dataclass
class StudentProfile:
    """
    学生画像数据类
    
    属性:
        student_id: 学生ID
        name: 学生姓名
        subject: 学习科目
        proficiency: 当前熟练度等级
        goal: 学习目标
        available_hours_per_week: 每周可学习小时数
        strengths: 优势知识点列表
        weaknesses: 薄弱知识点列表
        learning_style: 学习风格（visual/auditory/kinesthetic）
        deadline: 目标截止日期（可选）
    """
    student_id: str
    name: str
    subject: str
    proficiency: ProficiencyLevel
    goal: LearningGoal
    available_hours_per_week: int = 10
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    learning_style: str = "visual"
    deadline: Optional[datetime] = None

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "subject": self.subject,
            "proficiency": self.proficiency.value,
            "goal": self.goal.value,
            "available_hours_per_week": self.available_hours_per_week,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "learning_style": self.learning_style,
            "deadline": self.deadline.isoformat() if self.deadline else None,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "StudentProfile":
        """从字典创建学生画像"""
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            subject=data["subject"],
            proficiency=ProficiencyLevel(data["proficiency"]),
            goal=LearningGoal(data["goal"]),
            available_hours_per_week=data.get("available_hours_per_week", 10),
            strengths=data.get("strengths", []),
            weaknesses=data.get("weaknesses", []),
            learning_style=data.get("learning_style", "visual"),
            deadline=datetime.fromisoformat(data["deadline"]) if data.get("deadline") else None,
        )


@dataclass
class LearningNode:
    """
    学习节点数据类（知识图谱中的节点）
    
    属性:
        id: 节点唯一标识
        name: 节点名称（知识点名称）
        description: 知识点描述
        level: 难度等级（1-5）
        estimated_hours: 预计学习时长（小时）
        prerequisites: 前置知识点ID列表
        resources: 学习资源列表
    """
    id: str
    name: str
    description: str
    level: int = 1
    estimated_hours: int = 2
    prerequisites: List[str] = field(default_factory=list)
    resources: List[Dict] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "level": self.level,
            "estimated_hours": self.estimated_hours,
            "prerequisites": self.prerequisites,
            "resources": self.resources,
        }


@dataclass
class LearningPath:
    """
    学习路径数据类
    
    属性:
        path_id: 路径唯一标识
        student_id: 对应的学生ID
        nodes: 按顺序排列的学习节点列表
        total_hours: 总预计学习时长
        estimated_completion_date: 预计完成日期
        created_at: 路径创建时间
    """
    path_id: str
    student_id: str
    nodes: List[LearningNode]
    total_hours: int = 0
    estimated_completion_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        return {
            "path_id": self.path_id,
            "student_id": self.student_id,
            "nodes": [n.to_dict() for n in self.nodes],
            "total_hours": self.total_hours,
            "estimated_completion_date": (
                self.estimated_completion_date.isoformat()
                if self.estimated_completion_date else None
            ),
            "created_at": self.created_at.isoformat(),
            "num_nodes": len(self.nodes),
        }


class KnowledgeGraph:
    """
    知识图谱
    
    存储知识点之间的依赖关系，用于路径规划。
    在模拟模式下使用内置的示例知识图谱。
    """

    def __init__(self, subject: str = "default"):
        """
        初始化知识图谱
        
        参数:
            subject: 学科名称，用于加载对应的知识图谱
        """
        self.subject = subject
        self.nodes: Dict[str, LearningNode] = {}
        self._load_knowledge_graph(subject)

    def _load_knowledge_graph(self, subject: str):
        """加载知识图谱（模拟数据）"""
        if subject == "数学":
            self._load_math_graph()
        elif subject in ("计算机", "编程", "Python"):
            self._load_computer_graph()
        else:
            self._load_default_graph()

    def _load_math_graph(self):
        """加载数学知识图谱"""
        nodes_data = [
            ("math_basic", "数学基础", "数与运算、代数式基础", 1, 4, []),
            ("equation", "方程与不等式", "一元一次方程、一元二次方程", 2, 6, ["math_basic"]),
            ("function", "函数基础", "函数概念、一次函数、二次函数", 2, 8, ["math_basic"]),
            ("trig", "三角函数", "正弦、余弦、正切", 3, 8, ["function"]),
            ("calculus", "微积分初步", "导数与积分基础", 4, 12, ["function", "trig"]),
            ("probability", "概率统计", "概率基础、统计方法", 3, 8, ["math_basic"]),
        ]
        for nid, name, desc, level, hours, prereqs in nodes_data:
            self.nodes[nid] = LearningNode(
                id=nid, name=name, description=desc,
                level=level, estimated_hours=hours, prerequisites=prereqs,
            )

    def _load_computer_graph(self):
        """加载计算机知识图谱"""
        nodes_data = [
            ("cs_basic", "计算机基础", "计算机组成、操作系统基础", 1, 4, []),
            ("programming_basic", "编程基础", "变量、控制结构、函数", 1, 8, ["cs_basic"]),
            ("data_structure", "数据结构", "数组、链表、树、图", 3, 12, ["programming_basic"]),
            ("algorithm", "算法基础", "排序、查找、递归", 3, 10, ["data_structure"]),
            ("database", "数据库基础", "SQL、关系模型", 2, 6, ["programming_basic"]),
            ("web_basic", "Web开发基础", "HTML、CSS、JavaScript", 2, 8, ["programming_basic"]),
            ("ml_basic", "机器学习基础", "监督学习、无监督学习", 4, 15, ["algorithm", "data_structure"]),
        ]
        for nid, name, desc, level, hours, prereqs in nodes_data:
            self.nodes[nid] = LearningNode(
                id=nid, name=name, description=desc,
                level=level, estimated_hours=hours, prerequisites=prereqs,
            )

    def _load_default_graph(self):
        """加载默认知识图谱"""
        nodes_data = [
            ("intro", "入门介绍", "基础概念和背景", 1, 2, []),
            ("basic_concept", "基本概念", "核心定义和基础原理", 1, 4, ["intro"]),
            ("core_tech", "核心技术", "主要技术和方法", 2, 6, ["basic_concept"]),
            ("advanced", "进阶内容", "高级主题和深入讨论", 3, 8, ["core_tech"]),
            ("practice", "实践应用", "实际案例和项目", 2, 6, ["basic_concept"]),
            ("summary", "总结复习", "知识梳理和综合练习", 2, 4, ["core_tech", "practice"]),
        ]
        for nid, name, desc, level, hours, prereqs in nodes_data:
            self.nodes[nid] = LearningNode(
                id=nid, name=name, description=desc,
                level=level, estimated_hours=hours, prerequisites=prereqs,
            )

    def get_node(self, node_id: str) -> Optional[LearningNode]:
        """获取指定节点"""
        return self.nodes.get(node_id)

    def get_prerequisites(self, node_id: str) -> List[LearningNode]:
        """获取节点的前置节点"""
        node = self.nodes.get(node_id)
        if not node:
            return []
        return [self.nodes[pid] for pid in node.prerequisites if pid in self.nodes]

    def get_all_nodes(self) -> List[LearningNode]:
        """获取所有节点"""
        return list(self.nodes.values())


class PathPlanner:
    """
    学习路径规划器
    
    根据学生画像和知识图谱，规划最优学习路径。
    
    属性:
        knowledge_graph: 知识图谱实例
        mock_mode: 是否使用模拟模式
    """

    def __init__(
        self,
        subject: str = "default",
        mock_mode: Optional[bool] = None,
    ):
        """
        初始化路径规划器
        
        参数:
            subject: 学科名称
            mock_mode: 是否使用模拟模式
        """
        self.mock_mode = mock_mode if mock_mode is not None else True
        self.knowledge_graph = KnowledgeGraph(subject)
        logger.info(f"路径规划器初始化完成，学科: {subject}")

    def plan(
        self,
        student_profile: StudentProfile,
        target_nodes: Optional[List[str]] = None,
        **kwargs
    ) -> LearningPath:
        """
        规划学习路径
        
        参数:
            student_profile: 学生画像
            target_nodes: 目标知识点ID列表（为 None 时根据画像自动确定）
            **kwargs: 其他规划参数
        
        返回:
            规划好的学习路径
        
        算法说明：
            1. 根据学生熟练度确定起点
            2. 根据学习目标确定终点
            3. 使用拓扑排序保证前置依赖
            4. 根据薄弱点调整优先级
        """
        logger.info(f"开始为学生学习路径，学生: {student_profile.name}")
        
        # 1. 确定需要学习的节点范围
        if target_nodes is None:
            target_nodes = self._determine_target_nodes(student_profile)
        
        # 2. 根据学生熟练度过滤已掌握的知识点
        nodes_to_learn = self._filter_by_proficiency(
            target_nodes, student_profile.proficiency
        )
        
        # 3. 拓扑排序（保证前置依赖）
        sorted_nodes = self._topological_sort(nodes_to_learn)
        
        # 4. 根据薄弱点调整顺序（薄弱点提前）
        sorted_nodes = self._adjust_by_weakness(sorted_nodes, student_profile.weaknesses)
        
        # 5. 计算总时长和预计完成日期
        total_hours = sum(n.estimated_hours for n in sorted_nodes)
        weeks_needed = total_hours / max(student_profile.available_hours_per_week, 1)
        estimated_completion = datetime.now() + timedelta(weeks=weeks_needed)
        
        # 如果学生设置了截止日期，进行提醒
        if student_profile.deadline:
            if estimated_completion > student_profile.deadline:
                logger.warning(
                    f"预计完成时间 {estimated_completion.date()} "
                    f"超过目标截止日期 {student_profile.deadline.date()}"
                )
        
        # 6. 构建学习路径
        path = LearningPath(
            path_id=f"path_{student_profile.student_id}_{datetime.now().strftime('%Y%m%d')}",
            student_id=student_profile.student_id,
            nodes=sorted_nodes,
            total_hours=total_hours,
            estimated_completion_date=estimated_completion,
        )
        
        logger.info(
            f"路径规划完成: {len(sorted_nodes)} 个节点，"
            f"预计 {total_hours} 小时，{weeks_needed:.1f} 周"
        )
        
        return path

    def _determine_target_nodes(self, profile: StudentProfile) -> List[str]:
        """
        根据学生画像确定目标知识点
        
        策略：
        - 入门水平：学习所有基础节点
        - 初级：跳过最基础内容，学习中级内容
        - 中级：学习中级和高级内容
        - 高级/专家：学习高级内容和专题
        """
        all_nodes = self.knowledge_graph.get_all_nodes()
        
        if profile.proficiency == ProficiencyLevel.BEGINNER:
            # 入门：学习所有1-2级难度的节点
            return [n.id for n in all_nodes if n.level <= 2]
        
        elif profile.proficiency == ProficiencyLevel.ELEMENTARY:
            return [n.id for n in all_nodes if 1 <= n.level <= 3]
        
        elif profile.proficiency == ProficiencyLevel.INTERMEDIATE:
            return [n.id for n in all_nodes if 2 <= n.level <= 4]
        
        else:  # ADVANCED, EXPERT
            return [n.id for n in all_nodes if n.level >= 3]

    def _filter_by_proficiency(
        self,
        node_ids: List[str],
        proficiency: ProficiencyLevel
    ) -> List[str]:
        """
        根据熟练度过滤已掌握的知识点
        
        在模拟模式下，假设低难度节点已掌握
        """
        # 根据熟练度确定"已掌握"的最大难度
        mastery_level_map = {
            ProficiencyLevel.BEGINNER: 0,     # 什么都不掌握
            ProficiencyLevel.ELEMENTARY: 1,    # 掌握难度1
            ProficiencyLevel.INTERMEDIATE: 2,  # 掌握难度1-2
            ProficiencyLevel.ADVANCED: 3,      # 掌握难度1-3
            ProficiencyLevel.EXPERT: 4,        # 掌握难度1-4
        }
        max_mastery = mastery_level_map.get(proficiency, 0)
        
        # 过滤掉已掌握的节点
        filtered = [
            nid for nid in node_ids
            if nid in self.knowledge_graph.nodes
            and self.knowledge_graph.nodes[nid].level > max_mastery
        ]
        
        return filtered

    def _topological_sort(self, node_ids: List[str]) -> List[LearningNode]:
        """
        拓扑排序
        
        保证输出的节点顺序满足前置依赖关系。
        使用 Kahn 算法。
        """
        # 构建邻接表和入度表
        in_degree = {nid: 0 for nid in node_ids}
        adj = {nid: [] for nid in node_ids}
        
        for nid in node_ids:
            node = self.knowledge_graph.nodes.get(nid)
            if node:
                for prereq in node.prerequisites:
                    if prereq in in_degree:  # 只关心在目标范围内的前置
                        adj[prereq].append(nid)
                        in_degree[nid] += 1
        
        # Kahn 算法
        queue = [nid for nid, deg in in_degree.items() if deg == 0]
        result = []
        
        while queue:
            # 按难度排序队列（难度低的先学）
            queue.sort(key=lambda x: self.knowledge_graph.nodes[x].level)
            current = queue.pop(0)
            result.append(self.knowledge_graph.nodes[current])
            
            for neighbor in adj[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return result

    def _adjust_by_weakness(
        self,
        nodes: List[LearningNode],
        weaknesses: List[str]
    ) -> List[LearningNode]:
        """
        根据学生的薄弱点调整学习顺序
        
        将涉及薄弱点的节点提前（在依赖允许的范围内）
        """
        if not weaknesses:
            return nodes
        
        # 将薄弱相关节点移到前面（保持拓扑顺序的前提下）
        weakness_set = set(weaknesses)
        
        # 简单策略：将标签匹配的节点提前
        adjusted = []
        normal = []
        
        for node in nodes:
            if node.name in weakness_set or node.id in weakness_set:
                adjusted.append(node)
            else:
                normal.append(node)
        
        return adjusted + normal

    def export_path(
        self,
        path: LearningPath,
        output_dir: Optional[str] = None,
        formats: List[str] = None,
    ) -> Dict:
        """
        导出学习路径为文件
        
        参数:
            path: 学习路径
            output_dir: 输出目录
            formats: 导出格式列表
        
        返回:
            导出结果字典
        """
        exporter = FileExporter(output_dir)
        
        if formats is None:
            formats = ["json", "md"]
        
        # 生成 Markdown 格式的路径说明
        md_content = self._path_to_markdown(path)
        
        filename = f"learning_path_{path.student_id}"
        results = {}
        
        for fmt in formats:
            if fmt == "json":
                result = exporter.export(
                    content="",
                    filename=filename,
                    formats=["json"],
                    mock_mode=True,
                    data=path.to_dict(),
                )
                results["json"] = result.get("json")
            
            elif fmt == "md":
                result = exporter.export(
                    content=md_content,
                    filename=f"{filename}_plan",
                    formats=["md"],
                    mock_mode=True,
                )
                results["md"] = result.get("md")
        
        return results

    def _path_to_markdown(self, path: LearningPath) -> str:
        """将学习路径转换为 Markdown 格式"""
        lines = [
            f"# 学习路径规划",
            "",
            f"- **路径ID**: {path.path_id}",
            f"- **学生ID**: {path.student_id}",
            f"- **节点数**: {len(path.nodes)}",
            f"- **总时长**: {path.total_hours} 小时",
            f"- **预计完成**: {path.estimated_completion_date.strftime('%Y-%m-%d') if path.estimated_completion_date else '未设定'}",
            f"- **创建时间**: {path.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 学习安排",
            "",
        ]
        
        cumulative_hours = 0
        for i, node in enumerate(path.nodes, 1):
            cumulative_hours += node.estimated_hours
            week = cumulative_hours / 10  # 假设每周学10小时
            lines.append(
                f"{i}. **{node.name}** (难度 {node.level}, {node.estimated_hours}h) "
                f"- 预计第 {week:.1f} 周完成"
            )
            lines.append(f"   > {node.description}")
            if node.prerequisites:
                prereq_names = [
                    self.knowledge_graph.nodes[pid].name
                    for pid in node.prerequisites
                    if pid in self.knowledge_graph.nodes
                ]
                lines.append(f"   - 前置知识: {', '.join(prereq_names)}")
            lines.append("")
        
        return "\n".join(lines)

    @staticmethod
    def create_mock_student(student_id: str = "student_001") -> StudentProfile:
        """创建模拟学生画像（用于测试）"""
        return StudentProfile(
            student_id=student_id,
            name="张三",
            subject="计算机",
            proficiency=ProficiencyLevel.ELEMENTARY,
            goal=LearningGoal.FOUNDATION,
            available_hours_per_week=8,
            strengths=["programming_basic"],
            weaknesses=["data_structure", "algorithm"],
            learning_style="visual",
            deadline=datetime.now() + timedelta(weeks=12),
        )
