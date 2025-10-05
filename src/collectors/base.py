# Base Collector
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger("ai-framework.collectors.base")

class DataCollector(ABC):
    """Base class for all data collectors."""
    
    def __init__(self, config):
        """
        Initialize the data collector.
        
        Args:
            config (dict): Configuration for this collector
        """
        self.config = config
        self.is_running = False
        self.storage = None  # Will be set by the collection manager
    
    @abstractmethod
    def start(self):
        """
        Start collecting data.
        
        Returns:
            bool: True if started successfully, False otherwise
        """
        pass
        
    @abstractmethod
    def stop(self):
        """
        Stop collecting data.
        
        Returns:
            bool: True if stopped successfully, False otherwise
        """
        pass
        
    @abstractmethod
    def get_schema(self):
        """
        Return the schema of collected data.
        
        Returns:
            dict: Schema definition
        """
        pass
    
    def set_storage(self, storage):
        """
        Set the storage manager to use for data persistence.
        
        Args:
            storage: StorageManager instance
        """
        self.storage = storage
        logger.debug(f"Storage set for {self.__class__.__name__}")