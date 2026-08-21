# Resume

A small, dependency-free resume and professional portfolio site that keeps content separate from presentation.

The live site for this repository is intended to be **https://resume.tomgigler.com**. The project is also designed to be easy to reuse: edit two JSON files, run one Python script, and deploy the generated static files wherever you like.

## Why it is structured this way

Resume content does not belong welded into a pile of HTML. This project separates the pieces:

- `resume.json` contains the person's resume content.
- `site.json` contains site-level settings such as URL, title, section order, and accent color.
- `template/` contains the HTML shells.
- `static/` contains reusable CSS and the favicon.
- `build.py` combines those pieces into a plain static site in `dist/`.

There are no runtime dependencies, no package manager, and no application server. Production is just HTML and CSS.

## Quick start

Python 3.9+ is sufficient.

```bash
python3 build.py
python3 -m http.server 8000 -d dist
```

Then open:

```text
http://127.0.0.1:8000
```

Every build recreates `dist/` from scratch.

## Customize your resume

For normal changes, you should rarely need to edit HTML.

### 1. Edit `resume.json`

This contains:

- name, headline, and optional eyebrow text
- contact information and links
- professional summary
- experience
- selected projects
- skills
- education

Empty optional values are omitted from the generated page.

`resume.example.json` contains a generic example that can be copied when reusing the project.

### 2. Edit `site.json`

This contains:

- canonical site URL
- page title and search description
- accent color
- print-button settings
- last-updated text
- section order
- section labels

The `sections` array controls both visibility and order. For example:

```json
"sections": ["summary", "experience", "projects", "skills", "education"]
```

Remove a section from the array to hide it, or rearrange the values to change the page order.

`site.example.json` contains generic settings for reuse.

### 3. Change the look only if you want to

Most visual changes belong in `static/styles.css` and `static/print.css`.

The primary accent color can be changed without touching CSS:

```json
"accentColor": "#214f7b"
```

## Print / PDF

The generated resume includes a **Print / Save PDF** button by default. Printing uses `static/print.css`, which strips the screen-only presentation and formats the resume for US Letter paper.

This keeps the HTML resume as the source of truth instead of maintaining a separate PDF that inevitably becomes six bullet points out of date.

Set this in `site.json` to hide the button:

```json
"showPrintButton": false
```

## Generated output

`build.py` creates:

```text
dist/
├── index.html
├── 404.html
├── robots.txt
├── sitemap.xml
└── assets/
    ├── favicon.svg
    ├── print.css
    └── styles.css
```

`dist/` is intentionally ignored by Git. The repository tracks the source of the site, not generated copies of it.

## Deploy to Ubuntu / Apache

The helper scripts are intentionally simple and optional.

### Build and copy the site

```bash
./deploy/deploy.sh
```

The script reads the hostname from `site.json` and, by default, deploys to:

```text
/var/www/<hostname>
```

For this repository that becomes:

```text
/var/www/resume.tomgigler.com
```

You can override the destination:

```bash
./deploy/deploy.sh /some/other/path
```

### Generate an Apache virtual host

```bash
python3 deploy/render_apache.py
```

To install it directly:

```bash
python3 deploy/render_apache.py | sudo tee /etc/apache2/sites-available/resume.conf
sudo a2ensite resume.conf
sudo apache2ctl configtest
sudo systemctl reload apache2
```

Once DNS points to the server and HTTP is working, add HTTPS using the server's normal certificate tooling.

`deploy/apache.conf.example` shows the resulting configuration with generic values.

## Continuous build check

`.github/workflows/build.yml` builds the site on every push and pull request. It does not deploy anything; it simply catches broken JSON, bad configuration, or build-script errors before they land unnoticed.

## Reusing this repository

The easiest reuse path is:

1. Create a new repository from this one, or fork/clone it.
2. Copy `resume.example.json` over `resume.json` and fill in your information.
3. Copy `site.example.json` over `site.json` and set your URL and presentation options.
4. Run `python3 build.py`.
5. Preview `dist/` locally.
6. Deploy the contents of `dist/` to any static web host.

If this repository is made public, GitHub's **Template repository** setting is a particularly clean way to let other people create their own copy without inheriting this repository's commit history.

## Repository layout

```text
.
├── .github/workflows/build.yml
├── .gitignore
├── LICENSE
├── README.md
├── build.py
├── resume.example.json
├── resume.json
├── site.example.json
├── site.json
├── deploy/
│   ├── apache.conf.example
│   ├── deploy.sh
│   └── render_apache.py
├── static/
│   ├── favicon.svg
│   ├── print.css
│   └── styles.css
└── template/
    ├── 404.html
    └── index.html
```

## License

MIT. See `LICENSE`.
