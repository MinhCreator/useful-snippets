# Useful Snippets

<div style="text-align: center;">
    <a href="https://minhcreator.github.io/useful-snippets/">[Go to website]</a>
</div>

A personal collection of reusable code snippets and cheatsheets for everyday development, built as a static documentation site with [docmd](https://www.docmd.io/).

## Contents

| Category                 | File                                    |
| ------------------------ | --------------------------------------- |
| Django & DRF             | `docs/snippets/django-snippet.md`       |
| Express.js               | `docs/snippets/expressjs-snippet.md`    |
| FastAPI                  | `docs/snippets/fastapi-snippet.md`      |
| Java                     | `docs/snippets/java-snippet.md`         |
| JavaScript               | `docs/snippets/javascript-snippet.md`   |
| Next.js                  | `docs/snippets/nextjs-snippet.md`       |
| Python                   | `docs/snippets/python-snippet.md`       |
| React Cheatsheet         | `docs/snippets/reactjs-cheatsheet.md`   |
| React Snippets (VS Code) | `docs/snippets/reactjs-snippet.md`      |
| React Code Examples      | `docs/snippets/reactjs-snippet-code.md` |
| TypeScript               | `docs/snippets/typescript-snippet.md`   |

## Usage

```bash
# Install dependencies
npm install

# Start local dev server with live reload
npm run dev

# Build static site
npm run build

# Preview built site
npm run preview
```

The static site is generated into the `site/` directory.

## Deploy

The site is automatically built and deployed to GitHub Pages via GitHub Actions on every push to `main`.
