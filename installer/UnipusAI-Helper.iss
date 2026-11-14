; =====================================================================
; Inno Setup 6 script for UnipusAI-Helper (Windows installer).
;
; All variant-specific values come from /D defines supplied by
; scripts/build_variant.py, e.g.:
;   ISCC.exe installer\UnipusAI-Helper.iss ^
;     /DAppVersion=3.9.10 /DBuildMode=release ^
;     /DMyAppExe=UnipusAI-Helper.exe /DAppDirName=UnipusAI-Helper ^
;     /DAppId=B7E4A1C2-3D5F-4A68-9B01-2C3D4E5F6A70 ^
;     /DSourceDir=C:\...\dist\UnipusAI-Helper ^
;     /DSetupBaseName=UnipusAI-Helper-Setup-3.9.10-win-x64-release ^
;     /DOutputDir=C:\...\installer
; The #ifndef defaults make the script directly runnable by hand as well.
; =====================================================================

#ifndef AppVersion
  #define AppVersion "3.9.10"
#endif
#ifndef BuildMode
  #define BuildMode "release"
#endif
#ifndef MyAppExe
  #define MyAppExe "UnipusAI-Helper.exe"
#endif
#ifndef AppDirName
  #define AppDirName "UnipusAI-Helper"
#endif
#ifndef AppId
  #define AppId "B7E4A1C2-3D5F-4A68-9B01-2C3D4E5F6A70"
#endif
#ifndef SourceDir
  #define SourceDir "..\dist\UnipusAI-Helper"
#endif
#ifndef SetupBaseName
  #define SetupBaseName "UnipusAI-Helper-Setup"
#endif
#ifndef OutputDir
  #define OutputDir "installer"
#endif

#define MyAppName "UnipusAI-Helper"
#define MyAppPublisher "UnipusAI-Helper Contributors"
#define MyAppURL "https://github.com/jason195421/UnipusAI-Helper/"

[Setup]
AppId={#AppId}
AppName={#MyAppName}
AppVersion={#AppVersion}
AppVerName={#MyAppName} {#AppVersion} ({#BuildMode})
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
VersionInfoVersion={#AppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoProductName={#MyAppName}
VersionInfoProductTextVersion={#AppVersion} ({#BuildMode})

; 用户级安装：不需要管理员权限，安装目录始终可写。冻结后的程序把
; config.json 与 logs/ 写在 exe 同目录，装到 Program Files 会因只读而失败。
DefaultDirName={localappdata}\{#AppDirName}
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
DisableProgramGroupPage=yes
DefaultGroupName={#MyAppName} ({#BuildMode})
DisableDirPage=auto
UsedUserAreasWarning=no

OutputDir={#OutputDir}
OutputBaseFilename={#SetupBaseName}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
ArchitecturesAllowed=x64
UninstallDisplayIcon={app}\{#MyAppExe}
UninstallDisplayName={#MyAppName} {#AppVersion} ({#BuildMode})
CloseApplications=yes
RestartApplications=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName} ({#BuildMode})"; Filename: "{app}\{#MyAppExe}"; WorkingDir: "{app}"
Name: "{autodesktop}\{#MyAppName} ({#BuildMode})"; Filename: "{app}\{#MyAppExe}"; Tasks: desktopicon; WorkingDir: "{app}"

[Run]
Filename: "{app}\{#MyAppExe}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent
