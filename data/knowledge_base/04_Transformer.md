# Transformer

## 1. 自注意力机制（Self-Attention）

自注意力机制是 Transformer 的核心创新，它允许模型在处理每个位置时，能够关注输入序列中的所有其他位置，从而捕获全局依赖关系。

### 注意力机制原理

注意力机制本质上是一种相似度计算。对于输入序列中的每个元素，自注意力计算它与其他所有元素之间的关联程度，并根据关联程度加权求和得到新的表示。

### 缩放点积注意力（Scaled Dot-Product Attention）

\[
\text{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{softmax}\left(\frac{\mathbf{Q}\mathbf{K}^T}{\sqrt{d_k}}\right)\mathbf{V}
\]

其中：
- \(\mathbf{Q} \in \mathbb{R}^{n \times d_k}\)（Query）：查询矩阵
- \(\mathbf{K} \in \mathbb{R}^{n \times d_k}\)（Key）：键矩阵
- \(\mathbf{V} \in \mathbb{R}^{n \times d_v}\)（Value）：值矩阵
- \(n\)：序列长度
- \(d_k\)：键的维度（用于缩放，防止点积结果过大导致 softmax 梯度消失）

```python
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    缩放点积注意力
    Q, K, V: (batch, seq_len, d_model)
    mask: 可选，用于遮挡某些位置（如 padding 或未来位置）
    """
    d_k = Q.size(-1)
    # 计算注意力分数
    scores = torch.matmul(Q, K.transpose(-2, -1)) / torch.sqrt(torch.tensor(d_k, dtype=torch.float))
    # (batch, seq_len, seq_len)
    
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
    
    # softmax 归一化
    attn_weights = F.softmax(scores, dim=-1)
    # 加权求和
    output = torch.matmul(attn_weights, V)
    return output, attn_weights

# 示例
batch_size, seq_len, d_model = 2, 5, 64
Q = torch.randn(batch_size, seq_len, d_model)
K = torch.randn(batch_size, seq_len, d_model)
V = torch.randn(batch_size, seq_len, d_model)

output, attn = scaled_dot_product_attention(Q, K, V)
print(f"输出形状: {output.shape}")          # (2, 5, 64)
print(f"注意力权重形状: {attn.shape}")      # (2, 5, 5)
print(f"注意力权重（第一行）:\n{attn[0, 0].detach().numpy()}")
```

### 注意力权重的可解释性

注意力权重直观地反映了序列中不同位置之间的关联程度。例如，在机器翻译任务中，可以看到模型在生成目标词时，主要关注源句子中对应的词。

## 2. 多头注意力（Multi-Head Attention）

多头注意力通过并行运行多个注意力头，使模型能够同时关注来自不同表示子空间的信息，增强了模型的表达能力。

### 公式

\[
\text{MultiHead}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h)\mathbf{W}^O
\]

\[
\text{head}_i = \text{Attention}(\mathbf{Q}\mathbf{W}_i^Q, \mathbf{K}\mathbf{W}_i^K, \mathbf{V}\mathbf{W}_i^V)
\]

其中，\(\mathbf{W}_i^Q \in \mathbb{R}^{d_{model} \times d_k}\)，\(\mathbf{W}_i^K \in \mathbb{R}^{d_{model} \times d_k}\)，\(\mathbf{W}_i^V \in \mathbb{R}^{d_{model} \times d_v}\)，\(\mathbf{W}^O \in \mathbb{R}^{hd_v \times d_{model}}\)。

通常设置 \(h=8\)，\(d_k = d_v = d_{model}/h\)。

```python
class MultiHeadAttention(nn.Module):
    """多头注意力机制实现"""
    def __init__(self, d_model, num_heads):
        super(MultiHeadAttention, self).__init__()
        assert d_model % num_heads == 0, "d_model 必须能被 num_heads 整除"
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # 所有头的 Q, K, V 投影矩阵
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
    
    def split_heads(self, x):
        """将最后一维分割成 (num_heads, d_k)"""
        batch_size, seq_len, _ = x.size()
        x = x.view(batch_size, seq_len, self.num_heads, self.d_k)
        return x.transpose(1, 2)  # (batch, num_heads, seq_len, d_k)
    
    def combine_heads(self, x):
        """合并多头"""
        batch_size, _, seq_len, _ = x.size()
        x = x.transpose(1, 2).contiguous()
        return x.view(batch_size, seq_len, self.d_model)
    
    def forward(self, Q, K, V, mask=None):
        batch_size = Q.size(0)
        
        # 线性投影
        Q = self.split_heads(self.W_q(Q))
        K = self.split_heads(self.W_k(K))
        V = self.split_heads(self.W_v(V))
        
        # 计算注意力
        scores = torch.matmul(Q, K.transpose(-2, -1)) / torch.sqrt(
            torch.tensor(self.d_k, dtype=torch.float)
        )
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        attn_weights = F.softmax(scores, dim=-1)
        output = torch.matmul(attn_weights, V)
        
        # 合并多头
        output = self.combine_heads(output)
        output = self.W_o(output)
        return output, attn_weights

# 示例
mha = MultiHeadAttention(d_model=512, num_heads=8)
x = torch.randn(4, 20, 512)  # (batch=4, seq_len=20, d_model=512)
output, attn = mha(x, x, x)  # 自注意力（Q=K=V）
print(f"多头注意力输出形状: {output.shape}")  # (4, 20, 512)
```

## 3. 位置编码（Positional Encoding）

由于 Transformer 完全基于注意力机制，没有循环或卷积结构，无法捕获序列中的位置信息。位置编码通过向输入嵌入中添加位置信息，使模型能够区分序列中词的顺序。

### 正弦/余弦位置编码

