<!-- generated from data/trends.db by scripts/render.py, do not edit by hand -->
# Relevant models

> This page is rendered from a SQLite database (`data/trends.db`) by GitHub Actions. See [How this repo works](#how-this-repo-works).

AI models worth knowing about if you build with AI, and why each one matters.

**Last updated:** 11 Nov 2026 (Prague)  
**How the ranking works:** what matters to a working AI developer: capability, whether you can call it through an API today, price for the performance, and how new it is. Vendor benchmark claims are the vendors' own.

## What changed lately

- **Claude Fable 5.2 / Mythos 5.2 (9 Nov):** Anthropic's top model got faster (up to 30% vs 5.1) and cheaper ($8/$40). A swarm of about 1,000 Fable agents formalized Fermat's Last Theorem in Lean in 30 hours.
- **Muse Ember (9 Nov):** Meta's small agent workhorse costs $0.10/$0.50, has a 1M-token context, and Meta claims it beats Haiku 5.5 and GPT-6 Luna on intelligence per dollar.
- **Inkling 2 Small (5 Nov):** Thinking Machines' 594B-total/17B-active MoE. It runs on Tinker now; the Apache 2.0 weights are promised after safety testing and were not on Hugging Face as of 11 Nov.
- **Gated cyber models:** GPT-6 Cyber (5 Nov) and Gemini 4 Carbon (28 Oct) are both out, but only to vetted defenders for now.
- **Kimi K3.1 Pro open weights (2 Nov):** a 2.8T-parameter MoE that you can download, competitive with closed frontier models on Moonshot's own tables.

## Ranked

| # | Model | Vendor | Released | Best for | Why you should care | Source |
|---|---|---|---|---|---|---|
| 1 | Claude Fable 5.2 | Anthropic | 9 Nov 2026 | Mathematicians, the hardest open-ended technical work | It's the model for heavy reasoning and math: 1,000 Fable agents formalized Fermat's Last Theorem in Lean in 30 h (Opus 5.5 managed 26% in 18 h), and it solved two open black-hole physics problems. Same model as Mythos 5.2 but with cyber/bio safeguards. Up to 30% faster than 5.1, $8/$40 per M tokens (fast mode $16/$80), `claude-fable-5-2`, also on AWS, Google Cloud and Azure. | [anthropic.com](https://www.anthropic.com/claude-fable-and-mythos-5-2) |
| 2 | Claude Opus 5.5 | Anthropic | 22 Sep 2026 | Everyday coding and agent work | Anthropic's recommended daily driver: about Fable 5.1 level at $4/$20 with $0.20 cache reads, and 40% cheaper to run than Opus 5. | [anthropic.com](https://www.anthropic.com/claude-opus-5-5) |
| 3 | GPT-6.1 Sol | OpenAI | 29 Sep 2026 | Coding, computer use, pro work at scale | Nearly matches Astra for a fifth of the price: $2/$10, $0.10 cached input. | [openai.com](https://openai.com/index/introducing-gpt-6-1-sol/) |
| 4 | GPT-6 Astra | OpenAI | 3 Sep 2026 | Maximum capability, computer use, science | OpenAI's most capable model: 98% on FrontierMath Tier 4 and helped prove new prime-gap bounds. It costs $10/$50 per M tokens. | [openai.com](https://openai.com/index/gpt-6-astra/) |
| 5 | Gemini 4 Argon | Google | 13 Oct 2026 | Long-horizon engineering, multimodal input | Google's GA frontier model: 1M unified input/output window with long decode. Intro price $2/$10 through 30 Nov, then $4/$20. | [aistudio.google.com](https://aistudio.google.com/learn/gemini-4-argon-developer-guide) |
| 6 | GPT-6.1 Terra | OpenAI | Oct 2026 | High-volume computer use and office automation | Fast and cheap at $1/$5; on par with Astra on Agents' Last Exam at a tenth of Astra's per-token price. | [openai.com](https://openai.com/index/introducing-gpt-6-1-terra/) |
| 7 | Kimi K3.1 Pro | Moonshot AI | 2 Nov 2026 (weights) | Open-weight frontier agentic coding | The biggest open-weight model here: 2.8T MoE / 104B active, 1M context, text+image. API as `kimi-k3.1-pro`; custom license. | [huggingface.co](https://huggingface.co/moonshotai/Kimi-K3.1-Pro) |
| 8 | DeepSeek-V4.1-Flash-1017 | DeepSeek | 17 Oct 2026 | Cheap strong open model, self-hosting | MIT-licensed 763B weights with a 1M context; it posts strong DeepSWE/Terminal-Bench scores on DeepSeek's own tables. | [huggingface.co](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017) |
| 9 | Jev 1.14 | TypeSafe AI | 14 Oct 2026 | Classifying, routing and scoring stuff in under a second | It's not a chatbot but a fast classifier: send it a state plus typed questions (Choice, Score, yes/no "Noul", Box) and get calibrated probabilities back in 70–500 ms instead of generated text. It never returns a type error, costs $0.042 per M input tokens, and output is free. | [docs.typesafe.ai](https://docs.typesafe.ai/models) |
| 10 | Muse Ember | Meta | 9 Nov 2026 | Subagents: tool calls, extraction, routing | Very cheap at $0.10/$0.50, with a 1M context and up to 512K output; Meta says it gives more intelligence per dollar than Haiku 5.5 or GPT-6 Luna. `muse-ember-1.0` on the Meta Model API. | [research.meta.ai](https://research.meta.ai/blog/muse-ember) |
| 11 | Claude Haiku 5.5 | Anthropic | 7 Oct 2026 | Fast, cheap subagents, support, browser use | $0.10/$0.50 for prompts up to 100K tokens, about 75% cheaper to run than Haiku 4.5, now with adjustable effort. | [anthropic.com](https://www.anthropic.com/claude-haiku-5-5) |
| 12 | Mistral Large 4 ("Le Chonk") | Mistral AI | Oct 2026 (weights) | Sovereign/self-hosted coding and cyber defense | European-trained ~1T open-weight model, $0.70/$2.10 via API. Free to use commercially unless you sell it as a model service. | [mistral.ai](https://mistral.ai/news/mistral-large-4-oss/) |
| 13 | Gemini 4 Carbon | Google | 28 Oct 2026 | Cyber defense, very long agentic runs | Google's strongest model (#1 on AA Intelligence Index v5 at 59), but for now only cyber defenders in the Fairwind Program can use it. | [blog.google](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/) |
| 14 | GPT-6 Cyber | OpenAI | 5 Nov 2026 | Vulnerability research, exploit validation | Found 81 high-severity Firefox bugs and 948 Linux exploits; access is limited to approved Daybreak Red customers. | [openai.com](https://openai.com/index/introducing-gpt-6-cyber) |
| 15 | Muse Wonder | Meta | 12 Oct 2026 | Personal/professional agents with memory | Meta's frontier model, built around Active Memory and Active Focus, on the Meta Model API and Muse Code. | [research.meta.ai](https://research.meta.ai/blog/muse-wonder) |
| 16 | Inkling 2 Small | Thinking Machines Lab | 5 Nov 2026 | Fine-tuning base, agentic coding | 594B/17B MoE built to be fine-tuned on Tinker. Apache 2.0 weights are promised but not out yet. | [thinkingmachines.ai](https://thinkingmachines.ai/news/inkling-2-small/) |
| 17 | Grok 4.7 | xAI (SpaceXSI) | 21 Sep 2026 | Coding, agents, knowledge work | xAI's current API flagship: 500K context at $2/$6. Grok 4.8 isn't on the API yet. | [docs.x.ai](https://docs.x.ai/developers/release-notes) |
| 18 | Qwen4-Max-Preview | Alibaba (Qwen) | 11 Nov 2026 (preview) | Alibaba's flagship reasoning, long video | First Qwen 4 model: 1M context, up to 393K output, text/image/video input. Token Plan only for now. | [docs.qwencloud.com](https://docs.qwencloud.com/developer-guides/getting-started/text-generation-models) |
| 19 | Gemini Omni 1.2 Flash | Google | 5 Nov 2026 | Video generation | GA video model: 15-second clips, multi-turn editing, $0.07/s at 720p (30% cheaper than 1.1). | [blog.google](https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemini-omni-1-2-flash/) |
| 20 | GPT-6 Luna | OpenAI | 22 Sep 2026 | Cheapest OpenAI workhorse | $0.10/$0.50; OpenAI pitches it for fast, efficient everyday work at scale. | [openai.com](https://openai.com/index/introducing-gpt-6-1-sol/) |

Prices are USD per million input/output tokens at standard API rates unless noted.

## Open weights worth running

Downloadable weights; the note gives the license.

- **Kimi K3.1 Pro**: open now, custom license
- **DeepSeek-V4.1-Flash-1017**: open now, MIT
- **Mistral Large 4 ("Le Chonk")**: open now, modified MIT; Model-as-a-Service use needs a commercial license
- **Inkling 2 Small**: pending: Apache 2.0 weights promised after safety testing

## Fast/cheap specialists

- **Jev 1.14**: classify and route in under a second
- **Muse Ember**
- **Claude Haiku 5.5**
- **GPT-6 Luna**

---

Refreshed on weekday mornings (Prague). Models are re-ranked by developer relevance (capability, API availability, price/performance, novelty), and every entry links a primary source checked at refresh time.

## How this repo works

A small, domain-agnostic trend-tracking pipeline. AI models are the first domain.

```
research (today: a scheduled assistant; planned: LangChain agents on a private VPS)
   │  scripts/upsert.py  (add / update / retire items, sources, change notes)
   ▼
data/trends.db  (SQLite, committed: the single source of truth)
   │  push to main → .github/workflows/render.yml → scripts/render.py
   ▼
README.md · reports/<domain>.md · reports/<domain>.pdf  (generated, never hand-edited)
```

| Domain | Last updated | Reports |
|---|---|---|
| Relevant models (`ai-models`) | 11 Nov 2026 | [Markdown](reports/ai-models.md) · [PDF](reports/ai-models.pdf) |

Schema: [`db/schema.sql`](db/schema.sql) · Architecture and how to add a domain: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
