"""
内容安全过滤模块

提供以下功能：
1. 敏感词检测（基于词库匹配）
2. 学术内容准确性检查（基于规则）
3. 内容合规性评分

基于规则实现，无需外部依赖，支持自定义词库。
"""

import re
import logging
from typing import List, Optional, Dict, Set
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class SafetyLevel(Enum):
    """安全等级枚举"""
    SAFE = "safe"           # 安全
    LOW_RISK = "low_risk"   # 低风险（警告）
    MEDIUM_RISK = "medium_risk"  # 中风险（需要审核）
    HIGH_RISK = "high_risk"      # 高风险（禁止）


@dataclass
class FilterResult:
    """
    过滤结果数据类
    
    属性:
        is_safe: 是否通过安全检测
        level: 安全等级
        matched_words: 命中的敏感词列表
        suggestions: 修改建议列表
        score: 安全评分（0-100，越高越安全）
        details: 详细信息字典
    """
    is_safe: bool
    level: SafetyLevel
    matched_words: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    score: float = 100.0
    details: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "is_safe": self.is_safe,
            "level": self.level.value,
            "matched_words": self.matched_words,
            "suggestions": self.suggestions,
            "score": self.score,
            "details": self.details,
        }


class SafetyFilter:
    """
    内容安全过滤器
    
    功能：
    1. 敏感词检测（政治、暴力、色情、违法等）
    2. 学术内容准确性检查（术语验证、引用检查）
    3. 内容合规性评分
    
    基于规则实现，支持自定义敏感词库。
    """

    # ==================== 敏感词库（示例，实际使用时需完善） ====================
    
    # 政治敏感词（示例，实际应根据需求定制）
    _SENSITIVE_POLITICAL = {
        # 此处仅作示例，实际词库需根据应用场景定制
        # 教育场景一般较少涉及政治敏感内容
    }

    # 暴力、恐怖相关
    _SENSITIVE_VIOLENCE = {
        "爆炸", "炸弹", "恐怖袭击", "杀人", "谋杀", "自杀方法",
        "武器制造", "毒品制造", "炸弹制作",
    }

    # 色情、低俗相关
    _SENSITIVE_PORN = {
        "色情", "淫秽", "裸聊", "成人影片", "色情网站",
        # 教育场景通常不需要过多此类词，基础过滤即可
    }

    # 违法、欺诈相关
    _SENSITIVE_ILLEGAL = {
        "造假", "伪造证件", "黑客攻击", "盗号", "诈骗",
        "洗钱", "赌博网站", "枪支出售", "毒品交易",
    }

    # 歧视、仇恨言论
    _SENSITIVE_DISCRIMINATION = {
        "种族歧视", "性别歧视", "地域歧视", "仇恨言论",
    }

    # 汇总所有敏感词
    _ALL_SENSITIVE_WORDS = (
        set(_SENSITIVE_VIOLENCE)
        | set(_SENSITIVE_PORN)
        | set(_SENSITIVE_ILLEGAL)
        | set(_SENSITIVE_DISCRIMINATION)
    )

    # ==================== 学术术语库（用于准确性检查） ====================
    
    # 常见学科领域术语（示例）
    _ACADEMIC_TERMS = {
        "数学": {
            "代数", "几何", "微积分", "概率论", "数理统计", "线性代数",
            "矩阵", "向量", "导数", "积分", "极限", "函数", "方程",
            "定理", "引理", "推论", "证明", "公理",
        },
        "计算机": {
            "算法", "数据结构", "编程语言", "操作系统", "数据库",
            "计算机网络", "机器学习", "深度学习", "人工智能",
            "Python", "Java", "C++", "JavaScript", "HTML", "CSS",
            "HTTP", "TCP/IP", "API", "JSON", "XML",
        },
        "物理": {
            "牛顿定律", "万有引力", "相对论", "量子力学", "热力学",
            "电磁感应", "光学", "波动", "粒子", "能量守恒",
        },
        "化学": {
            "元素", "化合物", "化学反应", "摩尔", "pH值",
            "氧化反应", "还原反应", "催化剂", "有机化学", "无机化学",
        },
    }

    # 常见学术不准确表述（需要警告的）
    _ACADEMIC_RED_FLAGS = {
        "绝对正确", "永远成立", "所有人都认为", "毫无疑问",
        "100%准确", "完全无误", "史上最佳", "无人能敌",
    }

    # 学术引用格式正则
    _CITATION_PATTERNS = [
        r"\[\d+\]",                    # [1], [2,3]
        r"\([A-Za-z]+,\s*\d{4}\)",   # (Smith, 2020)
        r"DOI:\s*10\.\d+",           # DOI: 10.xxxx
        r"https?://doi\.org",        # https://doi.org/...
    ]

    def __init__(self, custom_sensitive_words: Optional[Set[str]] = None):
        """
        初始化安全过滤器
        
        参数:
            custom_sensitive_words: 自定义敏感词集合（会合并到默认词库）
        """
        self.sensitive_words = self._ALL_SENSITIVE_WORDS.copy()
        if custom_sensitive_words:
            self.sensitive_words.update(custom_sensitive_words)
        
        logger.info(f"安全过滤器初始化完成，敏感词库大小: {len(self.sensitive_words)}")

    def detect_sensitive_words(self, text: str) -> List[str]:
        """
        检测文本中的敏感词
        
        参数:
            text: 待检测文本
        
        返回:
            命中的敏感词列表（去重）
        """
        matched = set()
        for word in self.sensitive_words:
            if word in text:
                matched.add(word)
        
        return list(matched)

    def check_academic_accuracy(self, text: str, subject: Optional[str] = None) -> Dict:
        """
        检查学术内容的准确性
        
        参数:
            text: 待检查的学术内容
            subject: 学科领域（如 "数学"、"计算机"），为 None 时检查所有领域
        
        返回:
            检查结果字典，包含：
            - valid_terms: 识别出的有效学术术语
            - red_flags: 检测到的不准确表述
            - has_citation: 是否包含引用
            - suggestions: 改进建议
        """
        result = {
            "valid_terms": [],
            "red_flags": [],
            "has_citation": False,
            "suggestions": [],
        }
        
        # 检查学术术语
        subjects = [subject] if subject else self._ACADEMIC_TERMS.keys()
        for subj in subjects:
            terms = self._ACADEMIC_TERMS.get(subj, set())
            for term in terms:
                if term in text and term not in result["valid_terms"]:
                    result["valid_terms"].append(term)
        
        # 检查不准确表述
        for flag in self._ACADEMIC_RED_FLAGS:
            if flag in text:
                result["red_flags"].append(flag)
        
        # 检查引用格式
        for pattern in self._CITATION_PATTERNS:
            if re.search(pattern, text):
                result["has_citation"] = True
                break
        
        # 生成建议
        if not result["has_citation"] and len(text) > 500:
            result["suggestions"].append("建议添加学术引用以增强内容可信度")
        
        if result["red_flags"]:
            result["suggestions"].append(
                f"以下内容可能表述过于绝对，建议修改: {', '.join(result['red_flags'])}"
            )
        
        if len(result["valid_terms"]) < 3 and len(text) > 200:
            result["suggestions"].append("内容中识别到的学术术语较少，建议增加专业术语以提升学术性")
        
        return result

    def filter(self, text: str, subject: Optional[str] = None) -> FilterResult:
        """
        对文本进行全面安全过滤
        
        参数:
            text: 待过滤文本
            subject: 学科领域（用于学术准确性检查）
        
        返回:
            FilterResult 对象，包含完整的过滤结果
        """
        # 1. 敏感词检测
        matched_words = self.detect_sensitive_words(text)
        
        # 2. 学术准确性检查
        academic_check = self.check_academic_accuracy(text, subject)
        
        # 3. 计算安全评分
        score = 100.0
        
        # 敏感词扣分（每个扣 20 分，最高扣到 0）
        score -= len(matched_words) * 20
        
        # 不准确表述扣分（每个扣 10 分）
        score -= len(academic_check["red_flags"]) * 10
        
        score = max(0, score)
        
        # 4. 确定安全等级
        if score >= 80:
            level = SafetyLevel.SAFE
        elif score >= 60:
            level = SafetyLevel.LOW_RISK
        elif score >= 30:
            level = SafetyLevel.MEDIUM_RISK
        else:
            level = SafetyLevel.HIGH_RISK
        
        # 5. 生成建议
        suggestions = []
        if matched_words:
            suggestions.append(f"请移除以下敏感词: {', '.join(matched_words)}")
        suggestions.extend(academic_check["suggestions"])
        
        # 6. 综合判断
        is_safe = (level == SafetyLevel.SAFE or level == SafetyLevel.LOW_RISK) and len(matched_words) == 0
        
        return FilterResult(
            is_safe=is_safe,
            level=level,
            matched_words=matched_words,
            suggestions=suggestions,
            score=score,
            details={
                "academic_check": academic_check,
                "text_length": len(text),
                "subject": subject,
            },
        )

    def batch_filter(self, texts: List[str], subject: Optional[str] = None) -> List[FilterResult]:
        """
        批量过滤多段文本
        
        参数:
            texts: 文本列表
            subject: 学科领域
        
        返回:
            FilterResult 列表
        """
        return [self.filter(text, subject) for text in texts]

    def add_sensitive_words(self, words: Set[str]) -> None:
        """
        动态添加敏感词到词库
        
        参数:
            words: 要添加的敏感词集合
        """
        self.sensitive_words.update(words)
        logger.info(f"已添加 {len(words)} 个敏感词到词库")

    def remove_sensitive_words(self, words: Set[str]) -> None:
        """
        从词库中移除敏感词
        
        参数:
            words: 要移除的敏感词集合
        """
        self.sensitive_words.difference_update(words)
        logger.info(f"已从词库移除 {len(words)} 个敏感词")

    @classmethod
    def load_sensitive_words_from_file(cls, filepath: str) -> Set[str]:
        """
        从文件加载敏感词库
        
        文件格式：每行一个敏感词
        
        参数:
            filepath: 敏感词文件路径
        
        返回:
            敏感词集合
        """
        words = set()
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    word = line.strip()
                    if word and not word.startswith("#"):
                        words.add(word)
            logger.info(f"从 {filepath} 加载了 {len(words)} 个敏感词")
        except FileNotFoundError:
            logger.warning(f"敏感词文件不存在: {filepath}")
        return words

    @classmethod
    def save_sensitive_words_to_file(cls, words: Set[str], filepath: str) -> None:
        """
        将敏感词保存到文件
        
        参数:
            words: 敏感词集合
            filepath: 保存路径
        """
        with open(filepath, "w", encoding="utf-8") as f:
            for word in sorted(words):
                f.write(word + "\n")
        logger.info(f"敏感词已保存到 {filepath}")
