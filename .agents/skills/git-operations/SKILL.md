# Git Operations Skill

Automate common git workflows including staging, committing, pushing, and resolving conflicts with rebase.

## Commands

### /git-status
Display current git status and branch information.

**Usage:**
```
/git-status
```

**Returns:**
- Current branch
- Untracked files
- Staged changes
- Unstaged changes
- Commits ahead of remote

### /git-add-commit-push
Stage all changes, create a commit, and push to remote in one command.

**Usage:**
```
/git-add-commit-push "commit message"
```

**Example:**
```
/git-add-commit-push "Add new features and fix bugs"
```

**Steps:**
1. Stages all changes (`git add .`)
2. Creates commit with provided message
3. Pushes to current branch (`git push`)
4. Displays success message with commit hash

### /git-add-selective
Stage specific files instead of all changes.

**Usage:**
```
/git-add-selective <file-paths...>
```

**Example:**
```
/git-add-selective src/main.py tests/test_main.py
```

### /git-commit
Create a commit with the currently staged changes.

**Usage:**
```
/git-commit "commit message"
```

**Example:**
```
/git-commit "Fix authentication bug in login flow"
```

### /git-push
Push commits to remote repository.

**Usage:**
```
/git-push [branch-name]
```

**Example:**
```
/git-push
/git-push feature/new-feature
```

**Options:**
- Omit branch to push current branch
- Use `-f` flag to force push (use with caution)

### /git-rebase-continue
Resolve conflicts during rebase and continue the operation.

**Usage:**
```
/git-rebase-continue
```

**Steps:**
1. Detects merge conflicts
2. Shows conflicted files
3. Helps resolve conflicts
4. Stages resolved files
5. Continues rebase (`git rebase --continue`)

### /git-rebase-interactive
Start interactive rebase for cleanup or reorganization.

**Usage:**
```
/git-rebase-interactive [number-of-commits]
```

**Example:**
```
/git-rebase-interactive 3
```

**Steps:**
1. Opens interactive rebase for last N commits
2. Allows squashing, reordering, or editing commits
3. Shows rebase editor for customization

### /git-resolve-conflicts
Manually resolve merge/rebase conflicts interactively.

**Usage:**
```
/git-resolve-conflicts
```

**Process:**
1. Shows conflicted files
2. Displays conflict markers
3. Guides through resolution
4. Stages resolved files
5. Completes merge or rebase

### /git-abort-rebase
Abort current rebase operation and return to previous state.

**Usage:**
```
/git-abort-rebase
```

**Aliases:**
- `/git-abort-merge` - Same functionality for merge operations

### /git-sync-branch
Sync current branch with remote main/master and handle conflicts.

**Usage:**
```
/git-sync-branch [target-branch]
```

**Example:**
```
/git-sync-branch
/git-sync-branch main
```

**Steps:**
1. Fetches latest from remote
2. Rebases current branch on target
3. Handles conflicts if they occur
4. Pushes updated branch

## Common Workflows

### Push changes quickly
```
/git-add-commit-push "Your commit message"
```

### Make changes and push specific files
```
/git-add-selective file1.py file2.py
/git-commit "Updated specific files"
/git-push
```

### Sync with main branch
```
/git-sync-branch main
```

### Resolve conflicts from rebase
```
/git-rebase-continue
```

### Undo rebase if something goes wrong
```
/git-abort-rebase
```

## Configuration

Add to `.claude/settings.json` for automatic conflict detection:
```json
{
  "skills": {
    "git-operations": {
      "auto_detect_conflicts": true,
      "default_remote": "origin"
    }
  }
}
```

## Safety Features

- Confirmation prompts for destructive operations
- Automatic backup of branch state before rebase
- Clear conflict markers and resolution guidance
- Option to abort operations safely
- Git reflog support for undoing mistakes

## Error Handling

- **No changes to commit:** Shows status and suggests changes
- **Push conflicts:** Suggests fetch and rebase
- **Merge conflicts:** Enters conflict resolution mode
- **Authentication fails:** Prompts for git credentials

## Tips

1. Always review changes before committing: `/git-status`
2. Use selective add for organized commits: `/git-add-selective`
3. Keep commit messages descriptive and concise
4. Sync regularly: `/git-sync-branch`
5. Use rebase instead of merge for cleaner history
