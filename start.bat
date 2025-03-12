@echo off
:start
::Server name [!EDIT THIS!]
set serverName=EXAMPLE NAME
::Server files location [DEFAULT !EDIT AS NEEDED!]
set serverDirectory="C:\Program Files (x86)\Steam\steamapps\common\DayZServer\"
::Server Port [DEFAULT]
set serverPort=2302
::Server config [DEFAULT. hostname= in serverDZ.cfg is what shows in the steam server browser. !EDIT AS NEEDED!.]
set serverConfig=serverDZ.cfg
::Server profile location. logfiles are written here and mods are configured here [DEFAULT]
set serverProfile=profiles
::Logical CPU cores to use (Equal or less than available)
set serverCPU=2
::modlist should be of the form "-mod=@CF;@SchanaModCompass;@BMW_M5_CS;@VPPAdminTools;@CannabisPlus;@Cl0ud's Military Gear;@Advanced Weapon Scopes"
set modList="-mod=@CF;@SchanaModCompass;@BMW_M5_CS;@VPPAdminTools;@CannabisPlus;@Cl0ud's Military Gear;@Advanced Weapon Scopes"
::Sets title for terminal (DONT edit)
title %serverName% batch
::DayZServer location (DONT edit)
cd /D "%serverDirectory%"
:: makes the profile directory if it doesn't already exist
if not exist "%serverProfile%" ( 
mkdir %serverProfile% > nul
) 
echo (%time%) %serverName% started.
::Launch parameters (edit end: -config=|-port=|-profiles=|-doLogs|-adminLog|-netLog|-freezeCheck|-filePatching|-BEpath=|-cpuCount=)
start "DayZ Server" /min DayZServer_x64.exe -config=%serverConfig% -port=%serverPort% -profiles=%serverProfile% -BEpath=battleye %modList% -cpuCount=%serverCPU% -dologs -adminlog -netlog -freezecheck

::Time in seconds before kill server process (14400 = 4 hours)
timeout 14400
taskkill /im DayZServer_x64.exe /F
::Time in seconds to wait before..
timeout 10
::Go back to the top and repeat the whole cycle again
goto start