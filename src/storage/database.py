# Database Storage Manager
import os
import json
import sqlite3
import logging
import time
from pathlib import Path
from datetime import datetime

logger = logging.getLogger("ai-framework.storage.database")

class StorageManager:
    """Manage data storage and retrieval."""
    
    def __init__(self, config):
        """
        Initialize storage manager.
        
        Args:
            config (dict): Storage configuration
        """
        self.config = config
        
        # Get database path from config or use default
        db_path = config.get("db_path", "~/.ai_assistant/data.db")
        
        # Expand user directory if needed
        if db_path.startswith("~"):
            db_path = str(Path(db_path).expanduser())
        
        # Ensure path exists
        db_dir = os.path.dirname(db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        self.db_path = db_path
        self.conn = None
    
    def initialize(self):
        """
        Initialize storage and create schema if needed.
        
        Returns:
            bool: True if successful
        """
        try:
            # Connect to database
            self.conn = sqlite3.connect(self.db_path)
            
            # Create tables if they don't exist
            self._create_schema()
            
            logger.info(f"Storage initialized: {self.db_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing storage: {e}")
            return False
    
    def _create_schema(self):
        """Create database schema if it doesn't exist."""
        cursor = self.conn.cursor()
        
        # Create file events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_events (
                id INTEGER PRIMARY KEY,
                timestamp REAL,
                operation TEXT,
                path TEXT,
                file_type TEXT,
                size INTEGER,
                app TEXT
            )
        ''')
        
        # Create application events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_events (
                id INTEGER PRIMARY KEY,
                timestamp REAL,
                app_name TEXT,
                window_title TEXT,
                focus_duration INTEGER,
                active BOOLEAN
            )
        ''')
        
        # Create system events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_events (
                id INTEGER PRIMARY KEY,
                timestamp REAL,
                cpu_percent REAL,
                memory_percent REAL,
                active_window TEXT,
                state TEXT
            )
        ''')
        
        # Create features table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS features (
                id INTEGER PRIMARY KEY,
                timestamp REAL,
                feature_type TEXT,
                feature_data TEXT
            )
        ''')
        
        # Create models table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS models (
                id INTEGER PRIMARY KEY,
                name TEXT,
                version TEXT,
                created_at REAL,
                model_type TEXT,
                serialized_model BLOB,
                performance_metrics TEXT
            )
        ''')
        
        self.conn.commit()
    
    def store_events(self, events, event_type):
        """
        Store collected events in database.
        
        Args:
            events (list): List of event dictionaries
            event_type (str): Type of events (file_events, app_events, etc.)
            
        Returns:
            bool: True if successful
        """
        if not self.conn:
            logger.error("Database not initialized")
            return False
        
        try:
            cursor = self.conn.cursor()
            
            if event_type == "file_events":
                for event in events:
                    cursor.execute('''
                        INSERT INTO file_events
                        (timestamp, operation, path, file_type, size, app)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        event["timestamp"],
                        event["operation"],
                        event["path"],
                        event["file_type"],
                        event["size"],
                        event["app"]
                    ))
            
            elif event_type == "app_events":
                for event in events:
                    cursor.execute('''
                        INSERT INTO app_events
                        (timestamp, app_name, window_title, focus_duration, active)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        event["timestamp"],
                        event["app_name"],
                        event["window_title"],
                        event["focus_duration"],
                        event["active"]
                    ))
            
            elif event_type == "system_events":
                for event in events:
                    cursor.execute('''
                        INSERT INTO system_events
                        (timestamp, cpu_percent, memory_percent, active_window, state)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        event["timestamp"],
                        event["cpu_percent"],
                        event["memory_percent"],
                        event["active_window"],
                        event["state"]
                    ))
            
            else:
                logger.warning(f"Unknown event type: {event_type}")
                return False
            
            self.conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error storing events: {e}")
            return False
    
    def get_events(self, event_type, start_time=None, end_time=None):
        """
        Retrieve events for given time period.
        
        Args:
            event_type (str): Type of events to retrieve
            start_time (float, optional): Start timestamp
            end_time (float, optional): End timestamp
            
        Returns:
            list: Events matching the criteria
        """
        if not self.conn:
            logger.error("Database not initialized")
            return []
        
        try:
            cursor = self.conn.cursor()
            query = f"SELECT * FROM {event_type}"
            params = []
            
            # Add time filters if provided
            if start_time or end_time:
                query += " WHERE "
                
                if start_time:
                    query += "timestamp >= ?"
                    params.append(start_time)
                
                if start_time and end_time:
                    query += " AND "
                
                if end_time:
                    query += "timestamp <= ?"
                    params.append(end_time)
            
            # Order by timestamp
            query += " ORDER BY timestamp ASC"
            
            # Execute query
            cursor.execute(query, params)
            
            # Get column names
            columns = [description[0] for description in cursor.description]
            
            # Convert to list of dictionaries
            events = []
            for row in cursor.fetchall():
                event = {}
                for i, column in enumerate(columns):
                    event[column] = row[i]
                events.append(event)
            
            return events
            
        except Exception as e:
            logger.error(f"Error retrieving events: {e}")
            return []
    
    def store_features(self, features, feature_type):
        """
        Store processed features.
        
        Args:
            features (dict): Features dictionary or DataFrame
            feature_type (str): Type of features
            
        Returns:
            bool: True if successful
        """
        if not self.conn:
            logger.error("Database not initialized")
            return False
        
        try:
            # Convert DataFrame to dict if needed
            if hasattr(features, "to_dict"):
                features_dict = features.to_dict("records")
            else:
                features_dict = features
            
            # Serialize features to JSON
            serialized = json.dumps(features_dict)
            
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO features
                (timestamp, feature_type, feature_data)
                VALUES (?, ?, ?)
            ''', (
                time.time(),
                feature_type,
                serialized
            ))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error storing features: {e}")
            return False
    
    def get_features(self, feature_type=None, limit=100):
        """
        Retrieve stored features.
        
        Args:
            feature_type (str, optional): Type of features to retrieve
            limit (int): Maximum number of records to return
            
        Returns:
            list: Feature records
        """
        if not self.conn:
            logger.error("Database not initialized")
            return []
        
        try:
            cursor = self.conn.cursor()
            query = "SELECT * FROM features"
            params = []
            
            if feature_type:
                query += " WHERE feature_type = ?"
                params.append(feature_type)
            
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            
            # Get column names
            columns = [description[0] for description in cursor.description]
            
            # Convert to list of dictionaries
            features = []
            for row in cursor.fetchall():
                feature = {}
                for i, column in enumerate(columns):
                    if column == "feature_data":
                        feature[column] = json.loads(row[i])
                    else:
                        feature[column] = row[i]
                features.append(feature)
            
            return features
            
        except Exception as e:
            logger.error(f"Error retrieving features: {e}")
            return []
    
    def store_model(self, name, version, model_type, serialized_model, metrics=None):
        """
        Store a trained model.
        
        Args:
            name (str): Model name
            version (str): Model version
            model_type (str): Type of model
            serialized_model (bytes): Serialized model data
            metrics (dict, optional): Performance metrics
            
        Returns:
            bool: True if successful
        """
        if not self.conn:
            logger.error("Database not initialized")
            return False
        
        try:
            # Serialize metrics to JSON if provided
            metrics_json = json.dumps(metrics) if metrics else None
            
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO models
                (name, version, created_at, model_type, serialized_model, performance_metrics)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                name,
                version,
                time.time(),
                model_type,
                serialized_model,
                metrics_json
            ))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error storing model: {e}")
            return False
    
    def get_model(self, name, version=None):
        """
        Retrieve a stored model.
        
        Args:
            name (str): Model name
            version (str, optional): Model version (latest if not specified)
            
        Returns:
            dict: Model record or None if not found
        """
        if not self.conn:
            logger.error("Database not initialized")
            return None
        
        try:
            cursor = self.conn.cursor()
            query = "SELECT * FROM models WHERE name = ?"
            params = [name]
            
            if version:
                query += " AND version = ?"
                params.append(version)
            else:
                query += " ORDER BY created_at DESC LIMIT 1"
            
            cursor.execute(query, params)
            row = cursor.fetchone()
            
            if not row:
                logger.warning(f"Model not found: {name} (version: {version})")
                return None
            
            # Convert to dictionary
            columns = [description[0] for description in cursor.description]
            model = {}
            for i, column in enumerate(columns):
                if column == "performance_metrics" and row[i]:
                    model[column] = json.loads(row[i])
                else:
                    model[column] = row[i]
            
            return model
            
        except Exception as e:
            logger.error(f"Error retrieving model: {e}")
            return None