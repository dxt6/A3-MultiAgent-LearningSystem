"""
文本处理工具模块

提供以下功能：
1. Markdown 转 HTML
2. 文本摘要生成
3. 关键词提取

支持模拟模式，无需外部依赖即可运行。
"""

import re
import hashlib
from typing import List, Optional
from collections import Counter
import logging

logger = logging.getLogger(__name__)


class MarkdownHelper:
    """
    Markdown 文本处理辅助类
    
    提供 Markdown 到 HTML 的转换、清理、格式化等功能。
    在模拟模式下使用内置规则，无需外部库。
    """

    @staticmethod
    def md_to_html(markdown_text: str, use_external: bool = False) -> str:
        """
        将 Markdown 文本转换为 HTML
        
        参数:
            markdown_text: Markdown 格式的原始文本
            use_external: 是否使用外部库（如 markdown 模块），默认 False
        
        返回:
            HTML 格式的字符串
        """
        if use_external:
            try:
                import markdown
                return markdown.markdown(
                    markdown_text,
                    extensions=["extra", "codehilite", "toc"]
                )
            except ImportError:
                logger.warning("markdown 库未安装，使用内置转换器")
        
        # 内置简单 Markdown 转 HTML（模拟模式）
        return MarkdownHelper._convert_md_to_html_builtin(markdown_text)

    @staticmethod
    def _convert_md_to_html_builtin(text: str) -> str:
        """内置 Markdown 转 HTML 实现（无需外部依赖）"""
        lines = text.split("\n")
        html_lines = []
        in_code_block = False
        in_list = False
        list_type = None  # "ul" 或 "ol"
        in_blockquote = False

        i = 0
        while i < len(lines):
            line = lines[i]

            # 代码块处理（``` 包裹）
            if line.strip().startswith("```"):
                if in_code_block:
                    html_lines.append("</code></pre>")
                    in_code_block = False
                else:
                    lang = line.strip()[3:].strip()
                    html_lines.append(f'<pre><code class="language-{lang}">')
                    in_code_block = True
                i += 1
                continue

            if in_code_block:
                html_lines.append(line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
                i += 1
                continue

            # 标题处理 (# ~ ######)
            heading_match = re.match(r"^(#{1,6})\s+(.*)", line)
            if heading_match:
                level = len(heading_match.group(1))
                content = heading_match.group(2).strip()
                html_lines.append(f"<h{level}>{content}</h{level}>")
                i += 1
                continue

            # 水平线 (--- 或 ***)
            if re.match(r"^[-*_]{3,}\s*$", line.strip()):
                html_lines.append("<hr>")
                i += 1
                continue

            # 列表处理
            ul_match = re.match(r"^(\s*)([-*+])\s+(.*)", line)
            ol_match = re.match(r"^(\s*)(\d+)\.\s+(.*)", line)

            if ul_match or ol_match:
                current_list_type = "ul" if ul_match else "ol"
                if not in_list:
                    html_lines.append(f"<{current_list_type}>")
                    in_list = True
                    list_type = current_list_type
                
                content = (ul_match.group(3) if ul_match else ol_match.group(3)).strip()
                content = MarkdownHelper._inline_md_to_html(content)
                html_lines.append(f"<li>{content}</li>")
                i += 1
                continue
            else:
                if in_list:
                    html_lines.append(f"</{list_type}>")
                    in_list = False
                    list_type = None

            # 引用块处理
            blockquote_match = re.match(r"^\>\s?(.*)", line)
            if blockquote_match:
                if not in_blockquote:
                    html_lines.append("<blockquote>")
                    in_blockquote = True
                content = MarkdownHelper._inline_md_to_html(blockquote_match.group(1))
                html_lines.append(f"<p>{content}</p>")
                i += 1
                continue
            else:
                if in_blockquote:
                    html_lines.append("</blockquote>")
                    in_blockquote = False

            # 普通段落
            if line.strip() == "":
                html_lines.append("")
            else:
                content = MarkdownHelper._inline_md_to_html(line.strip())
                # 检查是否是独立的 <p> 还是与其他内容合并
                if html_lines and html_lines[-1] == "":
                    html_lines[-1] = f"<p>{content}</p>"
                else:
                    html_lines.append(f"<p>{content}</p>")

            i += 1

        # 关闭未关闭的标签
        if in_list:
            html_lines.append(f"</{list_type}>")
        if in_blockquote:
            html_lines.append("</blockquote>")

        return "\n".join(html_lines)

    @staticmethod
    def _inline_md_to_html(text: str) -> str:
        """处理行内 Markdown 语法（粗体、斜体、代码、链接）"""
        # 行内代码
        text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
        # 粗体
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"__(.+?)__", r"<strong>\1</strong>", text)
        # 斜体
        text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
        text = re.sub(r"_(.+?)_", r"<em>\1</em>", text)
        # 链接
        text = re.sub(r"\[([^\]]+)\]\(([^\)]+)\)", r'<a href="\2">\1</a>', text)
        return text

    @staticmethod
    def clean_md(text: str) -> str:
        """
        清理 Markdown 文本中的多余空行和格式问题
        
        参数:
            text: 原始 Markdown 文本
        
        返回:
            清理后的文本
        """
        # 去除多余空行（最多保留一个空行）
        text = re.sub(r"\n{3,}", "\n\n", text)
        # 去除行尾空格
        text = "\n".join(line.rstrip() for line in text.split("\n"))
        return text.strip()

    @staticmethod
    def extract_sections(markdown_text: str) -> list[dict]:
        """
        提取 Markdown 文档的章节结构
        
        参数:
            markdown_text: Markdown 文档内容
        
        返回:
            章节列表，每个元素为 {'level': int, 'title': str, 'content': str}
        """
        sections = []
        lines = markdown_text.split("\n")
        current_section = None
        current_content = []

        for line in lines:
            heading_match = re.match(r"^(#{1,6})\s+(.*)", line)
            if heading_match:
                # 保存上一个章节
                if current_section is not None:
                    current_section["content"] = "\n".join(current_content).strip()
                    sections.append(current_section)
                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()
                current_section = {"level": level, "title": title}
                current_content = []
            else:
                if current_section is not None:
                    current_content.append(line)
        
        # 保存最后一个章节
        if current_section is not None:
            current_section["content"] = "\n".join(current_content).strip()
            sections.append(current_section)
        
        return sections


