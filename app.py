"""
A3-MultiAgent-LearningSystem
多智能体自适应学习系统 - Streamlit Web 应用（手绘风格版）
"""

import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pandas as pd

# ========================
# 加载自定义CSS样式（使用 st.html 更可靠）
# ========================
def load_css():
    """加载手绘风格CSS样式"""
    try:
        with open("assets/custom_clean.css", "r", encoding="utf-8") as f:
            css_content = f.read()
        # 使用 st.html 注入 CSS（比 st.markdown 更可靠）
        st.html(f"<style>{css_content}</style>")
    except FileNotFoundError:
        # 备用：内联CSS
        inline_css = """
            body, .stApp { background: #1a1a2e !important; color: #e0e0e0 !important; }
            h1, h2, h3 { font-family: serif !important; }
        """
        st.html(f"<style>{inline_css}</style>")

# 加载CSS
load_css()

# ========================
# 图标系统（使用emoji确保可靠显示）
# ========================
def render_icon(icon_name, size=24, color="#ffffff"):
    """渲染图标 - 使用emoji（最可靠的方式）"""
    icon_map = {
        'robot': '🤖', 'brain': '🧠', 'book_open': '📖', 'books': '📚',
        'gear': '⚙️', 'map': '🗺️', 'check': '✅', 'target': '🎯',
        'chat': '💬', 'user': '👤', 'rocket': '🚀', 'info': 'ℹ️',
        'building': '🏗️', 'lightning': '⚡', 'download': '📥', 'file': '📄',
        'clock': '⏱️', 'chart_bar': '📊', 'flag': '🏁', 'chart_line': '📈',
        'magnifier': '🔍', 'star': '⭐', 'nav_home': '🏠', 'nav_brain': '🧠',
        'nav_book': '📖', 'nav_map': '🗺️', 'nav_check': '✅', 'settings': '⚙️',
        'refresh': '🔄', 'bulb': '💡', 'warning': '⚠️', 'pencil': '✏️',
    }
    emoji = icon_map.get(icon_name, '📌')
    return f'<span style="font-size:{size}px;">{emoji}</span>'

def hand_drawn_divider():
    """手绘风格分割线"""
    st.markdown('<hr class="hand-drawn-divider">', unsafe_allow_html=True)

def hand_drawn_title(title_text, icon_name=None, icon_size=28):
    """渲染带手绘图标的标题"""
    if icon_name:
        icon = render_icon(icon_name, icon_size)
        st.markdown(f"{icon} <h2 style='display:inline; margin-left:8px;'>{title_text}</h2>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h2>{title_text}</h2>", unsafe_allow_html=True)

def render_card(content_html, card_class="card-uneven-1"):
    """渲染手绘风格卡片"""
    st.markdown(f'<div class="{card_class}">{content_html}</div>', unsafe_allow_html=True)

def render_handdrawn_flowchart():
    """渲染手绘风格多智能体协作流程图"""
    flowchart_svg = """
    <svg viewBox="0 0 900 500" width="100%" style="background: rgba(26,26,46,0.3); border-radius: 12px 6px 14px 4px; padding: 20px;">
        <!-- 定义手绘风格滤镜 -->
        <defs>
            <filter id="handdrawn">
                <feTurbulence type="turbulence" baseFrequency="0.05" numOctaves="2" result="noise"/>
                <feDisplacementMap in="SourceGraphic" in2="noise" scale="2" xChannelSelector="R" yChannelSelector="G"/>
            </filter>
        </defs>
        
        <!-- 标题 -->
        <text x="450" y="30" text-anchor="middle" fill="#e0e0e0" font-size="18" font-weight="bold">多智能体协作流程图</text>
        
        <!-- 学生用户输入框（手绘风格） -->
        <rect x="50" y="60" width="150" height="60" rx="8" ry="6" fill="none" stroke="#4a6fa5" stroke-width="2" stroke-dasharray="5,3" filter="url(#handdrawn)"/>
        <text x="125" y="95" text-anchor="middle" fill="#e0e0e0" font-size="14">学生用户输入</text>
        
        <!-- 箭头1：用户输入 → 画像构建Agent -->
        <path d="M 210 90 L 280 90" stroke="#4a6fa5" stroke-width="2" fill="none" stroke-dasharray="4,3" marker-end="url(#arrowhead)"/>
        <polygon points="280,85 290,90 280,95" fill="#4a6fa5"/>
        
        <!-- 画像构建Agent（手绘框） -->
        <rect x="300" y="60" width="150" height="60" rx="6" ry="8" fill="rgba(74,111,165,0.15)" stroke="#4a6fa5" stroke-width="2" stroke-dasharray="3,2"/>
        <text x="375" y="90" text-anchor="middle" fill="#e0e0e0" font-size="13">画像构建</text>
        <text x="375" y="108" text-anchor="middle" fill="#a0a0b0" font-size="11">Agent</text>
        
        <!-- 箭头2：画像构建 → 资源规划Agent -->
        <path d="M 460 90 L 530 90" stroke="#4a6fa5" stroke-width="2" fill="none" stroke-dasharray="4,3"/>
        <polygon points="530,85 540,90 530,95" fill="#4a6fa5"/>
        
        <!-- 资源规划Agent（手绘框） -->
        <rect x="560" y="60" width="150" height="60" rx="8" ry="5" fill="rgba(74,111,165,0.15)" stroke="#4a6fa5" stroke-width="2" stroke-dasharray="2,3"/>
        <text x="635" y="90" text-anchor="middle" fill="#e0e0e0" font-size="13">资源规划</text>
        <text x="635" y="108" text-anchor="middle" fill="#a0a0b0" font-size="11">Agent</text>
        
        <!-- 箭头3：资源规划 → 资源生成Agent -->
        <path d="M 720 90 L 790 90" stroke="#4a6fa5" stroke-width="2" fill="none" stroke-dasharray="4,3"/>
        <polygon points="790,85 800,90 790,95" fill="#4a6fa5"/>
        
        <!-- 资源生成Agent（手绘框） -->
        <rect x="820" y="60" width="150" height="60" rx="5" ry="7" fill="rgba(74,111,165,0.15)" stroke="#4a6fa5" stroke-width="2" stroke-dasharray="3,2"/>
        <text x="895" y="90" text-anchor="middle" fill="#e0e0e0" font-size="13">资源生成</text>
        <text x="895" y="108" text-anchor="middle" fill="#a0a0b0" font-size="11">Agent</text>
        
        <!-- 箭头4：资源生成 → 质量评估Agent -->
        <path d="M 895 130 L 895 180" stroke="#4a6fa5" stroke-width="2" fill="none" stroke-dasharray="4,3"/>
        <polygon points="890,180 895,190 900,180" fill="#4a6fa5"/>
        
        <!-- 质量评估Agent（手绘框） -->
        <rect x="820" y="200" width="150" height="60" rx="7" ry="6" fill="rgba(74,111,165,0.15)" stroke="#4a6fa5" stroke-width="2" stroke-dasharray="2,3"/>
        <text x="895" y="230" text-anchor="middle" fill="#e0e0e0" font-size="13">质量评估</text>
        <text x="895" y="248" text-anchor="middle" fill="#a0a0b0" font-size="11">Agent</text>
        
        <!-- 箭头5：质量评估 → 输出资源 -->
        <path d="M 820 230 L 750 230" stroke="#4a6fa5" stroke-width="2" fill="none" stroke-dasharray="4,3"/>
        <polygon points="750,225 740,230 750,235" fill="#4a6fa5"/>
        
        <!-- 输出资源（手绘框） -->
        <rect x="560" y="200" width="150" height="60" rx="6" ry="8" fill="rgba(74,111,165,0.25)" stroke="#4a6fa5" stroke-width="2.5"/>
        <text x="635" y="230" text-anchor="middle" fill="#e0e0e0" font-size="13">输出资源</text>
        <text x="635" y="248" text-anchor="middle" fill="#a0a0b0" font-size="11">个性化学习内容</text>
        
        <!-- 反馈箭头：质量评估 → 资源生成（循环优化） -->
        <path d="M 820 230 Q 780 150 800 100" stroke="#3d5a8a" stroke-width="1.5" fill="none" stroke-dasharray="3,4"/>
        <text x="780" y="140" text-anchor="middle" fill="#a0a0b0" font-size="10">循环优化</text>
        
        <!-- 底部说明文字 -->
        <text x="450" y="320" text-anchor="middle" fill="#a0a0b0" font-size="12">基于学生画像的多智能体协同工作流程</text>
        
        <!-- 手绘装饰箭头 -->
        <path d="M 100 350 L 200 350 L 220 340" stroke="#4a6fa5" stroke-width="1.5" fill="none" stroke-dasharray="2,2" opacity="0.5"/>
        <text x="120" y="370" fill="#a0a0b0" font-size="11" opacity="0.6">系统工作流程</text>
        
        <!-- 手绘圆圈装饰 -->
        <circle cx="850" y="400" r="30" fill="none" stroke="#4a6fa5" stroke-width="1" stroke-dasharray="3,2" opacity="0.3"/>
        <circle cx="100" y="450" r="20" fill="none" stroke="#3d5a8a" stroke-width="1" stroke-dasharray="2,3" opacity="0.3"/>
    </svg>
    """
    st.markdown(flowchart_svg, unsafe_allow_html=True)

