<!-- generated from data/trends.db by scripts/render.py, do not edit by hand -->
# Relevant models

AI models worth knowing about if you build with AI, and why each one matters.

**Last updated:** 23 Nov 2026 (Prague)  
**How the ranking works:** what matters to a working AI developer: capability, whether you can call it through an API today, price for the performance, and how new it is. Vendor benchmark claims are the vendors' own.

## What changed lately

- **Inkling 2 Mini (20 Nov):** Thinking Machines released Inkling 2 Mini, a small looped-transformer MoE (26.4B total, 3.4B active) that fits in about 20GB and runs offline on a laptop, with Apache 2.0 weights on Hugging Face. Added at #17. Mistral Large 4 dropped to keep the list at 20.
- **Gemini 4 Neon (18 Nov):** Google's new fast frontier model scores 61 on the AA Intelligence Index (#3 overall) and tops the AA Coding Agent Index at $3/$15 per M tokens with a 1M context. Added at #3. Gemini 4 Carbon, still limited to Fairwind cyber defenders and now outscored, dropped to keep the list at 20.
- **Cheaper slow lane for OpenAI (public beta):** Responses API background requests with a 2h or 8h completion window now cost 30% or 40% below Standard on GPT-6.2 Astra, GPT-6.2 Sol, GPT-6.1 Terra and GPT-6 Luna. New models from 6.2 on launch without Flex processing.
- **Qwen4-Max and Hy4 flash (16 Nov):** Alibaba took Qwen4-Max out of preview onto the QwenCloud API (moved up to #9). Tencent launched Hy4 flash, a fast, very cheap 12B-active MoE (added at #14). Grok 4.7 and Muse Wonder dropped to keep the list at 20.
- **GPT-6.2 Astra and Sol, MAI Code 2 (17 Nov):** OpenAI shipped GPT-6.2 Astra (20% cheaper than GPT-6 Astra) and GPT-6.2 Sol (same price as 6.1 Sol), replacing both older models at #2 and #3. Microsoft launched MAI Code 2 for GitHub Copilot (added at #12). GPT-6 Cyber dropped to keep the list at 20.

## Ranked

| # | Model | Vendor | Released | Best for | Why you should care | Source |
|---|---|---|---|---|---|---|
| 1 | Claude Fable 5.2 | Anthropic | 9 Nov 2026 | Mathematicians, the hardest open-ended technical work | It's the model for heavy reasoning and math: 1,000 Fable agents formalized Fermat's Last Theorem in Lean in 30 h (Opus 5.5 managed 26% in 18 h), and it solved two open black-hole physics problems. Same model as Mythos 5.2 but with cyber/bio safeguards. Up to 30% faster than 5.1, $8/$40 per M tokens (fast mode $16/$80), `claude-fable-5-2`, also on AWS, Google Cloud and Azure. | [anthropic.com](https://www.anthropic.com/claude-fable-and-mythos-5-2) |
| 2 | GPT-6.2 Astra | OpenAI | 17 Nov 2026 | Maximum capability for the hardest professional and coding work | OpenAI's new frontier model replaces GPT-6 Astra at 20% lower prices: $8 in / $40 out per M tokens, $0.40 cached input. On the API as gpt-6.2-astra, with Ultrafast at launch. | [openai.com](https://openai.com/index/introducing-gpt-6-2-astra-sol/), [OpenAI docs: discounted windows](https://developers.openai.com/api/docs/guides/background) |
| 3 | Gemini 4 Neon | Google | 18 Nov 2026 | Fast frontier coding, agents and knowledge work | Google's new top generally available model: #3 overall at 61 on the AA Intelligence Index (xhigh) and #1 on the AA Coding Agent Index, at $3/$15 per M tokens ($0.15 cached) with a 1M context. In the Gemini API via AI Studio, Gemini for business, Antigravity and the Gemini app. | [blog.google](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/) |
| 4 | GPT-6.2 Sol | OpenAI | 17 Nov 2026 | Coding, computer use, pro work at scale | Replaces GPT-6.1 Sol with better results on fewer output tokens at the same price: $2 in / $10 out per M tokens, $0.10 cached input. On the API as gpt-6.2-sol. | [openai.com](https://openai.com/index/introducing-gpt-6-2-astra-sol/), [OpenAI docs: discounted windows](https://developers.openai.com/api/docs/guides/background) |
| 5 | Claude Opus 5.5 | Anthropic | 22 Sep 2026 | Everyday coding and agent work | Anthropic's recommended daily driver: about Fable 5.1 level at $4/$20 with $0.20 cache reads, and 40% cheaper to run than Opus 5. | [anthropic.com](https://www.anthropic.com/claude-opus-5-5) |
| 6 | Gemini 4 Hydrogen | Google | 12 Nov 2026 | Fast everyday coding and agent execution | Google's fast workhorse that edges out Argon on the AA Intelligence Index (51 vs 50 at default, 54 at xhigh) at a flat $1.50/$7.50 across its 1M context, with up to 1M output and four thinking levels. `gemini-4-hydrogen` on the Gemini API and AI Studio. | [blog.google](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-hydrogen/) |
| 7 | Gemini 4 Argon | Google | 13 Oct 2026 | Long-horizon engineering, multimodal input | Google's GA frontier model: 1M unified input/output window with long decode. Intro price $2/$10 through 30 Nov, then $4/$20. | [aistudio.google.com](https://aistudio.google.com/learn/gemini-4-argon-developer-guide) |
| 8 | GPT-6.1 Terra | OpenAI | Oct 2026 | High-volume computer use and office automation | Fast and cheap at $1/$5; on par with Astra on Agents' Last Exam at a tenth of Astra's per-token price. | [openai.com](https://openai.com/index/introducing-gpt-6-1-terra/) |
| 9 | Kimi K3.1 Pro | Moonshot AI | 2 Nov 2026 (weights) | Open-weight frontier agentic coding | The biggest open-weight model here: 2.8T MoE / 104B active, 1M context, text+image. API as `kimi-k3.1-pro`; custom license. | [huggingface.co](https://huggingface.co/moonshotai/Kimi-K3.1-Pro) |
| 10 | Qwen4-Max | Alibaba (Qwen) | 16 Nov 2026 | Alibaba's flagship for coding, agents and visual reasoning | Now generally available on the QwenCloud API: a 2.4T-parameter MoE with 71B active per token, native vision and a 1M-token context. Alibaba says it is #6 on Code Arena and cuts cost per task about 60% versus Qwen3.8-Max. | [alibabacloud.com](https://www.alibabacloud.com/en/press-room/alibaba-unveils-qwen4-max) |
| 11 | DeepSeek-V4.1-Flash-1017 | DeepSeek | 17 Oct 2026 | Cheap strong open model, self-hosting | MIT-licensed 763B weights with a 1M context; it posts strong DeepSWE/Terminal-Bench scores on DeepSeek's own tables. | [huggingface.co](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017) |
| 12 | LongCat-2.5 | Meituan | Nov 2026 (weights) | Open-weight agentic coding under MIT | 1.6T MoE / ~48B active with native image and video input; MIT license. Meituan's own scores put it near Claude Opus 5 on coding-agent benchmarks. | [huggingface.co](https://huggingface.co/meituan-longcat/LongCat-2.5) |
| 13 | MAI Code 2 | Microsoft | 17 Nov 2026 | Everyday enterprise coding at a low price | Microsoft's coding model, with a high-volume Code 2 Flash sibling. Microsoft claims 98% of GPT-6.1 Sol's coding performance at 40% of the cost (at a promotional price). Available in GitHub Copilot now; Code 2 Flash is in limited preview on Microsoft Foundry. | [microsoft.ai](https://microsoft.ai/news/introducing-mai-code-2-and-mai-code-2-flash/) |
| 14 | Jev 1.14 | TypeSafe AI | 14 Oct 2026 | Classifying, routing and scoring stuff in under a second | It's not a chatbot but a fast classifier: send it a state plus typed questions (Choice, Score, yes/no "Noul", Box) and get calibrated probabilities back in 70–500 ms instead of generated text. It never returns a type error, costs $0.042 per M input tokens, and output is free. | [docs.typesafe.ai](https://docs.typesafe.ai/models) |
| 15 | Gemini Decision 1 | Google | 11 Nov 2026 | Fast yes/no, choice and rubric decisions over any media | Google's answer to Jev: send one input (text, images, audio, video or PDF, up to 256K tokens) plus up to 1,000 typed questions and get calibrated probabilities back in about 150–250 ms. $0.10 per M input tokens, output free, via the Gemini Decisions API. | [blog.google](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-decisions-api/), [AI Studio docs](https://aistudio.google.com/docs/models/gemini-decision-1) |
| 16 | Hy4 flash | Tencent | 16 Nov 2026 | Cheap everyday agent work: docs, decks, research | A 224B MoE with only 12B active, 1M context and multimodal input, decoding at 150+ tokens/s for about $0.07 in / $0.28 out per M tokens on Tencent Cloud TokenHub. Tencent plans to open-source it. | [tencent.com](https://www.tencent.com/tencent-launches-hy4-flash-to-power-high-speed-cost-efficient-ai-deployment-for-everyday-workflows/) |
| 17 | Inkling 2 Mini | Thinking Machines Lab | 20 Nov 2026 | Local agentic coding on a laptop | 26.4B/3.4B-active looped MoE that fits in about 20GB, so it runs offline on a laptop; Thinking Machines says it leads open models under 100B on DeepSWE v1.1 (48.2%). Apache 2.0 weights on Hugging Face, also on Tinker. | [thinkingmachines.ai](https://thinkingmachines.ai/news/inkling-2-mini/), [huggingface.co](https://huggingface.co/thinkingmachines/Inkling-2-Mini) |
| 18 | Muse Ember | Meta | 9 Nov 2026 | Subagents: tool calls, extraction, routing | Very cheap at $0.10/$0.50, with a 1M context and up to 512K output; Meta says it gives more intelligence per dollar than Haiku 5.5 or GPT-6 Luna. `muse-ember-1.0` on the Meta Model API. | [research.meta.ai](https://research.meta.ai/blog/muse-ember) |
| 19 | Inkling 2 Small | Thinking Machines Lab | 5 Nov 2026 | Open-weight fine-tuning base, agentic coding | 594B/17B MoE with image input and a 1M context, built to be fine-tuned. Apache 2.0 weights are now on Hugging Face (NVFP4 needs about 500GB of VRAM), with API access at NVIDIA, Fireworks, Together and others. | [thinkingmachines.ai](https://thinkingmachines.ai/news/inkling-2-small/), [huggingface.co](https://huggingface.co/thinkingmachines/Inkling-2-Small) |
| 20 | Claude Haiku 5.5 | Anthropic | 7 Oct 2026 | Fast, cheap subagents, support, browser use | $0.10/$0.50 for prompts up to 100K tokens, about 75% cheaper to run than Haiku 4.5, now with adjustable effort. | [anthropic.com](https://www.anthropic.com/claude-haiku-5-5) |

Prices are USD per million input/output tokens at standard API rates unless noted.

## Open weights worth running

Downloadable weights; the note gives the license.

- **Kimi K3.1 Pro**: open now, custom license
- **DeepSeek-V4.1-Flash-1017**: open now, MIT
- **LongCat-2.5**: MIT license, weights on Hugging Face
- **Inkling 2 Mini**: open now, Apache 2.0
- **Inkling 2 Small**: open now, Apache 2.0

## Fast/cheap specialists

- **Jev 1.14**: classify and route in under a second
- **Gemini Decision 1**: multimodal decisions in ~200 ms
- **Hy4 flash**: 12B active, ~$0.07/$0.28 per M tokens
- **Muse Ember**
- **Claude Haiku 5.5**

---

Refreshed on weekday mornings (Prague). Models are re-ranked by developer relevance (capability, API availability, price/performance, novelty), and every entry links a primary source checked at refresh time.
