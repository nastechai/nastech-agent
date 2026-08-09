---
sidebar_position: 9
title: "Optional Skills Catalog"
description: "Official optional skills shipped with nastech-agent — install via nastech skills install official/<category>/<skill>"
---

# Optional Skills Catalog

Optional skills ship with nastech-agent under `optional-skills/` but are **not active by default**. Install them explicitly:

```bash
nastech skills install official/<category>/<skill>
```

For example:

```bash
nastech skills install official/blockchain/solana
nastech skills install official/mlops/flash-attention
```

Each skill below links to a dedicated page with its full definition, setup, and usage.

To uninstall:

```bash
nastech skills uninstall <skill-name>
```

## autonomous-ai-agents

| Skill | Description |
|-------|-------------|
| [**antigravity-cli**](/nastech-agent/docs/user-guide/skills/optional/autonomous-ai-agents/autonomous-ai-agents-antigravity-cli) | Operate the Antigravity CLI (agy): plugins, auth, sandbox. |
| [**blackbox**](/nastech-agent/docs/user-guide/skills/optional/autonomous-ai-agents/autonomous-ai-agents-blackbox) | Delegate coding tasks to the Blackbox AI multi-model CLI. |
| [**grok**](/nastech-agent/docs/user-guide/skills/optional/autonomous-ai-agents/autonomous-ai-agents-grok) | Delegate coding to xAI Grok Build CLI (features, PRs). |
| [**honcho**](/nastech-agent/docs/user-guide/skills/optional/autonomous-ai-agents/autonomous-ai-agents-honcho) | Configure and troubleshoot Honcho memory for Nastech. |
| [**openhands**](/nastech-agent/docs/user-guide/skills/optional/autonomous-ai-agents/autonomous-ai-agents-openhands) | Delegate coding to OpenHands CLI (model-agnostic, LiteLLM). |

## blockchain

| Skill | Description |
|-------|-------------|
| [**evm**](/nastech-agent/docs/user-guide/skills/optional/blockchain/blockchain-evm) | Read-only EVM client: wallets, tokens, gas across 8 chains. |
| [**hyperliquid**](/nastech-agent/docs/user-guide/skills/optional/blockchain/blockchain-hyperliquid) | Hyperliquid market data, account history, trade review. |
| [**solana**](/nastech-agent/docs/user-guide/skills/optional/blockchain/blockchain-solana) | Query Solana wallets, tokens, txs, and NFTs in USD. |

## communication

| Skill | Description |
|-------|-------------|
| [**one-three-one-rule**](/nastech-agent/docs/user-guide/skills/optional/communication/communication-one-three-one-rule) | Structured decision-making framework for technical proposals and trade-off analysis. When the user faces a choice between multiple approaches (architecture decisions, tool selection, refactoring strategies, migration paths), this skill p... |

## creative

| Skill | Description |
|-------|-------------|
| [**audiocraft-audio-generation**](/nastech-agent/docs/user-guide/skills/optional/creative/creative-audiocraft-audio-generation) | AudioCraft: MusicGen text-to-music, AudioGen text-to-sound. |
| [**baoyu-article-illustrator**](/nastech-agent/docs/user-guide/skills/optional/creative/creative-baoyu-article-illustrator) | Article illustrations: type × style × palette consistency. |
| [**baoyu-comic**](/nastech-agent/docs/user-guide/skills/optional/creative/creative-baoyu-comic) | Knowledge comics (知识漫画): educational, biography, tutorial. |
| [**blender-mcp**](/nastech-agent/docs/user-guide/skills/optional/creative/creative-blender-mcp) | Drive Blender via the catalog blender MCP, with bpy recipes. |
| [**concept-diagrams**](/nastech-agent/docs/user-guide/skills/optional/creative/creative-concept-diagrams) | Generate flat, minimal educational SVG visuals as HTML. |
| [**creative-ideation**](/nastech-agent/docs/user-guide/skills/optional/creative/creative-creative-ideation) | Generate ideas via named methods from creative practice. |
| [**heartmula**](/nastech-agent/docs/user-guide/skills/optional/creative/creative-heartmula) | HeartMuLa: Suno-like song generation from lyrics + tags. |
| [**hyperframes**](/nastech-agent/docs/user-guide/skills/optional/creative/creative-hyperframes) | Render MP4/WebM videos from HTML compositions. |
| [**kanban-video-orchestrator**](/nastech-agent/docs/user-guide/skills/optional/creative/creative-kanban-video-orchestrator) | Plan and run multi-agent video production pipelines. |
| [**meme-generation**](/nastech-agent/docs/user-guide/skills/optional/creative/creative-meme-generation) | Create meme PNGs from templates with Pillow text overlay. |
| [**pixel-art**](/nastech-agent/docs/user-guide/skills/optional/creative/creative-pixel-art) | Pixel art w/ era palettes (NES, Game Boy, PICO-8). |
| [**tldraw-offline**](/nastech-agent/docs/user-guide/skills/optional/creative/creative-tldraw-offline) | Drive and script tldraw offline canvases with an agent. |
| [**unreal-mcp**](/nastech-agent/docs/user-guide/skills/optional/creative/creative-unreal-mcp) | Automate Unreal Engine editor scenes, actors, and renders. |