# ========================
# 页面配置
# ========================
st.set_page_config(
    page_title="A3 多智能体自适应学习系统",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ========================
# 模拟数据
# ========================
SAMPLE_PROFILE = {
    "name": "张三",
    "student_id": "202301001",
    "major": "计算机科学与技术",
    "knowledge_mastery": {
        "Python基础": 0.92,
        "数据结构": 0.78,
        "机器学习": 0.65,
        "深度学习": 0.42,
        "自然语言处理": 0.30,
        "强化学习": 0.18,
    },
    "learning_style": "视觉型 + 动手实践",
    "weak_points": ["深度学习", "自然语言处理", "强化学习"],
    "strong_points": ["Python基础", "数据结构"],
    "total_study_hours": 128,
    "completed_courses": 6,
    "current_level": "中级",
}

SAMPLE_RESOURCES = {
    "深度学习基础": {
        "concept_map": "# 深度学习基础\n\n## 核心概念\n\n### 神经网络\n- **定义**：受人脑神经元结构启发的人工神经网络（ANN）\n- **基本单元**：神经元（Neuron）\n  - 输入加权求和：`z = w₁x₁ + w₂x₂ + ... + b`\n  - 激活函数：`a = σ(z)`\n\n### 激活函数\n| 函数名 | 公式 | 特点 |\n|--------|------|------|\n| Sigmoid | `σ(x) = 1/(1+e⁻ˣ)` | 输出(0,1)，易梯度消失 |\n| Tanh | `tanh(x) = (eˣ-e⁻ˣ)/(eˣ+e⁻ˣ)` | 输出(-1,1)，零中心化 |\n| ReLU | `max(0, x)` | 计算快，易死神经元 |\n| Leaky ReLU | `max(0.01x, x)` | 解决死神经元问题 |\n\n### 前向传播与反向传播\n1. **前向传播**：输入 → 隐藏层 → 输出层 → 预测值\n2. **损失计算**：`Loss = L(ŷ, y)`\n3. **反向传播**：链式法则计算梯度\n4. **参数更新**：`w ← w - η·∇w`\n\n## 代码实践\n\n```python\nimport torch\nimport torch.nn as nn\n\nclass SimpleNN(nn.Module):\n    def __init__(self):\n        super().__init__()\n        self.fc1 = nn.Linear(784, 128)\n        self.fc2 = nn.Linear(128, 64)\n        self.fc3 = nn.Linear(64, 10)\n        self.relu = nn.ReLU()\n    \n    def forward(self, x):\n        x = self.relu(self.fc1(x))\n        x = self.relu(self.fc2(x))\n        return self.fc3(x)\n\nmodel = SimpleNN()\nprint(model)\n```\n\n## 练习题\n\n1. 计算题：一个3层全连接网络，输入层784维，隐藏层128维和64维，输出层10维，求总参数量。\n2. 简答题：ReLU相比Sigmoid有哪些优势？\n3. 编程题：用PyTorch实现一个2层神经网络完成MNIST分类。\n",
        "summary": "## 📝 知识摘要\n\n### 一、神经网络基础\n- 神经元是神经网络的基本单元\n- 每层神经元通过权重连接，形成层级结构\n- 深度神经网络 = 多个隐藏层堆叠\n\n### 二、关键组件\n1. **权重初始化**：Xavier / He 初始化\n2. **激活函数**：引入非线性\n3. **损失函数**：衡量预测与真实值差距\n4. **优化器**：SGD、Adam、RMSProp\n\n### 三、训练流程\n```\n初始化参数 → 前向传播 → 计算损失 → 反向传播 → 更新参数 → 重复\n```\n\n### 四、常见网络结构\n| 结构 | 适用场景 |\n|------|----------|\n| CNN | 图像识别、计算机视觉 |\n| RNN/LSTM | 序列数据、时间序列 |\n| Transformer | NLP、多模态 |\n| GNN | 图数据、社交网络 |\n",
    },
    "机器学习算法": {
        "concept_map": "# 机器学习核心算法\n\n## 监督学习\n\n### 线性回归\n- **假设函数**：`hθ(x) = θ₀ + θ₁x`\n- **损失函数（MSE）**：`J(θ) = 1/2m Σ(hθ(x⁽ⁱ⁾) - y⁽ⁱ⁾)²`\n- **闭式解**：`θ = (XᵀX)⁻¹Xᵀy`\n\n### 逻辑回归\n- **Sigmoid**：`hθ(x) = 1 / (1 + e⁻ᵒ)`\n- **交叉熵损失**：`J(θ) = -1/m Σ[y⁽ⁱ⁾log(h⁽ⁱ⁾) + (1-y⁽ⁱ⁾)log(1-h⁽ⁱ⁾)]`\n\n### 决策树\n```python\nfrom sklearn.tree import DecisionTreeClassifier\n\nmodel = DecisionTreeClassifier(\n    max_depth=5,\n    min_samples_split=10,\n    criterion='gini'\n)\nmodel.fit(X_train, y_train)\n```\n\n## 无监督学习\n\n### K-Means聚类\n1. 随机初始化K个质心\n2. 将每个样本分配到最近的质心\n3. 重新计算每个簇的质心\n4. 重复步骤2-3直到收敛\n\n### 主成分分析（PCA）\n- 目标：找到数据方差最大的方向\n- 步骤：中心化 → 计算协方差矩阵 → 特征值分解 → 取前K个特征向量\n",
        "summary": "## 📝 知识摘要\n\n### 监督学习三大类\n1. **回归**：预测连续值（线性回归、岭回归）\n2. **分类**：预测离散标签（逻辑回归、SVM、决策树）\n3. **排序**：预测顺序关系（RankNet、LambdaMART）\n\n### 无监督学习两类\n1. **聚类**：K-Means、DBSCAN、层次聚类\n2. **降维**：PCA、t-SNE、AutoEncoder\n\n### 模型评估指标\n| 任务 | 指标 |\n|------|------|\n| 回归 | MSE、MAE、R² |\n| 二分类 | Accuracy、Precision、Recall、F1、AUC |\n| 多分类 | 混淆矩阵、宏/微平均F1 |\n",
    },
}

SAMPLE_LEARNING_PATH = [
    {"day": 1, "title": "Python基础复习", "status": "completed", "score": 95, "duration": "2h"},
    {"day": 2, "title": "数据结构：链表与树", "status": "completed", "score": 88, "duration": "3h"},
    {"day": 3, "title": "数据结构：图与排序", "status": "completed", "score": 82, "duration": "3h"},
    {"day": 4, "title": "机器学习：线性回归", "status": "completed", "score": 90, "duration": "2.5h"},
    {"day": 5, "title": "机器学习：逻辑回归与SVM", "status": "completed", "score": 85, "duration": "3h"},
    {"day": 6, "title": "机器学习：决策树与集成学习", "status": "in_progress", "score": None, "duration": "3h"},
    {"day": 7, "title": "深度学习：神经网络基础", "status": "pending", "score": None, "duration": "3h"},
    {"day": 8, "title": "深度学习：CNN卷积神经网络", "status": "pending", "score": None, "duration": "4h"},
    {"day": 9, "title": "深度学习：RNN与LSTM", "status": "pending", "score": None, "duration": "4h"},
    {"day": 10, "title": "自然语言处理：词向量与Embedding", "status": "pending", "score": None, "duration": "3h"},
    {"day": 11, "title": "自然语言处理：Seq2Seq与Attention", "status": "pending", "score": None, "duration": "4h"},
    {"day": 12, "title": "自然语言处理：Transformer架构", "status": "pending", "score": None, "duration": "4h"},
    {"day": 13, "title": "强化学习：马尔可夫决策过程", "status": "pending", "score": None, "duration": "3h"},
    {"day": 14, "title": "强化学习：Q-Learning与Policy Gradient", "status": "pending", "score": None, "duration": "4h"},
]

SAMPLE_QUALITY_REPORTS = [
    {
        "resource_name": "深度学习基础概念图",
        "type": "概念知识地图",
        "overall_score": 92,
        "dimensions": {
            "内容准确性": 95,
            "知识结构完整性": 90,
            "难度适配度": 88,
            "表达清晰度": 94,
            "互动性": 85,
        },
        "strengths": ["数学公式规范", "代码示例完整", "层次结构清晰"],
        "weaknesses": ["缺少习题答案", "高级概念解释较简略"],
        "suggestion": "建议增加梯度消失/爆炸的直观示意图，补充Batch Normalization相关内容。",
    },
    {
        "resource_name": "机器学习算法摘要",
        "type": "知识摘要",
        "overall_score": 88,
        "dimensions": {
            "内容准确性": 92,
            "知识结构完整性": 85,
            "难度适配度": 90,
            "表达清晰度": 87,
            "互动性": 78,
        },
        "strengths": ["公式标注清晰", "代码示例简洁", "评估指标表格直观"],
        "weaknesses": ["无监督学习部分偏少", "缺少算法对比维度"],
        "suggestion": "建议补充各算法的适用场景对比表，增加异常检测相关内容。",
    },
    {
        "resource_name": "神经网络前向传播练习题",
        "type": "练习题",
        "overall_score": 85,
        "dimensions": {
            "内容准确性": 88,
            "知识结构完整性": 82,
            "难度适配度": 90,
            "表达清晰度": 84,
            "互动性": 80,
        },
        "strengths": ["难度梯度合理", "计算题设计巧妙"],
        "weaknesses": ["缺少编程题提示", "无自动判分说明"],
        "suggestion": "建议为每个编程题提供测试用例和评分标准。",
    },
]

KNOWLEDGE_POINTS = [
    "Python基础", "数据结构", "算法设计",
    "机器学习基础", "监督学习", "无监督学习",
    "深度学习基础", "CNN", "RNN与LSTM",
    "自然语言处理", "Transformer", "强化学习",
]
RESOURCE_TYPES = ["概念知识地图", "知识摘要", "练习题", "案例分析", "代码实践"]


# ========================
# 工具函数
# ========================
def simulate_streaming(text: str, placeholder, delay: float = 0.008):
    """模拟流式输出，逐字显示文本"""
    displayed = ""
    for char in text:
        displayed += char
        placeholder.markdown(displayed + "▌")
        time.sleep(delay)
    placeholder.markdown(displayed)


def get_mastery_color(score: float) -> str:
    """根据掌握度返回颜色"""
    if score >= 0.8:
        return "#28a745"
    elif score >= 0.6:
        return "#ffc107"
    else:
        return "#dc3545"


def get_status_icon(status: str) -> str:
    """根据状态返回图标"""
    return {"completed": "✅", "in_progress": "🔄", "pending": "⏳"}.get(status, "❓")


# ========================
# 会话状态初始化
# ========================
def init_session_state():
    if "page" not in st.session_state:
        st.session_state.page = "首页"
    if "profile" not in st.session_state:
        st.session_state.profile = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "generated_resource" not in st.session_state:
        st.session_state.generated_resource = None
    if "resource_loading" not in st.session_state:
        st.session_state.resource_loading = False

init_session_state()


# ========================
# 页面：首页
# ========================
def render_home():
    # 顶部横幅 - 使用手绘图标
    st.markdown(
        f"""
        <div style='text-align:center; padding: 20px 0 10px 0; position: relative;'>
            <div style='position: absolute; top: 10px; right: 20px; opacity: 0.3;'>
                {render_icon('bulb', 32)}
            </div>
            <h1 style='display:inline;'>{render_icon('robot', 36)} A3 多智能体自适应学习系统</h1>
            <p style='font-size: 18px; color: #a0a0b0; margin-top: 10px;'>
                Adaptive Agent-based Learning System
            </p>
            <div style='margin-top: 15px;'>
                <svg viewBox="0 0 200 20" width="200" height="20">
                    <path d="M0 10 Q25 5, 50 10 T100 10 T150 10 T200 10" stroke="#4a6fa5" stroke-width="1.5" fill="none" stroke-linecap="round" opacity="0.5"/>
                </svg>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    hand_drawn_divider()

    # 项目介绍 - 改写文案，删除空话
    with st.container():
        st.markdown('<div class="card-uneven-1">', unsafe_allow_html=True)
        hand_drawn_title("项目介绍", "book_open", 28)
        st.markdown(
            """
            **A3（Adaptive Agent-based Learning System）** 是一个基于多智能体协作的个性化自适应学习平台。
            
            **具体实现方式：**
            - 系统包含4个专用Agent：画像构建、资源生成、路径规划、质量评估
            - 每个Agent负责特定的子任务，通过消息传递实现协同工作
            - 学生画像包含6个维度：知识基础、认知风格、兴趣点、薄弱点、学习进度、学习目标
            """
        )
        st.markdown('</div>', unsafe_allow_html=True)

    hand_drawn_divider()

    # 三大特色卡片 - 使用不同的card-uneven类
    st.markdown('<h2 class="hand-drawn-underline">核心特色</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card-uneven-1">', unsafe_allow_html=True)
        st.markdown(f"### {render_icon('brain', 24)} 智能画像构建", unsafe_allow_html=True)
        st.markdown(
            """
            **具体功能：**
            - 基于6维度学生画像（知识基础、认知风格、兴趣点、薄弱点、学习进度、学习目标）
            - 支持对话式交互和一键加载示例
            - 动态更新知识点掌握度（0-1区间）
            """
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card-uneven-2">', unsafe_allow_html=True)
        st.markdown(f"### {render_icon('books', 24)} 自适应资源生成", unsafe_allow_html=True)
        st.markdown(
            """
            **支持生成：**
            - 概念知识地图、知识摘要、练习题
            - 案例分析、代码实践
            - 基于知识图谱的个性化内容
            
            **技术实现：**
            - 基于模板的内容生成（演示版）
            - 支持5种资源类型选择
            - 难度等级可调（入门-高级）
            """
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="card-uneven-3">', unsafe_allow_html=True)
        st.markdown(f"### {render_icon('map', 24)} 动态路径规划", unsafe_allow_html=True)
        st.markdown(
            """
            **实现方式：**
            - 基于知识图谱拓扑排序
            - 确保先修知识点优先学习
            - 动态调整学习顺序
            
            **展示功能：**
            - 14天学习路径时间轴
            - 实时进度追踪
            - 知识点掌握度总览
            """
        )
        st.markdown('</div>', unsafe_allow_html=True)

    hand_drawn_divider()

    # 系统架构 - 用SVG手绘流程图替换文字描述
    st.markdown('<h2 class="hand-drawn-underline">系统架构</h2>', unsafe_allow_html=True)
    
    # 使用手绘风格流程图
    render_handdrawn_flowchart()
    
    # 技术栈说明
    with st.expander("技术栈详情", expanded=False):
        arch_col1, arch_col2 = st.columns(2)
        with arch_col1:
            st.markdown(f"#### {render_icon('gear', 20)} 多智能体分工", unsafe_allow_html=True)
            st.markdown(
                """
                - **画像构建 Agent**：分析学习行为，更新学生画像
                - **资源生成 Agent**：根据需求生成个性化学习内容
                - **路径规划 Agent**：制定并动态调整学习路径
                - **质量评估 Agent**：多维度评估生成资源的质量
                """
            )
        with arch_col2:
            st.markdown(f"#### {render_icon('settings', 20)} 技术栈", unsafe_allow_html=True)
            st.markdown(
                """
                - **前端**：Streamlit（本应用）
                - **Agent框架**：[可接入 LangChain / AutoGen]
                - **知识图谱**：[可接入 Neo4j]
                - **向量数据库**：[可接入 Chroma / FAISS]
                - **LLM**：[可接入 讯飞星火 / OpenAI / 本地模型]
                """
            )

    hand_drawn_divider()

    # 使用说明 - 添加手绘编号图标
    st.markdown('<h2 class="hand-drawn-underline">使用说明</h2>', unsafe_allow_html=True)
    
    steps = [
        (f"{render_icon('nav_brain', 24)}", "**构建学习画像**", "进入「学习画像构建」页面，通过对话或一键加载示例画像。"),
        (f"{render_icon('nav_book', 24)}", "**生成学习资源**", "进入「资源生成」页面，选择知识点和资源类型，点击生成。"),
        (f"{render_icon('nav_map', 24)}", "**查看学习路径**", "进入「学习路径规划」页面，查看个性化学习路径与进度。"),
        (f"{render_icon('nav_check', 24)}", "**评估资源质量**", "进入「质量评估」页面，查看生成资源的质量评分与改进建议。"),
    ]
    
    for icon, title, desc in steps:
        st.markdown(f"#### {icon} {title}\n{desc}", unsafe_allow_html=True)
        st.markdown("<div style='margin-left: 40px; border-left: 2px dashed #3a4a6a; height: 20px;'></div>", unsafe_allow_html=True)

    hand_drawn_divider()
    
    # 页面底部信息 - 添加开发环境、适用场景、项目局限性
    st.markdown('<h2 class="hand-drawn-underline">关于本项目</h2>', unsafe_allow_html=True)
    
    info_col1, info_col2, info_col3 = st.columns(3)
    
    with info_col1:
        st.markdown('<div class="card-uneven-1">', unsafe_allow_html=True)
        st.markdown(f"#### {render_icon('gear', 20)} 开发环境", unsafe_allow_html=True)
        st.markdown(
            """
            - Python 3.10+
            - Streamlit 1.30+
            - 讯飞星火API
            - 主要依赖：pandas, numpy
            """
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with info_col2:
        st.markdown('<div class="card-uneven-2">', unsafe_allow_html=True)
        st.markdown(f"#### {render_icon('bulb', 20)} 适用场景", unsafe_allow_html=True)
        st.markdown(
            """
            - 高校个性化学习
            - 自适应教育平台
            - 智能 tutoring 系统
            - 在线教育内容生成
            """
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with info_col3:
        st.markdown('<div class="card-uneven-3">', unsafe_allow_html=True)
        st.markdown(f"#### {render_icon('warning', 20)} 项目局限性", unsafe_allow_html=True)
        st.markdown(
            """
            - 当前为演示版本，部分功能使用模拟数据
            - 真实部署需要接入讯飞星火API密钥
            - 知识库内容需要持续更新和维护
            - 多智能体协同效率有待进一步优化
            """
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(
        "<div style='text-align:center; color:#6a6a7a; font-size:13px; margin-top: 30px;'>"
        "A3 MultiAgent Learning System · 期末答辩演示版 · 2025"
        "</div>",
        unsafe_allow_html=True,
    )


# ========================
# 页面：学习画像构建
# ========================
def render_profile():
    # 标题区域 - 使用手绘图标
    st.markdown(
        f"""
        <div style='display: flex; align-items: center; margin-bottom: 20px;'>
            <div style='margin-right: 10px;'>{render_icon('brain', 32)}</div>
            <h2 style='margin: 0;'>学习画像构建</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("通过对话式交互，系统将逐步了解你的学习情况，构建个性化学习画像。")
    hand_drawn_divider()

    # 左侧：对话区  右侧：画像卡片
    left, right = st.columns([1, 1])

    with left:
        st.markdown(f"#### {render_icon('chat', 20)} 对话交互", unsafe_allow_html=True)
        
        # 一键加载示例
        if st.button(f"{render_icon('lightning', 16)} 一键加载示例画像（演示用）", use_container_width=True):
            st.session_state.profile = SAMPLE_PROFILE.copy()
            st.session_state.chat_history = [
                {"role": "assistant", "content": f"你好 {SAMPLE_PROFILE['name']}！我已经为你构建了学习画像，请在右侧查看详情。"},
                {"role": "assistant", "content": "根据你的学习记录，我发现你在**深度学习**和**自然语言处理**方面还有提升空间，建议优先学习这两个模块！"},
            ]
            st.rerun()

        # 对话历史
        chat_container = st.container(height=350, border=True)
        with chat_container:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.chat_message("user").write(msg["content"])
                else:
                    st.chat_message("assistant").write(msg["content"])

        # 用户输入
        user_input = st.chat_input("输入你的学习内容、目标或困惑...")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            # 模拟 AI 回复
            with st.spinner("AI 正在分析..."):
                time.sleep(1)
                # 简单模拟回复逻辑
                if "深度学习" in user_input or "神经网络" in user_input:
                    reply = "深度学习确实是难点！建议你先巩固**神经网络基础**，再学习CNN和RNN。我可以帮你生成相关的学习资源 📚"
                elif "机器学习" in user_input:
                    reply = "机器学习是AI的基础，你已经掌握了线性回归和决策树，接下来可以深入学习集成学习（Random Forest、XGBoost）🎯"
                elif "NLP" in user_input or "自然语言" in user_input:
                    reply = "NLP是当前最热门的方向！建议学习路径：词向量 → Seq2Seq → Attention → Transformer → LLM。要不要我帮你规划具体路径？🗺️"
                else:
                    reply = f"收到：「{user_input}」\n我已经记录到你的学习画像中，会继续优化对你的学习建议 🤖"
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

    with right:
        st.markdown(f"#### {render_icon('card', 20)} 学生画像卡片", unsafe_allow_html=True)
        
        if st.session_state.profile is None:
            st.info("👆 请通过对话交互构建画像，或点击「一键加载示例画像」查看演示效果。")
        else:
            p = st.session_state.profile
            
            # 卡片式展示 - 使用手绘边框样式
            st.markdown('<div class="card-uneven-1">', unsafe_allow_html=True)
            st.markdown(f"#### {render_icon('user', 20)} {p['name']}", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            c1.markdown(f"**学号**：{p['student_id']}")
            c1.markdown(f"**专业**：{p['major']}")
            c2.markdown(f"**学习级别**：{p['current_level']}")
            c2.markdown(f"**累计学习**：{p['total_study_hours']} 小时")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 知识点掌握度 - 使用自定义CSS样式
            st.markdown('<div class="card-uneven-2">', unsafe_allow_html=True)
            st.markdown(f"#### {render_icon('chart_bar', 20)} 知识点掌握度", unsafe_allow_html=True)
            
            for kp, score in p["knowledge_mastery"].items():
                col_label, col_bar = st.columns([1, 2])
                col_label.markdown(f"**{kp}**")
                # 使用自定义进度条样式
                col_bar.progress(score, text=f"{score*100:.0f}%")
            st.markdown('</div>', unsafe_allow_html=True)
            
            col3, col4 = st.columns(2)
            
            with col3:
                st.markdown('<div class="card-uneven-1">', unsafe_allow_html=True)
                st.markdown(f"#### {render_icon('check', 20)} 优势领域", unsafe_allow_html=True)
                for sp in p["strong_points"]:
                    st.markdown(f"✅ {sp}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col4:
                st.markdown('<div class="card-uneven-2">', unsafe_allow_html=True)
                st.markdown(f"#### {render_icon('warning', 20)} 待提升", unsafe_allow_html=True)
                for wp in p["weak_points"]:
                    st.markdown(f"🔴 {wp}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="card-uneven-3">', unsafe_allow_html=True)
            st.markdown(f"#### {render_icon('pencil', 20)} 学习风格", unsafe_allow_html=True)
            st.info(f"**{p['learning_style']}**")
            st.markdown('</div>', unsafe_allow_html=True)


# ========================
# 页面：资源生成
# ========================
def render_resource():
    # 标题区域
    st.markdown(
        f"""
        <div style='display: flex; align-items: center; margin-bottom: 20px;'>
            <div style='margin-right: 10px;'>{render_icon('books', 32)}</div>
            <h2 style='margin: 0;'>学习资源生成</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("选择知识点与资源类型，系统将为你生成个性化学习资源。")
    hand_drawn_divider()

    # 配置区 - 添加手绘图标
    st.markdown('<div class="card-uneven-1">', unsafe_allow_html=True)
    st.markdown(f"#### {render_icon('gear', 20)} 生成配置", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        selected_kp = st.selectbox(f"{render_icon('target', 16)} 选择知识点", KNOWLEDGE_POINTS, index=6)
    with c2:
        selected_type = st.selectbox(f"{render_icon('file', 16)} 资源类型", RESOURCE_TYPES, index=0)
    with c3:
        difficulty = st.select_slider(
            f"{render_icon('chart_line', 16)} 难度等级",
            options=["入门", "基础", "中级", "进阶", "高级"],
            value="中级",
        )

    col_btn1, col_btn2 = st.columns([1, 3])
    with col_btn1:
        generate_clicked = st.button(f"{render_icon('lightning', 16)} 生成资源", use_container_width=True, type="primary")
    with col_btn2:
        if st.button(f"{render_icon('download', 16)} 加载示例资源（演示用）", use_container_width=True):
            key = selected_kp if selected_kp in SAMPLE_RESOURCES else "深度学习基础"
            st.session_state.generated_resource = {
                "title": f"{selected_kp} - {selected_type}",
                "content": SAMPLE_RESOURCES.get(key, SAMPLE_RESOURCES["深度学习基础"]).get(
                    "concept_map" if selected_type == "概念知识地图" else "summary",
                    SAMPLE_RESOURCES["深度学习基础"]["concept_map"]
                ),
                "meta": {
                    "知识点": selected_kp,
                    "类型": selected_type,
                    "难度": difficulty,
                    "生成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "字数": random.randint(800, 2000),
                },
            }
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

    # 生成逻辑
    if generate_clicked:
        st.session_state.resource_loading = True
        # 模拟生成过程
        status_placeholder = st.empty()
        with status_placeholder:
            with st.spinner("🔍 正在分析知识点结构..."):
                time.sleep(0.8)
            with st.spinner("🧠 正在检索相关知识..."):
                time.sleep(0.8)
            with st.spinner("✍️ 正在生成学习内容..."):
                time.sleep(1.0)
            with st.spinner("🔎 正在进行质量自检..."):
                time.sleep(0.6)
        status_placeholder.empty()

        # 生成结果
        key = selected_kp if selected_kp in SAMPLE_RESOURCES else "深度学习基础"
        st.session_state.generated_resource = {
            "title": f"{selected_kp} - {selected_type}",
            "content": SAMPLE_RESOURCES.get(key, SAMPLE_RESOURCES["深度学习基础"]).get(
                "concept_map" if selected_type == "概念知识地图" else "summary",
                SAMPLE_RESOURCES["深度学习基础"]["concept_map"]
            ),
            "meta": {
                "知识点": selected_kp,
                "类型": selected_type,
                "难度": difficulty,
                "生成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "字数": random.randint(800, 2000),
            },
        }
        st.session_state.resource_loading = False
        st.success("✅ 资源生成成功！")
        st.rerun()

    # 展示区
    hand_drawn_divider()
    st.markdown(f"#### {render_icon('book_open', 20)} 生成结果", unsafe_allow_html=True)

    if st.session_state.generated_resource is None:
        st.info("请在上方选择知识点和资源类型，然后点击「生成资源」按钮。")
        return

    res = st.session_state.generated_resource

    # 元信息
    meta_col1, meta_col2, meta_col3, meta_col4, meta_col5 = st.columns(5)
    meta_col1.metric("知识点", res["meta"]["知识点"])
    meta_col2.metric("资源类型", res["meta"]["类型"])
    meta_col3.metric("难度", res["meta"]["难度"])
    meta_col4.metric("字数", res["meta"]["字数"])
    meta_col5.metric("生成时间", res["meta"]["生成时间"])

    hand_drawn_divider()

    # 内容展示（支持流式输出演示）
    tab1, tab2 = st.tabs([f"{render_icon('file', 16)} 内容预览", f"{render_icon('download', 16)} 导出"])

    with tab1:
        # 流式输出演示按钮
        if st.button("▶️ 演示流式输出"):
            stream_placeholder = st.empty()
            simulate_streaming(res["content"], stream_placeholder, delay=0.003)
        else:
            st.markdown(res["content"], unsafe_allow_html=True)

    with tab2:
        st.markdown(f"#### {render_icon('download', 20)} 导出选项", unsafe_allow_html=True)
        export_col1, export_col2, export_col3 = st.columns(3)
        with export_col1:
            st.download_button(
                f"{render_icon('file', 16)} 导出为 Markdown",
                res["content"],
                file_name=f"{res['meta']['知识点']}_{res['meta']['类型']}.md",
                mime="text/markdown",
                use_container_width=True,
            )
        with export_col2:
            st.button(f"{render_icon('books', 16)} 导出为 PDF", use_container_width=True, disabled=True)
        with export_col3:
            st.button(f"{render_icon('link', 16)} 导出为 HTML", use_container_width=True, disabled=True)


# ========================
# 页面：学习路径规划
# ========================
def render_path():
    # 标题区域
    st.markdown(
        f"""
        <div style='display: flex; align-items: center; margin-bottom: 20px;'>
            <div style='margin-right: 10px;'>{render_icon('map', 32)}</div>
            <h2 style='margin: 0;'>个性化学习路径规划</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("基于你的学习画像，系统为你规划了最优学习路径，并根据学习进度动态调整。")
    hand_drawn_divider()

    # 路径概览
    total = len(SAMPLE_LEARNING_PATH)
    completed = sum(1 for x in SAMPLE_LEARNING_PATH if x["status"] == "completed")
    in_progress = sum(1 for x in SAMPLE_LEARNING_PATH if x["status"] == "in_progress")
    pending = total - completed - in_progress
    avg_score = sum(x["score"] for x in SAMPLE_LEARNING_PATH if x["score"] is not None) / max(completed, 1)

    overview_col1, overview_col2, overview_col3, overview_col4 = st.columns(4)
    overview_col1.metric("总节点数", total)
    overview_col2.metric("已完成", f"{completed}/{total}", f"{completed/total*100:.0f}%")
    overview_col3.metric("进行中", in_progress)
    overview_col4.metric("平均成绩", f"{avg_score:.1f}")

    hand_drawn_divider()

    # 时间轴展示 - 用HTML/CSS实现手绘风格时间轴
    st.markdown(f"#### {render_icon('clock', 20)} 学习路径时间轴", unsafe_allow_html=True)
    
    # 使用自定义CSS样式的时间轴
    timeline_html = """
    <div style='padding: 20px; max-height: 500px; overflow-y: auto;'>
    """
    
    for i, node in enumerate(SAMPLE_LEARNING_PATH):
        icon = get_status_icon(node["status"])
        color = {"completed": "#28a745", "in_progress": "#007bff", "pending": "#6c757d"}[node["status"]]
        
        score_str = f" 🏆 {node['score']}分" if node["score"] else ""
        status_text = {"completed": "已完成", "in_progress": "进行中", "pending": "待学习"}[node["status"]]
        
        timeline_html += f"""
        <div style='display:flex; align-items:center; margin-bottom:12px;'>
            <div style='
                width:36px; height:36px; border-radius:50%;
                background:{color}; color:white;
                display:flex; align-items:center; justify-content:center;
                font-size:16px; flex-shrink:0;
            '>{icon}</div>
            <div style='margin-left:12px; flex-grow:1;'>
                <span style='font-weight:bold;'>{node['title']}</span>
                <span style='color:#999; font-size:12px; margin-left:8px;'>Day {node['day']} · {node['duration']}{score_str}</span>
            </div>
            <div style='
                background:{color}22; color:{color};
                padding:2px 10px; border-radius:12px;
                font-size:12px; font-weight:bold;
            '>{status_text}</div>
        </div>
        """
        
        if i < len(SAMPLE_LEARNING_PATH) - 1:
            timeline_html += "<div style='margin-left:17px; border-left:2px dashed #3a4a6a; height:16px;'></div>"
    
    timeline_html += "</div>"
    
    st.markdown(timeline_html, unsafe_allow_html=True)

    hand_drawn_divider()

    # 进度详情表格
    st.markdown(f"#### {render_icon('chart_bar', 20)} 学习进度详情", unsafe_allow_html=True)
    df = pd.DataFrame(SAMPLE_LEARNING_PATH)
    df["状态"] = df["status"].map({"completed": "✅ 已完成", "in_progress": "🔄 进行中", "pending": "⏳ 待学习"})
    df["成绩"] = df["score"].apply(lambda x: f"{x} 分" if x else "-")
    st.dataframe(
        df[["day", "title", "状态", "成绩", "duration"]].rename(
            columns={"day": "Day", "title": "学习内容", "duration": "预计时长"}
        ),
        use_container_width=True,
        hide_index=True,
    )

    hand_drawn_divider()

    # 知识掌握度雷达图（用文字模拟）
    st.markdown(f"#### {render_icon('target', 20)} 当前知识掌握度总览", unsafe_allow_html=True)
    progress_cols = st.columns(len(SAMPLE_PROFILE["knowledge_mastery"]))
    for i, (kp, score) in enumerate(SAMPLE_PROFILE["knowledge_mastery"].items()):
        with progress_cols[i]:
            st.metric(kp, f"{score*100:.0f}%")
            st.progress(score)


# ========================
# 页面：质量评估
# ========================
def render_quality():
    # 标题区域
    st.markdown(
        f"""
        <div style='display: flex; align-items: center; margin-bottom: 20px;'>
            <div style='margin-right: 10px;'>{render_icon('check', 32)}</div>
            <h2 style='margin: 0;'>资源质量评估</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("质量评估 Agent 对生成的学习资源进行多维度自动评估，确保资源质量。")
    hand_drawn_divider()

    # 选择报告
    report_titles = [r["resource_name"] for r in SAMPLE_QUALITY_REPORTS]
    selected_report_name = st.selectbox(f"{render_icon('file', 16)} 选择评估报告", report_titles)
    report = next(r for r in SAMPLE_QUALITY_REPORTS if r["resource_name"] == selected_report_name)

    # 总评分卡片 - 使用手绘边框
    st.markdown('<div class="card-uneven-1">', unsafe_allow_html=True)
    st.markdown(f"#### {render_icon('file', 20)} {report['resource_name']}", unsafe_allow_html=True)
    st.caption(f"资源类型：{report['type']}")

    score_col, detail_col = st.columns([1, 2])

    with score_col:
        # 大号评分展示
        score_color = "#28a745" if report["overall_score"] >= 90 else "#ffc107" if report["overall_score"] >= 75 else "#dc3545"
        st.markdown(
            f"""
            <div style='
                text-align:center;
                padding:30px 0;
                border-radius:16px;
                background:{score_color}15;
                border:2px solid {score_color}44;
            '>
                <div style='font-size:48px; font-weight:bold; color:{score_color};'>{report['overall_score']}</div>
                <div style='color:#666; margin-top:4px;'>综合质量评分</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with detail_col:
        st.markdown(f"#### {render_icon('chart_line', 20)} 多维度评分", unsafe_allow_html=True)
        for dim, score in report["dimensions"].items():
            col_label, col_bar, col_val = st.columns([1.5, 2, 0.5])
            col_label.markdown(f"**{dim}**")
            # 使用自定义进度条样式
            col_bar.progress(score / 100)
            col_val.markdown(f"`{score}`")

    st.markdown('</div>', unsafe_allow_html=True)

    hand_drawn_divider()

    # 评估详情
    col_feedback1, col_feedback2 = st.columns(2)

    with col_feedback1:
        st.markdown('<div class="card-uneven-2">', unsafe_allow_html=True)
        st.markdown(f"#### {render_icon('check', 20)} 优势分析", unsafe_allow_html=True)
        for adv in report["strengths"]:
            st.markdown(f"- {adv}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_feedback2:
        st.markdown('<div class="card-uneven-3">', unsafe_allow_html=True)
        st.markdown(f"#### {render_icon('warning', 20)} 待改进", unsafe_allow_html=True)
        for weak in report["weaknesses"]:
            st.markdown(f"- {weak}")
        st.markdown('</div>', unsafe_allow_html=True)

    hand_drawn_divider()

    # 改进建议
    st.markdown('<div class="card-uneven-1">', unsafe_allow_html=True)
    st.markdown(f"#### {render_icon('bulb', 20)} 改进建议", unsafe_allow_html=True)
    st.info(report["suggestion"])
    st.markdown('</div>', unsafe_allow_html=True)

    hand_drawn_divider()

    # 所有报告对比
    st.markdown(f"#### {render_icon('chart_bar', 20)} 评估报告总览", unsafe_allow_html=True)
    compare_data = []
    for r in SAMPLE_QUALITY_REPORTS:
        compare_data.append({
            "资源名称": r["resource_name"],
            "类型": r["type"],
            "综合评分": r["overall_score"],
            "内容准确性": r["dimensions"]["内容准确性"],
            "结构完整性": r["dimensions"]["知识结构完整性"],
            "难度适配": r["dimensions"]["难度适配度"],
            "表达清晰": r["dimensions"]["表达清晰度"],
            "互动性": r["dimensions"]["互动性"],
        })
    df_reports = pd.DataFrame(compare_data)
    st.dataframe(df_reports, use_container_width=True, hide_index=True)

    # 评分趋势（柱状图）
    hand_drawn_divider()
    st.markdown(f"#### {render_icon('chart_line', 20)} 质量评分对比图", unsafe_allow_html=True)
    chart_data = pd.DataFrame({
        "资源": [r["resource_name"][:8] + "..." for r in SAMPLE_QUALITY_REPORTS],
        "综合评分": [r["overall_score"] for r in SAMPLE_QUALITY_REPORTS],
    })
    st.bar_chart(chart_data.set_index("资源"))


# ========================
# 主函数 / 路由
# ========================
PAGES = {
    "首页": render_home,
    "学习画像构建": render_profile,
    "资源生成": render_resource,
    "学习路径规划": render_path,
    "质量评估": render_quality,
}

# Sidebar 导航 - 使用手绘图标
with st.sidebar:
    st.markdown(
        f"""
        <div style='text-align:center; padding:10px 0 20px 0;'>
            <h2>{render_icon('robot', 28)} A3</h2>
            <p style='color:#a0a0b0; font-size:13px;'>多智能体自适应学习系统</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    hand_drawn_divider()

    # 导航菜单 - 使用手绘图标
    selected_page = st.radio(
        "导航菜单",
        list(PAGES.keys()),
        index=list(PAGES.keys()).index(st.session_state.page),
        label_visibility="collapsed",
    )
    st.session_state.page = selected_page

    hand_drawn_divider()

    # Sidebar 底部信息 - 改为操作引导文字
    st.markdown("### ℹ️ 操作引导")
    
    # 根据当前页面显示不同的引导提示
    if st.session_state.profile is None:
        st.markdown(
            f"""
            {render_icon('bulb', 16)} **建议：**
            先构建学习画像，系统才能为你推荐合适的学习资源
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            {render_icon('check', 16)} **学习画像：** 已构建
            
            {render_icon('bulb', 16)} **建议：**
            可以尝试生成不同知识点的学习资源
            """,
            unsafe_allow_html=True,
        )
    
    if st.session_state.generated_resource is None:
        st.markdown(
            f"""
            {render_icon('books', 16)} **生成资源：** 未生成
            
            {render_icon('arrow_right', 16)} 前往「资源生成」页面生成学习资源
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            {render_icon('books', 16)} **生成资源：** 已生成
            """,
            unsafe_allow_html=True,
        )

    hand_drawn_divider()
    
    # 底部装饰
    st.markdown(
        "<div style='text-align:center; color:#6a6a7a; font-size:11px;'>"
        f"{render_icon('info', 14)} A3 MultiAgent Learning System<br>期末答辩演示版"
        "</div>",
        unsafe_allow_html=True,
    )

# 渲染选中页面
PAGES[selected_page]()