class TextSummarizer:
    """
    文本摘要生成器
    
    支持两种模式：
    1. 模拟模式：基于规则提取关键句子
    2. 真实模式：可接入 LLM 生成摘要（预留接口）
    """

    @staticmethod
    def summarize(text: str, max_sentences: int = 3, mock_mode: bool = True) -> str:
        """
        生成文本摘要
        
        参数:
            text: 待摘要的原始文本
            max_sentences: 摘要最大句子数
            mock_mode: 是否使用模拟模式
        
        返回:
            摘要文本
        """
        if mock_mode:
            return TextSummarizer._extractive_summarize(text, max_sentences)
        
        # 预留真实模式接口（调用 LLM）
        return TextSummarizer._llm_summarize(text, max_sentences)

    @staticmethod
    def _extractive_summarize(text: str, max_sentences: int) -> str:
        """
        抽取式摘要（基于规则）
        
        策略：
        1. 分句
        2. 计算每个句子的得分（基于词频、位置等）
        3. 选择得分最高的 N 个句子
        """
        sentences = re.split(r"[。！？!?.]+", text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= max_sentences:
            return " ".join(sentences)
        
        # 计算词频
        all_words = re.findall(r"[\w\u4e00-\u9fff]+", text)
        word_freq = Counter(all_words)
        
        # 为每个句子评分
        sentence_scores = []
        for i, sent in enumerate(sentences):
            words = re.findall(r"[\w\u4e00-\u9fff]+", sent)
            # 评分因素：词频、位置（首句和尾句权重高）
            score = sum(word_freq.get(w, 0) for w in words) / max(len(words), 1)
            # 位置权重
            if i == 0:
                score *= 1.5  # 首句
            elif i == len(sentences) - 1:
                score *= 1.2  # 尾句
            sentence_scores.append((i, score, sent))
        
        # 选择得分最高的句子，按原文顺序排序
        top_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)[:max_sentences]
        top_sentences = sorted(top_sentences, key=lambda x: x[0])
        
        return " ".join(s for _, _, s in top_sentences) + "。"

    @staticmethod
    def _llm_summarize(text: str, max_sentences: int) -> str:
        """LLM 生成式摘要（预留接口）"""
        logger.info("LLM 摘要接口待实现，当前使用模拟模式")
        return TextSummarizer._extractive_summarize(text, max_sentences)