Transformer 原论文提出了一种固定的位置编码方案：

\[
PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d_{model}}}\right)
\]

\[
PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d_{model}}}\right)
\]

其中 \(pos\) 是位置，\(i\) 是维度索引。

```python
def positional_encoding(seq_len, d_model):
    """
    正弦/余弦位置编码
    返回形状: (1, seq_len, d_model)
    """
    pe = np.zeros((seq_len, d_model))
    position = np.arange(seq_len)[:, np.newaxis]
    div_term = np.exp(np.arange(0, d_model, 2) * -(np.log(10000.0) / d_model))
    
    pe[:, 0::2] = np.sin(position * div_term)
    pe[:, 1::2] = np.cos(position * div_term)
    return torch.FloatTensor(pe).unsqueeze(0)  # (1, seq_len, d_model)

# 可视化位置编码
import matplotlib.pyplot as plt

seq_len, d_model = 50, 128
pe = positional_encoding(seq_len, d_model)
plt.figure(figsize=(10, 6))
plt.imshow(pe.squeeze(0).T, cmap='RdBu', aspect='auto')
plt.xlabel('Position')
plt.ylabel('Dimension')
plt.title('Positional Encoding')
plt.colorbar()
plt.show()
```

### 可学习位置编码

BERT 等模型使用可学习的位置编码，通过训练自动学习位置表示。

```python
class LearnablePositionalEncoding(nn.Module):
    """可学习位置编码"""
    def __init__(self, max_len, d_model):
        super(LearnablePositionalEncoding, self).__init__()
        self.pe = nn.Embedding(max_len, d_model)
    
    def forward(self, x):
        """
        x: (batch, seq_len, d_model)
        """
        seq_len = x.size(1)
        positions = torch.arange(seq_len, device=x.device).unsqueeze(0)
        return x + self.pe(positions)

# 在 Transformer 中使用
d_model = 512
max_len = 512
embed = nn.Embedding(30000, d_model)
pos_enc = LearnablePositionalEncoding(max_len, d_model)

x = torch.randint(0, 30000, (8, 100))  # (batch=8, seq_len=100)
embeddings = embed(x)                    # (8, 100, 512)
embeddings_with_pos = pos_enc(embeddings) # 添加位置编码
```

## 4. BERT 与 GPT

### BERT（Bidirectional Encoder Representations from Transformers）

BERT 是基于 Transformer 编码器（Encoder）的预训练语言模型，通过双向上下文建模，在多种 NLP 任务上取得了突破性性能。

#### 预训练任务

1. **Masked Language Modeling（MLM）**：随机掩盖输入中 15% 的词，让模型预测被掩盖的词。
2. **Next Sentence Prediction（NSP）**：判断两个句子是否连续。

```python
from transformers import BertTokenizer, BertModel

# 使用预训练 BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertModel.from_pretrained('bert-base-chinese')

text = "深度学习是人工智能的核心技术。"
encoded = tokenizer(text, return_tensors='pt')
output = model(**encoded)
print(f"最后一层隐藏状态形状: {output.last_hidden_state.shape}")
# (1, seq_len, 768)
```

### GPT（Generative Pre-trained Transformer）

GPT 是基于 Transformer 解码器（Decoder）的自回归语言模型，通过预测下一个词进行预训练，擅长文本生成任务。

#### GPT 系列演进

- **GPT-1**（2018）：1.17 亿参数，无监督预训练 + 有监督微调
- **GPT-2**（2019）：15 亿参数，零样本学习
- **GPT-3**（2020）：1750 亿参数，少样本/零样本学习
- **GPT-4**（2023）：多模态输入，推理能力大幅提升

```python
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# 使用预训练 GPT-2 进行文本生成
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

prompt = "Artificial intelligence will"
input_ids = tokenizer.encode(prompt, return_tensors='pt')
output = model.generate(input_ids, max_length=50, num_return_sequences=1)
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(f"生成文本: {generated_text}")
```

### BERT vs GPT 对比

| 特性 | BERT | GPT |
|------|------|-----|
| 架构 | Transformer Encoder | Transformer Decoder |
| 注意力 | 双向自注意力 | 单向（因果）自注意力 |
| 预训练任务 | MLM + NSP | 自回归语言模型 |
| 擅长任务 | 理解类（分类、问答、NER） | 生成类（对话、续写） |
| 上下文 | 同时看到左右上下文 | 只能看到左侧上下文 |

### Transformer 的完整结构

完整的 Transformer 模型由编码器堆（Encoder Stack）和解码器堆（Decoder Stack）组成：

- **编码器**：多头自注意力 + 前馈网络 + 残差连接 + 层归一化
- **解码器**：掩码多头自注意力 + 编码器-解码器注意力 + 前馈网络

```python
class TransformerBlock(nn.Module):
    """Transformer Encoder Block"""
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super(TransformerBlock, self).__init__()
        self.attention = MultiHeadAttention(d_model, num_heads)
        self.norm1 = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Linear(d_ff, d_model)
        )
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, mask=None):
        # 多头自注意力 + 残差连接
        attn_out, _ = self.attention(x, x, x, mask)
        x = self.norm1(x + self.dropout(attn_out))
        # 前馈网络 + 残差连接
        ff_out = self.ff(x)
        x = self.norm2(x + self.dropout(ff_out))
        return x
```

## 小结

Transformer 通过自注意力机制捕获全局依赖，通过多头注意力增强表达能力，通过位置编码引入序列顺序信息。基于 Transformer 的 BERT 和 GPT 分别开创了预训练语言模型的两个重要方向：双向编码和自回归生成。Transformer 已成为自然语言处理乃至整个深度学习领域的基石架构。
