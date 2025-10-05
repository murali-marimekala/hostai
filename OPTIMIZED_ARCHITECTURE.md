# AI Local Learning Framework - Optimized Architecture Document

## Overview

This document outlines the architecture for an AI framework that enables local machine learning using system events and user activity. The framework collects data, trains models, and generates predictions entirely on the user's device, ensuring complete privacy and offline operation. This architecture is designed for incremental implementation with GitHub Copilot.

## Implementation Principles

### 1. **Modularity First**
- **Independent components**: Each module functions independently
- **Clear interfaces**: Well-defined APIs between modules
- **Testable units**: Each component can be tested in isolation
- **Incremental development**: Build and test one module at a time

### 2. **Concrete Technology Choices**
- **Python 3.8+**: Core implementation language
- **scikit-learn**: Primary ML framework for models
- **SQLite**: Local data storage
- **Watchdog**: File system monitoring
- **psutil**: System resource and application monitoring
- **pandas/numpy**: Data processing
- **PyQt5**: User interface (desktop application)

### 3. **Simplified Extensibility**
- **Config-based customization**: Control behavior via configuration
- **Standardized interfaces**: Easy to add new collectors or models
- **Data pipeline patterns**: Consistent data flow across components

## System Architecture

### Core Components

#### 1. Data Collection

**Purpose**: Gather system events and user activity data.

**Implementation**:
```python
# src/collectors/base.py
class DataCollector:
    """Base class for all data collectors."""
    def __init__(self, config: dict):
        self.config = config
        self.is_running = False
        self.storage = None  # Set by the collection manager
    
    def start(self) -> bool:
        """Start collecting data."""
        pass
        
    def stop(self) -> bool:
        """Stop collecting data."""
        pass
        
    def get_schema(self) -> dict:
        """Return the schema of collected data."""
        pass
```

**Key Collectors**:

1. **File System Collector**
   - Monitors file operations (create, modify, delete, access)
   - Records file paths, operations, timestamps
   - Configurable paths and event types

2. **Application Usage Collector**
   - Tracks active applications and window focus
   - Records app name, window title, focus duration
   - Samples at configurable intervals

3. **System Activity Collector**
   - Monitors CPU, memory, network usage
   - Tracks system state (idle, active, sleep)
   - Records at configurable intervals

**Data Schemas**:

```python
# File System Event Schema
file_event = {
    "timestamp": datetime,      # When the event occurred
    "operation": str,           # "create", "modify", "delete", "access"
    "path": str,                # Absolute file path
    "file_type": str,           # File extension
    "size": int,                # File size in bytes
    "app": str                  # Application causing the event (if available)
}

# Application Usage Schema
app_event = {
    "timestamp": datetime,      # When the sample was taken
    "app_name": str,            # Application name
    "window_title": str,        # Window title
    "focus_duration": int,      # Seconds app was in focus
    "active": bool              # Whether user was actively using it
}
```

#### 2. Data Processing

**Purpose**: Transform raw collected data into features for machine learning.

**Implementation**:
```python
# src/processing/processor.py
class DataProcessor:
    """Process raw data into features for ML models."""
    def __init__(self, config: dict):
        self.config = config
        self.transformers = {}  # Feature transformers
    
    def process_batch(self, data: list, data_type: str) -> pd.DataFrame:
        """Process a batch of raw data into features."""
        pass
        
    def get_feature_names(self) -> list:
        """Get names of features this processor generates."""
        pass
```

**Key Processors**:

1. **Time-based Feature Extractor**
   - Extract time of day, day of week, weekend vs weekday
   - Identify patterns in user activity timing
   - Calculate activity durations and intervals

2. **Activity Classifier**
   - Categorize activities (work, leisure, communication)
   - Identify application purposes
   - Group related activities

3. **Content Analyzer**
   - Extract file types and categories
   - Identify project contexts from paths and content
   - Detect work vs personal content (no inspection of content)

**Feature Examples**:
```python
# Time Features
time_features = {
    "hour_of_day": int,         # 0-23 hour
    "day_of_week": int,         # 0-6 (Monday-Sunday)
    "is_weekend": bool,         # True if weekend
    "time_period": str,         # "morning", "afternoon", "evening", "night"
    "is_work_hours": bool       # True if typical work hours
}

# Activity Features
activity_features = {
    "activity_type": str,       # "coding", "writing", "browsing", etc.
    "app_category": str,        # "development", "productivity", "communication"
    "focus_duration": float,    # Duration of focused activity
    "context_switches": int     # Number of app switches in period
}
```

#### 3. Storage Layer

**Purpose**: Persist collected data, processed features, and trained models.

