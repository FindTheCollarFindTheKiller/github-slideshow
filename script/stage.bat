@echo off
REM Windows batch script to stage the site to GitHub Pages

setlocal

set account=training-staging

if "%1"=="" (
  set repo=caption-this
) else (
  set repo=%1
)

REM Build the site
echo.
echo # Building site...
echo --------------------------------------------------
set DISABLE_WHITELIST=1
bundle exec jekyll build --baseurl "/%account%/%repo%"
if errorlevel 1 (
  echo Build failed
  exit /b 1
)

REM Create a temp Git repo to push from
echo.
echo # Creating a temp Git repo...
echo --------------------------------------------------
cd _site
git init
if errorlevel 1 exit /b 1

git remote add staging https://ghe.io/%account%/%repo%.git
if errorlevel 1 exit /b 1

git add .
if errorlevel 1 exit /b 1

git commit -m "Staging latest changes"
if errorlevel 1 exit /b 1

REM Push the site
echo.
echo # Publishing...
echo --------------------------------------------------
git push staging master:gh-pages --force
if errorlevel 1 exit /b 1

git remote rm staging

REM Celebrate and open the staging site
echo.
echo # Success!
start https://pages.ghe.io/%account%/%repo%/

endlocal
