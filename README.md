# devops-lab-<gh-user>

Personal lab repository for the **IBM DevOps & Software Engineering Professional Certificate** cohort.

This repo grows every week alongside the Coursera coursework. By the end of the program it serves as the Capstone submission and a portfolio piece.

## How to use this template

This is a **GitHub Template Repository**. Don't fork it, instead:

1. Click **Use this template → Create a new repository** at the top of this page.
2. Name it `devops-lab-<your-gh-handle>` (e.g. `devops-lab-hayth2015`).
3. Set visibility — **public is recommended** for unlimited Actions minutes once CI starts in Week 20.
4. Click **Create repository**.

Then locally:

```bash
git clone https://github.com/<your-gh-handle>/devops-lab-<your-gh-handle>.git
cd devops-lab-<your-gh-handle>
chmod +x setup.sh
./setup.sh
```

## Toolchain check

Run `./setup.sh` to verify everything you need is installed.

## Repo structure

```
├── README.md           ← edit this to describe your project
├── LICENCE             ← MIT
├── .gitignore          ← Python + IDE + OS junk
├── .editorconfig       ← consistent indentation across editors
├── setup.sh            ← toolchain verification
├── docs/               ← project docs (CALMS reflection, ADRs, architecture)
└── .github/
└── PULL_REQUEST_TEMPLATE.md
```

## The Weekly Ritual

See the [Cohort Handbook](https://github.com/pcp-devops-2026/mentoring-hub/blob/main/README.md) for the 13-step Weekly Ritual you'll run every week from Week 7 onwards.

## Conventional commits

Use prefixes: `feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`, `ci:`.

Example: `feat: add /healthz endpoint to Flask API`