**Implementation**:
```python
# src/storage/database.py
class StorageManager:
    """Manage data storage and retrieval."""
    def __init__(self, config: dict):
        self.db_path = config.get("db_path", "~/.ai_assistant/data.db")
        self.conn = None
    
    def initialize(self) -> bool:
        """Initialize storage and create schema if needed."""
        pass
        
    def store_events(self, events: list, event_type: str) -> bool:
        """Store collected events in database."""
        pass
        
    def get_events(self, event_type: str, start_time: datetime, 
                  end_time: datetime) -> list:
        """Retrieve events for given time period."""
        pass
        
    def store_features(self, features: pd.DataFrame, feature_type: str) -> bool:
        """Store processed features."""
        pass
```

**Database Schema**:
```sql
-- Events tables
CREATE TABLE file_events (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    operation TEXT,
    path TEXT,
    file_type TEXT,
    size INTEGER,
    app TEXT
);

CREATE TABLE app_events (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    app_name TEXT,
    window_title TEXT,
    focus_duration INTEGER,
    active BOOLEAN
);

-- Features table
CREATE TABLE features (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    feature_type TEXT,
    feature_data TEXT  -- JSON serialized features
);

-- Models table
CREATE TABLE models (
    id INTEGER PRIMARY KEY,
    name TEXT,
    version TEXT,
    created_at TEXT,
    model_type TEXT,
    serialized_model BLOB,
    performance_metrics TEXT  -- JSON serialized metrics
);
```

#### 4. Machine Learning

**Purpose**: Train and use models to generate predictions from features.

**Implementation**:
```python
# src/models/model_manager.py
class ModelManager:
    """Manage ML models for training and prediction."""
    def __init__(self, config: dict, storage_manager):
        self.config = config
        self.storage = storage_manager
        self.models = {}  # Loaded models
    
    def train_model(self, model_name: str, features: pd.DataFrame, 
                   labels: pd.Series) -> dict:
        """Train a model with the given features and labels."""
        pass
        
    def predict(self, model_name: str, features: pd.DataFrame) -> pd.Series:
        """Generate predictions using the specified model."""
        pass
        
    def evaluate_model(self, model_name: str, test_features: pd.DataFrame,
                      test_labels: pd.Series) -> dict:
        """Evaluate model performance."""
        pass
```

**Key Models**:

1. **Productivity Classifier**
   - Classify activities as productive/unproductive
   - Random Forest Classifier
   - Features: time, application, duration
   - Training: User-labeled activities as ground truth

2. **Work Pattern Analyzer**
   - Identify optimal work times and patterns
   - Gradient Boosting Regressor
   - Features: time, activity type, duration
   - Output: Productivity score prediction

3. **Task Recommender**
   - Suggest next tasks based on context
   - k-Nearest Neighbors
   - Features: current time, recent activities
   - Output: Recommended activity type

#### 5. User Interface

**Purpose**: Provide user interaction, visualization, and configuration.

**Implementation**:
```python
# src/ui/main_window.py
class MainWindow:
    """Main application window."""
    def __init__(self, app_controller):
        self.controller = app_controller
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        pass
        
    def update_dashboard(self, data: dict):
        """Update dashboard with new data and predictions."""
        pass
        
    def show_settings(self):
        """Display settings dialog."""
        pass
```

**Key UI Components**:

1. **Dashboard**
   - Activity summary
   - Productivity insights
   - Recommendations panel

2. **Settings Panel**
   - Data collection configuration
   - Privacy controls
   - Model training options

3. **Feedback System**
   - Accept/reject recommendations
   - Manual activity labeling
   - Model performance feedback

#### 6. Application Core

**Purpose**: Coordinate all components and manage application lifecycle.

**Implementation**:
```python
# src/core/controller.py
class ApplicationController:
    """Main application controller."""
    def __init__(self, config_path: str):
        self.config = self.load_config(config_path)
        self.storage = None
        self.collectors = {}
        self.processors = {}
        self.model_manager = None
        self.ui = None
    
    def initialize(self) -> bool:
        """Initialize all application components."""
        pass
        
    def start(self) -> bool:
        """Start the application."""
        pass
        
    def stop(self) -> bool:
        """Stop the application."""
        pass
```

## Data Flow and Processing

### 1. Collection Flow

```
System Events → Data Collectors → Validation → Storage Layer
```

**Implementation Details**:
- Collectors run as background threads/processes
- Events are batched for efficient storage
- Privacy filters applied at collection time
- Events stored with timestamps for sequential processing

### 2. Processing Flow

```
Raw Events → Feature Extraction → Feature Storage → Model Training → Model Storage
```

**Implementation Details**:
- Processing runs on schedule or trigger
- Features derived from multiple event types
- Sliding window approach for time-series features
- Features versioned with source events

### 3. Prediction Flow

```
Current Context → Feature Extraction → Model Inference → Result Processing → UI Presentation
```

**Implementation Details**:
- Triggered by user login or explicit request
- Uses most recent data and context
- Multiple models may generate different insights
- Results ranked and filtered before presentation

## Configuration System

**Purpose**: Allow customization without code changes.

**Implementation**:
```yaml
# config.yaml example
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
```

