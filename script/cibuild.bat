@echo off
REM Windows batch script to build and test the site

bundle exec jekyll build --baseurl "."
if errorlevel 1 exit /b 1

htmlproofer _site/index.html --empty-alt-ignore
if errorlevel 1 exit /b 1
