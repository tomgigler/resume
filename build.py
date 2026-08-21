#!/usr/bin/env python3
"""Build a static resume site from resume.json and site.json.

No third-party packages are required.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DEFAULT_RESUME = ROOT / "resume.json"
DEFAULT_SITE = ROOT / "site.json"
DEFAULT_OUTPUT = ROOT / "dist"
TEMPLATE_DIR = ROOT / "template"
STATIC_DIR = ROOT / "static"

HEX_COLOR = re.compile(r"^#[0-9a-fA-F]{6}$")
ALLOWED_SECTIONS = {"summary", "experience", "projects", "skills", "education"}


def fail(message: str) -> "NoReturn":
    raise SystemExit(f"build.py: {message}")


def load_json(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
    except FileNotFoundError:
        fail(f"missing file: {path}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"expected a JSON object in {path}")
    return value


def text(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def require(data: dict, key: str, source: str) -> str:
    value = str(data.get(key, "")).strip()
    if not value:
        fail(f"{source} must define a non-empty '{key}'")
    return value


def safe_url(value: object) -> str:
    url = str(value or "").strip()
    if not url:
        return ""
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https", "mailto"}:
        fail(f"unsupported URL scheme in {url!r}")
    return html.escape(url, quote=True)


def link(label: str, url: str) -> str:
    return f'<a href="{safe_url(url)}">{text(label)}</a>'


def render_contact(resume: dict) -> str:
    contact = resume.get("contact") or {}
    items: list[str] = []

    email = str(contact.get("email") or "").strip()
    if email:
        items.append(link(email, f"mailto:{email}"))

    location = str(contact.get("location") or "").strip()
    if location:
        items.append(f'<span>{text(location)}</span>')

    for item in contact.get("links") or []:
        label = str(item.get("label") or "").strip()
        url = str(item.get("url") or "").strip()
        if label and url:
            items.append(link(label, url))

    if not items:
        return ""

    separator = '<span class="separator" aria-hidden="true">·</span>'
    return '<section class="contact" aria-label="Contact information">\n      ' + f"\n      {separator}\n      ".join(items) + "\n    </section>"


def section_heading(site: dict, key: str) -> str:
    labels = site.get("sectionLabels") or {}
    return text(labels.get(key) or key.replace("_", " ").title())


def render_summary(resume: dict, site: dict) -> str:
    summary = str(resume.get("summary") or "").strip()
    if not summary:
        return ""
    return f"""    <section>
      <h2>{section_heading(site, 'summary')}</h2>
      <p>{text(summary)}</p>
    </section>"""


def render_experience(resume: dict, site: dict) -> str:
    roles = resume.get("experience") or []
    if not roles:
        return ""
    rendered = []
    for role in roles:
        bullets = "\n".join(f"          <li>{text(item)}</li>" for item in role.get("bullets") or [])
        bullet_list = f"\n        <ul>\n{bullets}\n        </ul>" if bullets else ""
        rendered.append(f"""      <article class="role">
        <div class="role-heading">
          <div>
            <h3>{text(role.get('company'))}</h3>
            <p class="role-title">{text(role.get('title'))}</p>
          </div>
          <p class="dates">{text(role.get('dates'))}</p>
        </div>{bullet_list}
      </article>""")
    return f"""    <section>
      <h2>{section_heading(site, 'experience')}</h2>

{chr(10).join(rendered)}
    </section>"""


def render_projects(resume: dict, site: dict) -> str:
    projects = resume.get("projects") or []
    if not projects:
        return ""
    cards = []
    for project in projects:
        name = text(project.get("name"))
        url = str(project.get("url") or "").strip()
        title = link(str(project.get("name") or ""), url) if url else name
        cards.append(f"""        <article>
          <h3>{title}</h3>
          <p>{text(project.get('description'))}</p>
        </article>""")
    return f"""    <section>
      <h2>{section_heading(site, 'projects')}</h2>
      <div class="projects">
{chr(10).join(cards)}
      </div>
    </section>"""


def render_skills(resume: dict, site: dict) -> str:
    skills = [str(item).strip() for item in resume.get("skills") or [] if str(item).strip()]
    if not skills:
        return ""
    return f"""    <section>
      <h2>{section_heading(site, 'skills')}</h2>
      <p class="skills">{' · '.join(text(item) for item in skills)}</p>
    </section>"""


def render_education(resume: dict, site: dict) -> str:
    items = resume.get("education") or []
    if not items:
        return ""
    rendered = []
    for item in items:
        detail = str(item.get("detail") or "").strip()
        detail_html = f'\n          <p class="detail">{text(detail)}</p>' if detail else ""
        rendered.append(f"""      <article class="education">
        <div>
          <h3>{text(item.get('school'))}</h3>
          <p>{text(item.get('degree'))}</p>{detail_html}
        </div>
        <p class="dates">{text(item.get('dates'))}</p>
      </article>""")
    return f"""    <section>
      <h2>{section_heading(site, 'education')}</h2>

