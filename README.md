# AI Local Learning Framework

A privacy-focused AI framework that learns from local machine activity to help you be more productive.

## Overview

The AI Local Learning Framework is an application that:

1. **Learns from your local machine activity** (file system, application usage)
2. **Processes all data locally** with no cloud dependencies
3. **Helps identify productivity patterns** and provides recommendations
4. **Respects your privacy** by keeping all data on your device

## Features

- **Local Data Collection**: Monitor file system activity and application usage
- **Machine Learning**: Identify productivity patterns and work habits
- **Personalized Recommendations**: Get suggestions for improving productivity
- **Complete Privacy**: All processing happens on your device, no data sharing
- **Modular Architecture**: Easily extendable with new data sources or models

## Architecture

This project follows a carefully designed modular architecture, allowing components to be developed and tested independently:

- **Data Collectors**: Gather system events and activity data
- **Data Processing**: Transform raw data into ML features
- **Storage**: Persist data and models locally
- **Machine Learning**: Train models and generate predictions
- **User Interface**: Visualize insights and present recommendations

For more details, see [OPTIMIZED_ARCHITECTURE.md](OPTIMIZED_ARCHITECTURE.md).

## Getting Started

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/murali-marimekala/hostai.git
cd hostai

# Initialize the project structure
./initialize_project.py

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Development Process

Follow the development roadmap in [DEVELOPMENT_ROADMAP.md](DEVELOPMENT_ROADMAP.md) for step-by-step implementation instructions.

For implementation guidance, see [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md).

## Tech Stack

- **Python 3.8+**: Core programming language
- **scikit-learn**: Machine learning framework
- **SQLite**: Local data storage
- **Watchdog**: File system monitoring
- **psutil**: System and application monitoring
- **PyQt5**: User interface
- **pandas/numpy**: Data processing

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```bash
# Check for sensitive files on GitHub
git ls-files | grep -E "\.(db|sqlite|pkl|h5|log)$"

# Check for sensitive patterns
git grep -i "password\|secret\|key\|token" -- "*.py" "*.yaml" "*.md"
```

### Step 4: Set Up Repository Settings

1. **Enable branch protection**:
   - Go to Settings → Branches
   - Add rule for `main` branch
   - Require pull request reviews
   - Require status checks to pass

2. **Add repository topics**:
   - productivity
   - ai
   - machine-learning
   - privacy
   - python

3. **Add repository description**:
   ```
   AI-powered personal productivity assistant that learns from your activity patterns to provide intelligent work recommendations. Privacy-first, offline operation.
   ```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### For Contributors

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes following security guidelines
4. Run tests: `pytest`
5. Submit a pull request

## 📋 Development

### Project Structure

```
src/
├── config/           # Configuration management
├── data_collection/  # Activity monitoring
├── data_processing/  # Data cleaning and feature engineering
├── machine_learning/ # Model training and inference
├── recommendation_engine/ # Recommendation generation
├── ui/              # User interface components
└── utils/           # Utility functions

tests/               # Unit and integration tests
docs/               # Documentation
```

### Running Tests

```bash
python -m pytest tests/
```

## 📄 Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture and design
- [SECURITY.md](SECURITY.md) - Security and privacy guidelines
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

## 🔄 CI/CD

This project uses GitHub Actions for continuous integration:

- **Security checks**: Prevents sensitive data commits
- **Code quality**: Linting, formatting, and security scanning
- **Testing**: Automated test execution
- **Building**: Package building and distribution

## 📊 Status

- **Current Phase**: Architecture and Security Setup
- **Next Phase**: Core data collection implementation

## ⚖️ License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

**Privacy Notice**: This software processes data locally on your device only. See [SECURITY.md](SECURITY.md) for privacy information.

## 🙋 Support

- **Issues**: Use GitHub Issues for bugs and feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Security**: See [SECURITY.md](SECURITY.md) for security-related concerns

## 🗺️ Roadmap

- [ ] Basic activity monitoring
- [ ] Initial ML model implementation
- [ ] User interface development
- [ ] Advanced recommendation algorithms
- [ ] Cross-platform packaging
- [ ] Performance optimizations

---

**Built with privacy and security in mind** 🔒✨