class KeywordExtractor:
    """
    关键词提取器
    
    支持两种模式：
    1. 模拟模式：基于 TF-IDF 和停用词过滤
    2. 真实模式：可接入 jieba/keybert 等工具（预留接口）
    """

    # 中文停用词列表（简化版）
    _STOPWORDS_CN = {
        "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一", "一个",
        "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好",
        "自己", "这", "他", "她", "它", "那", "这些", "那些", "什么", "怎么", "如何",
        "可以", "这个", "那个", "但是", "如果", "因为", "所以", "对于", "关于",
    }

    # 英文停用词列表（简化版）
    _STOPWORDS_EN = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "up", "about", "into", "over", "after",
        "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
        "do", "does", "did", "will", "would", "should", "could", "may", "might",
        "this", "that", "these", "those", "i", "you", "he", "she", "it", "we", "they",
    }

    _STOPWORDS = _STOPWORDS_CN | _STOPWORDS_EN

    @staticmethod
    def extract(text: str, top_k: int = 10, mock_mode: bool = True) -> List[str]:
        """
        从文本中提取关键词
        
        参数:
            text: 原始文本
            top_k: 返回关键词数量
            mock_mode: 是否使用模拟模式
        
        返回:
            关键词列表
        """
        if mock_mode:
            return KeywordExtractor._extract_by_tfidf(text, top_k)
        
        # 预留真实模式接口
        return KeywordExtractor._extract_by_jieba(text, top_k)

    @staticmethod
    def _extract_by_tfidf(text: str, top_k: int) -> List[str]:
        """
        基于词频的关键词提取（TF 简化版）
        
        策略：
        1. 分词（中英文混合处理）
        2. 过滤停用词
        3. 按词频排序取 Top-K
        """
        # 提取中英文词汇
        chinese_words = re.findall(r"[\u4e00-\u9fff]+", text)
        english_words = re.findall(r"[a-zA-Z]{2,}", text.lower())
        all_words = chinese_words + english_words
        
        # 过滤停用词和短词
        filtered_words = [
            w for w in all_words
            if w not in KeywordExtractor._STOPWORDS and len(w) > 1
        ]
        
        # 按词频排序
        word_counts = Counter(filtered_words)
        return [word for word, _ in word_counts.most_common(top_k)]

    @staticmethod
    def _extract_by_jieba(text: str, top_k: int) -> List[str]:
        """基于 jieba 的关键词提取（预留接口）"""
        try:
            import jieba.analyse
            return jieba.analyse.extract_tags(text, topK=top_k)
        except ImportError:
            logger.warning("jieba 未安装，使用内置 TF 提取")
            return KeywordExtractor._extract_by_tfidf(text, top_k)

    @staticmethod
    def extract_with_weight(text: str, top_k: int = 10) -> List[tuple]:
        """
        提取关键词及其权重
        
        返回:
            [(关键词, 权重), ...] 列表
        """
        chinese_words = re.findall(r"[\u4e00-\u9fff]+", text)
        english_words = re.findall(r"[a-zA-Z]{2,}", text.lower())
        all_words = chinese_words + english_words
        
        filtered_words = [
            w for w in all_words
            if w not in KeywordExtractor._STOPWORDS and len(w) > 1
        ]
        
        word_counts = Counter(filtered_words)
        total = sum(word_counts.values())
        
        results = []
        for word, count in word_counts.most_common(top_k):
            weight = round(count / total, 4) if total > 0 else 0
            results.append((word, weight))
        
        return results
