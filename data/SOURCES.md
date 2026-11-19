# 来源、许可证与扩展入口

本文件记录“去哪里找真实材料”，以及把新材料加入语料库时的检查清单。

## 用户提供的公共数据集入口

1. Awesome Public Datasets  
   https://github.com/awesomedata/awesome-public-datasets  
   用途：按主题寻找公开数据集；使用前逐个检查数据集自己的许可证。

2. 腾讯云开发者社区文章：公开数据集整理  
   https://cloud.tencent.com/developer/article/2256189  
   用途：中文入口和数据集索引；文章本身不是数据许可证，仍要回到原始数据集页面确认。

## 香港官方与公共数据入口

以下是入口级链接，适合后续扩展语料；具体文件的使用条款以网站为准。

| 来源 | 链接 | 适合补充的主题 |
|---|---|---|
| 香港政府开放数据 | https://data.gov.hk/ | 交通、天气、人口、公共设施、统计 |
| 政府统计处 | https://www.censtatd.gov.hk/ | 人口、就业、行业统计 |
| 香港金融管理局 | https://www.hkma.gov.hk/ | 金融科技、虚拟银行、支付、合规 |
| Invest Hong Kong | https://www.investhk.gov.hk/ | 行业概览、营商环境、外来投资 |
| 香港科技园 | https://www.hkstp.org/ | 创科生态、园区公司、招聘入口 |
| Cyberport | https://www.cyberport.hk/ | 数码科技、初创、招聘入口 |
| 医院管理局 | https://www.ha.org.hk/ | 医疗体系、服务、公开资料 |
| 环境保护署 | https://www.epd.gov.hk/ | 环保政策、空气质量、减废 |
| 机电工程署 | https://www.emsd.gov.hk/ | 建筑机电、能源效率、规管 |
| 房屋署 | https://www.housingauthority.gov.hk/ | 公营房屋、建筑与物业管理 |
| 机场管理局 | https://www.hongkongairport.com/ | 航空货运、机场运营 |
| 港铁 | https://www.mtr.com.hk/ | 铁路运营、资产维护、客流 |

## 真实岗位检索入口

| 入口 | 链接 | 用法 |
|---|---|---|
| JobsDB Hong Kong | https://hk.jobsdb.com/ | 搜索 `AI application developer`、`LLM`、`RAG`、`data analyst` |
| LinkedIn Jobs | https://www.linkedin.com/jobs/ | 搜索岗位 + Hong Kong；看技能要求 |
| HKSTP 招聘 | https://www.hkstp.org/ | 园区公司招聘入口 |
| Cyberport 招聘 | https://www.cyberport.hk/ | 初创与数码科技岗位 |
| 公司官网 Careers | 各公司官网 | 以官网 JD 为准，避免二手转载 |

## 加入真实材料时的检查清单

每加入一份真实文档，至少记录：

- `source_url`：原始链接
- `publisher`：发布机构
- `access_date`：访问日期
- `license`：许可证或使用条款
- `version`：版本号或发布日期
- `doc_id`：语料库内唯一编号
- `notes`：解析是否可靠、是否有表格/扫描件/缺页

## 许可证提醒

- 政府网站、招聘网站、公司 JD、PDF 规范通常有各自的使用条款；不要默认可以整篇转载。
- 学习项目里可以保留链接、标题、摘要和短引用；大段正文应先确认许可。
- 公开数据集要看数据集页面的 license，而不是看聚合列表的 license。
- 不确定时，优先使用“自写摘要 + 原始链接”，不要把全文复制进仓库。
