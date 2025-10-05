# File System Collector
import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from src.collectors.base import DataCollector

logger = logging.getLogger("ai-framework.collectors.file_system")

class FileSystemEventProcessor(FileSystemEventHandler):
    """Process file system events."""
    
    def __init__(self, collector):
        """
        Initialize with parent collector.
        
        Args:
            collector: FileSystemCollector instance
        """
        self.collector = collector
    
    def on_created(self, event):
        """Process file creation event."""
        if event.is_directory:
            return
        
        self._process_event(event.src_path, "create")
    
    def on_modified(self, event):
        """Process file modification event."""
        if event.is_directory:
            return
        
        if "modify" not in self.collector.monitored_events:
            return
            
        self._process_event(event.src_path, "modify")
    
    def on_deleted(self, event):
        """Process file deletion event."""
        if event.is_directory:
            return
        
        if "delete" not in self.collector.monitored_events:
            return
            
        self._process_event(event.src_path, "delete")
    
    def on_moved(self, event):
        """Process file move event."""
        if event.is_directory:
            return
        
        if "move" not in self.collector.monitored_events:
            return
            
        # Record as delete of source and create of destination
        self._process_event(event.src_path, "delete")
        self._process_event(event.dest_path, "create")
    
    def _process_event(self, file_path, operation):
        """
        Process a file event.
        
        Args:
            file_path (str): Path to the file
            operation (str): Operation type (create, modify, delete)
        """
        # Skip if path is excluded
        if self.collector.is_path_excluded(file_path):
            return
        
        try:
            path = Path(file_path)
            file_type = path.suffix[1:] if path.suffix else ""
            size = path.stat().st_size if operation != "delete" and path.exists() else 0
            
            event = {
                "timestamp": time.time(),
                "operation": operation,
                "path": file_path,
                "file_type": file_type,
                "size": size,
                "app": ""  # Would require additional system info to determine
            }
            
            logger.debug(f"File event: {operation} {file_path}")
            
            # Store the event if storage is available
            if self.collector.storage:
                self.collector.storage.store_events([event], "file_events")
        except Exception as e:
            logger.error(f"Error processing file event: {e}")


class FileSystemCollector(DataCollector):
    """Collect file system events."""
    
    def __init__(self, config):
        """
        Initialize file system collector.
        
        Args:
            config (dict): Configuration dictionary
        """
        super().__init__(config)
        
        # Extract configuration
        self.paths = self._resolve_paths(config.get("paths", []))
        self.exclude_paths = self._resolve_paths(config.get("exclude_paths", []))
        self.monitored_events = config.get("events", ["create", "modify", "delete"])
        
        # Initialize watchdog components
        self.event_handler = FileSystemEventProcessor(self)
        self.observers = []
    
    def _resolve_paths(self, paths):
        """
        Resolve path strings to absolute paths.
        
        Args:
            paths (list): List of path strings
            
        Returns:
            list: Resolved absolute paths
        """
        resolved = []
        for path in paths:
            # Expand user directory if needed
            if path.startswith("~"):
                path = str(Path(path).expanduser())
            resolved.append(Path(path).resolve())
        return resolved
    
    def is_path_excluded(self, path):
        """
        Check if a path should be excluded.
        
        Args:
            path (str): Path to check
            
        Returns:
            bool: True if path should be excluded
        """
        path = Path(path)
        
        # Check against exclusion paths
        for exclude in self.exclude_paths:
            if str(path).startswith(str(exclude)):
                return True
        
        return False
    
    def start(self):
        """
        Start collecting file system events.
        
        Returns:
            bool: True if successful
        """
        if self.is_running:
            logger.warning("File system collector already running")
            return True
        
        try:
            # Create an observer for each path
            for path in self.paths:
                if not path.exists():
                    logger.warning(f"Path does not exist, creating: {path}")
                    path.mkdir(parents=True, exist_ok=True)
                
                observer = Observer()
                observer.schedule(self.event_handler, str(path), recursive=True)
                observer.start()
                self.observers.append(observer)
                logger.info(f"Watching directory: {path}")
            
            self.is_running = True
            logger.info("File system collector started")
            return True
            
        except Exception as e:
            logger.error(f"Error starting file system collector: {e}")
            self.stop()  # Cleanup any partial setup
            return False
    
    def stop(self):
        """
        Stop collecting file system events.
        
        Returns:
            bool: True if successful
        """
        if not self.is_running:
            return True
        
        try:
            # Stop all observers
            for observer in self.observers:
                observer.stop()
            
            # Wait for observers to finish
            for observer in self.observers:
                observer.join()
            
            self.observers = []
            self.is_running = False
            logger.info("File system collector stopped")
            return True
            
        except Exception as e:
            logger.error(f"Error stopping file system collector: {e}")
            return False
    
    def get_schema(self):
        """
        Return the schema of collected data.
        
        Returns:
            dict: Schema definition
        """
        return {
            "timestamp": "float",  # UNIX timestamp
            "operation": "str",    # create, modify, delete
            "path": "str",         # Absolute file path
            "file_type": "str",    # File extension
            "size": "int",         # File size in bytes
            "app": "str"           # Application causing the event (if available)
        }