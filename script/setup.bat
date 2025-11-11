@echo off
REM Windows batch script to set up the project

cd /d "%~dp0\.."

REM Check if Gemfile exists and install gem dependencies
if exist "Gemfile" (
  echo ==^> Installing gem dependencies...
  bundle install --no-cache --quiet --without production
  if errorlevel 1 (
    echo Error installing gem dependencies
    exit /b 1
  )
)

REM Update git submodules
git submodule update --init
if errorlevel 1 (
  echo Error updating git submodules
  exit /b 1
)

echo ==^> App is now ready to go!
