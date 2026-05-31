#!/usr/bin/env python3
"""
Git Operations Skill Implementation
Provides automation for git workflows: add, commit, push, and conflict resolution via rebase.
"""

import subprocess
import sys
from typing import Optional, List, Tuple
from pathlib import Path


class GitOperations:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)

    def run_git_command(self, *args: str) -> Tuple[int, str, str]:
        """Execute a git command and return (return_code, stdout, stderr)."""
        cmd = ["git", *args]
        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            return result.returncode, result.stdout, result.stderr
        except FileNotFoundError:
            return 1, "", "Git is not installed"

    def git_status(self) -> dict:
        """Get current git status."""
        returncode, stdout, stderr = self.run_git_command("status", "--porcelain")

        if returncode != 0:
            return {"error": f"Failed to get git status: {stderr}"}

        # Get current branch
        _, branch, _ = self.run_git_command("rev-parse", "--abbrev-ref", "HEAD")

        return {
            "branch": branch.strip(),
            "status": stdout,
            "clean": len(stdout.strip()) == 0,
        }

    def git_add(self, files: Optional[List[str]] = None) -> dict:
        """Stage files for commit."""
        if files:
            args = ["add"] + files
        else:
            args = ["add", "."]

        returncode, stdout, stderr = self.run_git_command(*args)

        if returncode != 0:
            return {"success": False, "error": stderr}

        return {"success": True, "message": f"Added {len(files or ['all'])} file(s)"}

    def git_commit(self, message: str) -> dict:
        """Create a commit with the staged changes."""
        returncode, stdout, stderr = self.run_git_command("commit", "-m", message)

        if returncode != 0:
            return {"success": False, "error": stderr}

        # Extract commit hash
        commit_hash = stdout.split("[")[1].split("]")[0] if "[" in stdout else "unknown"

        return {
            "success": True,
            "commit": commit_hash,
            "message": stdout.strip(),
        }

    def git_push(self, branch: Optional[str] = None, force: bool = False) -> dict:
        """Push commits to remote."""
        args = ["push"]

        if force:
            args.append("-f")

        if branch:
            args.append(branch)

        returncode, stdout, stderr = self.run_git_command(*args)

        if returncode != 0:
            return {"success": False, "error": stderr}

        return {"success": True, "message": stdout.strip()}

    def git_add_commit_push(self, message: str, files: Optional[List[str]] = None) -> dict:
        """Combined operation: add, commit, push."""
        # Stage
        add_result = self.git_add(files)
        if not add_result.get("success"):
            return add_result

        # Commit
        commit_result = self.git_commit(message)
        if not commit_result.get("success"):
            return commit_result

        # Push
        push_result = self.git_push()
        if not push_result.get("success"):
            return push_result

        return {
            "success": True,
            "commit": commit_result.get("commit"),
            "message": f"Successfully committed and pushed: {message}",
        }

    def has_conflicts(self) -> bool:
        """Check if there are merge/rebase conflicts."""
        returncode, stdout, _ = self.run_git_command("status")
        return "both modified" in stdout or "conflict" in stdout

    def get_conflicted_files(self) -> List[str]:
        """Get list of files with conflicts."""
        _, stdout, _ = self.run_git_command("status", "--porcelain")

        conflicts = []
        for line in stdout.split("\n"):
            if line.startswith("UU ") or line.startswith("AA ") or "both modified" in line:
                conflicts.append(line.split()[-1])

        return conflicts

    def git_rebase_continue(self) -> dict:
        """Continue rebase after resolving conflicts."""
        if not self.has_conflicts():
            return {"success": False, "error": "No conflicts to resolve"}

        # Stage all resolved files
        self.git_add(["."])

        returncode, stdout, stderr = self.run_git_command("rebase", "--continue")

        if returncode != 0:
            return {
                "success": False,
                "error": stderr,
                "hint": "Fix remaining conflicts and try again",
            }

        return {"success": True, "message": "Rebase continued successfully"}

    def git_abort_rebase(self) -> dict:
        """Abort rebase operation."""
        returncode, stdout, stderr = self.run_git_command("rebase", "--abort")

        if returncode != 0:
            # Try abort merge if rebase fails
            returncode, stdout, stderr = self.run_git_command("merge", "--abort")

        if returncode != 0:
            return {"success": False, "error": f"Nothing to abort: {stderr}"}

        return {"success": True, "message": "Rebase/merge aborted successfully"}

    def git_sync_branch(self, target_branch: str = "main") -> dict:
        """Sync current branch with target branch using rebase."""
        # Fetch latest
        self.run_git_command("fetch", "origin")

        # Get current branch
        _, current_branch, _ = self.run_git_command("rev-parse", "--abbrev-ref", "HEAD")
        current_branch = current_branch.strip()

        # Rebase on target
        returncode, stdout, stderr = self.run_git_command("rebase", f"origin/{target_branch}")

        if returncode != 0:
            if self.has_conflicts():
                return {
                    "success": False,
                    "error": "Conflicts occurred during rebase",
                    "conflicts": self.get_conflicted_files(),
                    "hint": "Resolve conflicts manually and use /git-rebase-continue",
                }
            return {"success": False, "error": stderr}

        # Push
        push_result = self.git_push(current_branch)

        if not push_result.get("success"):
            return push_result

        return {
            "success": True,
            "message": f"Successfully synced {current_branch} with {target_branch}",
        }

    def git_resolve_conflicts_interactive(self) -> dict:
        """Guide through interactive conflict resolution."""
        conflicts = self.get_conflicted_files()

        if not conflicts:
            return {"success": False, "error": "No conflicts found"}

        return {
            "success": True,
            "conflicts": conflicts,
            "message": "Conflicted files found. Review and resolve them, then use /git-rebase-continue",
            "hint": "Edit each conflicted file and remove conflict markers (<<<, ===, >>>)",
        }


def main():
    """CLI interface for git operations."""
    if len(sys.argv) < 2:
        print("Usage: git-operations <command> [args...]")
        print("Commands: status, add, commit, push, add-commit-push, sync, resolve-conflicts, abort-rebase")
        sys.exit(1)

    git_ops = GitOperations()
    command = sys.argv[1]

    if command == "status":
        result = git_ops.git_status()
    elif command == "add":
        files = sys.argv[2:] if len(sys.argv) > 2 else None
        result = git_ops.git_add(files)
    elif command == "commit":
        message = sys.argv[2] if len(sys.argv) > 2 else "Update"
        result = git_ops.git_commit(message)
    elif command == "push":
        branch = sys.argv[2] if len(sys.argv) > 2 else None
        result = git_ops.git_push(branch)
    elif command == "add-commit-push":
        message = sys.argv[2] if len(sys.argv) > 2 else "Update"
        files = sys.argv[3:] if len(sys.argv) > 3 else None
        result = git_ops.git_add_commit_push(message, files)
    elif command == "sync":
        target = sys.argv[2] if len(sys.argv) > 2 else "main"
        result = git_ops.git_sync_branch(target)
    elif command == "resolve-conflicts":
        result = git_ops.git_resolve_conflicts_interactive()
    elif command == "rebase-continue":
        result = git_ops.git_rebase_continue()
    elif command == "abort-rebase":
        result = git_ops.git_abort_rebase()
    else:
        result = {"error": f"Unknown command: {command}"}

    import json
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