## data-science

| Skill | Description |
|-------|-------------|
| [**jupyter-notebook**](/nastech-agent/docs/user-guide/skills/optional/data-science/data-science-jupyter-notebook) | Iterative Python via live Jupyter kernel (hamelnb). |

## devops

| Skill | Description |
|-------|-------------|
| [**actual-setup**](/nastech-agent/docs/user-guide/skills/optional/devops/devops-actual-setup) | Set up Actual Computer (actual.inc) inference in Nastech. |
| [**inference-sh-cli**](/nastech-agent/docs/user-guide/skills/optional/devops/devops-cli) | Run 150+ AI apps (image, video, LLM) via inference.sh CLI. |
| [**docker-management**](/nastech-agent/docs/user-guide/skills/optional/devops/devops-docker-management) | Manage Docker containers, images, volumes, and Compose. |
| [**nastech-s6-container-supervision**](/nastech-agent/docs/user-guide/skills/optional/devops/devops-nastech-s6-container-supervision) | Modify or debug s6 services in the Nastech Docker image. |
| [**pinggy-tunnel**](/nastech-agent/docs/user-guide/skills/optional/devops/devops-pinggy-tunnel) | Zero-install localhost tunnels over SSH via Pinggy. |
| [**watchers**](/nastech-agent/docs/user-guide/skills/optional/devops/devops-watchers) | Poll RSS, JSON APIs, and GitHub with watermark dedup. |

## dogfood

| Skill | Description |
|-------|-------------|
| [**adversarial-ux-test**](/nastech-agent/docs/user-guide/skills/optional/dogfood/dogfood-adversarial-ux-test) | Roleplay a hostile user to find and triage UX pain points. |

## email

| Skill | Description |
|-------|-------------|
| [**agentmail**](/nastech-agent/docs/user-guide/skills/optional/email/email-agentmail) | Give the agent its own inbox: send and receive email. |

## finance

| Skill | Description |
|-------|-------------|
| [**3-statement-model**](/nastech-agent/docs/user-guide/skills/optional/finance/finance-3-statement-model) | Build integrated IS/BS/CF financial workbooks in Excel. |
| [**comps-analysis**](/nastech-agent/docs/user-guide/skills/optional/finance/finance-comps-analysis) | Build comparable-company valuation workbooks in Excel. |
| [**dcf-model**](/nastech-agent/docs/user-guide/skills/optional/finance/finance-dcf-model) | Build discounted cash flow valuation workbooks in Excel. |
| [**excel-author**](/nastech-agent/docs/user-guide/skills/optional/finance/finance-excel-author) | Build auditable financial workbooks headless via openpyxl. |
| [**lbo-model**](/nastech-agent/docs/user-guide/skills/optional/finance/finance-lbo-model) | Build leveraged buyout workbooks with IRR/MOIC in Excel. |
| [**merger-model**](/nastech-agent/docs/user-guide/skills/optional/finance/finance-merger-model) | Build M&A accretion/dilution workbooks in Excel. |
| [**polymarket**](/nastech-agent/docs/user-guide/skills/optional/finance/finance-polymarket) | Query Polymarket: markets, prices, orderbooks, history. |
| [**pptx-author**](/nastech-agent/docs/user-guide/skills/optional/finance/finance-pptx-author) | Build PowerPoint decks headless with python-pptx. |
| [**stocks**](/nastech-agent/docs/user-guide/skills/optional/finance/finance-stocks) | Stock quotes, history, search, compare, crypto via Yahoo. |

