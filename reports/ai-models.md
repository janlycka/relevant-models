<!-- generated from data/trends.db by scripts/render.py, do not edit by hand -->
# Relevant models

AI models worth knowing about if you build with AI, and why each one matters.

**Last updated:** 13 Nov 2026 (Prague)  
**How the ranking works:** what matters to a working AI developer: capability, whether you can call it through an API today, price for the performance, and how new it is. Vendor benchmark claims are the vendors' own.

## What changed lately

- **Gemini 4 Hydrogen (12 Nov):** Google's new fast model beats Argon on the AA Intelligence Index at $1.50/$7.50 per M tokens and is available on all Gemini API tiers.
- **Inkling 2 Small weights out (12 Nov):** Thinking Machines released the Apache 2.0 weights on Hugging Face, plus API access through NVIDIA, Fireworks, Together, Baseten, Nebius, Modal and Cloudflare.
- **Gemini Decision 1 (11 Nov):** Google launched the Gemini Decisions API, joining Jev and OpenAI in decision models: up to 1,000 yes/no, choice or rubric questions per multimodal input in one pass, about 200 ms, $0.10 per M input tokens with free output.
- **Claude Fable 5.2 / Mythos 5.2 (9 Nov):** Anthropic's top model got faster (up to 30% vs 5.1) and cheaper ($8/$40). A swarm of about 1,000 Fable agents formalized Fermat's Last Theorem in Lean in 30 hours.
- **Muse Ember (9 Nov):** Meta's small agent workhorse costs $0.10/$0.50, has a 1M-token context, and Meta claims it beats Haiku 5.5 and GPT-6 Luna on intelligence per dollar.

## Ranked

