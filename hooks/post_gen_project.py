#!/usr/bin/env python
"""Post-project generation script."""
import os
import shutil
import subprocess
from pathlib import Path

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
    subprocess.run(['git', 'init'], check=True)
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)

def setup_poetry():
    """Set up poetry environment."""
    subprocess.run(['poetry', 'install'], check=True)
    if '{{ cookiecutter.use_pre_commit }}' == 'y':
        subprocess.run(['poetry', 'run', 'pre-commit', 'install'], check=True)

def setup_env():
    """Set up environment files."""
    if Path('.env.example').exists():
        shutil.copy('.env.example', '.env')
        print('📝 Created .env file from .env.example')

def main():
    """Main function."""
    print('🚀 Finalizing project setup...')
    
    try:
        # Remove unwanted files/directories based on user choices
        paths_to_remove = []
        
        if '{{ cookiecutter.use_docker }}' != 'y':
            paths_to_remove.extend([
                'docker',
                'docker-compose.yml',
                'Dockerfile',
                '.dockerignore'
            ])
            
        if '{{ cookiecutter.use_make }}' != 'y':
            paths_to_remove.append('Makefile')
            
        if '{{ cookiecutter.use_mkdocs }}' != 'y':
            paths_to_remove.extend([
                'docs',
                'mkdocs.yml'
            ])
            
        if '{{ cookiecutter.include_examples }}' != 'y':
            paths_to_remove.append('examples')
            
        if '{{ cookiecutter.use_github_actions }}' != 'y':
            paths_to_remove.append('.github')

        if not any([
            '{{ cookiecutter.use_docker }}' == 'y',
            '{{ cookiecutter.use_make }}' == 'y'
        ]):
            paths_to_remove.append('.env.example')
            
        print('🗑️  Removing unnecessary files...')
        remove_paths(paths_to_remove)
        
        print('📦 Setting up Poetry environment...')
        setup_poetry()

        print('🔧 Setting up environment...')
        setup_env()
        
        print('🔧 Initializing Git repository...')
        init_git()
        
        print('✨ Project setup completed successfully!')
        
    except subprocess.CalledProcessError as e:
        print(f'❌ Error during setup: {e}')
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main()) 