## gaming

| Skill | Description |
|-------|-------------|
| [**minecraft-modpack-server**](/nastech-agent/docs/user-guide/skills/optional/gaming/gaming-minecraft-modpack-server) | Host modded Minecraft servers (CurseForge, Modrinth). |
| [**pokemon-player**](/nastech-agent/docs/user-guide/skills/optional/gaming/gaming-pokemon-player) | Play Pokemon via headless emulator + RAM reads. |

## health

| Skill | Description |
|-------|-------------|
| [**fitness-nutrition**](/nastech-agent/docs/user-guide/skills/optional/health/health-fitness-nutrition) | Gym workout planner and nutrition tracker. Search 690+ exercises by muscle, equipment, or category via wger. Look up macros and calories for 380,000+ foods via USDA FoodData Central. Compute BMI, TDEE, one-rep max, macro splits, and body... |
| [**neuroskill-bci**](/nastech-agent/docs/user-guide/skills/optional/health/health-neuroskill-bci) | Connect to a running NeuroSkill instance and incorporate the user's real-time cognitive and emotional state (focus, relaxation, mood, cognitive load, drowsiness, heart rate, HRV, sleep staging, and 40+ derived EXG scores) into responses.... |

## mcp

| Skill | Description |
|-------|-------------|
| [**fastmcp**](/nastech-agent/docs/user-guide/skills/optional/mcp/mcp-fastmcp) | Build, test, and deploy Python MCP servers. |
| [**mcp-oauth-remote-gateway**](/nastech-agent/docs/user-guide/skills/optional/mcp/mcp-mcp-oauth-remote-gateway) | Manual OAuth for remote MCP servers on headless gateways. |
| [**mcporter**](/nastech-agent/docs/user-guide/skills/optional/mcp/mcp-mcporter) | List, auth, and call MCP servers/tools from the terminal. |

## migration

| Skill | Description |
|-------|-------------|
| [**openclaw-migration**](/nastech-agent/docs/user-guide/skills/optional/migration/migration-openclaw-migration) | Import an OpenClaw setup (memories, skills) into Nastech. |

## mlops

| Skill | Description |
|-------|-------------|
| [**huggingface-accelerate**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-accelerate) | Run PyTorch training across GPUs with minimal changes. |
| [**axolotl**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-training-axolotl) | Axolotl: YAML LLM fine-tuning (LoRA, DPO, GRPO). |
| [**chroma**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-chroma) | Embedding database for RAG and semantic search. |
| [**clip**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-clip) | Zero-shot image classification and image-text search. |
| [**dspy**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-research-dspy) | DSPy: declarative LM programs, auto-optimize prompts, RAG. |
| [**faiss**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-faiss) | Fast vector similarity search at billion scale. |
| [**optimizing-attention-flash**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-flash-attention) | Speed up long-sequence transformer training and inference. |
| [**guidance**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-guidance) | Constrain LLM output with grammars; guarantee valid JSON. |
| [**huggingface-tokenizers**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-huggingface-tokenizers) | Fast BPE/WordPiece tokenization and custom vocab training. |
| [**instructor**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-instructor) | Structured LLM outputs validated with Pydantic. |
| [**lambda-labs-gpu-cloud**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-lambda-labs) | On-demand GPU cloud instances for ML training. |
| [**llava**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-llava) | Vision-language chat: VQA, captioning, image dialogue. |
| [**modal-serverless-gpu**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-modal) | Serverless GPU cloud for ML jobs and model APIs. |
| [**nemo-curator**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-nemo-curator) | Curate LLM training data: dedupe, filter, PII redaction. |
| [**obliteratus**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-obliteratus) | OBLITERATUS: abliterate LLM refusals (diff-in-means). |
| [**outlines**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-inference-outlines) | Outlines: structured JSON/regex/Pydantic LLM generation. |
| [**peft-fine-tuning**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-peft) | Fine-tune large LLMs with LoRA on limited GPU memory. |
| [**pinecone**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-pinecone) | Managed vector DB for production RAG and search. |
| [**pytorch-fsdp**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-pytorch-fsdp) | Fully sharded data-parallel training for large models. |
| [**pytorch-lightning**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-pytorch-lightning) | Clean training loops with built-in distributed support. |
| [**qdrant-vector-search**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-qdrant) | Vector search engine for production RAG systems. |
| [**sparse-autoencoder-training**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-saelens) | Train sparse autoencoders to interpret model features. |
| [**segment-anything-model**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-models-segment-anything-model) | SAM: zero-shot image segmentation via points, boxes, masks. |
| [**simpo-training**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-simpo) | Reference-free preference alignment, simpler than DPO. |
| [**slime-rl-training**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-slime) | RL post-training for LLMs with Megatron and SGLang. |
| [**stable-diffusion-image-generation**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-stable-diffusion) | Text-to-image generation, inpainting, and img2img. |
| [**tensorrt-llm**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-tensorrt-llm) | High-throughput LLM inference on NVIDIA GPUs. |
| [**distributed-llm-pretraining-torchtitan**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-torchtitan) | Pretrain LLMs at scale with PyTorch 4D parallelism. |
| [**fine-tuning-with-trl**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-training-trl-fine-tuning) | TRL: SFT, DPO, GRPO, RLOO reward modeling for LLM RLHF. |
| [**unsloth**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-training-unsloth) | Unsloth: 2-5x faster LoRA/QLoRA fine-tuning, less VRAM. |
| [**whisper**](/nastech-agent/docs/user-guide/skills/optional/mlops/mlops-whisper) | Transcribe and translate speech in 99 languages. |

