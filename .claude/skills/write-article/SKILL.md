---
name: write-article
description: Writes a technical tutorial, blog post, or doc from a brief in briefs/, in Daisy's voice, and exports paste-ready files for Medium, Substack, and dev.to. Use when Daisy asks to write, draft, or create an article, post, tutorial, or doc.
---

# Write Article

Follow these stages in order. Never skip a stage. At each checkpoint, stop and wait for Daisy's approval.

All files for an article go in `output/<article-slug>/`.

## Stage 1: Brief
1. If Daisy names a brief, read `briefs/<slug>.yaml`.
2. If she describes a new idea instead, copy `briefs/_template.yaml` to `briefs/<slug>.yaml` and fill in what she told you.
3. If she gives neither, list the briefs in `briefs/` (excluding `_template.yaml`) and ask which one to use.
4. Check the required fields: topic, format, key_takeaway. Ask for any that are missing.
5. If the key takeaway is vague, propose a sharper version and ask Daisy to confirm it.
6. If the format is a blog post and the experience field is empty, ask Daisy for the real story behind it. Never invent it.
7. Read everything listed in source_material.

## Stage 2: Research
1. Identify every fact, API, library, and version the article depends on that isn't covered by the source material.
2. Verify each one against official documentation using web search.
3. Save findings to `research.md` with a link for each source.

## Stage 3: Outline (Checkpoint 1)
1. Read every file in `voice-samples/`.
2. Write `outline.md` containing: a working title, the opening hook in one or two sentences, each H2 and H3 heading with one line describing what it covers, where code blocks go, and how the piece ends.
3. Show Daisy the outline and ask for approval.
4. Revise until she approves. Do not start drafting before approval.

## Stage 4: Draft
1. Write `draft.md` following every rule in CLAUDE.md.
2. For tutorials and any piece with code: save each code block to the `code/` folder and run it in the `writer-agent` conda environment. Use the real output for every "You should see..." line.
3. If a code block can't be run (it needs credentials, a paid service, or special hardware), add the comment `<!-- VERIFY: reason -->` above it.

## Stage 5: Review (Checkpoint 2)
1. Reread the draft against CLAUDE.md: voice, format structure, code rules, and platform-safe formatting. Fix every issue you find.
2. Search the draft for em dashes and remove any you find.
3. Tell Daisy the draft is ready and give her: the word count, the opening hook, and a list of every VERIFY item.
4. Ask her to review `draft.md`. Revise until she approves. Do not export before approval.

## Stage 6: Export
1. Create `devto.md`. Start with this front matter, then the article body:

    ---
    title: <title>
    published: false
    description: <one-sentence summary>
    tags: <tag1>, <tag2>, <tag3>, <tag4>
    ---

2. Create `preview.html`: convert the article body to HTML using the Python `markdown` package with the `fenced_code` extension, in the `writer-agent` environment. Wrap it in a simple HTML page with the title as an H1 and readable styling.
3. Create `publish-kit.md` with every item listed in the Outputs section of CLAUDE.md.
4. Tell Daisy the three files are ready, and remind her:
    - dev.to: paste the contents of `devto.md` into the dev.to editor.
    - Medium and Substack: open `preview.html` in a browser, select all, copy, and paste into the editor.