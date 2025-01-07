import os
from pathlib import Path

def print_directory_tree(start_path, output_file, shallow_dirs=None):
    """
    Print the directory tree structure and file contents for Django/React projects.
    
    Args:
        start_path (str): The root directory to start from
        output_file (str): Path to the output file
        shallow_dirs (set): Set of directory names that should not be traversed deeply
    """

    # Directories to exclude completely
    exclude_dirs = {
        # Django specific
        '__pycache__', 
        'migrations',
        'venv',
        '.env',
        '.pytest_cache',
        '.coverage',
        
        # React/Node specific
        'node_modules',
        'build',
        'dist',
        'coverage',
        
        # Version control and IDE
        '.git',
        '.idea',
        '.vscode',
        
        # Cache and temporary files
        '.cache',
        'tmp'
    }

    # File patterns to exclude
    exclude_file_patterns = {
        # Django
        '*.pyc',
        '*.pyo',
        '*.pyd',
        'db.sqlite3',
        '*.logs',
        
        # React/Node
        'package-lock.json',
        'yarn.lock',
        '*.map',
        
        # Other
        '.DS_Store',
        '*.swp',
        '*.swo',
        '.env',
        '*.pid'
    }

    # File extensions to include
    include_extensions = {
        # Django/Python
        '.py',
        '.env.example',
        'requirements.txt',
        'Dockerfile',
        'docker-compose.yml',
        
        # React/JavaScript
        '.js',
        '.jsx',
        '.ts',
        '.tsx',
        '.css',
        '.scss',
        '.html',
        '.json',
        
        # Configuration files
        '.yml',
        '.yaml',
        '.toml',
        '.ini',
        '.conf'
    }
    
    if shallow_dirs:
        exclude_dirs.update(shallow_dirs)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Project Structure for: {start_path}\n")
        f.write("=" * 50 + "\n\n")
        
        # Print directory tree
        f.write("Directory Structure:\n")
        f.write("-" * 20 + "\n")
        
        for root, dirs, files in os.walk(start_path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            # Calculate relative path for cleaner output
            relative_root = os.path.relpath(root, start_path)
            level = relative_root.count(os.sep)
            indent = '│   ' * level
            
            # Get the current directory name
            current_dir = os.path.basename(root)
            
            if relative_root != '.':
                f.write(f"{indent}├── {current_dir}/\n")
            
            subindent = '│   ' * (level + 1)
            
            # Filter and sort files
            included_files = []
            for file in sorted(files):
                file_path = os.path.join(relative_root, file)
                
                # Check if file should be included
                should_include = (
                    file_path.endswith(tuple(include_extensions)) and
                    not any(file_path.endswith(pat.replace('*', '')) for pat in exclude_file_patterns)
                )
                
                if should_include:
                    included_files.append(file)
                    f.write(f"{subindent}├── {file}\n")
        
        # Only print file contents for the main directory, not for shallow directories
        f.write("\nFile Contents:\n")
        f.write("=" * 50 + "\n\n")
        
        for root, dirs, files in os.walk(start_path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in sorted(files):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, start_path)
                
                # Check if file should be included
                should_include = (
                    relative_path.endswith(tuple(include_extensions)) and
                    not any(relative_path.endswith(pat.replace('*', '')) for pat in exclude_file_patterns)
                )
                
                if should_include:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as content_file:
                            content = content_file.read()
                            f.write(f"File: {relative_path}\n")
                            f.write("-" * len(f"File: {relative_path}") + "\n")
                            f.write(content)
                            f.write("\n\n" + "=" * 50 + "\n\n")
                    except Exception as e:
                        f.write(f"Could not read {relative_path}: {str(e)}\n\n")

if __name__ == "__main__":
    # Paths configuration
    backend_path = "/home/pirat/Desktop/pyth/scraper/backend"
    backend_output = "/home/pirat/Desktop/TreeContent/django_structure.txt"
    
    frontend_path = "/home/pirat/Desktop/pyth/scraper/frontend"
    frontend_output = "/home/pirat/Desktop/TreeContent/react_structure.txt"
    
    main_path = "/home/pirat/Desktop/pyth/scraper"
    main_output = "/home/pirat/Desktop/TreeContent/main.txt"
    
    # Define directories to show but not traverse deeply in main output
    shallow_dirs = ['backend', 'frontend']
    
    # Export backend structure
    print_directory_tree(backend_path, backend_output)
    print(f"Django project structure exported to {backend_output}")
    
    # Export frontend structure
    print_directory_tree(frontend_path, frontend_output)
    print(f"React project structure exported to {frontend_output}")
    
    # Export main structure with shallow directories
    print_directory_tree(main_path, main_output, shallow_dirs)
    print(f"Overall project structure exported to {main_output}")