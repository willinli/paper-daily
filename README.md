# Paper Daily

一个基于 GitHub Pages + GitHub Actions 的每日论文雷达。它会按研究方向检索 arXiv，计算匹配度，并生成中文创新总结与论文链接。

## 工作方式

- GitHub Actions 每天北京时间 06:00 自动运行，也可以手动运行。
- 默认读取 `config/interests.json`。
- 如果存在标题为 `Research Interests` 的 open issue，则优先读取 issue 中的 JSON 配置。
- 生成结果写入 `web/data/papers.json`，并部署 `web/` 到 GitHub Pages。
- 每次更新会合并上一轮数据，历史论文只保留匹配度 `high` 和 `medium` 的条目，`low` 不跨天保留。
- 默认最多保存 300 篇论文或 5 MiB 数据；超过限制时会先删除 `low`，再按论文发布时间从旧到新删除。
- 页面端只负责展示和筛选，不保存密钥，也不调用模型 API。

## 配置研究方向

在仓库 Issues 中新建一个标题为 `Research Interests` 的 issue，使用模板中的 JSON。修改 issue 后会自动触发更新。

每个方向包含：

```json
{
  "id": "llm_low_precision_quantization",
  "name": "大模型低精度量化",
  "description": "方向描述",
  "keywords": ["LLM quantization", "INT4"],
  "arxiv_categories": ["cs.CL", "cs.LG"]
}
```

## 接入模型 API

高质量中文创新总结建议接入模型 API。项目支持 DeepSeek、OpenAI，或其他 OpenAI-compatible `/chat/completions` 服务。

在 GitHub 仓库设置中添加 Secrets：

- DeepSeek：添加 `DEEPSEEK_API_KEY`
- OpenAI：添加 `OPENAI_API_KEY`
- 通用兼容服务：添加 `LLM_API_KEY`

可选 Variables：

- `LLM_BASE_URL`，例如 `https://api.deepseek.com/v1`
- `LLM_MODEL`，例如 `deepseek-chat`
- `LLM_CONCURRENCY`，模型并发数，默认 `2`
- `MAX_STORED_PAPERS`，最多保存论文数，默认 `300`，设为 `0` 表示不按数量裁剪
- `MAX_DATA_BYTES`，`web/data/papers.json` 最大字节数，默认 `5242880`，设为 `0` 表示不按大小裁剪

`LLM_BASE_URL` 和 `LLM_MODEL` 也可以放在 Secrets 中；workflow 会优先读取 Variables，未设置时读取 Secrets。

不配置 API key 时，项目仍会正常抓取论文，但中文总结会退化为基础摘要。

## 启用 GitHub Pages

进入仓库：

```text
Settings -> Pages -> Build and deployment -> Source -> GitHub Actions
```

保存后，手动运行一次 `Paper Daily` workflow。

## 本地运行

```bash
python scripts/collect_papers.py --days 7 --max-per-topic 10 --max-summaries 5
python -m http.server 8000 --directory web
```

打开：

```text
http://localhost:8000
```

## 数据源

当前版本使用 arXiv API。后续可以扩展 Semantic Scholar、OpenReview、Papers with Code、GitHub Trending 和 Hugging Face Papers。
