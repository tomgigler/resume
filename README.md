# Resume

A small, dependency-free resume and professional portfolio site that keeps content separate from presentation.

The repository is designed to work well as a GitHub template: customize JSON, run one Python script, and deploy the generated static files wherever you like. The default branch intentionally contains only example data.

## Quick start

Python 3.9+ is sufficient. The GitHub Actions workflow currently builds with Python 3.11.

### Windows / PowerShell

```powershell
py -3.11 build.py
py -3.11 -m http.server 8000 -d dist
```

### Linux / macOS

```bash
python3 build.py
python3 -m http.server 8000 -d dist
```

Then open `http://127.0.0.1:8000`.

Every build recreates `dist/` from scratch.

## What to customize

Most users should only need to edit two files:

- `resume.json` contains resume content.
- `site.json` contains presentation and site settings.

The repository also contains `resume.example.json` and `site.example.json` as clean reference copies.

See [SCHEMA.md](SCHEMA.md) for the supported JSON formats, including optional evidence links, grouped skills, section ordering, and favicon customization.

## Why it is structured this way

Resume content does not belong welded into HTML. This project separates:

- **content** — `resume.json`
- **site configuration** — `site.json`
- **presentation** — `template/` and `static/`
- **build** — `build.py`
- **deployable artifact** — `dist/`
- **deployment mechanics** — `deploy/`

Production is plain HTML, CSS, SVG, and metadata. There is no application server, database, package manager, or client-side framework required to display the resume.

See [DESIGN.md](DESIGN.md) for the design decisions and intentionally omitted complexity.

## Print / PDF

The generated resume includes a **Print / Save PDF** button by default. Printing uses `static/print.css`, which removes screen-only presentation and formats the resume for US Letter paper.

This keeps the HTML resume as the source of truth rather than maintaining a separate PDF that slowly disagrees with it.

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

`dist/` is intentionally ignored by Git. The repository tracks the source of the site, not generated copies.

## GitHub Actions

`.github/workflows/build.yml` runs on every push and pull request. It:

1. checks out the repository;
2. provisions Python 3.11;
3. builds the active configuration;
4. builds the example configuration to keep the reusable sample honest; and
5. uploads the active `dist/` directory as a workflow artifact.

The workflow does **not** deploy anything. That keeps validation useful to anyone who creates a repository from this template while leaving deployment opt-in.

The uploaded artifact is also a useful foundation for later CI/CD: a deployment job can promote the exact artifact that passed the build instead of rebuilding it somewhere else.

## Deployment model

The included deployment helpers use immutable release directories plus an atomic `current` symlink:

```text
/var/www/resume.example.com/
├── releases/
│   ├── <release-id>/
│   └── <another-release-id>/
└── current -> releases/<release-id>
```

Apache serves `current`. A deployment copies a complete new release first and only then switches the symlink. That avoids exposing a half-copied site and makes rollback a symlink change rather than a reconstruction exercise.

### Prepare the web root

Do this once, using an account that will own deployments:

```bash
sudo install -d -o <deploy-user> -g www-data -m 2755 /var/www/resume.example.com
sudo install -d -o <deploy-user> -g www-data -m 2755 /var/www/resume.example.com/releases
```

### Manual build and publish

On the deployment host:

```bash
./deploy/deploy.sh
```

By default the script derives the host from `site.json`, builds `dist/`, uses the current Git commit as the release ID, publishes it under `/var/www/<hostname>/releases/`, and atomically moves `current`.

Override the deployment root if needed:

```bash
./deploy/deploy.sh /some/other/path
```

`deploy/publish.sh` is the lower-level primitive. It publishes an already-built directory without rebuilding it:

```bash
./deploy/publish.sh <built-site-dir> <deploy-root> <release-id>
```

That distinction is intentional: future CI/CD can build once, transfer `dist/`, and publish exactly what was validated.

### Generate an Apache virtual host

```bash
python3 deploy/render_apache.py
```

The generated configuration serves `/var/www/<hostname>/current` by default. To install it:

```bash
python3 deploy/render_apache.py | sudo tee /etc/apache2/sites-available/resume.conf
sudo a2ensite resume.conf
sudo apache2ctl configtest
sudo systemctl reload apache2
```

Once DNS points to the server and HTTP works, add HTTPS using the host's normal certificate tooling.

## Keeping the template generic while deploying a real resume

A useful maintenance pattern is:

```text
main                 reusable template/example data
site-specific branch real resume.json + site.json
```

Both branches can use the same builder and validation workflow. A later deployment workflow can be restricted to the site-specific branch.

This is organizational separation, **not privacy**. In a public repository, data on another branch remains public and discoverable.

## Using this repository as a template

On GitHub, enable **Settings → General → Template repository**. New repositories created with **Use this template** get a fresh Git history rather than becoming forks.

The default branch is deliberately generic so the normal template experience does not copy someone else's resume content.

## Repository layout

```text
.
├── .github/workflows/build.yml
├── .gitignore
├── DESIGN.md
├── LICENSE
├── README.md
├── SCHEMA.md
├── build.py
├── resume.example.json
├── resume.json
├── site.example.json
├── site.json
├── deploy/
│   ├── apache.conf.example
│   ├── deploy.sh
│   ├── publish.sh
│   └── render_apache.py
├── static/
│   ├── print.css
│   └── styles.css
└── template/
    ├── 404.html
    ├── favicon.svg
    └── index.html
```

## License

MIT. See [LICENSE](LICENSE).
