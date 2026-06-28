[Skip to content](https://github.com/msitarzewski/agency-agents#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/msitarzewski/agency-agents) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/msitarzewski/agency-agents) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/msitarzewski/agency-agents) to refresh your session.Dismiss alert

{{ message }}

[msitarzewski](https://github.com/msitarzewski)/ **[agency-agents](https://github.com/msitarzewski/agency-agents)** Public

- [Notifications](https://github.com/login?return_to=%2Fmsitarzewski%2Fagency-agents) You must be signed in to change notification settings
- [Fork\\
18.8k](https://github.com/login?return_to=%2Fmsitarzewski%2Fagency-agents)
- [Star\\
115k](https://github.com/login?return_to=%2Fmsitarzewski%2Fagency-agents)


main

[**19** Branches](https://github.com/msitarzewski/agency-agents/branches) [**0** Tags](https://github.com/msitarzewski/agency-agents/tags)

[Go to Branches page](https://github.com/msitarzewski/agency-agents/branches)[Go to Tags page](https://github.com/msitarzewski/agency-agents/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>![msitarzewski](https://avatars.githubusercontent.com/u/1972242?v=4&size=40)![claude](https://avatars.githubusercontent.com/u/81847?v=4&size=40)<br>[msitarzewski](https://github.com/msitarzewski/agency-agents/commits?author=msitarzewski)<br>and<br>[claude](https://github.com/msitarzewski/agency-agents/commits?author=claude)<br>[Add tools.json canonical registry + check-tools.sh guard (](https://github.com/msitarzewski/agency-agents/commit/9262649a48aff36f90350b455f015e248c2038ce) [#606](https://github.com/msitarzewski/agency-agents/pull/606) [)](https://github.com/msitarzewski/agency-agents/commit/9262649a48aff36f90350b455f015e248c2038ce)<br>Open commit detailssuccess<br>1 hour agoJun 22, 2026<br>[9262649](https://github.com/msitarzewski/agency-agents/commit/9262649a48aff36f90350b455f015e248c2038ce) · 1 hour agoJun 22, 2026<br>## History<br>[347 Commits](https://github.com/msitarzewski/agency-agents/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/msitarzewski/agency-agents/commits/main/) 347 Commits |
| [.github](https://github.com/msitarzewski/agency-agents/tree/main/.github ".github") | [.github](https://github.com/msitarzewski/agency-agents/tree/main/.github ".github") | [Drop strategy/ as a division — it's playbooks/runbooks, not agents (](https://github.com/msitarzewski/agency-agents/commit/4d07efdb70ea9cbb6c471bc126400ddec1639a08 "Drop strategy/ as a division — it's playbooks/runbooks, not agents (#595)  strategy/ holds 16 markdown files and ZERO have agent frontmatter — they're playbooks (playbooks/phase-*.md), runbooks (runbooks/scenario-*.md), and briefs (EXECUTIVE-BRIEF.md, QUICKSTART.md, nexus-strategy.md), not agent definitions. There are 16 real agent divisions, 232 agents; strategy is not one of them.  #592 added `strategy` to lint-agents.sh AGENT_DIRS and the lint workflow paths (to match divisions.json), which made CI lint those 16 frontmatter-less docs as agents and fail every one with \"missing frontmatter opening ---\". So any PR touching strategy/ broke CI. The original lint-agents.sh correctly excluded strategy; #592 misread that deliberate exclusion as drift (same mistake as integrations/ in #593).  Fix: remove strategy from convert.sh / lint-agents.sh AGENT_DIRS, the lint workflow, and divisions.json; add it to NON_DIVISION_DIRS in check-divisions.sh. divisions.json is now 16, matching the app's parse_agent count exactly.  Also add a content-derived backstop to check-divisions.sh: every division must contain at least one .md with '---' frontmatter, or the build fails. This is what stops a docs/playbook directory from being registered as an empty agent division again — regardless of whether someone remembers the exclude list.  check-divisions.sh PASSES at 16; negative-tested that re-adding strategy fails with \"division 'strategy' has no agent files\".  Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") [#595](https://github.com/msitarzewski/agency-agents/pull/595) | 4 days agoJun 17, 2026 |
| [academic](https://github.com/msitarzewski/agency-agents/tree/main/academic "academic") | [academic](https://github.com/msitarzewski/agency-agents/tree/main/academic "academic") | [feat: add Academic Division with 5 storytelling-focused agents](https://github.com/msitarzewski/agency-agents/commit/7f171ae094ab55c5d858f0fdebfdd46bd4e70c82 "feat: add Academic Division with 5 storytelling-focused agents  Add Anthropologist, Geographer, Historian, Narratologist, and Psychologist agents to support world-building and narrative design with scholarly rigor. Update README with new Academic Division table.  Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>") | 3 months agoMar 15, 2026 |
| [design](https://github.com/msitarzewski/agency-agents/tree/main/design "design") | [design](https://github.com/msitarzewski/agency-agents/tree/main/design "design") | [Add Persona Walkthrough Specialist (](https://github.com/msitarzewski/agency-agents/commit/0ab5b45c77a38b96046a15dee4305a600d88602b "Add Persona Walkthrough Specialist (#507)  Thanks @hedonnn — original (passed the originality check), on-template (full persona sections), and verified clean. 🙏") [#507](https://github.com/msitarzewski/agency-agents/pull/507) [)](https://github.com/msitarzewski/agency-agents/commit/0ab5b45c77a38b96046a15dee4305a600d88602b "Add Persona Walkthrough Specialist (#507)  Thanks @hedonnn — original (passed the originality check), on-template (full persona sections), and verified clean. 🙏") | 3 weeks agoJun 3, 2026 |
| [engineering](https://github.com/msitarzewski/agency-agents/tree/main/engineering "engineering") | [engineering](https://github.com/msitarzewski/agency-agents/tree/main/engineering "engineering") | [feat: add WordPress Shopping Cart Engineer agent to Engineering Divis…](https://github.com/msitarzewski/agency-agents/commit/0750e1c90798ad3f68a8496970e357fc00b881be "feat: add WordPress Shopping Cart Engineer agent to Engineering Division (#569)  Co-authored-by: Claude Opus 4.8 <noreply@anthropic.com>") | 2 weeks agoJun 6, 2026 |
| [examples](https://github.com/msitarzewski/agency-agents/tree/main/examples "examples") | [examples](https://github.com/msitarzewski/agency-agents/tree/main/examples "examples") | [Move book co-author into marketing category structure](https://github.com/msitarzewski/agency-agents/commit/1955c9120f26688202612b12b0edd8250209ec50 "Move book co-author into marketing category structure") | 3 months agoMar 11, 2026 |
| [finance](https://github.com/msitarzewski/agency-agents/tree/main/finance "finance") | [finance](https://github.com/msitarzewski/agency-agents/tree/main/finance "finance") | [fix: align 5 finance agents with CONTRIBUTING.md template (](https://github.com/msitarzewski/agency-agents/commit/4eaf2309fbafe3efa7ec25ed0996b51a4ee25c47 "fix: align 5 finance agents with CONTRIBUTING.md template (#436)  Aligns all 5 finance agents with CONTRIBUTING.md template: fixes section headers, emojis, consolidates Technical Deliverables sections, and adds missing Learning & Memory sections with domain-specific content.") [#436](https://github.com/msitarzewski/agency-agents/pull/436) [)](https://github.com/msitarzewski/agency-agents/commit/4eaf2309fbafe3efa7ec25ed0996b51a4ee25c47 "fix: align 5 finance agents with CONTRIBUTING.md template (#436)  Aligns all 5 finance agents with CONTRIBUTING.md template: fixes section headers, emojis, consolidates Technical Deliverables sections, and adds missing Learning & Memory sections with domain-specific content.") | 2 months agoApr 11, 2026 |
| [game-development](https://github.com/msitarzewski/agency-agents/tree/main/game-development "game-development") | [game-development](https://github.com/msitarzewski/agency-agents/tree/main/game-development "game-development") | [Add Blender Add-on Engineer agent and update README](https://github.com/msitarzewski/agency-agents/commit/fe7f036b1ac2a86ec4cc586f0153c9825d44b0d2 "Add Blender Add-on Engineer agent and update README") | 3 months agoMar 13, 2026 |
| [gis](https://github.com/msitarzewski/agency-agents/tree/main/gis "gis") | [gis](https://github.com/msitarzewski/agency-agents/tree/main/gis "gis") | [feat: add GIS division with 13 specialized agents across 4 tiers (](https://github.com/msitarzewski/agency-agents/commit/a077c9ac0be381ec15e7dcbb690f641d6091a5db "feat: add GIS division with 13 specialized agents across 4 tiers (#572)  * feat: add GIS division with 13 specialized agents across 4 tiers  - Strategic: Technical Consultant, Solution Engineer - Core: GIS Analyst, Spatial Data Engineer, Geoprocessing Specialist, QA Engineer - Emerging: GeoAI/ML Engineer, BIM/GIS Specialist, 3D & Scene Developer,   Spatial Data Scientist, Drone/Reality Mapping - Delivery: Web GIS Developer, Cartography Designer  Also: - Add Smart Campus Digital Twin use case scenario - Update agent counts (218→231) and division counts (15→16) - All agents follow existing format: frontmatter + identity + mission + rules + process  * Wire gis/ division into toolchain + reconcile roster  The PR added the gis/ agents + README rows but didn't register the division where the toolchain looks, so the 13 agents would be silently skipped by convert/install/lint. Register gis (alpha: after game-development) in: - scripts/convert.sh AGENT_DIRS - scripts/install.sh AGENT_DIRS + ALL_DIVISIONS + division_emoji (🌍) - scripts/lint-agents.sh AGENT_DIRS - .github/workflows/lint-agents.yml (paths trigger + changed-file globs)  README: count 231 -> 232 / 16 divisions and add the Strategy Duel Agent roster row (reconciles the row #390 left out), so rows == count == 232.  Verified: lint PASS, convert generates all 13, `install.sh --list teams` shows \"gis 13 agents\", roster drift 0.  Co-Authored-By: Cyruschu430 <Cyruschu430@users.noreply.github.com> Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>  ---------  Co-authored-by: Hermes Agent <agent@hermes.ai> Co-authored-by: Michael Sitarzewski <msitarzewski@gmail.com> Co-authored-by: Cyruschu430 <Cyruschu430@users.noreply.github.com> Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") [#572](https://github.com/msitarzewski/agency-agents/pull/572) [)](https://github.com/msitarzewski/agency-agents/commit/a077c9ac0be381ec15e7dcbb690f641d6091a5db "feat: add GIS division with 13 specialized agents across 4 tiers (#572)  * feat: add GIS division with 13 specialized agents across 4 tiers  - Strategic: Technical Consultant, Solution Engineer - Core: GIS Analyst, Spatial Data Engineer, Geoprocessing Specialist, QA Engineer - Emerging: GeoAI/ML Engineer, BIM/GIS Specialist, 3D & Scene Developer,   Spatial Data Scientist, Drone/Reality Mapping - Delivery: Web GIS Developer, Cartography Designer  Also: - Add Smart Campus Digital Twin use case scenario - Update agent counts (218→231) and division counts (15→16) - All agents follow existing format: frontmatter + identity + mission + rules + process  * Wire gis/ division into toolchain + reconcile roster  The PR added the gis/ agents + README rows but didn't register the division where the toolchain looks, so the 13 agents would be silently skipped by convert/install/lint. Register gis (alpha: after game-development) in: - scripts/convert.sh AGENT_DIRS - scripts/install.sh AGENT_DIRS + ALL_DIVISIONS + division_emoji (🌍) - scripts/lint-agents.sh AGENT_DIRS - .github/workflows/lint-agents.yml (paths trigger + changed-file globs)  README: count 231 -> 232 / 16 divisions and add the Strategy Duel Agent roster row (reconciles the row #390 left out), so rows == count == 232.  Verified: lint PASS, convert generates all 13, `install.sh --list teams` shows \"gis 13 agents\", roster drift 0.  Co-Authored-By: Cyruschu430 <Cyruschu430@users.noreply.github.com> Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>  ---------  Co-authored-by: Hermes Agent <agent@hermes.ai> Co-authored-by: Michael Sitarzewski <msitarzewski@gmail.com> Co-authored-by: Cyruschu430 <Cyruschu430@users.noreply.github.com> Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") | 2 weeks agoJun 7, 2026 |
| [integrations](https://github.com/msitarzewski/agency-agents/tree/main/integrations "integrations") | [integrations](https://github.com/msitarzewski/agency-agents/tree/main/integrations "integrations") | [feat(gemini-cli): switch to native subagents (](https://github.com/msitarzewski/agency-agents/commit/f954ca5378e10590be1895807323c60f8b6c8036 "feat(gemini-cli): switch to native subagents (#565)  Migrates Gemini CLI to native subagents (~/.gemini/agents/) + quotes zk-steward description. Rebased from #472; e2e-verified with real gemini v0.43.0. Closes #473.  Co-Authored-By: Tomo Wang <tomo_wang@163.com>") [#565](https://github.com/msitarzewski/agency-agents/pull/565) [)](https://github.com/msitarzewski/agency-agents/commit/f954ca5378e10590be1895807323c60f8b6c8036 "feat(gemini-cli): switch to native subagents (#565)  Migrates Gemini CLI to native subagents (~/.gemini/agents/) + quotes zk-steward description. Rebased from #472; e2e-verified with real gemini v0.43.0. Closes #473.  Co-Authored-By: Tomo Wang <tomo_wang@163.com>") | 3 weeks agoJun 4, 2026 |
| [marketing](https://github.com/msitarzewski/agency-agents/tree/main/marketing "marketing") | [marketing](https://github.com/msitarzewski/agency-agents/tree/main/marketing "marketing") | [Replace corrupt soft-hyphen heading with intended thought-bubble emoji (](https://github.com/msitarzewski/agency-agents/commit/44d730cde851f142c1e3b01c33883fbfbd0a0ce7 "Replace corrupt soft-hyphen heading with intended thought-bubble emoji (#479)  Thanks @mvanhorn! 🙏") | 2 weeks agoJun 4, 2026 |
| [paid-media](https://github.com/msitarzewski/agency-agents/tree/main/paid-media "paid-media") | [paid-media](https://github.com/msitarzewski/agency-agents/tree/main/paid-media "paid-media") | [Add OpenClaw integration, emoji/vibe frontmatter, services field, and…](https://github.com/msitarzewski/agency-agents/commit/6d58ad4c0a3b8cfa9bb77125f18152312dd1e5bb "Add OpenClaw integration, emoji/vibe frontmatter, services field, and AP agent cleanup  OpenClaw support: - Add section-splitting convert_openclaw() to convert.sh that routes   ## headers by keyword into SOUL.md (persona) vs AGENTS.md (operations)   and generates IDENTITY.md with emoji + vibe from frontmatter - Add integrations/openclaw/ to .gitignore  Frontmatter additions (all 112 agents): - Add emoji and vibe fields to every agent for OpenClaw IDENTITY.md   generation and future dashboard/catalog use - Add services field to carousel-growth-engine (Gemini API, Upload-Post) - Add emoji/vibe to 7 new paid-media agents from PR #83  Agent quality: - Rewrite accounts-payable-agent to be vendor-agnostic (remove AgenticBTC   dependency, use generic payments.* interface)  Documentation: - CONTRIBUTING.md: Add Persona/Operations section grouping guidance,   emoji/vibe/services frontmatter fields, external services editorial policy - README.md: Add OpenClaw to supported tools, update agent count to 112,   reduce third-party OpenClaw repo mention to one-line attribution  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>") | 3 months agoMar 10, 2026 |
| [product](https://github.com/msitarzewski/agency-agents/tree/main/product "product") | [product](https://github.com/msitarzewski/agency-agents/tree/main/product "product") | [Add Product Manager agent - Product Division](https://github.com/msitarzewski/agency-agents/commit/cd2faa2a2a152a2e6c5d613feb1cfbf21e45591d "Add Product Manager agent - Product Division") | 3 months agoMar 13, 2026 |
| [project-management](https://github.com/msitarzewski/agency-agents/tree/main/project-management "project-management") | [project-management](https://github.com/msitarzewski/agency-agents/tree/main/project-management "project-management") | [Add Meeting Notes Specialist - project-management (](https://github.com/msitarzewski/agency-agents/commit/97f5ee539a1f0ca7a245cdf78cb0c6b3c63d4f7f "Add Meeting Notes Specialist - project-management (#521)  Thanks @jmlozano1990 — original (passed the originality check), on-template (full persona sections), and verified clean. 🙏") [#521](https://github.com/msitarzewski/agency-agents/pull/521) [)](https://github.com/msitarzewski/agency-agents/commit/97f5ee539a1f0ca7a245cdf78cb0c6b3c63d4f7f "Add Meeting Notes Specialist - project-management (#521)  Thanks @jmlozano1990 — original (passed the originality check), on-template (full persona sections), and verified clean. 🙏") | 3 weeks agoJun 3, 2026 |
| [sales](https://github.com/msitarzewski/agency-agents/tree/main/sales "sales") | [sales](https://github.com/msitarzewski/agency-agents/tree/main/sales "sales") | [Add Offer and Lead Gen Strategist (](https://github.com/msitarzewski/agency-agents/commit/4fdf1ebf2bf32ee23b54abd24eaf36131cce8cdb "Add Offer and Lead Gen Strategist (#510)  Thanks @hedonnn — original (passed the originality check), on-template (full persona sections), and verified clean. 🙏") [#510](https://github.com/msitarzewski/agency-agents/pull/510) [)](https://github.com/msitarzewski/agency-agents/commit/4fdf1ebf2bf32ee23b54abd24eaf36131cce8cdb "Add Offer and Lead Gen Strategist (#510)  Thanks @hedonnn — original (passed the originality check), on-template (full persona sections), and verified clean. 🙏") | 3 weeks agoJun 3, 2026 |
| [scripts](https://github.com/msitarzewski/agency-agents/tree/main/scripts "scripts") | [scripts](https://github.com/msitarzewski/agency-agents/tree/main/scripts "scripts") | [Add tools.json canonical registry + check-tools.sh guard (](https://github.com/msitarzewski/agency-agents/commit/9262649a48aff36f90350b455f015e248c2038ce "Add tools.json canonical registry + check-tools.sh guard (#606)  Mirrors the divisions.json / check-divisions.sh pattern for the supported tool set. tools.json (repo root) is the single source of truth for all 13 tools, consumed by the Agency Agents app and by scripts/convert.sh + scripts/install.sh. scripts/check-tools.sh (no-jq, bash 3.2) fails the build if tools.json disagrees with ALL_TOOLS in install.sh or the converter set in convert.sh, or if any entry is missing id/label/kebab/format/dest.  Every tool carries its real install contract (format, dest, scope, detect, version) — verified against actual convert.sh/install.sh behavior via a sandboxed install pass (all dest templates resolve to the real on-disk layout).  `format` is the renderer contract: same name => byte-identical output. The five formerly-undescribed tools get distinct names — aider-conventions, antigravity-skill (its non-deterministic date_added means it can't share osaurus's skill-md), kimi-agent, openclaw-workspace, windsurf-rules — none colliding with the app's implemented renderers. Removed the `wired` field: it encoded app renderer state (not catalog truth); consumers derive installability from `format` against their own implemented-format set. check-tools.sh requires format+dest for every tool, not just some. Also fixes antigravity detect (.gemini/antigravity-cli -> .gemini/antigravity/skills, matching the actual code).  Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") [#606](https://github.com/msitarzewski/agency-agents/pull/606) [)](https://github.com/msitarzewski/agency-agents/commit/9262649a48aff36f90350b455f015e248c2038ce "Add tools.json canonical registry + check-tools.sh guard (#606)  Mirrors the divisions.json / check-divisions.sh pattern for the supported tool set. tools.json (repo root) is the single source of truth for all 13 tools, consumed by the Agency Agents app and by scripts/convert.sh + scripts/install.sh. scripts/check-tools.sh (no-jq, bash 3.2) fails the build if tools.json disagrees with ALL_TOOLS in install.sh or the converter set in convert.sh, or if any entry is missing id/label/kebab/format/dest.  Every tool carries its real install contract (format, dest, scope, detect, version) — verified against actual convert.sh/install.sh behavior via a sandboxed install pass (all dest templates resolve to the real on-disk layout).  `format` is the renderer contract: same name => byte-identical output. The five formerly-undescribed tools get distinct names — aider-conventions, antigravity-skill (its non-deterministic date_added means it can't share osaurus's skill-md), kimi-agent, openclaw-workspace, windsurf-rules — none colliding with the app's implemented renderers. Removed the `wired` field: it encoded app renderer state (not catalog truth); consumers derive installability from `format` against their own implemented-format set. check-tools.sh requires format+dest for every tool, not just some. Also fixes antigravity detect (.gemini/antigravity-cli -> .gemini/antigravity/skills, matching the actual code).  Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") | 1 hour agoJun 22, 2026 |
| [security](https://github.com/msitarzewski/agency-agents/tree/main/security "security") | [security](https://github.com/msitarzewski/agency-agents/tree/main/security "security") | [feat: add Security division (resolves RFC](https://github.com/msitarzewski/agency-agents/commit/8237f99b850db8d5195815f80893554034fe983d "feat: add Security division (resolves RFC #438) (#566)  New security/ division: 6 new agents (#223, #326) + 4 relocated; differentiated Security Architect; 209 agents / 15 divisions. Closes #223, #326.  Co-Authored-By: anonym88-ai <anonym88-ai@users.noreply.github.com> Co-Authored-By: caveat-ops <caveat-ops@users.noreply.github.com>") [#438](https://github.com/msitarzewski/agency-agents/discussions/438) [) (](https://github.com/msitarzewski/agency-agents/commit/8237f99b850db8d5195815f80893554034fe983d "feat: add Security division (resolves RFC #438) (#566)  New security/ division: 6 new agents (#223, #326) + 4 relocated; differentiated Security Architect; 209 agents / 15 divisions. Closes #223, #326.  Co-Authored-By: anonym88-ai <anonym88-ai@users.noreply.github.com> Co-Authored-By: caveat-ops <caveat-ops@users.noreply.github.com>") [#566](https://github.com/msitarzewski/agency-agents/pull/566) [)](https://github.com/msitarzewski/agency-agents/commit/8237f99b850db8d5195815f80893554034fe983d "feat: add Security division (resolves RFC #438) (#566)  New security/ division: 6 new agents (#223, #326) + 4 relocated; differentiated Security Architect; 209 agents / 15 divisions. Closes #223, #326.  Co-Authored-By: anonym88-ai <anonym88-ai@users.noreply.github.com> Co-Authored-By: caveat-ops <caveat-ops@users.noreply.github.com>") | 2 weeks agoJun 4, 2026 |
| [spatial-computing](https://github.com/msitarzewski/agency-agents/tree/main/spatial-computing "spatial-computing") | [spatial-computing](https://github.com/msitarzewski/agency-agents/tree/main/spatial-computing "spatial-computing") | [Add OpenClaw integration, emoji/vibe frontmatter, services field, and…](https://github.com/msitarzewski/agency-agents/commit/6d58ad4c0a3b8cfa9bb77125f18152312dd1e5bb "Add OpenClaw integration, emoji/vibe frontmatter, services field, and AP agent cleanup  OpenClaw support: - Add section-splitting convert_openclaw() to convert.sh that routes   ## headers by keyword into SOUL.md (persona) vs AGENTS.md (operations)   and generates IDENTITY.md with emoji + vibe from frontmatter - Add integrations/openclaw/ to .gitignore  Frontmatter additions (all 112 agents): - Add emoji and vibe fields to every agent for OpenClaw IDENTITY.md   generation and future dashboard/catalog use - Add services field to carousel-growth-engine (Gemini API, Upload-Post) - Add emoji/vibe to 7 new paid-media agents from PR #83  Agent quality: - Rewrite accounts-payable-agent to be vendor-agnostic (remove AgenticBTC   dependency, use generic payments.* interface)  Documentation: - CONTRIBUTING.md: Add Persona/Operations section grouping guidance,   emoji/vibe/services frontmatter fields, external services editorial policy - README.md: Add OpenClaw to supported tools, update agent count to 112,   reduce third-party OpenClaw repo mention to one-line attribution  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>") | 3 months agoMar 10, 2026 |
| [specialized](https://github.com/msitarzewski/agency-agents/tree/main/specialized "specialized") | [specialized](https://github.com/msitarzewski/agency-agents/tree/main/specialized "specialized") | [Strategy Duel Agent: Model-agnostic, Game Theory & Stratagems Orchest…](https://github.com/msitarzewski/agency-agents/commit/d6553e261e595c651064f899a6c33dd5aa71c9e3 "Strategy Duel Agent: Model-agnostic, Game Theory & Stratagems Orchestrator (#390)  * Add Strategy Duel Agent: model-agnostic, game theory & stratagems orchestrator  * fix: move Strategy Duel Agent to specialized/ per reviewer feedback  Relocate from engineering/ to specialized/specialized-strategy-duel-agent.md as the agent is a strategic thinking/negotiation simulator, not a software engineering tool.  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>  * Strip leftover review-note comment above frontmatter  The agent file led with an HTML comment block before the YAML frontmatter, so the first line was not '---'. That breaks the linter's frontmatter check and is_agent_file() (convert/install would silently skip the agent). Remove it so '---' is line 1.  Co-Authored-By: DKFuH <info@tischlermeister-klas.de> Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>  ---------  Co-authored-by: Claude Sonnet 4.6 <noreply@anthropic.com> Co-authored-by: Michael Sitarzewski <msitarzewski@gmail.com>") | 2 weeks agoJun 7, 2026 |
| [strategy](https://github.com/msitarzewski/agency-agents/tree/main/strategy "strategy") | [strategy](https://github.com/msitarzewski/agency-agents/tree/main/strategy "strategy") | [fix: rename 'Data Analytics Reporter' to 'Analytics Reporter' in stra…](https://github.com/msitarzewski/agency-agents/commit/81f5a6998a8c340b2c1121b41fe3c0bd81025843 "fix: rename 'Data Analytics Reporter' to 'Analytics Reporter' in strategy docs  The strategy documentation references a 'Data Analytics Reporter' agent that does not exist. The actual agent is 'Analytics Reporter' defined in support/support-analytics-reporter.md. This fixes all 6 occurrences across 4 strategy files.  Fixes #291  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>") | 3 months agoMar 21, 2026 |
| [support](https://github.com/msitarzewski/agency-agents/tree/main/support "support") | [support](https://github.com/msitarzewski/agency-agents/tree/main/support "support") | [Add OpenClaw integration, emoji/vibe frontmatter, services field, and…](https://github.com/msitarzewski/agency-agents/commit/6d58ad4c0a3b8cfa9bb77125f18152312dd1e5bb "Add OpenClaw integration, emoji/vibe frontmatter, services field, and AP agent cleanup  OpenClaw support: - Add section-splitting convert_openclaw() to convert.sh that routes   ## headers by keyword into SOUL.md (persona) vs AGENTS.md (operations)   and generates IDENTITY.md with emoji + vibe from frontmatter - Add integrations/openclaw/ to .gitignore  Frontmatter additions (all 112 agents): - Add emoji and vibe fields to every agent for OpenClaw IDENTITY.md   generation and future dashboard/catalog use - Add services field to carousel-growth-engine (Gemini API, Upload-Post) - Add emoji/vibe to 7 new paid-media agents from PR #83  Agent quality: - Rewrite accounts-payable-agent to be vendor-agnostic (remove AgenticBTC   dependency, use generic payments.* interface)  Documentation: - CONTRIBUTING.md: Add Persona/Operations section grouping guidance,   emoji/vibe/services frontmatter fields, external services editorial policy - README.md: Add OpenClaw to supported tools, update agent count to 112,   reduce third-party OpenClaw repo mention to one-line attribution  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>") | 3 months agoMar 10, 2026 |
| [testing](https://github.com/msitarzewski/agency-agents/tree/main/testing "testing") | [testing](https://github.com/msitarzewski/agency-agents/tree/main/testing "testing") | [fix: scrub hardcoded test credentials (](https://github.com/msitarzewski/agency-agents/commit/4e905cff59e3e3e5b5566d410b2b49e9ab22ecb0 "fix: scrub hardcoded test credentials (#477) (#571)  Replace literal passwords in two testing-agent code samples with environment-variable reads — the secure, idiomatic pattern for each framework rather than a placeholder string: - testing-api-tester.md: 'secure_password' -> process.env.TEST_USER_PASSWORD - testing-performance-benchmarker.md: 'password123' -> __ENV.TEST_USER_PASSWORD (k6)  Removes the weak-credential examples flagged in #477 and models good secrets hygiene for anyone copying these snippets.  Closes #477  Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") [#477](https://github.com/msitarzewski/agency-agents/issues/477) [) (](https://github.com/msitarzewski/agency-agents/commit/4e905cff59e3e3e5b5566d410b2b49e9ab22ecb0 "fix: scrub hardcoded test credentials (#477) (#571)  Replace literal passwords in two testing-agent code samples with environment-variable reads — the secure, idiomatic pattern for each framework rather than a placeholder string: - testing-api-tester.md: 'secure_password' -> process.env.TEST_USER_PASSWORD - testing-performance-benchmarker.md: 'password123' -> __ENV.TEST_USER_PASSWORD (k6)  Removes the weak-credential examples flagged in #477 and models good secrets hygiene for anyone copying these snippets.  Closes #477  Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") [#571](https://github.com/msitarzewski/agency-agents/pull/571) [)](https://github.com/msitarzewski/agency-agents/commit/4e905cff59e3e3e5b5566d410b2b49e9ab22ecb0 "fix: scrub hardcoded test credentials (#477) (#571)  Replace literal passwords in two testing-agent code samples with environment-variable reads — the secure, idiomatic pattern for each framework rather than a placeholder string: - testing-api-tester.md: 'secure_password' -> process.env.TEST_USER_PASSWORD - testing-performance-benchmarker.md: 'password123' -> __ENV.TEST_USER_PASSWORD (k6)  Removes the weak-credential examples flagged in #477 and models good secrets hygiene for anyone copying these snippets.  Closes #477  Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") | 2 weeks agoJun 6, 2026 |
| [.gitattributes](https://github.com/msitarzewski/agency-agents/blob/main/.gitattributes ".gitattributes") | [.gitattributes](https://github.com/msitarzewski/agency-agents/blob/main/.gitattributes ".gitattributes") | [Add .gitattributes to enforce LF line endings](https://github.com/msitarzewski/agency-agents/commit/f2449908cddaf67ee5e59af572cff1074a0b893b "Add .gitattributes to enforce LF line endings  Prevents CRLF line endings from being committed on Windows, which can break frontmatter parsing in agent markdown files.") | 3 months agoMar 5, 2026 |
| [.gitignore](https://github.com/msitarzewski/agency-agents/blob/main/.gitignore ".gitignore") | [.gitignore](https://github.com/msitarzewski/agency-agents/blob/main/.gitignore ".gitignore") | [Add Osaurus tool target + document the division contract (](https://github.com/msitarzewski/agency-agents/commit/f56a2179455e35a76dfb8fead36d9cf5c2612eff "Add Osaurus tool target + document the division contract (#603)  Tooling: add Osaurus (Anthropic Agent-Skills SKILL.md format) as a conversion and install target, wired into convert.sh (convert_osaurus + dispatch/valid/all/ parallel lists, --osaurus flag) and install.sh (detect/label/dest/install_osaurus + dispatch). Generated output lands in integrations/osaurus/agency-*/SKILL.md and is gitignored like every other tool's output (regenerate via convert.sh osaurus).  Docs/guardrails — make the division contract discoverable, since it lived only in scattered script comments and tripped up multiple contributors: - CONTRIBUTING.md: complete the division list to all 16 (was missing academic/   gis/sales) and document that divisions.json is the source of truth (CI-checked   by check-divisions.sh), how to propose a new division, and that strategy/   (NEXUS playbooks) and integrations/ (generated output) are NOT divisions. - install.sh: correct the stale \"sync with convert.sh / lint-agents.sh\" comment —   install.sh intentionally keeps strategy/ in AGENT_DIRS (filtered at scan time),   so it is deliberately NOT the same set as the other two. - .gitignore: ignore integrations/osaurus/agency-*/ (the osaurus output was the   one tool whose generated files weren't excluded).  Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") [#603](https://github.com/msitarzewski/agency-agents/pull/603) [)](https://github.com/msitarzewski/agency-agents/commit/f56a2179455e35a76dfb8fead36d9cf5c2612eff "Add Osaurus tool target + document the division contract (#603)  Tooling: add Osaurus (Anthropic Agent-Skills SKILL.md format) as a conversion and install target, wired into convert.sh (convert_osaurus + dispatch/valid/all/ parallel lists, --osaurus flag) and install.sh (detect/label/dest/install_osaurus + dispatch). Generated output lands in integrations/osaurus/agency-*/SKILL.md and is gitignored like every other tool's output (regenerate via convert.sh osaurus).  Docs/guardrails — make the division contract discoverable, since it lived only in scattered script comments and tripped up multiple contributors: - CONTRIBUTING.md: complete the division list to all 16 (was missing academic/   gis/sales) and document that divisions.json is the source of truth (CI-checked   by check-divisions.sh), how to propose a new division, and that strategy/   (NEXUS playbooks) and integrations/ (generated output) are NOT divisions. - install.sh: correct the stale \"sync with convert.sh / lint-agents.sh\" comment —   install.sh intentionally keeps strategy/ in AGENT_DIRS (filtered at scan time),   so it is deliberately NOT the same set as the other two. - .gitignore: ignore integrations/osaurus/agency-*/ (the osaurus output was the   one tool whose generated files weren't excluded).  Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") | 10 hours agoJun 21, 2026 |
| [CONTRIBUTING.md](https://github.com/msitarzewski/agency-agents/blob/main/CONTRIBUTING.md "CONTRIBUTING.md") | [CONTRIBUTING.md](https://github.com/msitarzewski/agency-agents/blob/main/CONTRIBUTING.md "CONTRIBUTING.md") | [Add Osaurus tool target + document the division contract (](https://github.com/msitarzewski/agency-agents/commit/f56a2179455e35a76dfb8fead36d9cf5c2612eff "Add Osaurus tool target + document the division contract (#603)  Tooling: add Osaurus (Anthropic Agent-Skills SKILL.md format) as a conversion and install target, wired into convert.sh (convert_osaurus + dispatch/valid/all/ parallel lists, --osaurus flag) and install.sh (detect/label/dest/install_osaurus + dispatch). Generated output lands in integrations/osaurus/agency-*/SKILL.md and is gitignored like every other tool's output (regenerate via convert.sh osaurus).  Docs/guardrails — make the division contract discoverable, since it lived only in scattered script comments and tripped up multiple contributors: - CONTRIBUTING.md: complete the division list to all 16 (was missing academic/   gis/sales) and document that divisions.json is the source of truth (CI-checked   by check-divisions.sh), how to propose a new division, and that strategy/   (NEXUS playbooks) and integrations/ (generated output) are NOT divisions. - install.sh: correct the stale \"sync with convert.sh / lint-agents.sh\" comment —   install.sh intentionally keeps strategy/ in AGENT_DIRS (filtered at scan time),   so it is deliberately NOT the same set as the other two. - .gitignore: ignore integrations/osaurus/agency-*/ (the osaurus output was the   one tool whose generated files weren't excluded).  Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") [#603](https://github.com/msitarzewski/agency-agents/pull/603) [)](https://github.com/msitarzewski/agency-agents/commit/f56a2179455e35a76dfb8fead36d9cf5c2612eff "Add Osaurus tool target + document the division contract (#603)  Tooling: add Osaurus (Anthropic Agent-Skills SKILL.md format) as a conversion and install target, wired into convert.sh (convert_osaurus + dispatch/valid/all/ parallel lists, --osaurus flag) and install.sh (detect/label/dest/install_osaurus + dispatch). Generated output lands in integrations/osaurus/agency-*/SKILL.md and is gitignored like every other tool's output (regenerate via convert.sh osaurus).  Docs/guardrails — make the division contract discoverable, since it lived only in scattered script comments and tripped up multiple contributors: - CONTRIBUTING.md: complete the division list to all 16 (was missing academic/   gis/sales) and document that divisions.json is the source of truth (CI-checked   by check-divisions.sh), how to propose a new division, and that strategy/   (NEXUS playbooks) and integrations/ (generated output) are NOT divisions. - install.sh: correct the stale \"sync with convert.sh / lint-agents.sh\" comment —   install.sh intentionally keeps strategy/ in AGENT_DIRS (filtered at scan time),   so it is deliberately NOT the same set as the other two. - .gitignore: ignore integrations/osaurus/agency-*/ (the osaurus output was the   one tool whose generated files weren't excluded).  Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") | 10 hours agoJun 21, 2026 |
| [CONTRIBUTING\_zh-CN.md](https://github.com/msitarzewski/agency-agents/blob/main/CONTRIBUTING_zh-CN.md "CONTRIBUTING_zh-CN.md") | [CONTRIBUTING\_zh-CN.md](https://github.com/msitarzewski/agency-agents/blob/main/CONTRIBUTING_zh-CN.md "CONTRIBUTING_zh-CN.md") | [Update CONTRIBUTING\_zh-CN.md](https://github.com/msitarzewski/agency-agents/commit/73c15438d67d6e894f364396104a2fa3a7c2f939 "Update CONTRIBUTING_zh-CN.md  Updated the resource links at the bottom of the document to point to msitarzewski/agency-agents instead of my personal fork, as requested.") | 3 months agoMar 12, 2026 |
| [LICENSE](https://github.com/msitarzewski/agency-agents/blob/main/LICENSE "LICENSE") | [LICENSE](https://github.com/msitarzewski/agency-agents/blob/main/LICENSE "LICENSE") | [Initial commit: The Agency - 51 AI Specialist Agents](https://github.com/msitarzewski/agency-agents/commit/98eea4c13983187cbabde84c1a2cd3e8a966b7d4 "Initial commit: The Agency - 51 AI Specialist Agents  Complete collection of specialized AI agent personalities: - 7 Engineering specialists (Frontend, Backend, Mobile, AI, DevOps, etc.) - 6 Design specialists (UI, UX, Brand, Whimsy, etc.) - 8 Marketing specialists (Growth, Content, Social Media, etc.) - 3 Product specialists (Sprint Planning, Research, Feedback) - 5 Project Management specialists - 7 Testing specialists (QA, Performance, API, etc.) - 6 Support specialists (Analytics, Finance, Legal, etc.) - 6 Spatial Computing specialists (XR, AR/VR, Vision Pro) - 3 Specialized agents (Orchestrator, Data Analytics, LSP)  Each agent includes: - Distinct personality and communication style - Technical deliverables with code examples - Step-by-step workflows - Success metrics and benchmarks - Real-world tested approaches  Ready for community contributions and feedback!") | 8 months agoOct 13, 2025 |
| [README.md](https://github.com/msitarzewski/agency-agents/blob/main/README.md "README.md") | [README.md](https://github.com/msitarzewski/agency-agents/blob/main/README.md "README.md") | [feat: add GIS division with 13 specialized agents across 4 tiers (](https://github.com/msitarzewski/agency-agents/commit/a077c9ac0be381ec15e7dcbb690f641d6091a5db "feat: add GIS division with 13 specialized agents across 4 tiers (#572)  * feat: add GIS division with 13 specialized agents across 4 tiers  - Strategic: Technical Consultant, Solution Engineer - Core: GIS Analyst, Spatial Data Engineer, Geoprocessing Specialist, QA Engineer - Emerging: GeoAI/ML Engineer, BIM/GIS Specialist, 3D & Scene Developer,   Spatial Data Scientist, Drone/Reality Mapping - Delivery: Web GIS Developer, Cartography Designer  Also: - Add Smart Campus Digital Twin use case scenario - Update agent counts (218→231) and division counts (15→16) - All agents follow existing format: frontmatter + identity + mission + rules + process  * Wire gis/ division into toolchain + reconcile roster  The PR added the gis/ agents + README rows but didn't register the division where the toolchain looks, so the 13 agents would be silently skipped by convert/install/lint. Register gis (alpha: after game-development) in: - scripts/convert.sh AGENT_DIRS - scripts/install.sh AGENT_DIRS + ALL_DIVISIONS + division_emoji (🌍) - scripts/lint-agents.sh AGENT_DIRS - .github/workflows/lint-agents.yml (paths trigger + changed-file globs)  README: count 231 -> 232 / 16 divisions and add the Strategy Duel Agent roster row (reconciles the row #390 left out), so rows == count == 232.  Verified: lint PASS, convert generates all 13, `install.sh --list teams` shows \"gis 13 agents\", roster drift 0.  Co-Authored-By: Cyruschu430 <Cyruschu430@users.noreply.github.com> Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>  ---------  Co-authored-by: Hermes Agent <agent@hermes.ai> Co-authored-by: Michael Sitarzewski <msitarzewski@gmail.com> Co-authored-by: Cyruschu430 <Cyruschu430@users.noreply.github.com> Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") [#572](https://github.com/msitarzewski/agency-agents/pull/572) [)](https://github.com/msitarzewski/agency-agents/commit/a077c9ac0be381ec15e7dcbb690f641d6091a5db "feat: add GIS division with 13 specialized agents across 4 tiers (#572)  * feat: add GIS division with 13 specialized agents across 4 tiers  - Strategic: Technical Consultant, Solution Engineer - Core: GIS Analyst, Spatial Data Engineer, Geoprocessing Specialist, QA Engineer - Emerging: GeoAI/ML Engineer, BIM/GIS Specialist, 3D & Scene Developer,   Spatial Data Scientist, Drone/Reality Mapping - Delivery: Web GIS Developer, Cartography Designer  Also: - Add Smart Campus Digital Twin use case scenario - Update agent counts (218→231) and division counts (15→16) - All agents follow existing format: frontmatter + identity + mission + rules + process  * Wire gis/ division into toolchain + reconcile roster  The PR added the gis/ agents + README rows but didn't register the division where the toolchain looks, so the 13 agents would be silently skipped by convert/install/lint. Register gis (alpha: after game-development) in: - scripts/convert.sh AGENT_DIRS - scripts/install.sh AGENT_DIRS + ALL_DIVISIONS + division_emoji (🌍) - scripts/lint-agents.sh AGENT_DIRS - .github/workflows/lint-agents.yml (paths trigger + changed-file globs)  README: count 231 -> 232 / 16 divisions and add the Strategy Duel Agent roster row (reconciles the row #390 left out), so rows == count == 232.  Verified: lint PASS, convert generates all 13, `install.sh --list teams` shows \"gis 13 agents\", roster drift 0.  Co-Authored-By: Cyruschu430 <Cyruschu430@users.noreply.github.com> Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>  ---------  Co-authored-by: Hermes Agent <agent@hermes.ai> Co-authored-by: Michael Sitarzewski <msitarzewski@gmail.com> Co-authored-by: Cyruschu430 <Cyruschu430@users.noreply.github.com> Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") | 2 weeks agoJun 7, 2026 |
| [SECURITY.md](https://github.com/msitarzewski/agency-agents/blob/main/SECURITY.md "SECURITY.md") | [SECURITY.md](https://github.com/msitarzewski/agency-agents/blob/main/SECURITY.md "SECURITY.md") | [fix: remove stray EOFcat heredoc artifact from SECURITY.md (](https://github.com/msitarzewski/agency-agents/commit/083ce47e1385cd10a5dbfa1f3254bc6f0249217e "fix: remove stray EOFcat heredoc artifact from SECURITY.md (#531)  Removes the stray `EOFcat SECURITY.md` line accidentally left at the end of SECURITY.md.  Closes #530. Thanks to @akhilesharora.") [#531](https://github.com/msitarzewski/agency-agents/pull/531) [)](https://github.com/msitarzewski/agency-agents/commit/083ce47e1385cd10a5dbfa1f3254bc6f0249217e "fix: remove stray EOFcat heredoc artifact from SECURITY.md (#531)  Removes the stray `EOFcat SECURITY.md` line accidentally left at the end of SECURITY.md.  Closes #530. Thanks to @akhilesharora.") | 3 weeks agoJun 2, 2026 |
| [divisions.json](https://github.com/msitarzewski/agency-agents/blob/main/divisions.json "divisions.json") | [divisions.json](https://github.com/msitarzewski/agency-agents/blob/main/divisions.json "divisions.json") | [Drop strategy/ as a division — it's playbooks/runbooks, not agents (](https://github.com/msitarzewski/agency-agents/commit/4d07efdb70ea9cbb6c471bc126400ddec1639a08 "Drop strategy/ as a division — it's playbooks/runbooks, not agents (#595)  strategy/ holds 16 markdown files and ZERO have agent frontmatter — they're playbooks (playbooks/phase-*.md), runbooks (runbooks/scenario-*.md), and briefs (EXECUTIVE-BRIEF.md, QUICKSTART.md, nexus-strategy.md), not agent definitions. There are 16 real agent divisions, 232 agents; strategy is not one of them.  #592 added `strategy` to lint-agents.sh AGENT_DIRS and the lint workflow paths (to match divisions.json), which made CI lint those 16 frontmatter-less docs as agents and fail every one with \"missing frontmatter opening ---\". So any PR touching strategy/ broke CI. The original lint-agents.sh correctly excluded strategy; #592 misread that deliberate exclusion as drift (same mistake as integrations/ in #593).  Fix: remove strategy from convert.sh / lint-agents.sh AGENT_DIRS, the lint workflow, and divisions.json; add it to NON_DIVISION_DIRS in check-divisions.sh. divisions.json is now 16, matching the app's parse_agent count exactly.  Also add a content-derived backstop to check-divisions.sh: every division must contain at least one .md with '---' frontmatter, or the build fails. This is what stops a docs/playbook directory from being registered as an empty agent division again — regardless of whether someone remembers the exclude list.  check-divisions.sh PASSES at 16; negative-tested that re-adding strategy fails with \"division 'strategy' has no agent files\".  Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") [#595](https://github.com/msitarzewski/agency-agents/pull/595) | 4 days agoJun 17, 2026 |
| [tools.json](https://github.com/msitarzewski/agency-agents/blob/main/tools.json "tools.json") | [tools.json](https://github.com/msitarzewski/agency-agents/blob/main/tools.json "tools.json") | [Add tools.json canonical registry + check-tools.sh guard (](https://github.com/msitarzewski/agency-agents/commit/9262649a48aff36f90350b455f015e248c2038ce "Add tools.json canonical registry + check-tools.sh guard (#606)  Mirrors the divisions.json / check-divisions.sh pattern for the supported tool set. tools.json (repo root) is the single source of truth for all 13 tools, consumed by the Agency Agents app and by scripts/convert.sh + scripts/install.sh. scripts/check-tools.sh (no-jq, bash 3.2) fails the build if tools.json disagrees with ALL_TOOLS in install.sh or the converter set in convert.sh, or if any entry is missing id/label/kebab/format/dest.  Every tool carries its real install contract (format, dest, scope, detect, version) — verified against actual convert.sh/install.sh behavior via a sandboxed install pass (all dest templates resolve to the real on-disk layout).  `format` is the renderer contract: same name => byte-identical output. The five formerly-undescribed tools get distinct names — aider-conventions, antigravity-skill (its non-deterministic date_added means it can't share osaurus's skill-md), kimi-agent, openclaw-workspace, windsurf-rules — none colliding with the app's implemented renderers. Removed the `wired` field: it encoded app renderer state (not catalog truth); consumers derive installability from `format` against their own implemented-format set. check-tools.sh requires format+dest for every tool, not just some. Also fixes antigravity detect (.gemini/antigravity-cli -> .gemini/antigravity/skills, matching the actual code).  Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") [#606](https://github.com/msitarzewski/agency-agents/pull/606) [)](https://github.com/msitarzewski/agency-agents/commit/9262649a48aff36f90350b455f015e248c2038ce "Add tools.json canonical registry + check-tools.sh guard (#606)  Mirrors the divisions.json / check-divisions.sh pattern for the supported tool set. tools.json (repo root) is the single source of truth for all 13 tools, consumed by the Agency Agents app and by scripts/convert.sh + scripts/install.sh. scripts/check-tools.sh (no-jq, bash 3.2) fails the build if tools.json disagrees with ALL_TOOLS in install.sh or the converter set in convert.sh, or if any entry is missing id/label/kebab/format/dest.  Every tool carries its real install contract (format, dest, scope, detect, version) — verified against actual convert.sh/install.sh behavior via a sandboxed install pass (all dest templates resolve to the real on-disk layout).  `format` is the renderer contract: same name => byte-identical output. The five formerly-undescribed tools get distinct names — aider-conventions, antigravity-skill (its non-deterministic date_added means it can't share osaurus's skill-md), kimi-agent, openclaw-workspace, windsurf-rules — none colliding with the app's implemented renderers. Removed the `wired` field: it encoded app renderer state (not catalog truth); consumers derive installability from `format` against their own implemented-format set. check-tools.sh requires format+dest for every tool, not just some. Also fixes antigravity detect (.gemini/antigravity-cli -> .gemini/antigravity/skills, matching the actual code).  Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>") | 1 hour agoJun 22, 2026 |
| View all files |

## Repository files navigation

# 🎭 The Agency: AI Specialists Ready to Transform Your Workflow

[Permalink: 🎭 The Agency: AI Specialists Ready to Transform Your Workflow](https://github.com/msitarzewski/agency-agents#-the-agency-ai-specialists-ready-to-transform-your-workflow)

> **A complete AI agency at your fingertips** \- From frontend wizards to Reddit community ninjas, from whimsy injectors to reality checkers. Each agent is a specialized expert with personality, processes, and proven deliverables.

[![GitHub stars](https://camo.githubusercontent.com/1bdae7a86b6ca2d1bc969d929a6dc4283a746aa96799f9fab75fce7bfed32560/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f73746172732f6d73697461727a6577736b692f6167656e63792d6167656e74733f7374796c653d736f6369616c)](https://github.com/msitarzewski/agency-agents)[![License: MIT](https://camo.githubusercontent.com/fdf2982b9f5d7489dcf44570e714e3a15fce6253e0cc6b5aa61a075aac2ff71b/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4c6963656e73652d4d49542d79656c6c6f772e737667)](https://opensource.org/licenses/MIT)[![PRs Welcome](https://camo.githubusercontent.com/dd0b24c1e6776719edb2c273548a510d6490d8d25269a043dfabbd38419905da/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5052732d77656c636f6d652d627269676874677265656e2e737667)](https://makeapullrequest.com/)[![Sponsor](https://camo.githubusercontent.com/856bf8030a60ef09cec6b0ccacae765ece8eef592b2642a33dcfec11fb623e49/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f53706f6e736f722d2545322539442541342d70696e6b3f6c6f676f3d676974687562)](https://github.com/sponsors/msitarzewski)

* * *

## 🚀 What Is This?

[Permalink: 🚀 What Is This?](https://github.com/msitarzewski/agency-agents#-what-is-this)

Born from a Reddit thread and months of iteration, **The Agency** is a growing collection of meticulously crafted AI agent personalities. Each agent is:

- **🎯 Specialized**: Deep expertise in their domain (not generic prompt templates)
- **🧠 Personality-Driven**: Unique voice, communication style, and approach
- **📋 Deliverable-Focused**: Real code, processes, and measurable outcomes
- **✅ Production-Ready**: Battle-tested workflows and success metrics

**Think of it as**: Assembling your dream team, except they're AI specialists who never sleep, never complain, and always deliver.

* * *

## ⚡ Quick Start

[Permalink: ⚡ Quick Start](https://github.com/msitarzewski/agency-agents#-quick-start)

### Option 1: Use with Claude Code (Recommended)

[Permalink: Option 1: Use with Claude Code (Recommended)](https://github.com/msitarzewski/agency-agents#option-1-use-with-claude-code-recommended)

```
# Install all agents to your Claude Code directory
./scripts/install.sh --tool claude-code

# Or manually copy a category if you only want one division
cp engineering/*.md ~/.claude/agents/

# Then activate any agent in your Claude Code sessions:
# "Hey Claude, activate Frontend Developer mode and help me build a React component"
```

### Option 2: Use as Reference

[Permalink: Option 2: Use as Reference](https://github.com/msitarzewski/agency-agents#option-2-use-as-reference)

Each agent file contains:

- Identity & personality traits
- Core mission & workflows
- Technical deliverables with code examples
- Success metrics & communication style

Browse the agents below and copy/adapt the ones you need!

### Option 3: Use with Other Tools (GitHub Copilot, Antigravity, Gemini CLI, OpenCode, OpenClaw, Cursor, Aider, Windsurf, Kimi Code, Codex)

[Permalink: Option 3: Use with Other Tools (GitHub Copilot, Antigravity, Gemini CLI, OpenCode, OpenClaw, Cursor, Aider, Windsurf, Kimi Code, Codex)](https://github.com/msitarzewski/agency-agents#option-3-use-with-other-tools-github-copilot-antigravity-gemini-cli-opencode-openclaw-cursor-aider-windsurf-kimi-code-codex)

```
# Step 1 -- generate integration files for all supported tools
./scripts/convert.sh

# Step 2 -- install interactively (auto-detects what you have installed)
./scripts/install.sh

# Or target a specific tool directly
./scripts/install.sh --tool antigravity
./scripts/install.sh --tool gemini-cli
./scripts/install.sh --tool opencode
./scripts/install.sh --tool copilot
./scripts/install.sh --tool openclaw
./scripts/install.sh --tool cursor
./scripts/install.sh --tool aider
./scripts/install.sh --tool windsurf
./scripts/install.sh --tool kimi
./scripts/install.sh --tool codex
```

**Install only the teams you need** (not everyone wants all 16 divisions):

```
./scripts/install.sh                                    # interactive wizard: pick tools + teams
./scripts/install.sh --tool claude-code --division engineering,security
./scripts/install.sh --tool cursor --agent frontend-developer,ui-designer
./scripts/install.sh --list teams                       # see every team + agent count
./scripts/install.sh --tool opencode --division engineering --dry-run
```

> **OpenCode note:** OpenCode's runtime currently registers only ~119 agents and silently drops the rest ( [upstream bug](https://github.com/anomalyco/opencode/issues/27988)). Installing a subset with `--division` keeps you under that limit. The installer warns you when a selection would exceed it.

See the [Multi-Tool Integrations](https://github.com/msitarzewski/agency-agents#-multi-tool-integrations) section below for full details.

* * *

## 🎨 The Agency Roster

[Permalink: 🎨 The Agency Roster](https://github.com/msitarzewski/agency-agents#-the-agency-roster)

### 💻 Engineering Division

[Permalink: 💻 Engineering Division](https://github.com/msitarzewski/agency-agents#-engineering-division)

Building the future, one commit at a time.

| Agent | Specialty | When to Use |
| --- | --- | --- |
| 🎨 [Frontend Developer](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-frontend-developer.md) | React/Vue/Angular, UI implementation, performance | Modern web apps, pixel-perfect UIs, Core Web Vitals optimization |
| 🏗️ [Backend Architect](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-backend-architect.md) | API design, database architecture, scalability | Server-side systems, microservices, cloud infrastructure |
| 📱 [Mobile App Builder](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-mobile-app-builder.md) | iOS/Android, React Native, Flutter | Native and cross-platform mobile applications |
| 🤖 [AI Engineer](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-ai-engineer.md) | ML models, deployment, AI integration | Machine learning features, data pipelines, AI-powered apps |
| 🚀 [DevOps Automator](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-devops-automator.md) | CI/CD, infrastructure automation, cloud ops | Pipeline development, deployment automation, monitoring |
| ⚡ [Rapid Prototyper](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-rapid-prototyper.md) | Fast POC development, MVPs | Quick proof-of-concepts, hackathon projects, fast iteration |
| 💎 [Senior Developer](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-senior-developer.md) | Laravel/Livewire, advanced patterns | Complex implementations, architecture decisions |
| 🔧 [Filament Optimization Specialist](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-filament-optimization-specialist.md) | Filament PHP admin UX, structural form redesign, resource optimization | Restructuring Filament resources/forms/tables for faster, cleaner admin workflows |
| ⚡ [Autonomous Optimization Architect](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-autonomous-optimization-architect.md) | LLM routing, cost optimization, shadow testing | Autonomous systems needing intelligent API selection and cost guardrails |
| 🔩 [Embedded Firmware Engineer](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-embedded-firmware-engineer.md) | Bare-metal, RTOS, ESP32/STM32/Nordic firmware | Production-grade embedded systems and IoT devices |
| 🚨 [Incident Response Commander](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-incident-response-commander.md) | Incident management, post-mortems, on-call | Managing production incidents and building incident readiness |
| ⛓️ [Solidity Smart Contract Engineer](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-solidity-smart-contract-engineer.md) | EVM contracts, gas optimization, DeFi | Secure, gas-optimized smart contracts and DeFi protocols |
| 🧭 [Codebase Onboarding Engineer](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-codebase-onboarding-engineer.md) | Fast developer onboarding, read-only codebase exploration, factual explanation | Helping new developers understand unfamiliar repos quickly by reading the code, tracing code paths, and stating facts about structure and behavior |
| 📚 [Technical Writer](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-technical-writer.md) | Developer docs, API reference, tutorials | Clear, accurate technical documentation |
| 💬 [WeChat Mini Program Developer](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-wechat-mini-program-developer.md) | WeChat ecosystem, Mini Programs, payment integration | Building performant apps for the WeChat ecosystem |
| 👁️ [Code Reviewer](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-code-reviewer.md) | Constructive code review, security, maintainability | PR reviews, code quality gates, mentoring through review |
| 🗄️ [Database Optimizer](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-database-optimizer.md) | Schema design, query optimization, indexing strategies | PostgreSQL/MySQL tuning, slow query debugging, migration planning |
| 🌿 [Git Workflow Master](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-git-workflow-master.md) | Branching strategies, conventional commits, advanced Git | Git workflow design, history cleanup, CI-friendly branch management |
| 🏛️ [Software Architect](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-software-architect.md) | System design, DDD, architectural patterns, trade-off analysis | Architecture decisions, domain modeling, system evolution strategy |
| 🛡️ [SRE](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-sre.md) | SLOs, error budgets, observability, chaos engineering | Production reliability, toil reduction, capacity planning |
| 🧬 [AI Data Remediation Engineer](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-ai-data-remediation-engineer.md) | Self-healing pipelines, air-gapped SLMs, semantic clustering | Fixing broken data at scale with zero data loss |
| 🔧 [Data Engineer](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-data-engineer.md) | Data pipelines, lakehouse architecture, ETL/ELT | Building reliable data infrastructure and warehousing |
| 🔗 [Feishu Integration Developer](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-feishu-integration-developer.md) | Feishu/Lark Open Platform, bots, workflows | Building integrations for the Feishu ecosystem |
| 🧱 [CMS Developer](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-cms-developer.md) | WordPress & Drupal themes, plugins/modules, content architecture | Code-first CMS implementation and customization |
| 📧 [Email Intelligence Engineer](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-email-intelligence-engineer.md) | Email parsing, MIME extraction, structured data for AI agents | Turning raw email threads into reasoning-ready context |
| 🎙️ [Voice AI Integration Engineer](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-voice-ai-integration-engineer.md) | Speech-to-text pipelines, Whisper, ASR, speaker diarization | End-to-end transcription pipelines, audio preprocessing, structured transcript delivery |
| 🖧 [IT Service Manager](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-it-service-manager.md) | ITIL 4 service management | Incident/problem/change management, SLAs, CMDB |
| 🪡 [Minimal Change Engineer](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-minimal-change-engineer.md) | Minimum-viable diffs | Fixing only what's asked, no scope creep |
| 📜 [OrgScript Engineer](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-orgscript-engineer.md) | OrgScript grammar & AST validation | Designing/parsing OrgScript business-logic definitions |
| 🧬 [Prompt Engineer](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-prompt-engineer.md) | LLM prompt design & optimization | Turning vague instructions into reliable AI behaviors |
| 🕸️ [Multi-Agent Systems Architect](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-multi-agent-systems-architect.md) | Multi-agent pipeline design & governance | Topology, context, trust, failure recovery for agent systems |
| 🛒 [Drupal Shopping Cart Engineer](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-drupal-shopping-cart.md) | Drupal Commerce storefronts | Catalog, payments, checkout, orders on Drupal 10/11 |
| 🛍️ [WordPress Shopping Cart Engineer](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-wordpress-shopping-cart.md) | WooCommerce storefronts | Catalog, payments, checkout, conversion on WordPress |

### 🎨 Design Division

[Permalink: 🎨 Design Division](https://github.com/msitarzewski/agency-agents#-design-division)

Making it beautiful, usable, and delightful.

| Agent | Specialty | When to Use |
| --- | --- | --- |
| 🎯 [UI Designer](https://github.com/msitarzewski/agency-agents/blob/main/design/design-ui-designer.md) | Visual design, component libraries, design systems | Interface creation, brand consistency, component design |
| 🔍 [UX Researcher](https://github.com/msitarzewski/agency-agents/blob/main/design/design-ux-researcher.md) | User testing, behavior analysis, research | Understanding users, usability testing, design insights |
| 🏛️ [UX Architect](https://github.com/msitarzewski/agency-agents/blob/main/design/design-ux-architect.md) | Technical architecture, CSS systems, implementation | Developer-friendly foundations, implementation guidance |
| 🎭 [Brand Guardian](https://github.com/msitarzewski/agency-agents/blob/main/design/design-brand-guardian.md) | Brand identity, consistency, positioning | Brand strategy, identity development, guidelines |
| 📖 [Visual Storyteller](https://github.com/msitarzewski/agency-agents/blob/main/design/design-visual-storyteller.md) | Visual narratives, multimedia content | Compelling visual stories, brand storytelling |
| ✨ [Whimsy Injector](https://github.com/msitarzewski/agency-agents/blob/main/design/design-whimsy-injector.md) | Personality, delight, playful interactions | Adding joy, micro-interactions, Easter eggs, brand personality |
| 📷 [Image Prompt Engineer](https://github.com/msitarzewski/agency-agents/blob/main/design/design-image-prompt-engineer.md) | AI image generation prompts, photography | Photography prompts for Midjourney, DALL-E, Stable Diffusion |
| 🌈 [Inclusive Visuals Specialist](https://github.com/msitarzewski/agency-agents/blob/main/design/design-inclusive-visuals-specialist.md) | Representation, bias mitigation, authentic imagery | Generating culturally accurate AI images and video |
| 🎭 [Persona Walkthrough Specialist](https://github.com/msitarzewski/agency-agents/blob/main/design/design-persona-walkthrough.md) | Persona-driven cognitive walkthroughs | Simulating user reactions and friction at each scroll position |

### 💰 Paid Media Division

[Permalink: 💰 Paid Media Division](https://github.com/msitarzewski/agency-agents#-paid-media-division)

Turning ad spend into measurable business outcomes.

| Agent | Specialty | When to Use |
| --- | --- | --- |
| 💰 [PPC Campaign Strategist](https://github.com/msitarzewski/agency-agents/blob/main/paid-media/paid-media-ppc-strategist.md) | Google/Microsoft/Amazon Ads, account architecture, bidding | Account buildouts, budget allocation, scaling, performance diagnosis |
| 🔍 [Search Query Analyst](https://github.com/msitarzewski/agency-agents/blob/main/paid-media/paid-media-search-query-analyst.md) | Search term analysis, negative keywords, intent mapping | Query audits, wasted spend elimination, keyword discovery |
| 📋 [Paid Media Auditor](https://github.com/msitarzewski/agency-agents/blob/main/paid-media/paid-media-auditor.md) | 200+ point account audits, competitive analysis | Account takeovers, quarterly reviews, competitive pitches |
| 📡 [Tracking & Measurement Specialist](https://github.com/msitarzewski/agency-agents/blob/main/paid-media/paid-media-tracking-specialist.md) | GTM, GA4, conversion tracking, CAPI | New implementations, tracking audits, platform migrations |
| ✍️ [Ad Creative Strategist](https://github.com/msitarzewski/agency-agents/blob/main/paid-media/paid-media-creative-strategist.md) | RSA copy, Meta creative, Performance Max assets | Creative launches, testing programs, ad fatigue refreshes |
| 📺 [Programmatic & Display Buyer](https://github.com/msitarzewski/agency-agents/blob/main/paid-media/paid-media-programmatic-buyer.md) | GDN, DSPs, partner media, ABM display | Display planning, partner outreach, ABM programs |
| 📱 [Paid Social Strategist](https://github.com/msitarzewski/agency-agents/blob/main/paid-media/paid-media-paid-social-strategist.md) | Meta, LinkedIn, TikTok, cross-platform social | Social ad programs, platform selection, audience strategy |

### 💼 Sales Division

[Permalink: 💼 Sales Division](https://github.com/msitarzewski/agency-agents#-sales-division)

Turning pipeline into revenue through craft, not CRM busywork.

| Agent | Specialty | When to Use |
| --- | --- | --- |
| 🎯 [Outbound Strategist](https://github.com/msitarzewski/agency-agents/blob/main/sales/sales-outbound-strategist.md) | Signal-based prospecting, multi-channel sequences, ICP targeting | Building pipeline through research-driven outreach, not volume |
| 🔍 [Discovery Coach](https://github.com/msitarzewski/agency-agents/blob/main/sales/sales-discovery-coach.md) | SPIN, Gap Selling, Sandler — question design and call structure | Preparing for discovery calls, qualifying opportunities, coaching reps |
| ♟️ [Deal Strategist](https://github.com/msitarzewski/agency-agents/blob/main/sales/sales-deal-strategist.md) | MEDDPICC qualification, competitive positioning, win planning | Scoring deals, exposing pipeline risk, building win strategies |
| 🛠️ [Sales Engineer](https://github.com/msitarzewski/agency-agents/blob/main/sales/sales-engineer.md) | Technical demos, POC scoping, competitive battlecards | Pre-sales technical wins, demo prep, competitive positioning |
| 🏹 [Proposal Strategist](https://github.com/msitarzewski/agency-agents/blob/main/sales/sales-proposal-strategist.md) | RFP response, win themes, narrative structure | Writing proposals that persuade, not just comply |
| 📊 [Pipeline Analyst](https://github.com/msitarzewski/agency-agents/blob/main/sales/sales-pipeline-analyst.md) | Forecasting, pipeline health, deal velocity, RevOps | Pipeline reviews, forecast accuracy, revenue operations |
| 🗺️ [Account Strategist](https://github.com/msitarzewski/agency-agents/blob/main/sales/sales-account-strategist.md) | Land-and-expand, QBRs, stakeholder mapping | Post-sale expansion, account planning, NRR growth |
| 🏋️ [Sales Coach](https://github.com/msitarzewski/agency-agents/blob/main/sales/sales-coach.md) | Rep development, call coaching, pipeline review facilitation | Making every rep and every deal better through structured coaching |
| 🎯 [Sales Outreach](https://github.com/msitarzewski/agency-agents/blob/main/specialized/sales-outreach.md) | Cold prospecting, multi-touch cadences, objection handling, proposals | Top-of-funnel B2B outreach — from cold email to booked discovery call |
| 🧲 [Offer & Lead Gen Strategist](https://github.com/msitarzewski/agency-agents/blob/main/sales/sales-offer-lead-gen-strategist.md) | Offers & lead magnets | Top-of-funnel offer construction and lead gen |

### 📢 Marketing Division

[Permalink: 📢 Marketing Division](https://github.com/msitarzewski/agency-agents#-marketing-division)

Growing your audience, one authentic interaction at a time.

| Agent | Specialty | When to Use |
| --- | --- | --- |
| 🚀 [Growth Hacker](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-growth-hacker.md) | Rapid user acquisition, viral loops, experiments | Explosive growth, user acquisition, conversion optimization |
| 📝 [Content Creator](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-content-creator.md) | Multi-platform content, editorial calendars | Content strategy, copywriting, brand storytelling |
| 🐦 [Twitter Engager](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-twitter-engager.md) | Real-time engagement, thought leadership | Twitter strategy, LinkedIn campaigns, professional social |
| 🛰️ [X/Twitter Intelligence Analyst](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-x-twitter-intelligence-analyst.md) | Social listening, trend detection, account monitoring | Brand risk, competitor, and audience intelligence on X/Twitter |
| 📱 [TikTok Strategist](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-tiktok-strategist.md) | Viral content, algorithm optimization | TikTok growth, viral content, Gen Z/Millennial audience |
| 📸 [Instagram Curator](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-instagram-curator.md) | Visual storytelling, community building | Instagram strategy, aesthetic development, visual content |
| 🤝 [Reddit Community Builder](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-reddit-community-builder.md) | Authentic engagement, value-driven content | Reddit strategy, community trust, authentic marketing |
| 📱 [App Store Optimizer](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-app-store-optimizer.md) | ASO, conversion optimization, discoverability | App marketing, store optimization, app growth |
| 🌐 [Social Media Strategist](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-social-media-strategist.md) | Cross-platform strategy, campaigns | Overall social strategy, multi-platform campaigns |
| 📕 [Xiaohongshu Specialist](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-xiaohongshu-specialist.md) | Lifestyle content, trend-driven strategy | Xiaohongshu growth, aesthetic storytelling, Gen Z audience |
| 💬 [WeChat Official Account Manager](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-wechat-official-account.md) | Subscriber engagement, content marketing | WeChat OA strategy, community building, conversion optimization |
| 🧠 [Zhihu Strategist](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-zhihu-strategist.md) | Thought leadership, knowledge-driven engagement | Zhihu authority building, Q&A strategy, lead generation |
| 🇨🇳 [Baidu SEO Specialist](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-baidu-seo-specialist.md) | Baidu optimization, China SEO, ICP compliance | Ranking in Baidu and reaching China's search market |
| 🎬 [Bilibili Content Strategist](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-bilibili-content-strategist.md) | B站 algorithm, danmaku culture, UP主 growth | Building audiences on Bilibili with community-first content |
| 🎠 [Carousel Growth Engine](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-carousel-growth-engine.md) | TikTok/Instagram carousels, autonomous publishing | Generating and publishing viral carousel content |
| 💼 [LinkedIn Content Creator](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-linkedin-content-creator.md) | Personal branding, thought leadership, professional content | LinkedIn growth, professional audience building, B2B content |
| 🛒 [China E-Commerce Operator](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-china-ecommerce-operator.md) | Taobao, Tmall, Pinduoduo, live commerce | Running multi-platform e-commerce in China |
| 🎥 [Kuaishou Strategist](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-kuaishou-strategist.md) | Kuaishou, 老铁 community, grassroots growth | Building authentic audiences in lower-tier markets |
| 🔍 [SEO Specialist](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-seo-specialist.md) | Technical SEO, content strategy, link building | Driving sustainable organic search growth |
| 📘 [Book Co-Author](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-book-co-author.md) | Thought-leadership books, ghostwriting, publishing | Strategic book collaboration for founders and experts |
| 🌏 [Cross-Border E-Commerce Specialist](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-cross-border-ecommerce.md) | Amazon, Shopee, Lazada, cross-border fulfillment | Full-funnel cross-border e-commerce strategy |
| 🎵 [Douyin Strategist](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-douyin-strategist.md) | Douyin platform, short-video marketing, algorithm | Growing audiences on China's leading short-video platform |
| 🎙️ [Livestream Commerce Coach](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-livestream-commerce-coach.md) | Host training, live room optimization, conversion | Building high-performing livestream e-commerce operations |
| 🎧 [Podcast Strategist](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-podcast-strategist.md) | Podcast content strategy, platform optimization | Chinese podcast market strategy and operations |
| 🔒 [Private Domain Operator](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-private-domain-operator.md) | WeCom, private traffic, community operations | Building enterprise WeChat private domain ecosystems |
| 🎬 [Short-Video Editing Coach](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-short-video-editing-coach.md) | Post-production, editing workflows, platform specs | Hands-on short-video editing training and optimization |
| 🔥 [Weibo Strategist](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-weibo-strategist.md) | Sina Weibo, trending topics, fan engagement | Full-spectrum Weibo operations and growth |
| 🎙️ [Global Podcast Strategist](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-global-podcast-strategist.md) | Show positioning, audience growth, monetisation | Podcast launch, platform algorithms, sponsorship, community building |
| 🔮 [AI Citation Strategist](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-ai-citation-strategist.md) | AEO/GEO, AI recommendation visibility, citation auditing | Improving brand visibility across ChatGPT, Claude, Gemini, Perplexity |
| 🇨🇳 [China Market Localization Strategist](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-china-market-localization-strategist.md) | Full-stack China market localization, Douyin/Xiaohongshu/WeChat GTM | Turning trend signals into executable China go-to-market strategies |
| 🎬 [Video Optimization Specialist](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-video-optimization-specialist.md) | YouTube algorithm strategy, chaptering, thumbnail concepts | YouTube channel growth, video SEO, audience retention optimization |
| 🏗️ [AEO Foundations Architect](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-aeo-foundations.md) | AI Engine Optimization infrastructure | llms.txt, AI-aware robots.txt, agent discovery files |
| 🤖 [Agentic Search Optimizer](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-agentic-search-optimizer.md) | WebMCP & agentic task completion | Making sites usable by AI browsing agents |
| 📧 [Email Marketing Strategist](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-email-strategist.md) | Lifecycle email & deliverability | CRM campaigns, automation, segmentation |
| 📡 [Multi-Platform Publisher](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-multi-platform-publisher.md) | One-click Chinese multi-platform publishing | Routing one article to 知乎/小红书/CSDN/B站/公众号/掘金 |
| 📣 [PR & Communications Manager](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-pr-communications-manager.md) | PR, media relations & crisis comms | Press releases, thought leadership, reputation |

### 📊 Product Division

[Permalink: 📊 Product Division](https://github.com/msitarzewski/agency-agents#-product-division)

Building the right thing at the right time.

| Agent | Specialty | When to Use |
| --- | --- | --- |
| 🎯 [Sprint Prioritizer](https://github.com/msitarzewski/agency-agents/blob/main/product/product-sprint-prioritizer.md) | Agile planning, feature prioritization | Sprint planning, resource allocation, backlog management |
| 🔍 [Trend Researcher](https://github.com/msitarzewski/agency-agents/blob/main/product/product-trend-researcher.md) | Market intelligence, competitive analysis | Market research, opportunity assessment, trend identification |
| 💬 [Feedback Synthesizer](https://github.com/msitarzewski/agency-agents/blob/main/product/product-feedback-synthesizer.md) | User feedback analysis, insights extraction | Feedback analysis, user insights, product priorities |
| 🧠 [Behavioral Nudge Engine](https://github.com/msitarzewski/agency-agents/blob/main/product/product-behavioral-nudge-engine.md) | Behavioral psychology, nudge design, engagement | Maximizing user motivation through behavioral science |
| 🧭 [Product Manager](https://github.com/msitarzewski/agency-agents/blob/main/product/product-manager.md) | Full lifecycle product ownership | Discovery, PRDs, roadmap planning, GTM, outcome measurement |

### 🎬 Project Management Division

[Permalink: 🎬 Project Management Division](https://github.com/msitarzewski/agency-agents#-project-management-division)

Keeping the trains running on time (and under budget).

| Agent | Specialty | When to Use |
| --- | --- | --- |
| 🎬 [Studio Producer](https://github.com/msitarzewski/agency-agents/blob/main/project-management/project-management-studio-producer.md) | High-level orchestration, portfolio management | Multi-project oversight, strategic alignment, resource allocation |
| 🐑 [Project Shepherd](https://github.com/msitarzewski/agency-agents/blob/main/project-management/project-management-project-shepherd.md) | Cross-functional coordination, timeline management | End-to-end project coordination, stakeholder management |
| ⚙️ [Studio Operations](https://github.com/msitarzewski/agency-agents/blob/main/project-management/project-management-studio-operations.md) | Day-to-day efficiency, process optimization | Operational excellence, team support, productivity |
| 🧪 [Experiment Tracker](https://github.com/msitarzewski/agency-agents/blob/main/project-management/project-management-experiment-tracker.md) | A/B tests, hypothesis validation | Experiment management, data-driven decisions, testing |
| 👔 [Senior Project Manager](https://github.com/msitarzewski/agency-agents/blob/main/project-management/project-manager-senior.md) | Realistic scoping, task conversion | Converting specs to tasks, scope management |
| 📋 [Jira Workflow Steward](https://github.com/msitarzewski/agency-agents/blob/main/project-management/project-management-jira-workflow-steward.md) | Git workflow, branch strategy, traceability | Enforcing Jira-linked Git discipline and delivery |
| 📋 [Meeting Notes Specialist](https://github.com/msitarzewski/agency-agents/blob/main/project-management/project-management-meeting-notes-specialist.md) | Structured meeting summaries | Extracting decisions, action items, open questions |

### 🧪 Testing Division

[Permalink: 🧪 Testing Division](https://github.com/msitarzewski/agency-agents#-testing-division)

Breaking things so users don't have to.

| Agent | Specialty | When to Use |
| --- | --- | --- |
| 📸 [Evidence Collector](https://github.com/msitarzewski/agency-agents/blob/main/testing/testing-evidence-collector.md) | Screenshot-based QA, visual proof | UI testing, visual verification, bug documentation |
| 🔍 [Reality Checker](https://github.com/msitarzewski/agency-agents/blob/main/testing/testing-reality-checker.md) | Evidence-based certification, quality gates | Production readiness, quality approval, release certification |
| 📊 [Test Results Analyzer](https://github.com/msitarzewski/agency-agents/blob/main/testing/testing-test-results-analyzer.md) | Test evaluation, metrics analysis | Test output analysis, quality insights, coverage reporting |
| ⚡ [Performance Benchmarker](https://github.com/msitarzewski/agency-agents/blob/main/testing/testing-performance-benchmarker.md) | Performance testing, optimization | Speed testing, load testing, performance tuning |
| 🔌 [API Tester](https://github.com/msitarzewski/agency-agents/blob/main/testing/testing-api-tester.md) | API validation, integration testing | API testing, endpoint verification, integration QA |
| 🛠️ [Tool Evaluator](https://github.com/msitarzewski/agency-agents/blob/main/testing/testing-tool-evaluator.md) | Technology assessment, tool selection | Evaluating tools, software recommendations, tech decisions |
| 🔄 [Workflow Optimizer](https://github.com/msitarzewski/agency-agents/blob/main/testing/testing-workflow-optimizer.md) | Process analysis, workflow improvement | Process optimization, efficiency gains, automation opportunities |
| ♿ [Accessibility Auditor](https://github.com/msitarzewski/agency-agents/blob/main/testing/testing-accessibility-auditor.md) | WCAG auditing, assistive technology testing | Accessibility compliance, screen reader testing, inclusive design verification |

### 🔒 Security Division

[Permalink: 🔒 Security Division](https://github.com/msitarzewski/agency-agents#-security-division)

Defending the stack — from secure-by-design architecture to breach response.

| Agent | Specialty | When to Use |
| --- | --- | --- |
| 🛡️ [Security Architect](https://github.com/msitarzewski/agency-agents/blob/main/security/security-architect.md) | Threat modeling, secure-by-design, trust boundaries | System security models, architecture reviews, defense-in-depth |
| 🔐 [Application Security Engineer](https://github.com/msitarzewski/agency-agents/blob/main/security/security-appsec-engineer.md) | SDLC security, SAST/DAST, secure code review | Securing the dev lifecycle, code-level vulnerabilities |
| 🗡️ [Penetration Tester](https://github.com/msitarzewski/agency-agents/blob/main/security/security-penetration-tester.md) | Authorized pentests, red team ops, exploitation | Finding exploitable weaknesses before attackers do |
| ☁️ [Cloud Security Architect](https://github.com/msitarzewski/agency-agents/blob/main/security/security-cloud-security-architect.md) | Zero trust, cloud-native defense-in-depth | Securing cloud infrastructure and architectures |
| 🚨 [Incident Responder](https://github.com/msitarzewski/agency-agents/blob/main/security/security-incident-responder.md) | DFIR, breach investigation, threat containment | Active breaches, forensics, crisis response |
| 🔍 [Threat Intelligence Analyst](https://github.com/msitarzewski/agency-agents/blob/main/security/security-threat-intelligence-analyst.md) | Adversary tracking, campaign mapping, ATT&CK | Understanding who's attacking and how |
| 🎯 [Threat Detection Engineer](https://github.com/msitarzewski/agency-agents/blob/main/security/security-threat-detection-engineer.md) | SIEM rules, threat hunting, ATT&CK mapping | Building detection layers and threat hunting |
| 🛡️ [Senior SecOps Engineer](https://github.com/msitarzewski/agency-agents/blob/main/security/security-senior-secops.md) | Secrets scanning, secure-by-default submissions | Defensive code-level security on every change |
| 📋 [Compliance Auditor](https://github.com/msitarzewski/agency-agents/blob/main/security/security-compliance-auditor.md) | SOC 2, ISO 27001, HIPAA, PCI-DSS | Guiding organizations through compliance certification |
| 🛡️ [Blockchain Security Auditor](https://github.com/msitarzewski/agency-agents/blob/main/security/security-blockchain-security-auditor.md) | Smart contract audits, exploit analysis | Finding vulnerabilities in contracts before deployment |

### 🛟 Support Division

[Permalink: 🛟 Support Division](https://github.com/msitarzewski/agency-agents#-support-division)

The backbone of the operation.

| Agent | Specialty | When to Use |
| --- | --- | --- |
| 💬 [Support Responder](https://github.com/msitarzewski/agency-agents/blob/main/support/support-support-responder.md) | Customer service, issue resolution | Customer support, user experience, support operations |
| 📊 [Analytics Reporter](https://github.com/msitarzewski/agency-agents/blob/main/support/support-analytics-reporter.md) | Data analysis, dashboards, insights | Business intelligence, KPI tracking, data visualization |
| 💰 [Finance Tracker](https://github.com/msitarzewski/agency-agents/blob/main/support/support-finance-tracker.md) | Financial planning, budget management | Financial analysis, cash flow, business performance |
| 🏗️ [Infrastructure Maintainer](https://github.com/msitarzewski/agency-agents/blob/main/support/support-infrastructure-maintainer.md) | System reliability, performance optimization | Infrastructure management, system operations, monitoring |
| ⚖️ [Legal Compliance Checker](https://github.com/msitarzewski/agency-agents/blob/main/support/support-legal-compliance-checker.md) | Compliance, regulations, legal review | Legal compliance, regulatory requirements, risk management |
| 📑 [Executive Summary Generator](https://github.com/msitarzewski/agency-agents/blob/main/support/support-executive-summary-generator.md) | C-suite communication, strategic summaries | Executive reporting, strategic communication, decision support |

### 🥽 Spatial Computing Division

[Permalink: 🥽 Spatial Computing Division](https://github.com/msitarzewski/agency-agents#-spatial-computing-division)

Building the immersive future.

| Agent | Specialty | When to Use |
| --- | --- | --- |
| 🏗️ [XR Interface Architect](https://github.com/msitarzewski/agency-agents/blob/main/spatial-computing/xr-interface-architect.md) | Spatial interaction design, immersive UX | AR/VR/XR interface design, spatial computing UX |
| 💻 [macOS Spatial/Metal Engineer](https://github.com/msitarzewski/agency-agents/blob/main/spatial-computing/macos-spatial-metal-engineer.md) | Swift, Metal, high-performance 3D | macOS spatial computing, Vision Pro native apps |
| 🌐 [XR Immersive Developer](https://github.com/msitarzewski/agency-agents/blob/main/spatial-computing/xr-immersive-developer.md) | WebXR, browser-based AR/VR | Browser-based immersive experiences, WebXR apps |
| 🎮 [XR Cockpit Interaction Specialist](https://github.com/msitarzewski/agency-agents/blob/main/spatial-computing/xr-cockpit-interaction-specialist.md) | Cockpit-based controls, immersive systems | Cockpit control systems, immersive control interfaces |
| 🍎 [visionOS Spatial Engineer](https://github.com/msitarzewski/agency-agents/blob/main/spatial-computing/visionos-spatial-engineer.md) | Apple Vision Pro development | Vision Pro apps, spatial computing experiences |
| 🔌 [Terminal Integration Specialist](https://github.com/msitarzewski/agency-agents/blob/main/spatial-computing/terminal-integration-specialist.md) | Terminal integration, command-line tools | CLI tools, terminal workflows, developer tools |

### 🎯 Specialized Division

[Permalink: 🎯 Specialized Division](https://github.com/msitarzewski/agency-agents#-specialized-division)

The unique specialists who don't fit in a box.

| Agent | Specialty | When to Use |
| --- | --- | --- |
| 🎭 [Agents Orchestrator](https://github.com/msitarzewski/agency-agents/blob/main/specialized/agents-orchestrator.md) | Multi-agent coordination, workflow management | Complex projects requiring multiple agent coordination |
| 🔍 [LSP/Index Engineer](https://github.com/msitarzewski/agency-agents/blob/main/specialized/lsp-index-engineer.md) | Language Server Protocol, code intelligence | Code intelligence systems, LSP implementation, semantic indexing |
| 📥 [Sales Data Extraction Agent](https://github.com/msitarzewski/agency-agents/blob/main/specialized/sales-data-extraction-agent.md) | Excel monitoring, sales metric extraction | Sales data ingestion, MTD/YTD/Year End metrics |
| 📈 [Data Consolidation Agent](https://github.com/msitarzewski/agency-agents/blob/main/specialized/data-consolidation-agent.md) | Sales data aggregation, dashboard reports | Territory summaries, rep performance, pipeline snapshots |
| 📬 [Report Distribution Agent](https://github.com/msitarzewski/agency-agents/blob/main/specialized/report-distribution-agent.md) | Automated report delivery | Territory-based report distribution, scheduled sends |
| 🔐 [Agentic Identity & Trust Architect](https://github.com/msitarzewski/agency-agents/blob/main/specialized/agentic-identity-trust.md) | Agent identity, authentication, trust verification | Multi-agent identity systems, agent authorization, audit trails |
| 🔗 [Identity Graph Operator](https://github.com/msitarzewski/agency-agents/blob/main/specialized/identity-graph-operator.md) | Shared identity resolution for multi-agent systems | Entity deduplication, merge proposals, cross-agent identity consistency |
| 💸 [Accounts Payable Agent](https://github.com/msitarzewski/agency-agents/blob/main/specialized/accounts-payable-agent.md) | Payment processing, vendor management, audit | Autonomous payment execution across crypto, fiat, stablecoins |
| 🌍 [Cultural Intelligence Strategist](https://github.com/msitarzewski/agency-agents/blob/main/specialized/specialized-cultural-intelligence-strategist.md) | Global UX, representation, cultural exclusion | Ensuring software resonates across cultures |
| 🗣️ [Developer Advocate](https://github.com/msitarzewski/agency-agents/blob/main/specialized/specialized-developer-advocate.md) | Community building, DX, developer content | Bridging product and developer community |
| 🔬 [Model QA Specialist](https://github.com/msitarzewski/agency-agents/blob/main/specialized/specialized-model-qa.md) | ML audits, feature analysis, interpretability | End-to-end QA for machine learning models |
| 🗃️ [ZK Steward](https://github.com/msitarzewski/agency-agents/blob/main/specialized/zk-steward.md) | Knowledge management, Zettelkasten, notes | Building connected, validated knowledge bases |
| 🔌 [MCP Builder](https://github.com/msitarzewski/agency-agents/blob/main/specialized/specialized-mcp-builder.md) | Model Context Protocol servers, AI agent tooling | Building MCP servers that extend AI agent capabilities |
| 📄 [Document Generator](https://github.com/msitarzewski/agency-agents/blob/main/specialized/specialized-document-generator.md) | PDF, PPTX, DOCX, XLSX generation from code | Professional document creation, reports, data visualization |
| ⚙️ [Automation Governance Architect](https://github.com/msitarzewski/agency-agents/blob/main/specialized/automation-governance-architect.md) | Automation governance, n8n, workflow auditing | Evaluating and governing business automations at scale |
| 📚 [Corporate Training Designer](https://github.com/msitarzewski/agency-agents/blob/main/specialized/corporate-training-designer.md) | Enterprise training, curriculum development | Designing training systems and learning programs |
| 🌱 [Personal Growth Mentor](https://github.com/msitarzewski/agency-agents/blob/main/specialized/personal-growth-mentor.md) | Goal clarity, habit systems, accountability, life strategy | Cross-domain personal development without motivational fluff |
| 🏛️ [Government Digital Presales Consultant](https://github.com/msitarzewski/agency-agents/blob/main/specialized/government-digital-presales-consultant.md) | China ToG presales, digital transformation | Government digital transformation proposals and bids |
| ⚕️ [Healthcare Marketing Compliance](https://github.com/msitarzewski/agency-agents/blob/main/specialized/healthcare-marketing-compliance.md) | China healthcare advertising compliance | Healthcare marketing regulatory compliance |
| 🎯 [Recruitment Specialist](https://github.com/msitarzewski/agency-agents/blob/main/specialized/recruitment-specialist.md) | Talent acquisition, recruiting operations | Recruitment strategy, sourcing, and hiring processes |
| 🎓 [Study Abroad Advisor](https://github.com/msitarzewski/agency-agents/blob/main/specialized/study-abroad-advisor.md) | International education, application planning | Study abroad planning across US, UK, Canada, Australia |
| 🔗 [Supply Chain Strategist](https://github.com/msitarzewski/agency-agents/blob/main/specialized/supply-chain-strategist.md) | Supply chain management, procurement strategy | Supply chain optimization and procurement planning |
| 🗺️ [Workflow Architect](https://github.com/msitarzewski/agency-agents/blob/main/specialized/specialized-workflow-architect.md) | Workflow discovery, mapping, and specification | Mapping every path through a system before code is written |
| ☁️ [Salesforce Architect](https://github.com/msitarzewski/agency-agents/blob/main/specialized/specialized-salesforce-architect.md) | Multi-cloud Salesforce design, governor limits, integrations | Enterprise Salesforce architecture, org strategy, deployment pipelines |
| 🇫🇷 [French Consulting Market Navigator](https://github.com/msitarzewski/agency-agents/blob/main/specialized/specialized-french-consulting-market.md) | ESN/SI ecosystem, portage salarial, rate positioning | Freelance consulting in the French IT market |
| 🇰🇷 [Korean Business Navigator](https://github.com/msitarzewski/agency-agents/blob/main/specialized/specialized-korean-business-navigator.md) | Korean business culture, 품의 process, relationship mechanics | Foreign professionals navigating Korean business relationships |
| 🏗️ [Civil Engineer](https://github.com/msitarzewski/agency-agents/blob/main/specialized/specialized-civil-engineer.md) | Structural analysis, geotechnical design, global building codes | Multi-standard structural engineering across Eurocode, ACI, AISC, and more |
| 🎧 [Customer Service](https://github.com/msitarzewski/agency-agents/blob/main/specialized/customer-service.md) | Omnichannel support, complaint handling, retention, escalation | Any industry customer support — retail, SaaS, hospitality, finance, logistics |
| 🏥 [Healthcare Customer Service](https://github.com/msitarzewski/agency-agents/blob/main/specialized/healthcare-customer-service.md) | HIPAA-aware patient support, billing, insurance, emergency routing | Healthcare organizations needing compliant, empathetic patient support |
| 🏨 [Hospitality Guest Services](https://github.com/msitarzewski/agency-agents/blob/main/specialized/hospitality-guest-services.md) | Reservations, concierge, complaint recovery, loyalty, events | Hotels, resorts, restaurants, and event venues |
| 🤝 [HR Onboarding](https://github.com/msitarzewski/agency-agents/blob/main/specialized/hr-onboarding.md) | Pre-boarding, compliance, benefits enrollment, 30-60-90 day plans | Any company onboarding new hires — from startups to enterprise |
| 🌐 [Language Translator](https://github.com/msitarzewski/agency-agents/blob/main/specialized/language-translator.md) | Spanish ↔ English translation, dialect awareness, cultural context | Travel, business, medical, and legal translation needs |
| ⏱️ [Legal Billing & Time Tracking](https://github.com/msitarzewski/agency-agents/blob/main/specialized/legal-billing-time-tracking.md) | Time capture, billing narratives, IOLTA compliance, collections | Law firms maximizing revenue recovery and billing accuracy |
| 📋 [Legal Client Intake](https://github.com/msitarzewski/agency-agents/blob/main/specialized/legal-client-intake.md) | Prospect qualification, conflict screening, consultation scheduling | Law firms converting inquiries into retained clients |
| ⚖️ [Legal Document Review](https://github.com/msitarzewski/agency-agents/blob/main/specialized/legal-document-review.md) | Contract review, risk flagging, version comparison, compliance | Attorney-ready first-pass review across any practice area |
| 🏦 [Loan Officer Assistant](https://github.com/msitarzewski/agency-agents/blob/main/specialized/loan-officer-assistant.md) | Borrower intake, TRID compliance, pipeline tracking, closing coordination | Mortgage and consumer lending teams |
| 🏠 [Real Estate Buyer & Seller](https://github.com/msitarzewski/agency-agents/blob/main/specialized/real-estate-buyer-seller.md) | Buyer/seller representation, offers, transaction coordination | Residential and investment real estate transactions |
| 🛒 [Retail Customer Returns](https://github.com/msitarzewski/agency-agents/blob/main/specialized/retail-customer-returns.md) | Return processing, fraud prevention, exchanges, vendor returns | Brick-and-mortar, e-commerce, and omnichannel retail |
| ♟️ [Business Strategist](https://github.com/msitarzewski/agency-agents/blob/main/specialized/business-strategist.md) | Management-consulting strategy | Competitive analysis, market entry, growth planning |
| 🔄 [Change Management Consultant](https://github.com/msitarzewski/agency-agents/blob/main/specialized/change-management-consultant.md) | ADKAR/Kotter/Prosci change | Guiding orgs through transformation & adoption |
| 🧭 [Chief of Staff](https://github.com/msitarzewski/agency-agents/blob/main/specialized/specialized-chief-of-staff.md) | Executive coordination | Filtering noise, owning processes, routing decisions |
| 🌟 [Customer Success Manager](https://github.com/msitarzewski/agency-agents/blob/main/specialized/customer-success-manager.md) | Onboarding, health & retention | QBRs, churn prevention, renewals & expansion |
| 📝 [Grant Writer](https://github.com/msitarzewski/agency-agents/blob/main/specialized/grant-writer.md) | Grant proposals & funding | LOIs, proposals, budgets for nonprofits/research |
| 🏥 [Medical Billing & Coding Specialist](https://github.com/msitarzewski/agency-agents/blob/main/specialized/medical-billing-coding-specialist.md) | ICD-10/CPT/HCPCS & revenue cycle | Claims, denial management, RCM optimization |
| 💰 [Pricing Analyst](https://github.com/msitarzewski/agency-agents/blob/main/specialized/specialized-pricing-analyst.md) | Pricing models & margin optimization | Competitor/cost analysis, value-based pricing |
| 💼 [Chief Financial Officer](https://github.com/msitarzewski/agency-agents/blob/main/specialized/chief-financial-officer.md) | Capital allocation & financial strategy | Treasury, FP&A, M&A finance, investor & board reporting |
| 🌱 [ESG & Sustainability Officer](https://github.com/msitarzewski/agency-agents/blob/main/specialized/esg-sustainability-officer.md) | ESG programs & disclosure | Sustainability strategy, decarbonization, reporting |
| 🔐 [Data Privacy Officer](https://github.com/msitarzewski/agency-agents/blob/main/specialized/data-privacy-officer.md) | GDPR/CCPA privacy compliance | Data mapping, DPIAs, consent, breach response |
| ⚙️ [Operations Manager](https://github.com/msitarzewski/agency-agents/blob/main/specialized/operations-manager.md) | Lean/Six Sigma operations | Process mapping, capacity planning, KPI governance |
| 🤝 [M&A Integration Manager](https://github.com/msitarzewski/agency-agents/blob/main/specialized/ma-integration-manager.md) | Post-merger integration | Day 1/100-day plans, synergy tracking, TSA management |
| 🧠 [Organizational Psychologist](https://github.com/msitarzewski/agency-agents/blob/main/specialized/organizational-psychologist.md) | Team dynamics & culture health | Psychological safety, burnout risk, high-performing teams |
| ⚔️ [Strategy Duel Agent](https://github.com/msitarzewski/agency-agents/blob/main/specialized/specialized-strategy-duel-agent.md) | Game theory & the 36 stratagems | Turn-based strategy duels, adversarial scenario simulation |

### 💵 Finance Division

[Permalink: 💵 Finance Division](https://github.com/msitarzewski/agency-agents#-finance-division)

Accounting, financial analysis, tax strategy, and investment research specialists.

| Agent | Specialty | When to Use |
| --- | --- | --- |
| 📒 [Bookkeeper & Controller](https://github.com/msitarzewski/agency-agents/blob/main/finance/finance-bookkeeper-controller.md) | Month-end close, reconciliation, GAAP compliance, internal controls | Day-to-day accounting operations, audit readiness, financial record-keeping |
| 📊 [Financial Analyst](https://github.com/msitarzewski/agency-agents/blob/main/finance/finance-financial-analyst.md) | Financial modeling, forecasting, scenario analysis, decision support | Three-statement models, variance analysis, data-driven business intelligence |
| 📈 [FP&A Analyst](https://github.com/msitarzewski/agency-agents/blob/main/finance/finance-fpa-analyst.md) | Budgeting, rolling forecasts, variance analysis, business reviews | Annual operating plans, monthly business reviews, strategic resource allocation |
| 🔍 [Investment Researcher](https://github.com/msitarzewski/agency-agents/blob/main/finance/finance-investment-researcher.md) | Due diligence, portfolio analysis, asset valuation, equity research | Investment thesis development, risk assessment, market research |
| 🏛️ [Tax Strategist](https://github.com/msitarzewski/agency-agents/blob/main/finance/finance-tax-strategist.md) | Tax optimization, multi-jurisdictional compliance, transfer pricing | Entity structuring, ETR analysis, audit defense, strategic tax planning |

### 🎮 Game Development Division

[Permalink: 🎮 Game Development Division](https://github.com/msitarzewski/agency-agents#-game-development-division)

Building worlds, systems, and experiences across every major engine.

#### Cross-Engine Agents (Engine-Agnostic)

[Permalink: Cross-Engine Agents (Engine-Agnostic)](https://github.com/msitarzewski/agency-agents#cross-engine-agents-engine-agnostic)

| Agent | Specialty | When to Use |
| --- | --- | --- |
| 🎯 [Game Designer](https://github.com/msitarzewski/agency-agents/blob/main/game-development/game-designer.md) | Systems design, GDD authorship, economy balancing, gameplay loops | Designing game mechanics, progression systems, writing design documents |
| 🗺️ [Level Designer](https://github.com/msitarzewski/agency-agents/blob/main/game-development/level-designer.md) | Layout theory, pacing, encounter design, environmental storytelling | Building levels, designing encounter flow, spatial narrative |
| 🎨 [Technical Artist](https://github.com/msitarzewski/agency-agents/blob/main/game-development/technical-artist.md) | Shaders, VFX, LOD pipeline, art-to-engine optimization | Bridging art and engineering, shader authoring, performance-safe asset pipelines |
| 🔊 [Game Audio Engineer](https://github.com/msitarzewski/agency-agents/blob/main/game-development/game-audio-engineer.md) | FMOD/Wwise, adaptive music, spatial audio, audio budgets | Interactive audio systems, dynamic music, audio performance |
| 📖 [Narrative Designer](https://github.com/msitarzewski/agency-agents/blob/main/game-development/narrative-designer.md) | Story systems, branching dialogue, lore architecture | Writing branching narratives, implementing dialogue systems, world lore |

#### Unity

[Permalink: Unity](https://github.com/msitarzewski/agency-agents#unity)

| Agent | Specialty | When to Use |
| --- | --- | --- |
| 🏗️ [Unity Architect](https://github.com/msitarzewski/agency-agents/blob/main/game-development/unity/unity-architect.md) | ScriptableObjects, data-driven modularity, DOTS/ECS | Large-scale Unity projects, data-driven system design, ECS performance work |
| ✨ [Unity Shader Graph Artist](https://github.com/msitarzewski/agency-agents/blob/main/game-development/unity/unity-shader-graph-artist.md) | Shader Graph, HLSL, URP/HDRP, Renderer Features | Custom Unity materials, VFX shaders, post-processing passes |
| 🌐 [Unity Multiplayer Engineer](https://github.com/msitarzewski/agency-agents/blob/main/game-development/unity/unity-multiplayer-engineer.md) | Netcode for GameObjects, Unity Relay/Lobby, server authority, prediction | Online Unity games, client prediction, Unity Gaming Services integration |
| 🛠️ [Unity Editor Tool Developer](https://github.com/msitarzewski/agency-agents/blob/main/game-development/unity/unity-editor-tool-developer.md) | EditorWindows, AssetPostprocessors, PropertyDrawers, build validation | Custom Unity Editor tooling, pipeline automation, content validation |

#### Unreal Engine

[Permalink: Unreal Engine](https://github.com/msitarzewski/agency-agents#unreal-engine)

| Agent | Specialty | When to Use |
| --- | --- | --- |
| ⚙️ [Unreal Systems Engineer](https://github.com/msitarzewski/agency-agents/blob/main/game-development/unreal-engine/unreal-systems-engineer.md) | C++/Blueprint hybrid, GAS, Nanite constraints, memory management | Complex Unreal gameplay systems, Gameplay Ability System, engine-level C++ |
| 🎨 [Unreal Technical Artist](https://github.com/msitarzewski/agency-agents/blob/main/game-development/unreal-engine/unreal-technical-artist.md) | Material Editor, Niagara, PCG, Substrate | Unreal materials, Niagara VFX, procedural content generation |
| 🌐 [Unreal Multiplayer Architect](https://github.com/msitarzewski/agency-agents/blob/main/game-development/unreal-engine/unreal-multiplayer-architect.md) | Actor replication, GameMode/GameState hierarchy, dedicated server | Unreal online games, replication graphs, server authoritative Unreal |
| 🗺️ [Unreal World Builder](https://github.com/msitarzewski/agency-agents/blob/main/game-development/unreal-engine/unreal-world-builder.md) | World Partition, Landscape, HLOD, LWC | Large open-world Unreal levels, streaming systems, terrain at scale |

#### Godot

[Permalink: Godot](https://github.com/msitarzewski/agency-agents#godot)

| Agent | Specialty | When to Use |
| --- | --- | --- |
| 📜 [Godot Gameplay Scripter](https://github.com/msitarzewski/agency-agents/blob/main/game-development/godot/godot-gameplay-scripter.md) | GDScript 2.0, signals, composition, static typing | Godot gameplay systems, scene composition, performance-conscious GDScript |
| 🌐 [Godot Multiplayer Engineer](https://github.com/msitarzewski/agency-agents/blob/main/game-development/godot/godot-multiplayer-engineer.md) | MultiplayerAPI, ENet/WebRTC, RPCs, authority model | Online Godot games, scene replication, server-authoritative Godot |
| ✨ [Godot Shader Developer](https://github.com/msitarzewski/agency-agents/blob/main/game-development/godot/godot-shader-developer.md) | Godot shading language, VisualShader, RenderingDevice | Custom Godot materials, 2D/3D effects, post-processing, compute shaders |

#### Blender

[Permalink: Blender](https://github.com/msitarzewski/agency-agents#blender)

| Agent | Specialty | When to Use |
| --- | --- | --- |
| 🧩 [Blender Addon Engineer](https://github.com/msitarzewski/agency-agents/blob/main/game-development/blender/blender-addon-engineer.md) | Blender Python (`bpy`), custom operators/panels, asset validators, exporters, pipeline automation | Building Blender add-ons, asset prep tools, export workflows, and DCC pipeline automation |

#### Roblox Studio

[Permalink: Roblox Studio](https://github.com/msitarzewski/agency-agents#roblox-studio)

| Agent | Specialty | When to Use |
| --- | --- | --- |
| ⚙️ [Roblox Systems Scripter](https://github.com/msitarzewski/agency-agents/blob/main/game-development/roblox-studio/roblox-systems-scripter.md) | Luau, RemoteEvents/Functions, DataStore, server-authoritative module architecture | Building secure Roblox game systems, client-server communication, data persistence |
| 🎯 [Roblox Experience Designer](https://github.com/msitarzewski/agency-agents/blob/main/game-development/roblox-studio/roblox-experience-designer.md) | Engagement loops, monetization, D1/D7 retention, onboarding flow | Designing Roblox game loops, Game Passes, daily rewards, player retention |
| 👗 [Roblox Avatar Creator](https://github.com/msitarzewski/agency-agents/blob/main/game-development/roblox-studio/roblox-avatar-creator.md) | UGC pipeline, accessory rigging, Creator Marketplace submission | Roblox UGC items, HumanoidDescription customization, in-experience avatar shops |

### 📚 Academic Division

[Permalink: 📚 Academic Division](https://github.com/msitarzewski/agency-agents#-academic-division)

Scholarly rigor for world-building, storytelling, and narrative design.

| Agent | Specialty | When to Use |
| --- | --- | --- |
| 🌍 [Anthropologist](https://github.com/msitarzewski/agency-agents/blob/main/academic/academic-anthropologist.md) | Cultural systems, kinship, rituals, belief systems | Designing culturally coherent societies with internal logic |
| 🌐 [Geographer](https://github.com/msitarzewski/agency-agents/blob/main/academic/academic-geographer.md) | Physical/human geography, climate, cartography | Building geographically coherent worlds with realistic terrain and settlements |
| 📚 [Historian](https://github.com/msitarzewski/agency-agents/blob/main/academic/academic-historian.md) | Historical analysis, periodization, material culture | Validating historical coherence, enriching settings with authentic period detail |
| 📜 [Narratologist](https://github.com/msitarzewski/agency-agents/blob/main/academic/academic-narratologist.md) | Narrative theory, story structure, character arcs | Analyzing and improving story structure with established theoretical frameworks |
| 🧠 [Psychologist](https://github.com/msitarzewski/agency-agents/blob/main/academic/academic-psychologist.md) | Personality theory, motivation, cognitive patterns | Building psychologically credible characters grounded in research |

* * *

### 🌍 GIS Division

[Permalink: 🌍 GIS Division](https://github.com/msitarzewski/agency-agents#-gis-division)

Mapping the Earth, analyzing the built world, and extracting intelligence from geospatial data.

| Agent | Specialty | When to Use |
| --- | --- | --- |
| 🧠 [Technical Consultant](https://github.com/msitarzewski/agency-agents/blob/main/gis/gis-technical-consultant.md) | GIS strategy, gap analysis, technology roadmaps, digital transformation | Understanding business needs, selecting the right geospatial stack, planning multi-phase GIS programs |
| 🔧 [Solution Engineer](https://github.com/msitarzewski/agency-agents/blob/main/gis/gis-solution-engineer.md) | Esri + FOSS4G prototype building, PoC delivery, technical feasibility | Building working demos, validating technical approaches, pre-sales support |
| 🖥️ [GIS Analyst](https://github.com/msitarzewski/agency-agents/blob/main/gis/gis-analyst.md) | Map production, data QC, symbology, layouts, spatial queries | Day-to-day GIS operations, creating publication-ready maps, maintaining data integrity |
| 📦 [Spatial Data Engineer](https://github.com/msitarzewski/agency-agents/blob/main/gis/gis-spatial-data-engineer.md) | Geospatial ETL, format conversion, CRS reprojection, automated pipelines | Ingesting messy data from any source, building repeatable data transformation pipelines |
| ⚙️ [Geoprocessing Specialist](https://github.com/msitarzewski/agency-agents/blob/main/gis/gis-geoprocessing-specialist.md) | ArcPy, Python Toolbox (.pyt), Model Builder, batch automation | Automating repetitive GIS workflows, building custom geoprocessing tools |
| ✅ [GIS QA Engineer](https://github.com/msitarzewski/agency-agents/blob/main/gis/gis-qa-engineer.md) | Topology validation, metadata audit, CRS consistency, accuracy assessment | Quality gates before data publication, compliance verification, data integrity audits |
| 🤖 [GeoAI/ML Engineer](https://github.com/msitarzewski/agency-agents/blob/main/gis/gis-geoai-ml-engineer.md) | Feature extraction, object detection, semantic segmentation, land cover classification | Extracting buildings/roads/vehicles from imagery, change detection, environmental monitoring |
| 🏗️ [BIM/GIS Specialist](https://github.com/msitarzewski/agency-agents/blob/main/gis/gis-bim-specialist.md) | Revit/IFC to GIS, indoor mapping, digital twin architecture, facility management | Smart campus, airport digital twins, indoor navigation, building operations |
| 🏔️ [3D & Scene Developer](https://github.com/msitarzewski/agency-agents/blob/main/gis/gis-3d-scene-developer.md) | Cesium, ArcGIS Scene Viewer, 3D Tiles, point clouds, terrain visualization | 3D city scenes, terrain flyovers, point cloud web viewers, OAuth-gated scene sharing |
| 📊 [Spatial Data Scientist](https://github.com/msitarzewski/agency-agents/blob/main/gis/gis-spatial-data-scientist.md) | Spatial statistics, clustering, regression, interpolation, point pattern analysis | Hotspot detection, spatial modeling, predictive analytics, research-grade analysis |
| 🛸 [Drone/Reality Mapping](https://github.com/msitarzewski/agency-agents/blob/main/gis/gis-drone-reality-mapping.md) | Photogrammetry, orthomosaic, DTM/DSM, point cloud classification, 3D mesh | Drone survey processing, reality capture, construction monitoring, environmental mapping |
| 🌐 [Web GIS Developer](https://github.com/msitarzewski/agency-agents/blob/main/gis/gis-web-gis-developer.md) | MapLibre GL JS, ArcGIS JS API, Leaflet, real-time dashboards, REST APIs | Building interactive web maps, operational dashboards, real-time data visualization |
| 🎨 [Cartography Designer](https://github.com/msitarzewski/agency-agents/blob/main/gis/gis-cartography-designer.md) | Color theory, typography, basemap design, visual hierarchy, print and web aesthetics | Making maps beautiful and readable, colorblind-safe palettes, professional map layouts |

* * *

## 🎯 Real-World Use Cases

[Permalink: 🎯 Real-World Use Cases](https://github.com/msitarzewski/agency-agents#-real-world-use-cases)

### Scenario 1: Building a Startup MVP

[Permalink: Scenario 1: Building a Startup MVP](https://github.com/msitarzewski/agency-agents#scenario-1-building-a-startup-mvp)

**Your Team**:

1. 🎨 **Frontend Developer** \- Build the React app
2. 🏗️ **Backend Architect** \- Design the API and database
3. 🚀 **Growth Hacker** \- Plan user acquisition
4. ⚡ **Rapid Prototyper** \- Fast iteration cycles
5. 🔍 **Reality Checker** \- Ensure quality before launch

**Result**: Ship faster with specialized expertise at every stage.

* * *

### Scenario 2: Marketing Campaign Launch

[Permalink: Scenario 2: Marketing Campaign Launch](https://github.com/msitarzewski/agency-agents#scenario-2-marketing-campaign-launch)

**Your Team**:

1. 📝 **Content Creator** \- Develop campaign content
2. 🐦 **Twitter Engager** \- Twitter strategy and execution
3. 📸 **Instagram Curator** \- Visual content and stories
4. 🤝 **Reddit Community Builder** \- Authentic community engagement
5. 📊 **Analytics Reporter** \- Track and optimize performance

**Result**: Multi-channel coordinated campaign with platform-specific expertise.

* * *

### Scenario 3: Enterprise Feature Development

[Permalink: Scenario 3: Enterprise Feature Development](https://github.com/msitarzewski/agency-agents#scenario-3-enterprise-feature-development)

**Your Team**:

1. 👔 **Senior Project Manager** \- Scope and task planning
2. 💎 **Senior Developer** \- Complex implementation
3. 🎨 **UI Designer** \- Design system and components
4. 🧪 **Experiment Tracker** \- A/B test planning
5. 📸 **Evidence Collector** \- Quality verification
6. 🔍 **Reality Checker** \- Production readiness

**Result**: Enterprise-grade delivery with quality gates and documentation.

* * *

### Scenario 4: Paid Media Account Takeover

[Permalink: Scenario 4: Paid Media Account Takeover](https://github.com/msitarzewski/agency-agents#scenario-4-paid-media-account-takeover)

**Your Team**:

1. 📋 **Paid Media Auditor** \- Comprehensive account assessment
2. 📡 **Tracking & Measurement Specialist** \- Verify conversion tracking accuracy
3. 💰 **PPC Campaign Strategist** \- Redesign account architecture
4. 🔍 **Search Query Analyst** \- Clean up wasted spend from search terms
5. ✍️ **Ad Creative Strategist** \- Refresh all ad copy and extensions
6. 📊 **Analytics Reporter** (Support Division) - Build reporting dashboards

**Result**: Systematic account takeover with tracking verified, waste eliminated, structure optimized, and creative refreshed — all within the first 30 days.

* * *

### Scenario 5: Full Agency Product Discovery

[Permalink: Scenario 5: Full Agency Product Discovery](https://github.com/msitarzewski/agency-agents#scenario-5-full-agency-product-discovery)

**Your Team**: All 8 divisions working in parallel on a single mission.

See the **[Nexus Spatial Discovery Exercise](https://github.com/msitarzewski/agency-agents/blob/main/examples/nexus-spatial-discovery.md)** \-\- a complete example where 8 agents (Product Trend Researcher, Backend Architect, Brand Guardian, Growth Hacker, Support Responder, UX Researcher, Project Shepherd, and XR Interface Architect) were deployed simultaneously to evaluate a software opportunity and produce a unified product plan covering market validation, technical architecture, brand strategy, go-to-market, support systems, UX research, project execution, and spatial UI design.

**Result**: Comprehensive, cross-functional product blueprint produced in a single session. [More examples](https://github.com/msitarzewski/agency-agents/blob/main/examples).

* * *

### Scenario 6: Smart Campus Digital Twin

[Permalink: Scenario 6: Smart Campus Digital Twin](https://github.com/msitarzewski/agency-agents#scenario-6-smart-campus-digital-twin)

**Your Team**:

1. 🧠 **Technical Consultant** \- Define the digital twin strategy: BIM for buildings, GIS for campus, IoT for real-time
2. 🏗️ **BIM/GIS Specialist** \- Convert Revit building models to GIS scene layers, design indoor floor plans
3. 🛸 **Drone/Reality Mapping** \- Fly the campus, generate orthomosaic and 3D mesh for context
4. 🌐 **Web GIS Developer** \- Build the campus dashboard with MapLibre, building layer, and room finder
5. 🏔️ **3D & Scene Developer** \- Create immersive 3D scene with terrain, buildings, and flyover tour
6. 🤖 **GeoAI/ML Engineer** \- Extract building footprints and tree canopy from drone imagery
7. ✅ **GIS QA Engineer** \- Validate data accuracy, check topology, verify CRS consistency

**Result**: A campus digital twin that combines BIM detail, drone reality capture, 3D visualization, and web accessibility — delivered by coordinated specialists in a single pipeline.

* * *

## 🤝 Contributing

[Permalink: 🤝 Contributing](https://github.com/msitarzewski/agency-agents#-contributing)

We welcome contributions! Here's how you can help:

### Add a New Agent

[Permalink: Add a New Agent](https://github.com/msitarzewski/agency-agents#add-a-new-agent)

1. Fork the repository
2. Create a new agent file in the appropriate category
3. Follow the agent template structure:
   - Frontmatter with name, description, color
   - Identity & Memory section
   - Core Mission
   - Critical Rules (domain-specific)
   - Technical Deliverables with examples
   - Workflow Process
   - Success Metrics
4. Submit a PR with your agent

### Improve Existing Agents

[Permalink: Improve Existing Agents](https://github.com/msitarzewski/agency-agents#improve-existing-agents)

- Add real-world examples
- Enhance code samples
- Update success metrics
- Improve workflows

### Share Your Success Stories

[Permalink: Share Your Success Stories](https://github.com/msitarzewski/agency-agents#share-your-success-stories)

Have you used these agents successfully? Share your story in the [Discussions](https://github.com/msitarzewski/agency-agents/discussions)!

* * *

## 📖 Agent Design Philosophy

[Permalink: 📖 Agent Design Philosophy](https://github.com/msitarzewski/agency-agents#-agent-design-philosophy)

Each agent is designed with:

1. **🎭 Strong Personality**: Not generic templates - real character and voice
2. **📋 Clear Deliverables**: Concrete outputs, not vague guidance
3. **✅ Success Metrics**: Measurable outcomes and quality standards
4. **🔄 Proven Workflows**: Step-by-step processes that work
5. **💡 Learning Memory**: Pattern recognition and continuous improvement

* * *

## 🎁 What Makes This Special?

[Permalink: 🎁 What Makes This Special?](https://github.com/msitarzewski/agency-agents#-what-makes-this-special)

### Unlike Generic AI Prompts:

[Permalink: Unlike Generic AI Prompts:](https://github.com/msitarzewski/agency-agents#unlike-generic-ai-prompts)

- ❌ Generic "Act as a developer" prompts
- ✅ Deep specialization with personality and process

### Unlike Prompt Libraries:

[Permalink: Unlike Prompt Libraries:](https://github.com/msitarzewski/agency-agents#unlike-prompt-libraries)

- ❌ One-off prompt collections
- ✅ Comprehensive agent systems with workflows and deliverables

### Unlike AI Tools:

[Permalink: Unlike AI Tools:](https://github.com/msitarzewski/agency-agents#unlike-ai-tools)

- ❌ Black box tools you can't customize
- ✅ Transparent, forkable, adaptable agent personalities

* * *

## 🎨 Agent Personality Highlights

[Permalink: 🎨 Agent Personality Highlights](https://github.com/msitarzewski/agency-agents#-agent-personality-highlights)

> "I don't just test your code - I default to finding 3-5 issues and require visual proof for everything."
>
> \-\- **Evidence Collector** (Testing Division)

> "You're not marketing on Reddit - you're becoming a valued community member who happens to represent a brand."
>
> \-\- **Reddit Community Builder** (Marketing Division)

> "Every playful element must serve a functional or emotional purpose. Design delight that enhances rather than distracts."
>
> \-\- **Whimsy Injector** (Design Division)

> "Let me add a celebration animation that reduces task completion anxiety by 40%"
>
> \-\- **Whimsy Injector** (during a UX review)

* * *

## 📊 Stats

[Permalink: 📊 Stats](https://github.com/msitarzewski/agency-agents#-stats)

- 🎭 **232 Specialized Agents** across 16 divisions
- 📝 **10,000+ lines** of personality, process, and code examples
- ⏱️ **Months of iteration** from real-world usage
- 🌟 **Battle-tested** in production environments
- 💬 **50+ requests** in first 12 hours on Reddit

* * *

## 🔌 Multi-Tool Integrations

[Permalink: 🔌 Multi-Tool Integrations](https://github.com/msitarzewski/agency-agents#-multi-tool-integrations)

The Agency works natively with Claude Code, and ships conversion + install scripts so you can use the same agents across every major agentic coding tool.

### Supported Tools

[Permalink: Supported Tools](https://github.com/msitarzewski/agency-agents#supported-tools)

- **[Claude Code](https://claude.ai/code)** — native `.md` agents, no conversion needed → `~/.claude/agents/`
- **[GitHub Copilot](https://github.com/copilot)** — native `.md` agents, no conversion needed → `~/.github/agents/` \+ `~/.copilot/agents/`
- **[Antigravity](https://github.com/google-gemini/antigravity)** — `SKILL.md` per agent → `~/.gemini/antigravity/skills/`
- **[Gemini CLI](https://github.com/google-gemini/gemini-cli)** — extension + `SKILL.md` files → `~/.gemini/extensions/agency-agents/`
- **[OpenCode](https://opencode.ai/)** — `.md` agent files → `.opencode/agents/`
- **[Cursor](https://cursor.sh/)** — `.mdc` rule files → `.cursor/rules/`
- **[Aider](https://aider.chat/)** — single `CONVENTIONS.md` → `./CONVENTIONS.md`
- **[Windsurf](https://codeium.com/windsurf)** — single `.windsurfrules` → `./.windsurfrules`
- **[OpenClaw](https://github.com/openclaw/openclaw)** — `SOUL.md` \+ `AGENTS.md` \+ `IDENTITY.md` per agent
- **[Qwen Code](https://github.com/QwenLM/qwen-code)** — `.md` SubAgent files → `~/.qwen/agents/`
- **[Kimi Code](https://github.com/MoonshotAI/kimi-cli)** — YAML agent specs → `~/.config/kimi/agents/`
- **[Codex](https://developers.openai.com/codex/overview)** — TOML custom agents → `~/.codex/agents/`

* * *

### ⚡ Quick Install

[Permalink: ⚡ Quick Install](https://github.com/msitarzewski/agency-agents#-quick-install)

**Step 1 -- Generate integration files:**

```
./scripts/convert.sh
# Faster (parallel, output order may vary): ./scripts/convert.sh --parallel
```

**Step 2 -- Install (interactive, auto-detects your tools):**

```
./scripts/install.sh
# Faster (parallel, output order may vary): ./scripts/install.sh --no-interactive --parallel
```

The installer scans your system for installed tools, shows a checkbox UI, and lets you pick exactly what to install:

```
  +------------------------------------------------+
  |   The Agency -- Tool Installer                 |
  +------------------------------------------------+

  System scan: [*] = detected on this machine

  [x]  1)  [*]  Claude Code     (claude.ai/code)
  [x]  2)  [*]  Copilot         (~/.github + ~/.copilot)
  [x]  3)  [*]  Antigravity     (~/.gemini/antigravity)
  [ ]  4)  [ ]  Gemini CLI      (~/.gemini/agents)
  [ ]  5)  [ ]  OpenCode        (opencode.ai)
  [ ]  6)  [ ]  OpenClaw        (~/.openclaw/agency-agents)
  [x]  7)  [*]  Cursor          (.cursor/rules)
  [ ]  8)  [ ]  Aider           (CONVENTIONS.md)
  [ ]  9)  [ ]  Windsurf        (.windsurfrules)
  [ ] 10)  [ ]  Qwen Code       (~/.qwen/agents)
  [ ] 11)  [ ]  Kimi Code       (~/.config/kimi/agents)
  [ ] 12)  [ ]  Codex           (~/.codex/agents)

  [1-12] toggle   [a] all   [n] none   [d] detected
  [Enter] install   [q] quit
```

**Or install a specific tool directly:**

```
./scripts/install.sh --tool cursor
./scripts/install.sh --tool opencode
./scripts/install.sh --tool openclaw
./scripts/install.sh --tool antigravity
./scripts/install.sh --tool codex
```

**Non-interactive (CI/scripts):**

```
./scripts/install.sh --no-interactive --tool all
```

**Faster runs (parallel)** — On multi-core machines, use `--parallel` so each tool is processed in parallel. Output order across tools is non-deterministic. Works with both interactive and non-interactive install: e.g. `./scripts/install.sh --interactive --parallel` (pick tools, then install in parallel) or `./scripts/install.sh --no-interactive --parallel`. Job count defaults to `nproc` (Linux), `sysctl -n hw.ncpu` (macOS), or 4; override with `--jobs N`.

```
./scripts/convert.sh --parallel                    # convert all tools in parallel
./scripts/convert.sh --parallel --jobs 8           # cap parallel jobs
./scripts/install.sh --no-interactive --parallel   # install all detected tools in parallel
./scripts/install.sh --interactive --parallel      # pick tools, then install in parallel
./scripts/install.sh --no-interactive --parallel --jobs 4
```

* * *

### Tool-Specific Instructions

[Permalink: Tool-Specific Instructions](https://github.com/msitarzewski/agency-agents#tool-specific-instructions)

**Claude Code**

Agents are copied directly from the repo into `~/.claude/agents/` \-\- no conversion needed.

```
./scripts/install.sh --tool claude-code
```

Then activate in Claude Code:

```
Use the Frontend Developer agent to review this component.
```

See [integrations/claude-code/README.md](https://github.com/msitarzewski/agency-agents/blob/main/integrations/claude-code/README.md) for details.

**GitHub Copilot**

Agents are copied directly from the repo into `~/.github/agents/` and `~/.copilot/agents/` \-\- no conversion needed.

```
./scripts/install.sh --tool copilot
```

Then activate in GitHub Copilot:

```
Use the Frontend Developer agent to review this component.
```

See [integrations/github-copilot/README.md](https://github.com/msitarzewski/agency-agents/blob/main/integrations/github-copilot/README.md) for details.

**Antigravity (Gemini)**

Each agent becomes a skill in `~/.gemini/antigravity/skills/agency-<slug>/`.

```
./scripts/install.sh --tool antigravity
```

Activate in Gemini with Antigravity:

```
@agency-frontend-developer review this React component
```

See [integrations/antigravity/README.md](https://github.com/msitarzewski/agency-agents/blob/main/integrations/antigravity/README.md) for details.

**Gemini CLI**

Installs as Gemini CLI subagents.
On a fresh clone, generate the Gemini agent files before running the installer.

```
./scripts/convert.sh --tool gemini-cli
./scripts/install.sh --tool gemini-cli
```

See [integrations/gemini-cli/README.md](https://github.com/msitarzewski/agency-agents/blob/main/integrations/gemini-cli/README.md) for details.

**OpenCode**

Agents are placed in `.opencode/agents/` in your project root (project-scoped).

```
cd /your/project
/path/to/agency-agents/scripts/install.sh --tool opencode
```

Or install globally:

```
mkdir -p ~/.config/opencode/agents
cp integrations/opencode/agents/*.md ~/.config/opencode/agents/
```

Activate in OpenCode:

```
@backend-architect design this API.
```

See [integrations/opencode/README.md](https://github.com/msitarzewski/agency-agents/blob/main/integrations/opencode/README.md) for details.

**Cursor**

Each agent becomes a `.mdc` rule file in `.cursor/rules/` of your project.

```
cd /your/project
/path/to/agency-agents/scripts/install.sh --tool cursor
```

Rules are auto-applied when Cursor detects them in the project. Reference them explicitly:

```
Use the @security-engineer rules to review this code.
```

See [integrations/cursor/README.md](https://github.com/msitarzewski/agency-agents/blob/main/integrations/cursor/README.md) for details.

**Aider**

All agents are compiled into a single `CONVENTIONS.md` file that Aider reads automatically.

```
cd /your/project
/path/to/agency-agents/scripts/install.sh --tool aider
```

Then reference agents in your Aider session:

```
Use the Frontend Developer agent to refactor this component.
```

See [integrations/aider/README.md](https://github.com/msitarzewski/agency-agents/blob/main/integrations/aider/README.md) for details.

**Windsurf**

All agents are compiled into `.windsurfrules` in your project root.

```
cd /your/project
/path/to/agency-agents/scripts/install.sh --tool windsurf
```

Reference agents in Windsurf's Cascade:

```
Use the Reality Checker agent to verify this is production ready.
```

See [integrations/windsurf/README.md](https://github.com/msitarzewski/agency-agents/blob/main/integrations/windsurf/README.md) for details.

**OpenClaw**

Each agent becomes a workspace with `SOUL.md`, `AGENTS.md`, and `IDENTITY.md` in `~/.openclaw/agency-agents/`.

```
./scripts/convert.sh --tool openclaw
./scripts/install.sh --tool openclaw
```

If the `openclaw` CLI is available, the installer registers each workspace automatically.
Run `openclaw gateway restart` after installation so the new agents are activated.

See [integrations/openclaw/README.md](https://github.com/msitarzewski/agency-agents/blob/main/integrations/openclaw/README.md) for details.

**Qwen Code**

SubAgents are installed to `.qwen/agents/` in your project root (project-scoped).

```
# Convert and install (run from your project root)
cd /your/project
./scripts/convert.sh --tool qwen
./scripts/install.sh --tool qwen
```

**Usage in Qwen Code:**

- Reference by name: `Use the frontend-developer agent to review this component`
- Or let Qwen auto-delegate based on task context
- Manage via `/agents` command in interactive mode

> 📚 [Qwen SubAgents Docs](https://qwenlm.github.io/qwen-code-docs/en/users/features/sub-agents/)

**Kimi Code**

Agents are converted to Kimi Code CLI format (YAML + system prompt) and installed to `~/.config/kimi/agents/`.

```
# Convert and install
./scripts/convert.sh --tool kimi
./scripts/install.sh --tool kimi
```

**Usage with Kimi Code:**

```
# Use an agent
kimi --agent-file ~/.config/kimi/agents/frontend-developer/agent.yaml

# In a project
kimi --agent-file ~/.config/kimi/agents/frontend-developer/agent.yaml \
     --work-dir /your/project \
     "Review this React component"
```

See [integrations/kimi/README.md](https://github.com/msitarzewski/agency-agents/blob/main/integrations/kimi/README.md) for details.

**Codex**

Each agent is converted into a Codex custom agent TOML file and installed to `~/.codex/agents/`.

```
./scripts/convert.sh --tool codex
./scripts/install.sh --tool codex
```

Then reference the custom agent by name in Codex:

```
Use the Frontend Developer agent to review this component.
```

See [integrations/codex/README.md](https://github.com/msitarzewski/agency-agents/blob/main/integrations/codex/README.md) for details.

* * *

### Regenerating After Changes

[Permalink: Regenerating After Changes](https://github.com/msitarzewski/agency-agents#regenerating-after-changes)

When you add new agents or edit existing ones, regenerate all integration files:

```
./scripts/convert.sh                    # regenerate all (serial)
./scripts/convert.sh --parallel         # regenerate all in parallel (faster)
./scripts/convert.sh --tool codex       # regenerate just one tool
./scripts/convert.sh --tool cursor      # regenerate just one tool
```

* * *

## 🗺️ Roadmap

[Permalink: 🗺️ Roadmap](https://github.com/msitarzewski/agency-agents#%EF%B8%8F-roadmap)

- [ ]  Interactive agent selector web tool
- [x]  Multi-agent workflow examples -- see [examples/](https://github.com/msitarzewski/agency-agents/blob/main/examples)
- [x]  Multi-tool integration scripts (Claude Code, GitHub Copilot, Antigravity, Gemini CLI, OpenCode, OpenClaw, Cursor, Aider, Windsurf, Qwen Code, Kimi Code, Codex)
- [ ]  Video tutorials on agent design
- [ ]  Community agent marketplace
- [ ]  Agent "personality quiz" for project matching
- [ ]  "Agent of the Week" showcase series

* * *

## 🌐 Community Translations & Localizations

[Permalink: 🌐 Community Translations & Localizations](https://github.com/msitarzewski/agency-agents#-community-translations--localizations)

Community-maintained translations and regional adaptations. These are independently maintained -- see each repo for coverage and version compatibility.

| Language | Maintainer | Link | Notes |
| --- | --- | --- | --- |
| 🇨🇳 简体中文 (zh-CN) | [@jnMetaCode](https://github.com/jnMetaCode) | [agency-agents-zh](https://github.com/jnMetaCode/agency-agents-zh) | 141 translated agents + 46 China-market originals |
| 🇨🇳 简体中文 (zh-CN) | [@dsclca12](https://github.com/dsclca12) | [agent-teams](https://github.com/dsclca12/agent-teams) | Independent translation with Bilibili, WeChat, Xiaohongshu localization |
| 🇧🇷 Português brasileiro (pt-BR) | [@jnMetaCode](https://github.com/jnMetaCode) | [agency-agents-pt-BR](https://github.com/jnMetaCode/agency-agents-pt-BR) | 184 upstream agents translated; Brazil-market PRs welcome |
| 🇷🇺 Русский (ru) | [@jnMetaCode](https://github.com/jnMetaCode) | [agency-agents-ru](https://github.com/jnMetaCode/agency-agents-ru) | 184 upstream agents translated; Russia-market PRs welcome |
| 🇮🇩 Bahasa Indonesia (id) | [@jnMetaCode](https://github.com/jnMetaCode) | [agency-agents-id](https://github.com/jnMetaCode/agency-agents-id) | 184 upstream agents translated; Indonesia-market PRs welcome |
| 🇸🇦 العربية (ar) | [@jnMetaCode](https://github.com/jnMetaCode) | [agency-agents-ar](https://github.com/jnMetaCode/agency-agents-ar) | 184 upstream agents translated; Arabic-market PRs welcome |
| 🇰🇷 한국어 (ko) | [@jnMetaCode](https://github.com/jnMetaCode) | [agency-agents-ko](https://github.com/jnMetaCode/agency-agents-ko) | 184 upstream agents fully translated; Korea-specific PRs welcome |
| 🇯🇵 日本語 (ja-JP) | [@sscodeai](https://github.com/sscodeai) | [agency-agents-ja](https://github.com/sscodeai/agency-agents-ja) | 281 Japan-localized agents + 97 Japan-market originals + 27 workflows |

Want to add a translation? Open an issue and we'll link it here.

* * *

## 🔗 Related Resources

[Permalink: 🔗 Related Resources](https://github.com/msitarzewski/agency-agents#-related-resources)

- [awesome-openclaw-agents](https://github.com/mergisi/awesome-openclaw-agents) — Community-maintained OpenClaw agent collection (derived from this repo)

* * *

## 📜 License

[Permalink: 📜 License](https://github.com/msitarzewski/agency-agents#-license)

MIT License - Use freely, commercially or personally. Attribution appreciated but not required.

* * *

## 🙏 Acknowledgments

[Permalink: 🙏 Acknowledgments](https://github.com/msitarzewski/agency-agents#-acknowledgments)

What started as a Reddit thread about AI agent specialization has grown into something remarkable — **232 agents across 16 divisions**, supported by a community of contributors from around the world. Every agent in this repo exists because someone cared enough to write it, test it, and share it.

To everyone who has opened a PR, filed an issue, started a Discussion, or simply tried an agent and told us what worked — thank you. You're the reason The Agency keeps getting better.

* * *

## 💬 Community

[Permalink: 💬 Community](https://github.com/msitarzewski/agency-agents#-community)

- **GitHub Discussions**: [Share your success stories](https://github.com/msitarzewski/agency-agents/discussions)
- **Issues**: [Report bugs or request features](https://github.com/msitarzewski/agency-agents/issues)
- **Reddit**: Join the conversation on r/ClaudeAI
- **Twitter/X**: Share with #TheAgency

* * *

## 🚀 Get Started

[Permalink: 🚀 Get Started](https://github.com/msitarzewski/agency-agents#-get-started)

1. **Browse** the agents above and find specialists for your needs
2. **Copy** the agents to `~/.claude/agents/` for Claude Code integration
3. **Activate** agents by referencing them in your Claude conversations
4. **Customize** agent personalities and workflows for your specific needs
5. **Share** your results and contribute back to the community

* * *

**🎭 The Agency: Your AI Dream Team Awaits 🎭**

[⭐ Star this repo](https://github.com/msitarzewski/agency-agents) • [🍴 Fork it](https://github.com/msitarzewski/agency-agents/fork) • [🐛 Report an issue](https://github.com/msitarzewski/agency-agents/issues) • [❤️ Sponsor](https://github.com/sponsors/msitarzewski)

Made with ❤️ by the community, for the community

## About

A complete AI agency at your fingertips - From frontend wizards to Reddit community ninjas, from whimsy injectors to reality checkers. Each agent is a specialized expert with personality, processes, and proven deliverables.


### Resources

[Readme](https://github.com/msitarzewski/agency-agents#readme-ov-file)

### License

[MIT license](https://github.com/msitarzewski/agency-agents#MIT-1-ov-file)

### Contributing

[Contributing](https://github.com/msitarzewski/agency-agents#contributing-ov-file)

### Security policy

[Security policy](https://github.com/msitarzewski/agency-agents#security-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/msitarzewski/agency-agents).

[Activity](https://github.com/msitarzewski/agency-agents/activity)

### Stars

[**115k**\\
stars](https://github.com/msitarzewski/agency-agents/stargazers)

### Watchers

[**858**\\
watching](https://github.com/msitarzewski/agency-agents/watchers)

### Forks

[**18.8k**\\
forks](https://github.com/msitarzewski/agency-agents/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fmsitarzewski%2Fagency-agents&report=msitarzewski+%28user%29)

## [Releases](https://github.com/msitarzewski/agency-agents/releases)

No releases published

## [Packages\  0](https://github.com/users/msitarzewski/packages?repo_name=agency-agents)

No packages published

## [Contributors\  87](https://github.com/msitarzewski/agency-agents/graphs/contributors)

- [![@msitarzewski](https://avatars.githubusercontent.com/u/1972242?s=64&v=4)](https://github.com/msitarzewski)
- [![@claude](https://avatars.githubusercontent.com/u/81847?s=64&v=4)](https://github.com/claude)
- [![@epowelljr](https://avatars.githubusercontent.com/u/7342666?s=64&v=4)](https://github.com/epowelljr)
- [![@4shil](https://avatars.githubusercontent.com/u/166588383?s=64&v=4)](https://github.com/4shil)
- [![@hedonnn](https://avatars.githubusercontent.com/u/6354660?s=64&v=4)](https://github.com/hedonnn)
- [![@DKFuH](https://avatars.githubusercontent.com/u/44840246?s=64&v=4)](https://github.com/DKFuH)
- [![@CagesThrottleUs](https://avatars.githubusercontent.com/u/62324457?s=64&v=4)](https://github.com/CagesThrottleUs)
- [![@DawnnnHuang](https://avatars.githubusercontent.com/u/261095274?s=64&v=4)](https://github.com/DawnnnHuang)
- [![@CelsoDeSa](https://avatars.githubusercontent.com/u/730584?s=64&v=4)](https://github.com/CelsoDeSa)
- [![@victorkzam](https://avatars.githubusercontent.com/u/11318394?s=64&v=4)](https://github.com/victorkzam)
- [![@Gujiassh](https://avatars.githubusercontent.com/u/92616678?s=64&v=4)](https://github.com/Gujiassh)
- [![@Shiven0504](https://avatars.githubusercontent.com/u/120889165?s=64&v=4)](https://github.com/Shiven0504)
- [![@aryanvr961](https://avatars.githubusercontent.com/u/256591019?s=64&v=4)](https://github.com/aryanvr961)
- [![@benjifriedman](https://avatars.githubusercontent.com/u/11360340?s=64&v=4)](https://github.com/benjifriedman)

[\+ 73 contributors](https://github.com/msitarzewski/agency-agents/graphs/contributors)

## Languages

- [Shell98.3%](https://github.com/msitarzewski/agency-agents/search?l=shell)
- [PowerShell1.7%](https://github.com/msitarzewski/agency-agents/search?l=powershell)

You can’t perform that action at this time.