## payments

| Skill | Description |
|-------|-------------|
| [**mpp-agent**](/nastech-agent/docs/user-guide/skills/optional/payments/payments-mpp-agent) | Pay HTTP 402 APIs via Machine Payments Protocol (MPP). |
| [**stripe-link-cli**](/nastech-agent/docs/user-guide/skills/optional/payments/payments-stripe-link-cli) | Agent payments via Stripe Link — cards, SPT, approvals. |
| [**stripe-projects**](/nastech-agent/docs/user-guide/skills/optional/payments/payments-stripe-projects) | Provision SaaS services + sync creds via Stripe Projects. |

## productivity

| Skill | Description |
|-------|-------------|
| [**canvas**](/nastech-agent/docs/user-guide/skills/optional/productivity/productivity-canvas) | Fetch Canvas LMS courses and assignments via API token. |
| [**here.now**](/nastech-agent/docs/user-guide/skills/optional/productivity/productivity-here-now) | Publish sites to &#123;slug&#125;.here.now and store files in Drives. |
| [**memento-flashcards**](/nastech-agent/docs/user-guide/skills/optional/productivity/productivity-memento-flashcards) | Spaced-repetition flashcard system. Create cards from facts or text, chat with flashcards using free-text answers graded by the agent, generate quizzes from YouTube transcripts, review due cards with adaptive scheduling, and export/impor... |
| [**shop**](/nastech-agent/docs/user-guide/skills/optional/productivity/productivity-shop) | Shop catalog search, checkout, order tracking, returns. |
| [**shopify**](/nastech-agent/docs/user-guide/skills/optional/productivity/productivity-shopify) | Query Shopify Admin/Storefront GraphQL APIs via curl. |
| [**siyuan**](/nastech-agent/docs/user-guide/skills/optional/productivity/productivity-siyuan) | Query and edit a SiYuan knowledge base via its API. |
| [**telephony**](/nastech-agent/docs/user-guide/skills/optional/productivity/productivity-telephony) | Provision Twilio numbers, SMS/MMS, and AI outbound calls. |

## research

