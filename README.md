# Writer Agent

A Claude Code agent that writes technical tutorials, blog posts, and documentation in my voice, then exports paste-ready files for Medium, Substack, and dev.to.

It runs inside VS Code using Claude Code. There's no API key and no orchestration code: the agent is a set of instructions, a skill, and two Python scripts.

## How it works

The agent follows a six-stage pipeline with two approval checkpoints:

1. **Brief:** reads a YAML brief describing the topic, format, audience, and key takeaway. If anything is missing, it asks.
2. **Research:** verifies facts, APIs, and versions against official documentation.
3. **Outline:** proposes a structure. *Checkpoint 1: I approve it before drafting starts.*
4. **Draft:** writes the article in my voice. For tutorials, it runs every code block and uses the real output.
5. **Review:** runs automated checks and fixes every issue. *Checkpoint 2: I approve the draft before export.*
6. **Export:** creates three paste-ready files, one for each publishing workflow.

The agent never invents personal experiences, quotes, or metrics. If a piece needs a real story and the brief doesn't include one, it asks.

## Output

Each article produces three files in `output/<article-slug>/`:

- `devto.md`: Markdown with dev.to front matter, ready to paste into the dev.to editor
- `preview.html`: the rendered article, to copy from a browser and paste into Medium and Substack
- `publish-kit.md`: title options, subtitle, tags for Medium and dev.to, a Substack subject line and preview text, an image list with alt text, and a social summary

## Project structure

```
writer-agent/
├── CLAUDE.md                          # Standing instructions: voice, formats, rules
├── .claude/skills/write-article/
│   └── SKILL.md                       # The six-stage pipeline
├── briefs/
│   └── _template.yaml                 # Copy this for each new article
├── scripts/
│   ├── check_draft.py                 # Automated rule checks
│   └── make_preview.py                # Builds preview.html from the draft
├── voice-samples/                     # Published articles the agent learns from (not committed)
└── output/                            # Drafts and exports (not committed)
```

## Automated checks

`scripts/check_draft.py` scans each draft and reports the line number of every:

- Em dash
- Hype word ("revolutionary", "game-changer")
- "Let us" where "let's" fits
- Heading other than H2 or H3 in the body
- Nested list or Markdown table
- Embedded image
- Code block without a language tag, or with curly quotes inside it

These rules keep the article consistent with the voice guidelines and make sure it pastes cleanly into all three platforms.

## Requirements

- VS Code with the [Claude Code extension](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)
- A paid Claude plan (Pro, Max, Team, or Enterprise)
- Python 3.10 or newer
- Git

## Setup

1. Clone the repo and open it in VS Code:

```bash
    git clone https://github.com/Daisy-Faith-Auma/writer-agent.git
    cd writer-agent
```

2. Install the Python packages:

```bash
    pip install markdown pyyaml
```

3. Create a `voice-samples/` folder and add three to five of your own published articles as `.md` files.

4. Edit `CLAUDE.md` to describe your voice. The current version describes mine.

5. Open the Claude Code panel in VS Code, sign in with your Claude account, then run **Developer: Reload Window** from the command palette so the skill loads.

## Usage

1. Create a brief:

```bash
    cp briefs/_template.yaml briefs/my-article.yaml
```

2. Fill in at least `topic`, `format`, and `key_takeaway`.

3. Start a new Claude Code session and run:

```
    /write-article Use briefs/my-article.yaml
```

4. Approve the outline, approve the draft, then paste the files from `output/my-article/` into each platform.

## Privacy

Voice samples, briefs, and all drafts are excluded by `.gitignore`. Only the agent itself is public. Nothing is published automatically: every article is pasted in by hand.

## Author

**Daisy Auma**, Developer Relations Engineer and Technical Writer

- GitHub: [Daisy-Faith-Auma](https://github.com/Daisy-Faith-Auma)
- LinkedIn: [daisyfaithauma](https://www.linkedin.com/in/daisyfaithauma)
- Medium: [@daisyfaithauma](https://medium.com/@daisyfaithauma)