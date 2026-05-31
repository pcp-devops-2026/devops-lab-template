# Fork Workflow

This document explains how students fork and work with the CampusHub reference project.

## Why Fork (Not Template)?

We use **forking** rather than GitHub's template feature because:

- Forks maintain a link to the upstream repo, making it easy to pull instructor updates
- Students can submit pull requests back to the reference repo for review
- It mirrors real-world open-source contribution workflows

## Getting Started

### 1. Fork the repository

Click **Fork** at the top of the reference repo page on GitHub.

### 2. Rename your fork

Rename it to follow the naming convention:

```
campushub-<service>-<your-github-id>
```

Examples:

- `campushub-catalog-alice123`
- `campushub-grades-bob456`
- `campushub-portal-charlie789`

To rename: **Settings** > **General** > **Repository name**

### 3. Clone locally

```bash
git clone https://github.com/<your-gh-handle>/campushub-<service>-<your-gh-handle>.git
cd campushub-<service>-<your-gh-handle>
chmod +x setup.sh
./setup.sh
```

### 4. Add upstream remote

```bash
git remote add upstream https://github.com/<org>/devops-lab-reference-project.git
git fetch upstream
```

## Daily Workflow

### Working on your service

1. Create a feature branch:

   ```bash
   git checkout -b feature/add-database
   ```

2. Make changes, commit with conventional prefixes:

   ```bash
   git add .
   git commit -m "feat: add PostgreSQL connection to catalog service"
   ```

3. Push and create a PR:

   ```bash
   git push -u origin feature/add-database
   ```

### Pulling instructor updates

When the instructor updates the reference repo (e.g., new Auth endpoints):

```bash
git fetch upstream
git merge upstream/main
```

Resolve any conflicts, then push to your fork.

## Branch Naming

| Prefix | Use |
|--------|-----|
| `feature/` | New functionality |
| `fix/` | Bug fixes |
| `docs/` | Documentation changes |
| `test/` | Adding or updating tests |
| `ci/` | CI/CD pipeline changes |
| `refactor/` | Code restructuring |

## Commit Messages

Use conventional commits:

```
feat: add /courses endpoint with pagination
fix: correct GPA calculation for dropped courses
docs: add API examples to README
test: add integration tests for enrollment flow
ci: add GitHub Actions workflow for linting
```