| # | Model | Vendor | Released | Best for | Why you should care | Source |
|---|---|---|---|---|---|---|
| 1 | Claude Fable 5.2 | Anthropic | 9 Nov 2026 | Mathematicians, the hardest open-ended technical work | It's the model for heavy reasoning and math: 1,000 Fable agents formalized Fermat's Last Theorem in Lean in 30 h (Opus 5.5 managed 26% in 18 h), and it solved two open black-hole physics problems. Same model as Mythos 5.2 but with cyber/bio safeguards. Up to 30% faster than 5.1, $8/$40 per M tokens (fast mode $16/$80), `claude-fable-5-2`, also on AWS, Google Cloud and Azure. | [anthropic.com](https://www.anthropic.com/claude-fable-and-mythos-5-2) |
| 2 | Claude Opus 5.5 | Anthropic | 22 Sep 2026 | Everyday coding and agent work | Anthropic's recommended daily driver: about Fable 5.1 level at $4/$20 with $0.20 cache reads, and 40% cheaper to run than Opus 5. | [anthropic.com](https://www.anthropic.com/claude-opus-5-5) |
| 3 | GPT-6.1 Sol | OpenAI | 29 Sep 2026 | Coding, computer use, pro work at scale | Nearly matches Astra for a fifth of the price: $2/$10, $0.10 cached input. | [openai.com](https://openai.com/index/introducing-gpt-6-1-sol/) |
| 4 | GPT-6 Astra | OpenAI | 3 Sep 2026 | Maximum capability, computer use, science | OpenAI's most capable model: 98% on FrontierMath Tier 4 and helped prove new prime-gap bounds. It costs $10/$50 per M tokens. | [openai.com](https://openai.com/index/gpt-6-astra/) |
| 5 | Gemini 4 Hydrogen | Google | 12 Nov 2026 | Fast everyday coding and agent execution | Google's fast workhorse that edges out Argon on the AA Intelligence Index (51 vs 50 at default, 54 at xhigh) at a flat $1.50/$7.50 across its 1M context, with up to 1M output and four thinking levels. `gemini-4-hydrogen` on the Gemini API and AI Studio. | [blog.google](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-hydrogen/) |
| 6 | Gemini 4 Argon | Google | 13 Oct 2026 | Long-horizon engineering, multimodal input | Google's GA frontier model: 1M unified input/output window with long decode. Intro price $2/$10 through 30 Nov, then $4/$20. | [aistudio.google.com](https://aistudio.google.com/learn/gemini-4-argon-developer-guide) |
| 7 | GPT-6.1 Terra | OpenAI | Oct 2026 | High-volume computer use and office automation | Fast and cheap at $1/$5; on par with Astra on Agents' Last Exam at a tenth of Astra's per-token price. | [openai.com](https://openai.com/index/introducing-gpt-6-1-terra/) |
| 8 | Kimi K3.1 Pro | Moonshot AI | 2 Nov 2026 (weights) | Open-weight frontier agentic coding | The biggest open-weight model here: 2.8T MoE / 104B active, 1M context, text+image. API as `kimi-k3.1-pro`; custom license. | [huggingface.co](https://huggingface.co/moonshotai/Kimi-K3.1-Pro) |
| 9 | DeepSeek-V4.1-Flash-1017 | DeepSeek | 17 Oct 2026 | Cheap strong open model, self-hosting | MIT-licensed 763B weights with a 1M context; it posts strong DeepSWE/Terminal-Bench scores on DeepSeek's own tables. | [huggingface.co](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017) |
| 10 | Jev 1.14 | TypeSafe AI | 14 Oct 2026 | Classifying, routing and scoring stuff in under a second | It's not a chatbot but a fast classifier: send it a state plus typed questions (Choice, Score, yes/no "Noul", Box) and get calibrated probabilities back in 70–500 ms instead of generated text. It never returns a type error, costs $0.042 per M input tokens, and output is free. | [docs.typesafe.ai](https://docs.typesafe.ai/models) |
| 11 | Gemini Decision 1 | Google | 11 Nov 2026 | Fast yes/no, choice and rubric decisions over any media | Google's answer to Jev: send one input (text, images, audio, video or PDF, up to 256K tokens) plus up to 1,000 typed questions and get calibrated probabilities back in about 150–250 ms. $0.10 per M input tokens, output free, via the Gemini Decisions API. | [blog.google](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-decisions-api/), [AI Studio docs](https://aistudio.google.com/docs/models/gemini-decision-1) |
| 12 | Muse Ember | Meta | 9 Nov 2026 | Subagents: tool calls, extraction, routing | Very cheap at $0.10/$0.50, with a 1M context and up to 512K output; Meta says it gives more intelligence per dollar than Haiku 5.5 or GPT-6 Luna. `muse-ember-1.0` on the Meta Model API. | [research.meta.ai](https://research.meta.ai/blog/muse-ember) |
| 13 | Inkling 2 Small | Thinking Machines Lab | 5 Nov 2026 | Open-weight fine-tuning base, agentic coding | 594B/17B MoE with image input and a 1M context, built to be fine-tuned. Apache 2.0 weights are now on Hugging Face (NVFP4 needs about 500GB of VRAM), with API access at NVIDIA, Fireworks, Together and others. | [thinkingmachines.ai](https://thinkingmachines.ai/news/inkling-2-small/), [huggingface.co](https://huggingface.co/thinkingmachines/Inkling-2-Small) |
| 14 | Claude Haiku 5.5 | Anthropic | 7 Oct 2026 | Fast, cheap subagents, support, browser use | $0.10/$0.50 for prompts up to 100K tokens, about 75% cheaper to run than Haiku 4.5, now with adjustable effort. | [anthropic.com](https://www.anthropic.com/claude-haiku-5-5) |
| 15 | Mistral Large 4 ("Le Chonk") | Mistral AI | Oct 2026 (weights) | Sovereign/self-hosted coding and cyber defense | European-trained ~1T open-weight model, $0.70/$2.10 via API. Free to use commercially unless you sell it as a model service. | [mistral.ai](https://mistral.ai/news/mistral-large-4-oss/) |
| 16 | Gemini 4 Carbon | Google | 28 Oct 2026 | Cyber defense, very long agentic runs | Google's strongest model (#1 on AA Intelligence Index v5 at 59), but for now only cyber defenders in the Fairwind Program can use it. | [blog.google](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/) |
| 17 | GPT-6 Cyber | OpenAI | 5 Nov 2026 | Vulnerability research, exploit validation | Found 81 high-severity Firefox bugs and 948 Linux exploits; access is limited to approved Daybreak Red customers. | [openai.com](https://openai.com/index/introducing-gpt-6-cyber) |
| 18 | Muse Wonder | Meta | 12 Oct 2026 | Personal/professional agents with memory | Meta's frontier model, built around Active Memory and Active Focus, on the Meta Model API and Muse Code. | [research.meta.ai](https://research.meta.ai/blog/muse-wonder) |
| 19 | Grok 4.7 | xAI (SpaceXSI) | 21 Sep 2026 | Coding, agents, knowledge work | xAI's current API flagship: 500K context at $2/$6. Grok 4.8 isn't on the API yet. | [docs.x.ai](https://docs.x.ai/developers/release-notes) |
| 20 | Qwen4-Max-Preview | Alibaba (Qwen) | 11 Nov 2026 (preview) | Alibaba's flagship reasoning, long video | First Qwen 4 model: 1M context, up to 393K output, text/image/video input. Token Plan only for now. | [docs.qwencloud.com](https://docs.qwencloud.com/developer-guides/getting-started/text-generation-models) |
| 21 | GPT-6 Luna | OpenAI | 22 Sep 2026 | Cheapest OpenAI workhorse | $0.10/$0.50; OpenAI pitches it for fast, efficient everyday work at scale. | [openai.com](https://openai.com/index/introducing-gpt-6-1-sol/) |

Prices are USD per million input/output tokens at standard API rates unless noted.

## Open weights worth running

Downloadable weights; the note gives the license.

- **Kimi K3.1 Pro**: open now, custom license
- **DeepSeek-V4.1-Flash-1017**: open now, MIT
- **Inkling 2 Small**: open now, Apache 2.0
- **Mistral Large 4 ("Le Chonk")**: open now, modified MIT; Model-as-a-Service use needs a commercial license

## Fast/cheap specialists

- **Jev 1.14**: classify and route in under a second
- **Gemini Decision 1**: multimodal decisions in ~200 ms
- **Muse Ember**
- **Claude Haiku 5.5**
- **GPT-6 Luna**

---

Refreshed on weekday mornings (Prague). Models are re-ranked by developer relevance (capability, API availability, price/performance, novelty), and every entry links a primary source checked at refresh time.
