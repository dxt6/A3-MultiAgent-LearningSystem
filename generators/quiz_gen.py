"""
题目生成器模块

调用 quiz_agent 生成各类题目（选择题、填空题、简答题等），
并保存为 JSON 格式文件。

支持模拟模式：无需真实 Agent，直接生成模拟题目数据。
"""

import os
import json
import logging
from typing import Optional, Dict, List, Literal
from pathlib import Path
from datetime import datetime
from enum import Enum

from ..config import config
from ..utils.file_exporter import FileExporter
from ..utils.safety_filter import SafetyFilter, FilterResult

logger = logging.getLogger(__name__)


class QuestionType(str, Enum):
    """题目类型枚举"""
    MULTIPLE_CHOICE = "multiple_choice"  # 单选题
    MULTIPLE_ANSWER = "multiple_answer"  # 多选题
    FILL_BLANK = "fill_blank"          # 填空题
    TRUE_FALSE = "true_false"          # 判断题
    SHORT_ANSWER = "short_answer"      # 简答题
    ESSAY = "essay"                    # 论述题
    CODING = "coding"                  # 编程题


class QuizAgentMock:
    """
    题目生成智能体模拟实现
    
    在模拟模式下替代真实的 quiz_agent，
    根据主题和题型生成模拟题目数据。
    """

    def generate(
        self,
        topic: str,
        question_type: QuestionType = QuestionType.MULTIPLE_CHOICE,
        num_questions: int = 5,
        difficulty: str = "medium",
        **kwargs
    ) -> List[Dict]:
        """
        模拟生成题目数据
        
        参数:
            topic: 题目主题
            question_type: 题目类型
            num_questions: 题目数量
            difficulty: 难度级别（easy/medium/hard）
            **kwargs: 其他生成参数
        
        返回:
            题目列表，每题为字典格式
        """
        questions = []
        for i in range(num_questions):
            if question_type == QuestionType.MULTIPLE_CHOICE:
                question = self._gen_multiple_choice(topic, i + 1, difficulty)
            elif question_type == QuestionType.MULTIPLE_ANSWER:
                question = self._gen_multiple_answer(topic, i + 1, difficulty)
            elif question_type == QuestionType.FILL_BLANK:
                question = self._gen_fill_blank(topic, i + 1, difficulty)
            elif question_type == QuestionType.TRUE_FALSE:
                question = self._gen_true_false(topic, i + 1, difficulty)
            elif question_type == QuestionType.SHORT_ANSWER:
                question = self._gen_short_answer(topic, i + 1, difficulty)
            elif question_type == QuestionType.CODING:
                question = self._gen_coding(topic, i + 1, difficulty)
            else:
                question = self._gen_multiple_choice(topic, i + 1, difficulty)
            questions.append(question)
        
        return questions

    def _gen_multiple_choice(self, topic: str, index: int, difficulty: str) -> Dict:
        """生成单选题"""
        return {
            "id": index,
            "type": QuestionType.MULTIPLE_CHOICE.value,
            "topic": topic,
            "difficulty": difficulty,
            "question": f"关于{topic}，下列说法正确的是？",
            "options": [
                f"A. {topic} 的基本概念是...",
                f"B. {topic} 的主要特征包括...",
                f"C. {topic} 的应用场景包括...",
                f"D. 以上说法都不正确",
            ],
            "answer": "A",
            "explanation": f"选项 A 正确描述了 {topic} 的基本概念。",
            "score": 5,
        }

    def _gen_multiple_answer(self, topic: str, index: int, difficulty: str) -> Dict:
        """生成多选题"""
        return {
            "id": index,
            "type": QuestionType.MULTIPLE_ANSWER.value,
            "topic": topic,
            "difficulty": difficulty,
            "question": f"以下哪些属于{topic}的核心特征？（多选）",
            "options": [
                f"A. 特征一",
                f"B. 特征二",
                f"C. 特征三",
                f"D. 特征四",
            ],
            "answer": ["A", "B", "C"],
            "explanation": f"特征一、二、三都是 {topic} 的核心特征。",
            "score": 8,
        }

    def _gen_fill_blank(self, topic: str, index: int, difficulty: str) -> Dict:
        """生成填空题"""
        return {
            "id": index,
            "type": QuestionType.FILL_BLANK.value,
            "topic": topic,
            "difficulty": difficulty,
            "question": f"{topic} 的核心定义是：______。",
            "answer": [f"{topic}的定义", f"{topic}的概念"],  # 支持多个正确答案
            "explanation": f"本题考查对 {topic} 基本概念的理解。",
            "score": 4,
        }

    def _gen_true_false(self, topic: str, index: int, difficulty: str) -> Dict:
        """生成判断题"""
        return {
            "id": index,
            "type": QuestionType.TRUE_FALSE.value,
            "topic": topic,
            "difficulty": difficulty,
            "question": f"{topic} 是现代学科体系中的重要组成部分。（判断题）",
            "answer": True,
            "explanation": f"{topic} 确实是现代学科体系中的重要组成部分。",
            "score": 3,
        }

    def _gen_short_answer(self, topic: str, index: int, difficulty: str) -> Dict:
        """生成简答题"""
        return {
            "id": index,
            "type": QuestionType.SHORT_ANSWER.value,
            "topic": topic,
            "difficulty": difficulty,
            "question": f"请简述 {topic} 的基本概念和主要应用场景。",
            "answer": f"{topic} 的基本概念是...主要应用场景包括...",
            "key_points": [
                f"要点1：{topic} 的定义",
                f"要点2：{topic} 的特征",
                f"要点3：{topic} 的应用",
            ],
            "explanation": "本题考查对基础概念的理解。",
            "score": 10,
        }

    def _gen_coding(self, topic: str, index: int, difficulty: str) -> Dict:
        """生成编程题"""
        return {
            "id": index,
            "type": QuestionType.CODING.value,
            "topic": topic,
            "difficulty": difficulty,
            "question": f"编写一个函数，实现与 {topic} 相关的基本功能。",
            "input_description": "输入：相关参数",
            "output_description": "输出：计算结果",
            "sample_input": "示例输入",
            "sample_output": "示例输出",
            "reference_code": f"def solve():\n    # 实现 {topic} 相关功能\n    pass",
            "test_cases": [
                {"input": "test1", "output": "result1"},
            ],
            "score": 20,
        }