## Detailed Roadmap for Implementation

### Phase 1: Foundation (Weeks 1-2)

#### Week 1: Core Infrastructure
1. **Setup project structure**
   - Create directory structure
   - Initialize Git repository
   - Set up virtual environment
   - Add basic dependencies

2. **Implement Storage Layer**
   - Create SQLite database schema
   - Implement StorageManager class
   - Build basic CRUD operations
   - Add unit tests

3. **Configuration System**
   - Implement config file loading
   - Create default configuration
   - Add validation logic

#### Week 2: Basic Data Collection
1. **File System Collector**
   - Implement watchdog-based monitoring
   - Create event filtering
   - Add data normalization
   - Build unit tests

2. **Application Usage Collector**
   - Implement psutil-based app monitoring
   - Create focus detection
   - Add data normalization
   - Build unit tests

3. **Collection Manager**
   - Implement collector lifecycle management
   - Build scheduler for periodic collection
   - Create data validation pipeline
   - Connect collectors to storage

### Phase 2: Processing & Learning (Weeks 3-4)

#### Week 3: Data Processing
1. **Feature Engineering**
   - Implement time-based feature extraction
   - Create activity classification
   - Build feature normalization
   - Add unit tests

2. **Data Pipeline**
   - Create processing workflow
   - Implement batch processing
   - Build incremental processing
   - Connect to storage layer

3. **Data Visualization**
   - Create basic data visualizations
   - Build activity summaries
   - Implement data exploration tools

#### Week 4: Machine Learning
1. **Model Implementation**
   - Create ProductivityClassifier
   - Implement WorkPatternAnalyzer
   - Build TaskRecommender
   - Add unit tests

2. **Training Pipeline**
   - Implement training workflow
   - Create validation framework
   - Build hyperparameter optimization
   - Add model persistence

3. **Prediction Service**
   - Create inference pipeline
   - Implement recommendation generation
   - Build confidence scoring
   - Connect to storage layer

### Phase 3: User Interface (Weeks 5-6)

#### Week 5: Basic UI
1. **Main Application Window**
   - Create PyQt5 main window
   - Implement navigation structure
   - Build settings dialogs
   - Add configuration UI

2. **Dashboard Implementation**
   - Create activity visualization
   - Implement productivity metrics
   - Build recommendation display
   - Add feedback controls

3. **Background Service**
   - Create system tray integration
   - Implement startup behavior
   - Build notification system

#### Week 6: Polish & Integration
1. **Complete Integration**
   - Connect all components
   - Implement end-to-end workflows
   - Build startup sequence
   - Add shutdown logic

2. **Feedback System**
   - Create recommendation feedback
   - Implement model improvement from feedback
   - Build activity labeling interface
   - Add continuous learning

3. **Testing & Refinement**
   - Perform end-to-end testing
   - Optimize performance
   - Refine UI/UX
   - Fix identified issues

### Phase 4: Extensions & Finalization (Week 7)

#### Week 7: Completion
1. **Advanced Features**
   - Implement data export/import
   - Create backup/restore functionality
   - Build model visualization
   - Add advanced configuration options

2. **Documentation**
   - Complete code documentation
   - Create user guide
   - Build API documentation
   - Add configuration reference

3. **Final Testing**
   - Perform security review
   - Test across environments
   - Validate data integrity
   - Verify resource usage

## Testing Strategy

### 1. Unit Testing

Each component should have unit tests covering:
- Core functionality
- Edge cases
- Error handling
- Configuration variations

**Example**:
```python
# tests/collectors/test_file_system_collector.py
def test_file_system_collector_creation():
    """Test creating and initializing a file system collector."""
    config = {"paths": ["~/test"], "events": ["create"]}
    collector = FileSystemCollector(config)
    assert collector.is_running == False
    assert collector.watched_paths == ["~/test"]

def test_file_system_collector_start_stop():
    """Test starting and stopping collection."""
    collector = FileSystemCollector({"paths": ["~/test"]})
    assert collector.start() == True
    assert collector.is_running == True
    assert collector.stop() == True
    assert collector.is_running == False
```

### 2. Integration Testing

Integration tests should verify:
- Component interactions
- Data flow between modules
- End-to-end functionality
- Configuration effects

### 3. Performance Testing

Performance tests should measure:
- Resource usage during collection
- Processing throughput
- Storage efficiency
- UI responsiveness

## Conclusion

This optimized architecture provides a detailed blueprint for implementing a local AI learning framework incrementally. By focusing on concrete implementations, well-defined interfaces, and a modular approach, you can build the system step-by-step with GitHub Copilot assistance.

The framework maintains the original privacy-first approach while providing specific code structures and implementation details that make development straightforward. The weekly roadmap gives a clear path from foundation to completed application.

Start with the storage layer and basic collectors in Phase 1, then progress through each module. Test each component thoroughly before integration, and follow the roadmap to ensure consistent progress.