#!/usr/bin/env python3
"""
AI Personal Productivity Assistant
Main entry point for the application
"""

import sys
import os
import logging
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config.config_manager import ConfigManager
from data_collection.activity_monitor import ActivityMonitor
from data_processing.data_processor import DataProcessor
from machine_learning.model_trainer import ModelTrainer
from recommendation_engine.recommender import Recommender
from ui.interface import UserInterface

class ProductivityAssistant:
    """Main application class for the AI Personal Productivity Assistant"""

    def __init__(self):
        self.config = None
        self.activity_monitor = None
        self.data_processor = None
        self.model_trainer = None
        self.recommender = None
        self.ui = None
        self.logger = None

    def initialize(self):
        """Initialize all components of the application"""
        try:
            # Load configuration
            self.config = ConfigManager()
            self.config.load_config()

            # Setup logging
            self._setup_logging()

            self.logger.info("Initializing AI Personal Productivity Assistant...")

            # Initialize components
            self.activity_monitor = ActivityMonitor(self.config)
            self.data_processor = DataProcessor(self.config)
            self.model_trainer = ModelTrainer(self.config)
            self.recommender = Recommender(self.config)
            self.ui = UserInterface(self.config)

            self.logger.info("All components initialized successfully")

        except Exception as e:
            print(f"Failed to initialize application: {e}")
            if self.logger:
                self.logger.error(f"Initialization failed: {e}")
            sys.exit(1)

    def _setup_logging(self):
        """Setup logging configuration"""
        log_config = self.config.get('LOGGING', {})
        log_level = getattr(logging, log_config.get('LEVEL', 'INFO').upper())
        log_file = os.path.expanduser(log_config.get('FILE', '~/.ai_productivity_assistant/logs/app.log'))

        # Create log directory if it doesn't exist
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )

        self.logger = logging.getLogger(__name__)

    def start(self):
        """Start the application"""
        try:
            self.logger.info("Starting AI Personal Productivity Assistant...")

            # Start activity monitoring
            self.activity_monitor.start()

            # Start data processing
            self.data_processor.start()

            # Start model training (background)
            self.model_trainer.start()

            # Start user interface
            self.ui.start()

            self.logger.info("Application started successfully")

        except Exception as e:
            self.logger.error(f"Failed to start application: {e}")
            self.stop()
            sys.exit(1)

    def stop(self):
        """Stop the application and cleanup resources"""
        self.logger.info("Stopping AI Personal Productivity Assistant...")

        try:
            if self.ui:
                self.ui.stop()
            if self.model_trainer:
                self.model_trainer.stop()
            if self.data_processor:
                self.data_processor.stop()
            if self.activity_monitor:
                self.activity_monitor.stop()

            self.logger.info("Application stopped successfully")

        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")

def main():
    """Main entry point"""
    app = ProductivityAssistant()
    app.initialize()

    try:
        app.start()
        # Keep the application running
        input("Press Enter to stop the application...\n")
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    finally:
        app.stop()

if __name__ == "__main__":
    main()