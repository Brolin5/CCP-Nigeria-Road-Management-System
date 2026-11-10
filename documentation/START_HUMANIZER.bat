@echo off
cd /d "C:\Users\ACER\Desktop\Report"
echo =======================================================
echo   STARTING AUTONOMOUS MULTI-BATCH HUMANIZER
echo =======================================================
echo Make sure your Chrome window with StealthWriter is visible.
echo.
python humanize_all_batches.py
pause
