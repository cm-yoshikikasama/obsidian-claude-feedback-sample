---
allowed-tools: Bash(git:*), Read, Grep, Glob, LS
description: Generate commit message from git diff
argument-hint: none
---

# Git Commit Message Generator

## Your task

1. Check git status and diff to understand changes
2. Analyze the changes comprehensively
3. Generate an appropriate commit message based on the changes

### Step 1: Check Git Status and Changes

```bash
git status
git diff --cached
git diff
```

### Step 2: Analyze Recent Commits (for style reference)

```bash
git log --oneline -10
```

Review recent commit messages to understand the repository's commit message style and conventions.

### Step 3: Generate Commit Message

Analyze all changes and generate a commit message following these guidelines:

#### Commit Message Requirements

Generate a commit message that:

1. **Format**: Follow conventional commit format or repository style
    - Type: feat, fix, docs, style, refactor, test, chore, etc.
    - Scope (optional): component or file affected
    - Description: concise summary of changes

2. **Content Analysis**:
    - Identify the primary purpose of changes
    - Group related changes logically
    - Focus on "why" rather than "what" when possible

3. **Message Structure**:

    ```
    <type>(<scope>): <subject>

    <body (optional)>

    <footer (optional)>
    ```

4. **Examples**:
    - `feat(auth): add OAuth2 login support`
    - `fix(api): resolve timeout issue in data fetching`
    - `docs: update README with installation instructions`
    - `refactor(utils): simplify date formatting logic`

5. **Best Practices**:
    - Use imperative mood ("add" not "added")
    - Keep subject line under 50 characters
    - Capitalize first letter of subject
    - No period at end of subject line
    - Separate subject from body with blank line
    - Wrap body at 72 characters
    - Explain what and why vs. how in body

### Step 4: Output

Display the generated commit message in a code block for easy copying:

```
<generated commit message>
```

**Important: Analyze all staged and unstaged changes before generating the message.**
