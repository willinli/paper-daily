---
name: Research Interests
about: 使用可视化页面生成或更新个性化文献检索配置
title: Research Interests
labels: config
assignees: ''
---

请先打开文献库中的“⚙ 设置”，在可视化页面增删研究方向和关键词。

把页面生成的 JSON 粘贴到下面，并保持 Issue 标题为 `Research Interests`。

```json
{
  "sources": [
    { "type": "europe_pmc", "name": "PubMed · Europe PMC" },
    { "type": "openalex", "name": "OpenAlex" },
    { "type": "crossref", "name": "Crossref" },
    { "type": "arxiv", "name": "arXiv" }
  ],
  "conference_sources": {
    "enabled": false,
    "include_default_venues": false,
    "venues": []
  },
  "topics": [
    {
      "id": "glp1_obesity_pharmacotherapy",
      "name": "GLP-1药物与肥胖治疗",
      "description": "关注GLP-1受体激动剂及多靶点肠促胰素药物的减重疗效、安全性与代谢结局。",
      "keywords": [
        "GLP-1 receptor agonist",
        "semaglutide obesity",
        "tirzepatide obesity",
        "liraglutide obesity",
        "retatrutide obesity"
      ],
      "exclude_keywords": ["type 1 diabetes"],
      "europe_pmc_query": "(TITLE_ABS:\"GLP-1 receptor agonist\" OR TITLE_ABS:semaglutide OR TITLE_ABS:tirzepatide) AND (TITLE_ABS:obesity OR TITLE_ABS:\"weight loss\")",
      "arxiv_categories": ["q-bio.BM", "q-bio.TO"]
    }
  ]
}
```
