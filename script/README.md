# Script Directory

This directory contains scripts for setting up, building, and running the GitHub Slideshow application.

## Available Scripts

### Unix/Linux/macOS (Shell Scripts)

- **setup** - Set up the project environment and install dependencies
- **server** - Start the Jekyll server to view the slideshow locally
- **cibuild** - Build and test the site (used in CI/CD)
- **stage** - Deploy the site to a staging environment

### Windows (Batch Scripts)

- **setup.bat** - Set up the project environment and install dependencies
- **server.bat** - Start the Jekyll server to view the slideshow locally
- **cibuild.bat** - Build and test the site (used in CI/CD)
- **stage.bat** - Deploy the site to a staging environment

## Usage

### On Unix/Linux/macOS

```bash
# Setup the project
./script/setup

# Start the server
./script/server

# Build and test
./script/cibuild

# Deploy to staging
./script/stage [repo-name]
```

### On Windows

```cmd
REM Setup the project
script\setup.bat

REM Start the server
script\server.bat

REM Build and test
script\cibuild.bat

REM Deploy to staging
script\stage.bat [repo-name]
```

## Prerequisites

### All Platforms
- Git
- Ruby (with Bundler)
- Jekyll

### Windows-Specific
- Ensure Ruby and Git are in your PATH
- Run scripts from the repository root directory
- Some scripts may require Git Bash or WSL for full functionality

## Notes

- The Windows batch scripts provide equivalent functionality to the Unix shell scripts
- The `stage.bat` script is designed for GitHub Enterprise staging environments
- All scripts should be run from the repository root directory
