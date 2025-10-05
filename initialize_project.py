#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Create the project structure

def create_project_structure():
    """
    Create the initial project structure according to the architecture
    """
    # Base directories
    directories = [
        "src/core",
        "src/collectors",
        "src/processing",
        "src/storage",
        "src/models",
        "src/analysis",
        "src/ui",
        "config",
        "tests/core",
        "tests/collectors", 
        "tests/processing",
        "tests/storage",
        "tests/models",
        "tests/analysis",
        "tests/ui",
        "docs",
        "data",
    ]
    
    # Create each directory
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        # Create __init__.py files
        if directory.startswith("src") or directory.startswith("tests"):
            init_file = Path(directory) / "__init__.py"
            init_file.touch()
    
    print("Project structure created successfully!")

def create_initial_files():
    """
    Create initial placeholder files
    """
    # Create README.md
    readme_content = """# AI Local Learning Framework

A privacy-focused AI framework that learns from local machine activity to help you be more productive.

## Features

- Locally processes all data - no cloud dependencies
- Learns from file system activity and application usage
- Provides productivity insights and recommendations
- Privacy-first design - you control your data

## Getting Started

See the [DEVELOPMENT_ROADMAP.md](DEVELOPMENT_ROADMAP.md) for implementation details.

## Architecture

The system architecture is described in [OPTIMIZED_ARCHITECTURE.md](OPTIMIZED_ARCHITECTURE.md).
"""
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    
    # Create initial requirements.txt
    requirements_content = """# Core dependencies
watchdog>=2.1.6
psutil>=5.9.0
pandas>=1.3.5
numpy>=1.21.5
scikit-learn>=1.0.2
pyyaml>=6.0
PyQt5>=5.15.6

# Development dependencies
pytest>=7.0.0
flake8>=4.0.1
black>=22.3.0
"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements_content)
    
    # Create example config
    example_config_content = """# Example configuration file
# Copy this to config.yaml and edit for your environment

data_collection:
  enabled: true
  collectors:
    file_system:
      enabled: true
      paths: ["~/Documents", "~/Projects"]
      exclude_paths: ["~/Documents/Personal", "~/.cache"]
      events: ["create", "modify", "delete"]
    application:
      enabled: true
      sample_interval: 60  # seconds
      exclude_apps: ["Password Manager", "Banking App"]
    system:
      enabled: true
      sample_interval: 300  # seconds

processing:
  schedules:
    feature_extraction: "hourly"
    model_training: "daily"
  
models:
  productivity_classifier:
    type: "RandomForestClassifier"
    parameters:
      n_estimators: 100
      max_depth: 10
    training:
      sample_size: 1000
      test_ratio: 0.2
      
privacy:
  data_retention_days: 90
  anonymize_paths: true
  collect_window_titles: false
"""
    
    with open("config/example_config.yaml", "w") as f:
        f.write(example_config_content)
    
    # Create main.py
    main_content = """#!/usr/bin/env python3
# Main application entry point

import os
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("ai-framework")

def main():
    """Main application entry point"""
    logger.info("Starting AI Local Learning Framework...")
    
    # Import controller here to avoid circular imports
    from src.core.controller import ApplicationController
    
    # Determine config path
    config_dir = Path("config")
    config_path = config_dir / "config.yaml"
    
    if not config_path.exists():
        config_path = config_dir / "example_config.yaml"
        logger.warning(f"Config not found, using example config: {config_path}")
    
    # Initialize controller
    try:
        controller = ApplicationController(config_path)
        controller.initialize()
        controller.start()
    except Exception as e:
        logger.error(f"Error starting application: {e}")
        sys.exit(1)
    
    logger.info("Application started successfully")
    
    # For command-line operation, we can add a simple loop here
    # In GUI mode, this would be handled by the UI event loop
    try:
        # This is a placeholder - in the real app, we'd use the UI event loop
        input("Press Enter to exit...\n")
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("Shutting down...")
        controller.stop()
    
    logger.info("Application terminated")

if __name__ == "__main__":
    main()
"""
    
    with open("src/main.py", "w") as f:
        f.write(main_content)
    
    # Create .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/

# IDE files
.idea/
.vscode/
*.swp
*.swo

# Application specific
/data/*.db
/data/models/
/config/config.yaml
/logs/
.coverage
htmlcov/
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    
    print("Initial files created successfully!")

def create_core_files():
    """
    Create core module files
    """
    # Controller
    controller_content = """# Main application controller
