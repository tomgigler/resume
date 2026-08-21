# resume.tomgigler.com

Starter repository for Tom Gigler's public resume site.

The site is intentionally static: plain HTML and CSS, no build system, package manager, database, application server, or JavaScript framework. That keeps deployment simple, print output predictable, and maintenance low.

## Contents

- `index.html` — resume content and metadata
- `styles.css` — screen layout
- `print.css` — print/PDF layout
- `404.html` — not-found page
- `assets/favicon.svg` — site icon
- `deploy/apache-resume.conf` — example Apache vhost
- `deploy/deploy.sh` — rsync-based deployment helper

## Before publishing

Search the repository for `[` to find intentionally unfinished placeholders. At minimum, replace:

- `[Company Name]`
- `[California State University campus]`

Then review all resume bullets for wording, dates, scope, and current accuracy.

## Preview locally

```bash
python3 -m http.server 8000
```

Open `http://127.0.0.1:8000`.

## Printing / PDF

The page includes a **Print / Save PDF** button. `print.css` removes screen-only UI and uses letter-size print settings. The HTML resume remains the source of truth, so a fresh PDF can be produced whenever needed without maintaining two resume documents.

## Ubuntu / Apache deployment

The included Apache example assumes the site is deployed to `/var/www/resume.tomgigler.com`. A typical first setup is:

```bash
sudo cp deploy/apache-resume.conf /etc/apache2/sites-available/resume.tomgigler.com.conf
sudo a2ensite resume.tomgigler.com.conf
sudo apache2ctl configtest
sudo systemctl reload apache2
./deploy/deploy.sh
```

Once DNS for `resume.tomgigler.com` points to the server and HTTP works, use the server's existing Certbot setup to add HTTPS.

## Updating production

After pulling a new revision:

```bash
./deploy/deploy.sh
```

Because the site is static, there is no application service to restart.

## Design goals

- professional and restrained presentation
- readable on desktop and mobile
- printable without maintaining a separate resume template
- no unnecessary dependencies
- easy to host on the existing Apache server
