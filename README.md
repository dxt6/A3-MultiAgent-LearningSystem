# A3 多智能体学习系统

基于讯飞星火大模型的多智能体协同学习系统，支持个性化学习路径规划、知识图谱构建与学习报告生成。

## 项目结构

```
A3-MultiAgent-LearningSystem/
├── agents/              # 多智能体模块
├── data/                # 数据存储目录
├── exports/             # 导出文件目录
├── generators/          # 内容生成器
├── sample_profiles/     # 示例学习档案
├── utils/               # 工具函数
├── config.py            # 配置管理模块
├── requirements.txt     # Python 依赖
└── .env                # 环境变量（需自行创建）
```

## 环境要求

- Python 3.9+
- 讯飞星火大模型 API 账号（可选，支持模拟模式）

## 安装步骤

1. 克隆项目并进入目录：
   ```bash
   cd A3-MultiAgent-LearningSystem
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 配置环境变量：
   ```bash
   # 复制模板文件
   cp .env.example .env

   # 编辑 .env，填入你的 API 密钥
   # 若无需真实 API，保持 MOCK_MODE=True 即可
   ```

## 运行方法

```bash
# 启动 Streamlit 应用
streamlit run app.py
```

> 若 `app.py` 入口文件名称不同，请根据实际情况调整命令。

## 模拟模式

设置 `MOCK_MODE=True`（默认）可在不调用真实 API 的情况下运行系统，方便本地开发与演示。

## 主要依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| streamlit | 1.30.0 | Web 应用框架 |
| requests | 2.31.0 | HTTP 请求 |
| websocket-client | 1.7.0 | WebSocket 通信 |
| pandas | 2.1.4 | 数据处理 |
| plotly | 5.18.0 | 交互式图表 |
| networkx | 3.2.1 | 知识图谱 |
| python-docx | 1.1.0 | Word 报告生成 |
| openpyxl | 3.1.2 | Excel 文件处理 |
