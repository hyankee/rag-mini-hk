---
doc_id: hk-jobs-llm-001
title: 香港 LLM 应用开发岗位能力画像
industry: cross_industry
region: Hong Kong
source_type: synthetic_brief
license: CC BY 4.0
version: 2026-11-06
disclaimer: 学习用岗位画像，非实时招聘信息；真实 JD 请查 JobsDB、LinkedIn 和公司官网。
---

# 香港 LLM 应用开发岗位能力画像

## 1. 先区分三类岗位

“LLM 开发”不是一个单一岗位。香港招聘市场里常见的相关职位可以粗分为三类：

1. **LLM 应用开发**：把模型 API、知识库、业务系统组合成可用产品，重点是 Python、API、RAG、结构化输出和评测。
2. **数据 / AI 分析**：用 SQL、Python 和模型做分析、报表、预测和业务洞察，重点是数据和业务理解。
3. **AI 产品 / 解决方案**：把客户需求翻译成方案，协调开发和交付，重点是行业知识、沟通和项目管理。

转行初期不必只盯“LLM Engineer”这个标题。`AI Application Developer`、`Data Analyst (AI)`、`Solution Consultant`、`AI Product Analyst` 都可能是入口。

## 2. 常见岗位标题（非实时招聘）

- AI Application Developer
- LLM Application Engineer
- RAG Engineer / Knowledge Base Engineer
- AI Solutions Consultant
- Data Analyst (AI / Automation)
- AI Product Analyst / Product Manager
- Conversation / Prompt Designer
- Digital Transformation Analyst

这些标题在不同公司含义不同；看 JD 时重点看“实际要做什么”，不要只看 title。

## 3. 核心技能

### 3.1 必须能写代码

- Python：函数、文件、JSON、异常、类型标注、虚拟环境。
- HTTP / API：请求、响应、鉴权、错误码、超时。
- 结构化输出：Pydantic 模型、字段约束、校验失败处理。
- Git：提交、分支、回滚的基本操作。

### 3.2 RAG 与 LLM 应用

- 文档解析：PDF、Markdown、TXT、HTML。
- 切片：按标题/段落切，保留元数据和来源。
- 检索：关键词、BM25、embedding、top-k。
- 上下文组装：把问题和片段放进 prompt，控制长度。
- 引用：回答必须能追溯到 `doc_id + 章节`。
- 拒答：没有证据时返回“资料中无法确认”。
- 评测：准备问题集，记录检索命中、回答正确、引用正确。

### 3.3 数据与工程基础

- SQL：查询、聚合、连接。
- 基础后端：至少能写一个简单的 API 或命令行工具。
- 数据处理：CSV/Excel、清洗、去重、字段映射。
- 日志与错误处理：能定位失败发生在哪一步。

### 3.4 行业与软技能

- 能把业务问题拆成“数据、流程、模型、人工复核”。
- 能向非技术同事解释模型能做什么、不能做什么。
- 能写清楚的 README、评测报告和限制说明。

## 4. 香港本地求职渠道

- JobsDB Hong Kong：https://hk.jobsdb.com/
- LinkedIn Jobs：https://www.linkedin.com/jobs/
- HKSTP：https://www.hkstp.org/
- Cyberport：https://www.cyberport.hk/
- 公司官网 Careers 页面

搜索关键词建议：

```text
AI application developer Hong Kong
LLM RAG Hong Kong
Python AI analyst Hong Kong
data analyst AI Hong Kong
digital transformation analyst Hong Kong
```

## 5. 转行者的作品集

比“上过什么课”更有说服力的是 2–3 个能演示的项目：

1. **结构化抽取**：把工程文本变成经过 Pydantic 校验的 JSON，带错误处理和测试。
2. **行业 RAG**：用本语料库做一个带来源的问答系统，能拒答无证据问题。
3. **评测报告**：10–20 道题，记录检索命中率、回答正确率和失败原因。

每个项目 README 写清楚：解决什么问题、怎么运行、用了什么模型、哪里会失败、下一步怎么改。

## 6. 从建筑行业转行的定位建议

不要把自己包装成“纯算法工程师”。更可信的定位是：

> 懂建筑/工程文档和流程，能用 Python、API 和 RAG 把文档变成可检索、可校验、可追溯的 AI 应用。

优先目标行业：

1. 绿色建筑 / PropTech / 设施管理（行业优势最大）。
2. 金融科技合规文档、物流单证、医疗非临床文档（文档密集，RAG 价值高）。
3. 旅游、创意媒体（更看重内容和运营，技术深度要求不同）。

## 7. 核验提示

本文件是能力画像，不是实时招聘信息，也不包含薪资承诺。真实岗位要求、薪资和工作地点请以招聘网站和公司 JD 为准。
