@echo off
setlocal EnableExtensions

REM Auto-detect selenium-server jar (place it in project root or in scripts\)
set "SELENIUM_JAR="
for %%F in ("%~dp0selenium-server-*.jar") do set "SELENIUM_JAR=%%~fF"
if not defined SELENIUM_JAR (
	for %%F in ("%~dp0..\selenium-server-*.jar") do set "SELENIUM_JAR=%%~fF"
)

if not defined SELENIUM_JAR (
	echo ERROR: selenium-server-*.jar not found.
	echo Put selenium-server-4.x.x.jar into project root or scripts\ folder.
	exit /b 1
)

echo Using: %SELENIUM_JAR%
java -jar "%SELENIUM_JAR%" hub
pause
