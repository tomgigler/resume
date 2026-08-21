# JSON schema guide

The project intentionally uses ordinary JSON rather than embedding presentation markup in resume data. `build.py` performs lightweight validation and fails the build when it encounters malformed or unsupported values.

## `resume.json`

### Identity and contact

```json
{
  "name": "Alex Example",
  "eyebrow": "Software Engineering · Developer Experience · Automation",
  "headline": "Senior Software Engineer",
  "contact": {
    "email": "alex@example.com",
    "location": "City, State",
    "links": [
      { "label": "GitHub", "url": "https://github.com/example" },
      { "label": "LinkedIn", "url": "https://www.linkedin.com/in/example" }
    ]
  }
}
```

Empty optional contact values are omitted from the generated page.

### Experience bullets

Existing string bullets remain supported:

```json
"bullets": [
  "Describe a concrete outcome."
]
```

A bullet can alternatively point to supporting evidence:

```json
"bullets": [
  {
    "text": "Designed a reusable tool that separated configuration from implementation.",
    "link": {
      "label": "View source",
      "url": "https://github.com/example/project"
    }
  }
]
```

The link is rendered after the bullet text. The JSON remains presentation-free and older string-only data remains valid.

### Projects

```json
"projects": [
  {
    "name": "Example Project",
    "url": "https://github.com/example/project",
    "description": "A concise explanation of why the project matters."
  }
]
```

If `url` is present, the project name becomes the link.

### Skills

A simple flat list remains supported:

```json
"skills": ["Git", "Python", "CI/CD"]
```

For resumes that benefit from categories, use grouped skills:

```json
"skills": [
  {
    "label": "Platform & Tooling",
    "items": ["Git", "CI/CD", "Developer Tooling"]
  },
  {
    "label": "Languages & Scripting",
    "items": ["Python", "PowerShell"]
  }
]
```

Do not mix flat strings and grouped objects in one `skills` array.

### Education details

A detail can remain a plain string:

```json
"detail": "Outstanding Undergraduate Student"
```

Or it can include an optional supporting link:

```json
"detail": {
  "text": "Capstone project later used as a teaching example.",
  "link": {
    "label": "University archive",
    "url": "https://example.edu/archive/project"
  }
}
```

## `site.json`

```json
{
  "url": "https://resume.example.com",
  "pageTitle": "Alex Example | Resume",
  "description": "Resume and professional background for Alex Example.",
  "accentColor": "#214f7b",
  "faviconText": "R",
  "showPrintButton": true,
  "printButtonLabel": "Print / Save PDF",
  "lastUpdated": "",
  "sections": ["summary", "experience", "projects", "skills", "education"],
  "sectionLabels": {
    "summary": "Professional Summary",
    "experience": "Experience",
    "projects": "Selected Projects",
    "skills": "Core Technologies",
    "education": "Education"
  }
}
```

### Section visibility and order

`sections` controls both. Remove a section to hide it or rearrange the array to move it. There is no need to rename or comment out the corresponding data in `resume.json`.

Supported values are:

- `summary`
- `experience`
- `projects`
- `skills`
- `education`

### Accent color

`accentColor` must be a six-digit hex color such as `#214f7b`.

### Favicon text

`faviconText` can contain one or two characters. It is rendered into a small SVG using the site's accent color. If omitted, the builder uses the first character of the resume name.

This allows a personal branch to choose a monogram without hard-coding one person's initials into the reusable template.

### URLs

User-configurable links are limited to `http`, `https`, and `mailto` schemes. Unsupported schemes fail the build.
