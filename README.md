# RAG Mini HK

![tests](https://github.com/hyankee/rag-mini-hk/actions/workflows/test.yml/badge.svg)

一个可以直接运行、也方便讲清楚的小型 RAG 工程：

**Markdown 文档 → 按章节切片 → BGE 向量化 → Chroma 余弦检索 → 带引用的回答 / 无答案拒答 → 固定题目评测 → FastAPI 单页 Demo**

项目面向香港行业与 LLM 应用岗位的学习语料，重点不是堆框架，而是把检索、引用、拒答和评测这条链路做完整、可复现、可解释。

## 项目亮点

- **章节级切片**：保留 `doc_id`、标题、行业、版本、章节等元数据，引用能落到具体章节。
- **本地向量检索**：`BAAI/bge-small-zh-v1.5` + Chroma 持久化集合，使用 cosine 距离。
- **带引用生成**：只把 top-k 证据交给 DeepSeek，要求每个事实性结论标注 `[S1]` 这类证据编号。
- **无答案拒答**：提示词明确要求证据不足时输出“资料中无法确认”，而不是用模型常识补全。
- **可复现评测**：固定 12 道题、固定 `top_k=3`，同时报告严格命中与宽松命中。
- **无密钥也能演示**：未配置 `DEEPSEEK_API_KEY` 时自动进入 retrieval-only 模式，仍然展示检索证据和相似度。
- **17 个离线测试**：切片、证据拼接、引用提取、拒答、评测状态和 API 合约都有覆盖。

## 架构

```text
data/docs/*.md
      │  front matter + 二级标题
      ▼
app/chunking.py  ──►  55 个 section chunks
      │
      ▼
BGE embedding（归一化向量）
      │
      ▼
Chroma persistent collection（cosine）
      │  top-k
      ▼
app/answer.py  ──►  DeepSeek 生成带 [S1] 引用的回答
      │                 └─ 证据不足 → “资料中无法确认”
      ▼
FastAPI + 单页 UI
```

## 快速开始

要求：Python 3.11+、[uv](https://docs.astral.sh/uv/)、首次运行时可访问 Hugging Face 下载 embedding 模型。

```bash
cd rag-mini-hk
uv sync

# 可选：配置生成模型；不配置也能跑 retrieval-only 模式
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY

# 建索引（首次会加载 BGE 模型）
uv run python scripts/build_index.py --reset

# 启动页面
uv run uvicorn app.api:app --reload
```

打开 <http://127.0.0.1:8000>，输入问题即可查看回答、引用和 top-k 证据。

## 命令行使用

```bash
# 只检索，不调用大模型
uv run python scripts/ask.py "物流行业哪些单证适合做结构化抽取？" --retrieval-only

# 调用已配置的 DeepSeek
uv run python scripts/ask.py "医疗行业使用 LLM 时要注意什么？"

# 重新跑 12 题检索评测
uv run python scripts/evaluate_retrieval.py --output reports/retrieval-eval.md

# 跑测试
uv run pytest
```

## 检索评测

固定 12 道题，其中 9 道有明确期望章节，3 道用于检查“资料中没有答案”的场景。`top_k=3` 的结果：

| 指标 | 结果 |
|---|---|
| 严格命中（期望章节全部进入 top-k） | **7 / 9** |
| 宽松命中（至少一个期望章节进入 top-k） | **8 / 9** |

完整逐题结果见 [`reports/retrieval-eval.md`](reports/retrieval-eval.md)。

两个已知问题没有被隐藏：

- **Q7**：创意媒体行业的问题没有把第 4 节排进 top-3，说明“行业 + 泛化问法”仍会被第 1～3 节吸走。
- **Q12**：PDPO 只命中医疗文档的第 6 节，第 2 节未进入 top-3，属于部分命中。

这份报告只评检索，不声称回答质量；回答是否正确、引用是否真的支持结论，仍需人工核对。

## 关键设计取舍

**为什么按二级标题切片，而不是固定字符数？**

语料本身就是“行业概览 + 分主题章节”的结构。按章节切可以把一个完整主题留在同一个 chunk 里，引用时也能直接定位到“某文档第几节”，比固定窗口更容易解释和排查。

**为什么用 Chroma 的 cosine？**

BGE 输出已经归一化，cosine 与点积排序等价；Chroma 直接存向量和元数据，适合这个规模的数据，也避免自己维护索引文件。55 个 chunk 的量级不需要更复杂的检索基础设施。

**为什么要有引用和拒答？**

RAG 的价值不是“让模型多说”，而是“让回答可追溯，并且在证据不足时停下来”。提示词把证据和问题分开，要求结论后标注证据编号；没有检索结果时直接拒答。

**为什么保留 retrieval-only 模式？**

招聘现场不一定有可用 API key。没有 key 时仍然能展示完整的检索链路、相似度和证据片段，不会因为外部服务不可用而让 Demo 失效。

## 目录结构

```text
app/
  chunking.py      Markdown front matter 解析与章节切片
  store.py         Chroma 集合、BGE 编码、top-k 检索
  retrieval.py     检索接口
  answer.py        证据拼接、提示词、引用解析、拒答
  evaluation.py    固定题目评测与 Markdown 报告
  api.py           FastAPI 路由
  web.py           单页 Demo UI
data/
  docs/            8 份合成行业语料
  questions.json   12 道固定评测题
scripts/
  build_index.py
  ask.py
  evaluate_retrieval.py
tests/             离线单元测试与 API 测试
reports/           检索评测报告
```

## 数据说明

`data/docs/` 是学习用合成整理，不是官方原文，也不是实时招聘信息。涉及法规、牌照、医疗、薪资和岗位数量时，只做学习提示，不构成法律、医疗或职业建议。真实信息请查政府、监管机构、JobsDB、LinkedIn 和公司官网。

语料以 CC BY 4.0 方式标注，详见 [`data/SOURCES.md`](data/SOURCES.md)。

## 局限与下一步

- 当前只做了 section-level dense retrieval，没有混合关键词检索，也没有 reranker。
- 拒答依赖生成模型遵循提示词；retrieval-only 模式只展示证据，不判断证据是否足够。
- 评测集只有 12 题，适合做回归基线，不足以证明泛化能力。
- 下一步可以加入 BM25 + 向量混合检索、cross-encoder rerank、引用支持度检查和更多真实文档。

## 面试时怎么讲

1. **先讲问题**：行业资料分散，直接问大模型容易得到没有出处的答案。
2. **再讲链路**：章节切片保留元数据 → BGE 归一化向量 → Chroma cosine top-k → 证据编号 → 生成时强制引用。
3. **讲一个失败案例**：Q7 没有命中第 4 节，说明泛化问法会被行业背景段落抢占；这是下一步加 hybrid retrieval / rerank 的依据。
4. **讲边界**：合成语料、12 题小评测、拒答仍依赖模型遵循提示词，不把 Demo 说成生产系统。
