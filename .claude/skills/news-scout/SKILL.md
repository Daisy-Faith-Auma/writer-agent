---
name: news-scout
description: Gathers the latest TLDR Tech and TLDR AI issues and the top Hacker News stories, filters them against scout-profile.md, and writes a daily digest with three suggested article topics to news/<date>.md. Use when Daisy asks for today's tech news, a news digest, or topic ideas, or when run as a scheduled task.
---

# News Scout

Use today's date in YYYY-MM-DD format wherever this skill says <today>.

## Stage 1: Gather
1. Run `~/anaconda3/envs/writer-agent/bin/python scripts/fetch_news.py`. It saves raw files to `news/raw/<today>/`.
2. If a source shows FAIL, continue with the sources that worked and note the failure at the top of the digest.

## Stage 2: Filter
1. Read `scout-profile.md` and every file in `news/raw/<today>/`.
2. Find the most recent previous digest in `news/` and skip any story it already covered.
3. Skip anything listed under "Skip" in the profile.
4. Pick up to 10 stories that best match the profile. Prefer stories with technical depth Daisy could teach or build from.

## Stage 3: Write the digest
Create `news/<today>.md` with a "Tech digest" title and two sections.

Section 1, "Top stories". For each story, give:
- The title
- The source: TLDR Tech, TLDR AI, or Hacker News (with points and comment count)
- The link
- A summary of 1 to 2 sentences in your own words. Never copy the newsletter's wording.
- One line on why it fits a topic in the profile

The Hacker News file only contains headlines. For those stories, summarize from the headline alone, label the summary "(headline only)", and never guess details.

Section 2, "Topic ideas". Exactly three ideas. For each, give:
- A working title
- The format: tutorial, blog post, or doc
- The angle: what Daisy could add that the news coverage doesn't
- A one-sentence key takeaway
- The stories it's based on
- One question for Daisy about her own experience that could power the opening hook

Never invent Daisy's experiences or opinions. Do not use em dashes.

## Stage 4: Finish
1. If this is a scheduled run, stop after writing the digest.
2. If Daisy is in the session, tell her the digest is ready and list the three topic titles.
3. When Daisy picks a topic:
    - Copy `briefs/_template.yaml` to `briefs/<topic-slug>.yaml`.
    - Fill in topic, format, key_takeaway, and source_material (the story links).
    - Ask Daisy the experience question and put her answer in the experience field.
    - Tell her to start a new session and run `/write-article Use briefs/<topic-slug>.yaml`.