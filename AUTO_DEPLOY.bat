@echo off
REM ═══════════════════════════════════════════════════════════
REM  DMCAShield Auto-Deploy Script
REM  Syncs local changes → GitHub → Netlify + Vercel auto-deploy
REM  Usage: Just double-click this file after making changes!
REM ═══════════════════════════════════════════════════════════

echo.
echo  ╔═══════════════════════════════════════════════╗
echo  ║  DMCAShield Auto-Deploy                       ║
echo  ║  Syncing to GitHub → Netlify + Vercel         ║
echo  ╚═══════════════════════════════════════════════╝
echo.

REM Step 1: Sync premium frontend from dmcashield to dmcashield-agency
echo [1/5] Syncing premium frontend...
xcopy /E /Y /Q "F:\Anti gravity projects\Dmca company\dmcashield\frontend\src\pages\*" "F:\Anti gravity projects\Dmca company\dmcashield-agency\frontend\src\pages\"
xcopy /E /Y /Q "F:\Anti gravity projects\Dmca company\dmcashield\frontend\src\components\*" "F:\Anti gravity projects\Dmca company\dmcashield-agency\frontend\src\components\"
xcopy /E /Y /Q "F:\Anti gravity projects\Dmca company\dmcashield\frontend\src\styles\*" "F:\Anti gravity projects\Dmca company\dmcashield-agency\frontend\src\styles\"
xcopy /E /Y /Q "F:\Anti gravity projects\Dmca company\dmcashield\frontend\src\config\*" "F:\Anti gravity projects\Dmca company\dmcashield-agency\frontend\src\config\"
echo    Done!

REM Step 2: Stage all changes
echo [2/5] Staging changes...
cd /d "F:\Anti gravity projects\Dmca company\dmcashield-agency"
git add -A
echo    Done!

REM Step 3: Commit with timestamp
echo [3/5] Committing...
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "timestamp=%dt:~0,4%-%dt:~4,2%-%dt:~6,2% %dt:~8,2%:%dt:~10,2%"
git commit -m "auto-deploy: %timestamp% - synced latest changes"
echo    Done!

REM Step 4: Push to GitHub (both branches for Vercel + Netlify)
echo [4/5] Pushing to GitHub...
git push origin master
git push origin master:main
echo    Done!

REM Step 5: Verify
echo [5/5] Deployment triggered!
echo.
echo  ✅ GitHub: https://github.com/afk6216534/dmcashield-agency
echo  ✅ Netlify (frontend): https://dmcashield.netlify.app
echo  ✅ Vercel (backend):   https://dmcashield-agency.vercel.app
echo.
echo  Both sites will auto-update in 2-5 minutes.
echo.
pause
