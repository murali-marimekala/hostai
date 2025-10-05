# AI Personal Productivity Assistant

An intelligent, offline AI application that learns from your laptop activity to provide personalized work recommendations and productivity insights.

## Features

- **Offline Learning**: Trains AI models locally on your machine
- **Activity Monitoring**: Tracks file usage, application patterns, and work habits
- **Smart Recommendations**: Suggests optimal tasks and work schedules
- **Privacy-First**: All data stays on your device
- **Cross-Platform**: Works on macOS, Windows, and Linux

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-productivity-assistant.git
cd ai-productivity-assistant
```

2. Run the setup script:
```bash
./setup.sh
```

3. Edit your privacy configuration:
```bash
nano ~/.ai_productivity_assistant/config/user_config.yaml
```

4. Run the application:
```bash
python3 src/main.py
```

## Architecture

This application follows a modular architecture with the following components:

- **Data Collection**: Monitors system activity and file usage
- **Data Processing**: Cleans and transforms raw activity data
- **Machine Learning**: Trains models on user patterns
- **Recommendation Engine**: Generates personalized suggestions
- **User Interface**: Provides intuitive access to insights

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed technical documentation.

## 🔒 Security & Privacy

This application is designed with privacy as the highest priority:

- **Local-only processing**: No data ever leaves your device
- **Configurable privacy controls**: Customize what data is collected
- **Automatic data cleanup**: Old data is regularly purged
- **Transparent operation**: Clear visibility into all data collection

For detailed security information, see [SECURITY.md](SECURITY.md).

## 🚀 Making Your Project Available on GitHub

### Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click "New repository"
3. Name it `ai-productivity-assistant`
4. **Important**: Initialize with a README (we'll replace it)
5. **Do NOT** add .gitignore (we have a custom one)

### Step 2: Push Your Code Safely

```bash
# Add all safe files to git
git add .

# Verify what will be committed (should NOT include sensitive files)
git status

# If sensitive files appear, check .gitignore and remove them
git reset HEAD sensitive_file.db

# Commit the safe files
git commit -m "Initial commit: AI Personal Productivity Assistant"

# Add your GitHub repository as remote
git remote add origin https://github.com/yourusername/ai-productivity-assistant.git

# Push to GitHub
git push -u origin main
```

### Step 3: Verify Security

Run these checks to ensure no sensitive data was committed:

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