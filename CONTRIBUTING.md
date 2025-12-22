# Contributing Guidelines

Thank you for your interest in contributing to the Intelligent Traffic & Parking
Monitoring System. This document defines the collaboration workflow, branching
strategy, and contribution standards used in this project.

---

## 📌 Branching Strategy

This project follows a simple and clear Git workflow suitable for team-based
development.

### Branches

- **main**
  - Stable, deliverable version of the project.
  - Direct commits are not allowed.

- **dev**
  - Integration branch for active development.
  - All feature branches are merged into `dev` via Pull Requests.

- **feature/***
  - Feature-specific branches.
  - Each task or component should be developed in its own feature branch.

### Examples

```text
feature/vehicle-detection
feature/area-based-counting
feature/docker-setup
````

---

## 🚀 Development Workflow

### 1️⃣ Start Development

1. Make sure you are on the `dev` branch and up to date:

```bash
git checkout dev
git pull
```

2. Create a new feature branch from `dev`:

```bash
git checkout -b feature/your-feature-name
```

3. (If applicable) Activate the virtual environment:

* **Windows (PowerShell):**

```powershell
venv\Scripts\Activate.ps1
```

* **Linux / macOS:**

```bash
source venv/bin/activate
```

---

### 2️⃣ Implement Changes

4. Implement your changes locally following the project structure.

5. Commit your changes with a clear and descriptive message:

```bash
git add .
git commit -m "feat: describe your change clearly"
```

6. Ensure all required dependencies are captured:

> ⚠️ Only update `requirements.txt` **if new dependencies were introduced**.

```bash
pip freeze > requirements.txt
```

---

### 3️⃣ Open a Pull Request

7. Push the feature branch to GitHub:

```bash
git push -u origin feature/your-feature-name
```

8. Ensure all CI checks (formatting and linting) pass before requesting a merge.

9. Open a Pull Request targeting the `dev` branch.

---

## 🔁 Handling Pull Request Feedback

If changes are requested during code review:

1. Stay on the **same feature branch**:

```bash
git checkout feature/your-feature-name
```

2. Apply the requested changes locally.

3. Commit the updates:

```bash
git add .
git commit -m "fix: address PR feedback"
```

4. Push the updates:

```bash
git push
```

> The existing Pull Request will be updated automatically.
> **Do not create a new branch or a new Pull Request for review fixes.**

---

## 🧹 Branch Cleanup (After Merge)

After the Pull Request is approved and merged:

1. Switch back to `dev`:

```bash
git checkout dev
```

2. Delete the local feature branch:

```bash
git branch -d feature/your-feature-name
```

3. Delete the remote feature branch:

```bash
git push origin --delete feature/your-feature-name
```

---

## ✍️ Commit Message Convention

Use the following format:

```text
<type>: <short description>
```

### Common Types

* `feat`: New features
* `fix`: Bug fixes
* `docs`: Documentation updates
* `chore`: Project setup and maintenance
* `refactor`: Code restructuring without behavior change

---

## 🧹 Code Quality Guidelines

* Follow PEP8 Python style guidelines.
* Keep functions small and focused.
* Avoid hard-coded configuration values.
* Use environment variables for runtime configuration.

---

## 📂 Project Structure

Contributors should respect the existing project structure and place code in the
appropriate modules (`vision`, `services`, `config`, `utils`).

---

## 📣 Communication & Issues

If something is unclear, requires discussion, or needs clarification:

* Open a GitHub Issue.
* Use issues to track tasks, bugs, or technical discussions.

Clear communication helps keep the project clean and maintainable.

---

Thank you for contributing!
