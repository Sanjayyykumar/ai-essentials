# Third-party notices

Everything in this repository is MIT-licensed (see `LICENSE`) except the adapted material below, which keeps its original licence and credit.

| Skill | Adapted from | Licence |
|---|---|---|
| `skills/karpathy-guidelines` | [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) | MIT |
| `skills/engineering-system` | [Creativestarjsp/e2eskill](https://github.com/Creativestarjsp/e2eskill), [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) | MIT |
| `skills/diagnosing-bugs`, `skills/grilling` | [mattpocock/skills](https://github.com/mattpocock/skills) | MIT |
| `skills/humanize-writing` | [blader/humanizer](https://github.com/blader/humanizer), stephenturner/skill-deslop | MIT |
| `skills/production-readiness` | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (shipping-and-launch) | MIT |
| `skills/postgres-best-practices` | [supabase/agent-skills](https://github.com/supabase/agent-skills) | MIT |
| `skills/playwright-cli` | [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli) | Apache-2.0 |
| `skills/hyperframes-video` | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | Apache-2.0 |
| `skills/premium-scroll-site` | ideas from scroll-craft, rewritten | — |

The repos indexed in `libraries/registry.json` are **not** included: `scripts/setup.* --fetch-missing` clones them from upstream into `vendor/` (git-ignored). Each keeps its own licence — note the AGPL (VoiceStudio) and non-commercial (XTTS weights, MusicGen) entries before commercial use.

## Installed at setup, not redistributed

`scripts/bootstrap.py` clones these from upstream into `vendor/` and copies their skill folders into your skills directory. They are not part of this repository:
ui-ux-pro-max (MIT) · impeccable (Apache-2.0) · taste-skill (MIT) · emil-design-eng (MIT) · Remotion skills (see repo; Remotion needs a company licence for larger teams) · lemo-opuscar plugin (MIT) · karpathy-skills plugin (MIT) · Superpowers plugin/extension ([obra/superpowers](https://github.com/obra/superpowers), MIT) · OpenCodeReview CLI + skills ([alibaba/open-code-review](https://github.com/alibaba/open-code-review), Apache-2.0; `templates/github/review.yml` calls its GitHub Action).
