# Retrieval Evaluation

- Fixed `top_k=3`; 12 questions.
- Strict hit@k: **7/9**
- Loose hit@k: **8/9**

| ID | Question | Top-k sources | Status |
|---|---|---|---|
| Q1 | 香港金融科技行业常见的三类岗位是什么？ | [S1] hk-fintech-001 §1；[S2] hk-fintech-001 §3；[S3] hk-fintech-001 §2 | 是（1/1） |
| Q2 | 物流行业哪些单证适合做结构化抽取？ | [S1] hk-logistics-001 §5；[S2] hk-logistics-001 §4；[S3] hk-logistics-001 §3 | 是（1/1） |
| Q3 | 旅游行业如何用 RAG 做多语言客服？ | [S1] hk-tourism-001 §6；[S2] hk-tourism-001 §3；[S3] hk-tourism-001 §4 | 是（1/1） |
| Q4 | 绿色建筑行业与建筑背景的转行切入点是什么？ | [S1] hk-greenbuilding-001 §1；[S2] hk-greenbuilding-001 §5；[S3] hk-greenbuilding-001 §4 | 是（1/1） |
| Q5 | 医疗行业使用 LLM 时，为什么不能把病人资料随意外发？ | [S1] hk-healthcare-001 §4；[S2] hk-healthcare-001 §2；[S3] hk-healthcare-001 §6 | 是（2/2） |
| Q6 | LLM 应用开发岗位需要哪些核心技能？ | [S1] hk-jobs-llm-001 §1；[S2] hk-jobs-llm-001 §3；[S3] hk-jobs-llm-001 §7 | 是（1/1） |
| Q7 | 创意媒体行业里，LLM 更适合做哪些工作？ | [S1] hk-creative-001 §1；[S2] hk-creative-001 §2；[S3] hk-creative-001 §3 | 否（0/1） |
| Q8 | 香港 2026 年 LLM 工程师的平均月薪是多少？ | [S1] hk-jobs-llm-001 §1；[S2] hk-greenbuilding-001 §2；[S3] hk-jobs-llm-001 §6 | — |
| Q9 | 香港哪一家银行在 2026 年招聘最多的 RAG 工程师？ | [S1] hk-fintech-001 §7；[S2] hk-jobs-transition-001 §1；[S3] hk-jobs-transition-001 §6 | — |
| Q10 | 2030 年香港绿色建筑行业的岗位数量会增长多少？ | [S1] hk-greenbuilding-001 §7；[S2] hk-greenbuilding-001 §1；[S3] hk-greenbuilding-001 §2 | — |
| Q11 | `hk-fintech-001` 这份文档的标题、行业和版本是什么？ | [S1] hk-fintech-001 §7；[S2] hk-creative-001 §7；[S3] hk-fintech-001 §1 | 是（文档命中） |
| Q12 | “PDPO”在医疗行业文档中是如何被提及的？ | [S1] hk-healthcare-001 §6；[S2] hk-healthcare-001 §4；[S3] hk-healthcare-001 §3 | 部分（1/2） |

> Strict means every expected section is in top-k. Loose means at least one is.
> This report evaluates retrieval only; it does not claim answer quality.