import logging
import yaml
from pathlib import Path

logger = logging.getLogger("ai-framework.controller")

class ApplicationController:
    """Main application controller."""
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.load_config(config_path)
        self.storage = None
        self.collectors = {}
        self.processors = {}
        self.model_manager = None
        self.ui = None
        self.running = False
    
    def load_config(self, config_path):
        """Load configuration from file."""
        logger.info(f"Loading configuration from {config_path}")
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise
    
    def initialize(self):
        """Initialize all application components."""
        logger.info("Initializing application components")
        
        # Initialize storage
        try:
            from src.storage.database import StorageManager
            self.storage = StorageManager(self.config.get('storage', {}))
            self.storage.initialize()
        except Exception as e:
            logger.error(f"Error initializing storage: {e}")
            raise
        
        # Initialize collectors
        if self.config.get('data_collection', {}).get('enabled', False):
            try:
                from src.collectors.manager import CollectionManager
                self.collection_manager = CollectionManager(
                    self.config.get('data_collection', {}),
                    self.storage
                )
                self.collection_manager.initialize()
            except Exception as e:
                logger.error(f"Error initializing collectors: {e}")
                raise
        
        # Other initializations will be added as components are developed
        
        logger.info("Application components initialized successfully")
        return True
    
    def start(self):
        """Start the application."""
        logger.info("Starting application")
        
        if self.collection_manager:
            self.collection_manager.start_collectors()
        
        # Start other components
        
        self.running = True
        logger.info("Application started")
        return True
    
    def stop(self):
        """Stop the application."""
        logger.info("Stopping application")
        
        if self.collection_manager:
            self.collection_manager.stop_collectors()
        
        # Stop other components
        
        self.running = False
        logger.info("Application stopped")
        return True
"""
    
    with open("src/core/controller.py", "w") as f:
        f.write(controller_content)

    # Config
    config_content = """# Configuration management
import os
import logging
import yaml
from pathlib import Path

logger = logging.getLogger("ai-framework.config")

class ConfigManager:
    """Manages loading and validating configuration."""
    
    def __init__(self, config_path=None):
        """Initialize with optional config path."""
        self.config_path = config_path
        self.config = {}
        
        # Set default config path if none provided
        if not config_path:
            self.config_path = Path("config/config.yaml")
            if not self.config_path.exists():
                self.config_path = Path("config/example_config.yaml")
    
    def load(self):
        """Load configuration from file."""
        logger.info(f"Loading configuration from {self.config_path}")
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            
            # Validate configuration
            self.validate()
            
            return self.config
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise
    
    def validate(self):
        """Validate configuration structure and values."""
        # Basic validation
        if not isinstance(self.config, dict):
            raise ValueError("Configuration must be a dictionary")
        
        # Check required sections
        required_sections = ['data_collection', 'processing', 'models', 'privacy']
        for section in required_sections:
            if section not in self.config:
                logger.warning(f"Configuration missing section: {section}")
                self.config[section] = {}
        
        # Validate data collection settings
        if 'data_collection' in self.config:
            dc = self.config['data_collection']
            if not isinstance(dc.get('collectors', {}), dict):
                raise ValueError("data_collection.collectors must be a dictionary")
        
        # More validation as needed
        
        logger.info("Configuration validation successful")
        return True
    
    def get(self, key, default=None):
        """Get a configuration value by key with optional default."""
        # Support nested keys with dot notation
        if '.' in key:
            keys = key.split('.')
            value = self.config
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return default
            return value
        
        return self.config.get(key, default)
"""
    
    with open("src/core/config.py", "w") as f:
        f.write(config_content)
    
    print("Core files created successfully!")

if __name__ == "__main__":
    print("Creating AI Local Learning Framework project structure...")
    create_project_structure()
    create_initial_files()
    create_core_files()
    print("\nProject initialized! Next steps:")
    print("1. Create a virtual environment: python -m venv venv")
    print("2. Activate the virtual environment:")
    print("   - On Windows: venv\\Scripts\\activate")
    print("   - On macOS/Linux: source venv/bin/activate")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Follow the DEVELOPMENT_ROADMAP.md file for implementation steps")