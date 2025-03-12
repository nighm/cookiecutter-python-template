#!/usr/bin/env python
"""Post-project generation script."""
import os
import shutil
import subprocess
import sys
from pathlib import Path


def check_command_exists(command):
    """Check if a command exists and is executable."""
    try:
        subprocess.run(
            [command, "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def remove_paths(paths):
    """Remove paths that are not needed."""
    for path in paths:
        path = Path(path)
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)


def init_git():
    """Initialize git repository."""
    if not check_command_exists("git"):
        print("⚠️ Git is not installed. Skipping repository initialization.")
        return False

    try:
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"],
            env={**os.environ, "GIT_AUTHOR_NAME": "{{ cookiecutter.full_name }}", "GIT_AUTHOR_EMAIL": "{{ cookiecutter.email }}"},
            check=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Failed to initialize git repository: {e}")
        return False


def setup_poetry():
    """Set up poetry environment."""
    if not check_command_exists("poetry"):
        print("❌ Poetry is not installed. Please install it first.")
        print("   https://python-poetry.org/docs/#installation")
        return False

    try:
        # 配置 poetry 使用项目内的虚拟环境
        subprocess.run(
            ["poetry", "config", "virtualenvs.in-project", "true", "--local"],
            check=True,
        )
        
        # 安装依赖
        subprocess.run(["poetry", "install", "--no-interaction"], check=True)
        
        # 如果启用了 pre-commit，安装 git hooks
        if "{{ cookiecutter.use_pre_commit }}" == "y":
            if check_command_exists("pre-commit"):
                subprocess.run(["poetry", "run", "pre-commit", "install"], check=True)
            else:
                print("⚠️ pre-commit is not available. Skipping hook installation.")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to set up Poetry environment: {e}")
        return False


def setup_env():
    """Set up environment files."""
    if Path(".env.example").exists():
        shutil.copy(".env.example", ".env")
        print("📝 Created .env file from .env.example")
        return True
    return False


def main():
    """Main function."""
    print("🚀 Starting project setup...")

    success = True
    try:
        # Remove unwanted files/directories based on user choices
        paths_to_remove = []

        if "{{ cookiecutter.use_docker }}" != "y":
            paths_to_remove.extend(
                ["docker", "docker-compose.yml", "Dockerfile", ".dockerignore"]
            )

        if "{{ cookiecutter.use_make }}" != "y":
            paths_to_remove.append("Makefile")

        if "{{ cookiecutter.use_mkdocs }}" != "y":
            paths_to_remove.extend(["docs", "mkdocs.yml"])

        if "{{ cookiecutter.include_examples }}" != "y":
            paths_to_remove.append("examples")

        if "{{ cookiecutter.use_github_actions }}" != "y":
            paths_to_remove.append(".github")

        if not any(
            [
                "{{ cookiecutter.use_docker }}" == "y",
                "{{ cookiecutter.use_make }}" == "y",
            ]
        ):
            paths_to_remove.append(".env.example")

        print("🗑️  Removing unnecessary files...")
        remove_paths(paths_to_remove)

        print("📦 Setting up Poetry environment...")
        if not setup_poetry():
            success = False

        print("🔧 Setting up environment...")
        setup_env()

        print("🔧 Initializing Git repository...")
        if not init_git():
            success = False

        if success:
            print("✨ Project setup completed successfully!")
        else:
            print("⚠️ Project setup completed with some warnings.")

    except Exception as e:
        print(f"❌ Error during setup: {e}")
        return 1

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
