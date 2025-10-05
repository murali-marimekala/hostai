# Collection Manager
import logging
import importlib
from pathlib import Path

logger = logging.getLogger("ai-framework.collectors.manager")

class CollectionManager:
    """Manages data collectors."""
    
    def __init__(self, config, storage):
        """
        Initialize collection manager.
        
        Args:
            config (dict): Collection configuration
            storage: Storage manager instance
        """
        self.config = config
        self.storage = storage
        self.collectors = {}
        self.collector_configs = config.get("collectors", {})
    
    def initialize(self):
        """
        Initialize all configured collectors.
        
        Returns:
            bool: True if successful
        """
        logger.info("Initializing collectors")
        
        # Initialize each configured collector
        for collector_name, collector_config in self.collector_configs.items():
            if not collector_config.get("enabled", True):
                logger.info(f"Collector {collector_name} disabled in config")
                continue
            
            try:
                # Import the collector module
                module_name = f"src.collectors.{collector_name}"
                
                try:
                    module = importlib.import_module(module_name)
                except ImportError as e:
                    logger.error(f"Could not import collector {module_name}: {e}")
                    continue
                
                # Find the collector class (assume it's named XxxCollector)
                class_name = "".join(word.capitalize() for word in collector_name.split("_")) + "Collector"
                
                if not hasattr(module, class_name):
                    logger.error(f"Collector class {class_name} not found in {module_name}")
                    continue
                
                # Instantiate the collector
                collector_class = getattr(module, class_name)
                collector = collector_class(collector_config)
                
                # Set storage
                collector.set_storage(self.storage)
                
                # Store in collectors dict
                self.collectors[collector_name] = collector
                logger.info(f"Initialized collector: {collector_name}")
                
            except Exception as e:
                logger.error(f"Error initializing collector {collector_name}: {e}")
        
        return len(self.collectors) > 0
    
    def start_collectors(self):
        """
        Start all collectors.
        
        Returns:
            bool: True if all collectors started successfully
        """
        logger.info("Starting collectors")
        
        success = True
        for name, collector in self.collectors.items():
            try:
                if collector.start():
                    logger.info(f"Started collector: {name}")
                else:
                    logger.error(f"Failed to start collector: {name}")
                    success = False
            except Exception as e:
                logger.error(f"Error starting collector {name}: {e}")
                success = False
        
        return success
    
    def stop_collectors(self):
        """
        Stop all collectors.
        
        Returns:
            bool: True if all collectors stopped successfully
        """
        logger.info("Stopping collectors")
        
        success = True
        for name, collector in self.collectors.items():
            try:
                if collector.stop():
                    logger.info(f"Stopped collector: {name}")
                else:
                    logger.error(f"Failed to stop collector: {name}")
                    success = False
            except Exception as e:
                logger.error(f"Error stopping collector {name}: {e}")
                success = False
        
        return success
    
    def get_collector(self, name):
        """
        Get a collector by name.
        
        Args:
            name (str): Collector name
            
        Returns:
            Collector instance or None if not found
        """
        return self.collectors.get(name)
    
    def get_collectors(self):
        """
        Get all collectors.
        
        Returns:
            dict: Dictionary of collector instances
        """
        return self.collectors