class QuizGenerator:
    """
    题目生成器
    
    负责调用 quiz_agent 生成各类题目，并进行安全过滤后保存为 JSON 文件。
    
    属性:
        agent: 题目生成智能体实例
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
        初始化题目生成器
        
        参数:
            agent: 题目生成智能体（为 None 时使用模拟 Agent）
            output_dir: 输出目录
            mock_mode: 是否使用模拟模式
        """
        self.mock_mode = mock_mode if mock_mode is not None else config.MOCK_MODE
        
        if self.mock_mode or agent is None:
            self.agent = QuizAgentMock()
            logger.info("题目生成器初始化完成（模拟模式）")
        else:
            self.agent = agent
            logger.info("题目生成器初始化完成（真实模式）")
        
        self.exporter = FileExporter(output_dir)
        self.safety_filter = SafetyFilter()

    def generate(
        self,
        topic: str,
        question_type: str = "multiple_choice",
        num_questions: int = 5,
        difficulty: str = "medium",
        filename: Optional[str] = None,
        export_formats: List[str] = None,
        **kwargs
    ) -> Dict:
        """
        生成题目并导出
        
        参数:
            topic: 题目主题
            question_type: 题目类型（multiple_choice/multiple_answer/fill_blank/true_false/short_answer/essay/coding）
            num_questions: 题目数量
            difficulty: 难度（easy/medium/hard）
            filename: 导出文件名
            export_formats: 导出格式列表（默认 ["json"]）
            **kwargs: 传递给 Agent 的其他参数
        
        返回:
            包含生成结果的字典
        """
        # 1. 调用 Agent 生成题目
        logger.info(
            f"开始生成题目，主题: {topic}, 类型: {question_type}, 数量: {num_questions}"
        )
        
        try:
            qtype = QuestionType(question_type)
        except ValueError:
            logger.warning(f"未知题目类型: {question_type}，使用默认单选题")
            qtype = QuestionType.MULTIPLE_CHOICE
        
        questions = self.agent.generate(
            topic=topic,
            question_type=qtype,
            num_questions=num_questions,
            difficulty=difficulty,
            **kwargs
        )
        
        # 2. 内容安全过滤（检查每道题的内容）
        logger.info("进行内容安全过滤...")
        all_text = " ".join(
            q.get("question", "") + " ".join(q.get("options", []))
            for q in questions
        )
        safety_result = self.safety_filter.filter(all_text, topic)
        
        if not safety_result.is_safe and not self.mock_mode:
            return {
                "success": False,
                "error": "题目内容安全检测未通过",
                "safety": safety_result.to_dict(),
            }
        
        # 3. 构建完整的题目数据包
        quiz_data = {
            "metadata": {
                "title": f"{topic} - {difficulty} 难度练习题",
                "topic": topic,
                "question_type": qtype.value,
                "difficulty": difficulty,
                "num_questions": len(questions),
                "total_score": sum(q.get("score", 0) for q in questions),
                "generated_at": datetime.now().isoformat(),
                "generator": "QuizGenerator",
            },
            "questions": questions,
        }
        
        # 4. 确定文件名并导出
        if filename is None:
            safe_topic = "".join(c for c in topic if c.isalnum() or c in (" ", "-", "_")).strip()
            safe_topic = safe_topic.replace(" ", "_")[:50]
            filename = f"quiz_{safe_topic}_{qtype.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if export_formats is None:
            export_formats = ["json"]
        
        logger.info(f"导出题目为 {export_formats} 格式...")
        export_results = self.exporter.export(
            content="",  # JSON 导出不需要 content
            filename=filename,
            formats=export_formats,
            mock_mode=self.mock_mode,
            data=quiz_data,
        )
        
        # 5. 返回结果
        result = {
            "success": True,
            "filename": filename,
            "export_paths": {k: str(v) for k, v in export_results.items() if v is not None},
            "num_questions": len(questions),
            "total_score": quiz_data["metadata"]["total_score"],
            "questions": questions,
            "safety": safety_result.to_dict(),
            "topic": topic,
            "generated_at": datetime.now().isoformat(),
        }
        
        logger.info(f"题目生成完成: {filename}，共 {len(questions)} 道题")
        return result

    def generate_mixed(
        self,
        topic: str,
        configs: List[Dict],
        filename: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """
        生成混合类型的题目集
        
        参数:
            topic: 题目主题
            configs: 题型配置列表，每项为 {"type": "multiple_choice", "num": 5, "difficulty": "easy"}
            filename: 导出文件名
            **kwargs: 其他参数
        
        返回:
            生成结果字典
        """
        all_questions = []
        for cfg in configs:
            qtype = cfg.get("type", "multiple_choice")
            num = cfg.get("num", 3)
            difficulty = cfg.get("difficulty", "medium")
            
            questions = self.agent.generate(
                topic=topic,
                question_type=QuestionType(qtype),
                num_questions=num,
                difficulty=difficulty,
            )
            all_questions.extend(questions)
        
        # 重新编号
        for i, q in enumerate(all_questions, 1):
            q["id"] = i
        
        quiz_data = {
            "metadata": {
                "title": f"{topic} - 综合练习题",
                "topic": topic,
                "num_questions": len(all_questions),
                "total_score": sum(q.get("score", 0) for q in all_questions),
                "generated_at": datetime.now().isoformat(),
                "generator": "QuizGenerator",
            },
            "questions": all_questions,
        }
        
        if filename is None:
            filename = f"quiz_mixed_{topic}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        export_results = self.exporter.export(
            content="",
            filename=filename,
            formats=["json"],
            mock_mode=self.mock_mode,
            data=quiz_data,
        )
        
        return {
            "success": True,
            "filename": filename,
            "export_paths": {k: str(v) for k, v in export_results.items() if v is not None},
            "num_questions": len(all_questions),
            "questions": all_questions,
        }