| Skill | Description |
|-------|-------------|
| [**bioinformatics**](/nastech-agent/docs/user-guide/skills/optional/research/research-bioinformatics) | Gateway to 400+ genomics and computational biology skills. |
| [**darwinian-evolver**](/nastech-agent/docs/user-guide/skills/optional/research/research-darwinian-evolver) | Evolve prompts/regex/SQL/code with Imbue's evolution loop. |
| [**domain-intel**](/nastech-agent/docs/user-guide/skills/optional/research/research-domain-intel) | Passive recon of subdomains, SSL certs, WHOIS, and DNS. |
| [**drug-discovery**](/nastech-agent/docs/user-guide/skills/optional/research/research-drug-discovery) | Pharmaceutical research assistant for drug discovery workflows. Search bioactive compounds on ChEMBL, calculate drug-likeness (Lipinski Ro5, QED, TPSA, synthetic accessibility), look up drug-drug interactions via OpenFDA, interpret ADMET... |
| [**duckduckgo-search**](/nastech-agent/docs/user-guide/skills/optional/research/research-duckduckgo-search) | Free keyless web, news, and image search via ddgs. |
| [**gitnexus-explorer**](/nastech-agent/docs/user-guide/skills/optional/research/research-gitnexus-explorer) | Serve an interactive codebase knowledge graph web UI. |
| [**osint-investigation**](/nastech-agent/docs/user-guide/skills/optional/research/research-osint-investigation) | Follow the money via public records and sanctions data. |
| [**parallel-cli**](/nastech-agent/docs/user-guide/skills/optional/research/research-parallel-cli) | Agent-native web search, deep research, and enrichment. |
| [**pinecone-research**](/nastech-agent/docs/user-guide/skills/optional/research/research-pinecone-research) | Agent RAG and long-term memory with Pinecone. |
| [**qmd**](/nastech-agent/docs/user-guide/skills/optional/research/research-qmd) | Hybrid local search over notes, docs, and transcripts. |
| [**scrapling**](/nastech-agent/docs/user-guide/skills/optional/research/research-scrapling) | Scrape sites with stealth browsing and Cloudflare bypass. |
| [**searxng-search**](/nastech-agent/docs/user-guide/skills/optional/research/research-searxng-search) | Free keyless meta-search aggregating 70+ engines. |

## security

| Skill | Description |
|-------|-------------|
| [**1password**](/nastech-agent/docs/user-guide/skills/optional/security/security-1password) | Set up op CLI, sign in, and read or inject secrets. |
| [**godmode**](/nastech-agent/docs/user-guide/skills/optional/security/security-godmode) | Jailbreak LLMs: Parseltongue, GODMODE, ULTRAPLINIAN. |
| [**oss-forensics**](/nastech-agent/docs/user-guide/skills/optional/security/security-oss-forensics) | Supply chain investigation, evidence recovery, and forensic analysis for GitHub repositories. Covers deleted commit recovery, force-push detection, IOC extraction, multi-source evidence collection, hypothesis formation/validation, and st... |
| [**sherlock**](/nastech-agent/docs/user-guide/skills/optional/security/security-sherlock) | Find accounts for a username across 400+ platforms. |
| [**unbroker**](/nastech-agent/docs/user-guide/skills/optional/security/security-unbroker) | Autonomously remove your info from data-broker sites. |
| [**web-pentest**](/nastech-agent/docs/user-guide/skills/optional/security/security-web-pentest) | Authorized web application penetration testing — reconnaissance, vulnerability analysis, proof-based exploitation, and professional reporting. Adapts Shannon's "No Exploit, No Report" methodology with hard guardrails for scope, authoriza... |

## software-development

| Skill | Description |
|-------|-------------|
| [**code-wiki**](/nastech-agent/docs/user-guide/skills/optional/software-development/software-development-code-wiki) | Generate wiki docs + Mermaid diagrams for any codebase. |
| [**rest-graphql-debug**](/nastech-agent/docs/user-guide/skills/optional/software-development/software-development-rest-graphql-debug) | Debug REST/GraphQL APIs: status codes, auth, schemas, repro. |
| [**subagent-driven-development**](/nastech-agent/docs/user-guide/skills/optional/software-development/software-development-subagent-driven-development) | Execute plans via delegate_task subagents (2-stage review). |

## web-development

| Skill | Description |
|-------|-------------|
| [**cloudflare-temporary-deploy**](/nastech-agent/docs/user-guide/skills/optional/web-development/web-development-cloudflare-temporary-deploy) | Deploy a Worker live, no account, via wrangler --temporary. |
| [**page-agent**](/nastech-agent/docs/user-guide/skills/optional/web-development/web-development-page-agent) | Embed an in-page natural-language GUI copilot in web apps. |

## yuanbao

| Skill | Description |
|-------|-------------|
| [**yuanbao**](/nastech-agent/docs/user-guide/skills/optional/yuanbao/yuanbao-yuanbao) | Yuanbao (元宝) groups: @mention users, query info/members. |

---

## Contributing Optional Skills

To add a new optional skill to the repository:

1. Create a directory under `optional-skills/<category>/<skill-name>/`
2. Add a `SKILL.md` with standard frontmatter (name, description, version, author)
3. Include any supporting files in `references/`, `templates/`, or `scripts/` subdirectories
4. Submit a pull request — the skill will appear in this catalog and get its own docs page once merged