{chr(10).join(rendered)}
    </section>"""


def render_body(resume: dict, site: dict) -> str:
    name = require(resume, "name", "resume.json")
    headline = str(resume.get("headline") or "").strip()
    eyebrow = str(resume.get("eyebrow") or "").strip()

    actions = ""
    if bool(site.get("showPrintButton", True)):
        label = text(site.get("printButtonLabel") or "Print / Save PDF")
        actions = f'''\n      <div class="actions no-print">\n        <button type="button" onclick="window.print()">{label}</button>\n      </div>'''

    header = f"""    <header class="hero">
      <div>
        {f'<p class="eyebrow">{text(eyebrow)}</p>' if eyebrow else ''}
        <h1>{text(name)}</h1>
        {f'<p class="headline">{text(headline)}</p>' if headline else ''}
      </div>{actions}
    </header>"""

    contact = render_contact(resume)
    renderers = {
        "summary": render_summary,
        "experience": render_experience,
        "projects": render_projects,
        "skills": render_skills,
        "education": render_education,
    }

    requested_sections = site.get("sections") or ["summary", "experience", "projects", "skills", "education"]
    unknown = [item for item in requested_sections if item not in ALLOWED_SECTIONS]
    if unknown:
        fail(f"site.json contains unsupported section name(s): {', '.join(unknown)}")

    sections = [renderers[key](resume, site) for key in requested_sections]
    sections = [value for value in sections if value]

    last_updated = str(site.get("lastUpdated") or "").strip()
    footer = f'''    <footer>\n      <p>Last updated {text(last_updated)}</p>\n    </footer>''' if last_updated else ""

    return "\n\n".join(value for value in [header, contact, *sections, footer] if value)


def structured_data(resume: dict, site: dict) -> str:
    contact = resume.get("contact") or {}
    same_as = [item.get("url") for item in contact.get("links") or [] if item.get("url")]
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": require(resume, "name", "resume.json"),
        "url": require(site, "url", "site.json").rstrip("/") + "/",
    }
    if resume.get("headline"):
        data["jobTitle"] = resume["headline"]
    if contact.get("email"):
        data["email"] = f"mailto:{contact['email']}"
    if same_as:
        data["sameAs"] = same_as
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def replace_tokens(template: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    remaining = sorted(set(re.findall(r"{{([A-Z0-9_]+)}}", template)))
    if remaining:
        fail(f"template contains unresolved token(s): {', '.join(remaining)}")
    return template


def validate_site(site: dict) -> tuple[str, str]:
    url = require(site, "url", "site.json").rstrip("/")
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        fail("site.json 'url' must be an absolute http(s) URL")
    accent = str(site.get("accentColor") or "#214f7b")
    if not HEX_COLOR.fullmatch(accent):
        fail("site.json 'accentColor' must be a six-digit hex color such as #214f7b")
    return url, accent


def build(resume_path: Path, site_path: Path, output: Path) -> None:
    resume = load_json(resume_path)
    site = load_json(site_path)
    url, accent = validate_site(site)

    page_title = str(site.get("pageTitle") or f"{require(resume, 'name', 'resume.json')} | Resume")
    description = str(site.get("description") or f"Resume for {require(resume, 'name', 'resume.json')}")

    index_template = (TEMPLATE_DIR / "index.html").read_text(encoding="utf-8")
    index = replace_tokens(index_template, {
        "PAGE_TITLE": text(page_title),
        "META_DESCRIPTION": text(description),
        "ACCENT_COLOR": accent,
        "CANONICAL_URL": text(url + "/"),
        "STRUCTURED_DATA": structured_data(resume, site),
        "RESUME_BODY": render_body(resume, site),
    })

    not_found_template = (TEMPLATE_DIR / "404.html").read_text(encoding="utf-8")
    not_found = replace_tokens(not_found_template, {
        "PERSON_NAME": text(require(resume, "name", "resume.json")),
        "ACCENT_COLOR": accent,
    })

    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    shutil.copytree(STATIC_DIR, output / "assets")

    (output / "index.html").write_text(index, encoding="utf-8")
    (output / "404.html").write_text(not_found, encoding="utf-8")
    (output / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {url}/sitemap.xml\n", encoding="utf-8")
    (output / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url><loc>{html.escape(url + '/')}</loc></url>\n"
        '</urlset>\n',
        encoding="utf-8",
    )

    print(f"Built {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resume", type=Path, default=DEFAULT_RESUME, help="resume JSON file")
    parser.add_argument("--site", type=Path, default=DEFAULT_SITE, help="site JSON file")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="output directory")
    args = parser.parse_args()
    build(args.resume, args.site, args.output)


if __name__ == "__main__":
    main()
