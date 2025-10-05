# Security & Privacy Policy

## Overview

The AI Local Learning Framework is built with privacy and security as foundational principles. This document outlines our approach to ensuring your data remains private, secure, and under your control at all times.

## Core Privacy Principles

### 1. Local-Only Processing

- **No Cloud Dependencies**: All data collection, processing, and storage happens exclusively on your local device
- **No Data Transmission**: The application does not transmit any of your data over networks
- **Offline Operation**: The system functions fully when disconnected from the internet

### 2. Data Minimization

- **Configurable Collection**: Only collect the specific data types you explicitly enable
- **Data Pruning**: Automatic removal of raw data after processing into features
- **Retention Limits**: Configurable retention periods with default limits

### 3. User Control

- **Transparent Collection**: Clear visibility into what data is being collected
- **Easy Opt-Out**: Disable specific collectors or the entire system at any time
- **Data Deletion**: Simple mechanisms to delete all or portions of collected data

## Data Security Measures

### Storage Security

- **Local Database**: All data is stored in a local SQLite database
- **Path Isolation**: Database stored in user-specific directories with appropriate permissions
- **No External Access**: Database connection is only available to the application

### File System Security

- **Secure Paths**: Monitored paths configurable to exclude sensitive directories
- **Access Controls**: Relies on operating system access controls for file security
- **Path Anonymization**: Option to anonymize collected file paths

### Application Security

- **Limited Privileges**: Application runs with minimal required system privileges
- **No Remote Code**: No downloading or execution of remote code
- **Dependency Security**: Regular updates of dependencies to address vulnerabilities

## Data Collection Details

### What is Collected

When enabled, the framework can collect:

1. **File System Events**
   - File creation, modification, deletion events
   - File paths, types, and sizes
   - No file contents are ever collected

2. **Application Usage**
   - Active application names
   - Window focus duration
   - Window titles (optional, disabled by default)

3. **System Activity**
   - CPU and memory usage
   - System state (active, idle, etc.)
   - No personally identifiable information

### What is NOT Collected

The framework explicitly does NOT collect:

- File contents
- Personally identifiable information
- Credentials or passwords
- Browser history or form data
- Email or message contents
- Network activity or connection data

## Configuration Privacy Options

The configuration file (`config/config.yaml`) includes the following privacy controls:

```yaml
privacy:
  # Data retention period in days (0 = keep indefinitely)
  data_retention_days: 90
  
  # Whether to anonymize file paths
  anonymize_paths: true
  
  # Whether to collect window titles (off by default)
  collect_window_titles: false
  
  # Paths to exclude from monitoring
  exclude_paths:
    - "~/Documents/Personal"
    - "~/Financial"
    - "~/.ssh"
    - "~/.gnupg"
    - "~/.password-store"
```

## Security Best Practices for Users

1. **Review Configuration**: Review and adjust the privacy settings before first use
2. **Regular Purging**: Use the built-in data purging features periodically
3. **Exclude Sensitive Paths**: Add any sensitive directories to the exclude_paths list
4. **Keep Updated**: Apply application updates to receive security improvements
5. **Limit Access**: Ensure your computer account has appropriate password protection

## Reporting Security Issues

If you discover a security vulnerability or have concerns about privacy in this application, please report it by:

1. Opening an issue on the GitHub repository
2. Marking the issue with the "security" label
3. Providing sufficient detail to understand and reproduce the issue

For sensitive security issues, please contact the repository owner directly.

## Security Updates

Security patches will be released promptly as issues are identified. Updates will be documented in the repository's release notes.

## Compliance

This application is designed with privacy regulations like GDPR and CCPA in mind, emphasizing:

- Data minimization
- Purpose limitation
- Storage limitation
- User control over personal data

## Conclusion

The AI Local Learning Framework takes a "privacy by design" approach. By processing all data locally and providing comprehensive user controls, we ensure that your personal information and activity data remain private, secure, and under your complete control.