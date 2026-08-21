# Design decisions

This project is intentionally small, but not accidental. The goal is not merely to produce a resume page; it is to keep the parts independent enough that the site can be reused, extended, validated, and deployed without turning a static document into a miniature software platform.

## Separate content from presentation

Resume content belongs in JSON. Layout belongs in templates and CSS. Site-wide choices such as URL, labels, section order, accent color, and favicon belong in site configuration.

This makes ordinary resume editing a data change rather than an HTML-editing exercise and lets presentation evolve without rewriting the resume itself.

## Static output is the deployment contract

`build.py` produces `dist/`. Production serves `dist/` and has no knowledge of Python, JSON, or the builder.

That boundary provides several useful properties:

- no application runtime to patch or monitor;
- no database or server-side state;
- straightforward caching and hosting;
- deterministic local previews; and
- easy movement between Apache, GitHub Pages, object storage, or another static host.

## No framework unless one earns its keep

The builder uses the Python standard library and the output is plain HTML/CSS/SVG. There is deliberately no Node toolchain, client framework, CMS, or templating package.

Those tools can be valuable when the problem needs them. A mostly textual resume does not.

## Extend the schema without breaking existing data

Features such as evidence links and grouped skills accept richer object forms while preserving the simpler string forms that already worked.

For example, an experience bullet may remain a string or become an object with text plus an optional link. This keeps simple cases simple while adding capability where there is a real use case.

## Build once, promote the same artifact

The GitHub Actions workflow builds `dist/` and uploads it as an artifact. A future deployment job can consume that artifact directly rather than rebuilding the site during deployment.

The artifact that passed validation should be the artifact that reaches production.

## Immutable releases and atomic promotion

The deployment helpers publish complete releases under:

```text
releases/<release-id>/
```

and point `current` at the active release. Apache serves `current`.

A deployment therefore becomes:

1. create a complete new release;
2. verify the files exist;
3. atomically switch the symlink.

The previous release remains available for an immediate rollback.

## Generic template vs. site-specific implementation

A repository that serves as both a reusable template and a real person's resume can keep the default branch generic and place site-specific configuration on another branch.

That keeps the normal repository/template experience reusable while allowing the same codebase to power a real deployment. It is a separation-of-concerns technique, not a privacy boundary: public branches remain public.

## Intentionally omitted

The project does not currently need:

- a database;
- authentication;
- a CMS;
- server-side rendering at request time;
- JavaScript routing;
- a package manager;
- containers; or
- a deployment orchestrator.

Adding complexity is easy. Removing it after other systems depend on it is less entertaining. Extension points are added when a concrete use case justifies them.
