; Inno Setup script for the Windows installer.
; Build:  ISCC /DAppVersion=0.1.0 installer\windows\Diode110.iss
; (paths are relative to this file; expects a Release build in ..\..\build)

#ifndef AppVersion
  #define AppVersion "0.0.0"
#endif

#define Artefacts "..\..\build\Diode110_artefacts\Release"

[Setup]
AppId={{4B8E1F27-9D3C-4A65-B0E2-6C17F5A93D48}
AppName=Diode 110
AppVersion={#AppVersion}
AppVerName=Diode 110 {#AppVersion}
AppPublisher=Transistor Labs
DefaultDirName={autopf}\Transistor Labs\Diode 110
DefaultGroupName=Transistor Labs
DisableDirPage=yes
DisableProgramGroupPage=yes
OutputDir=..\..\dist
OutputBaseFilename=Diode110-{#AppVersion}-Windows-Setup
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
UninstallDisplayName=Diode 110

[Types]
Name: "full";   Description: "VST3 plug-in and standalone app"
Name: "custom"; Description: "Choose components"; Flags: iscustom

[Components]
Name: "vst3"; Description: "VST3 plug-in (Ableton Live, Bitwig, Reaper, Cubase...)"; Types: full custom
Name: "app";  Description: "Standalone app";                                         Types: full custom

[Files]
Source: "{#Artefacts}\VST3\Diode 110.vst3\*"; DestDir: "{commoncf64}\VST3\Diode 110.vst3"; Components: vst3; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#Artefacts}\Standalone\Diode 110.exe"; DestDir: "{app}"; Components: app; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\Diode 110"; Filename: "{app}\Diode 110.exe"; Components: app

[Messages]
FinishedLabel=Diode 110 is installed.%n%nRescan plug-ins in your DAW (Ableton Live: Settings > Plug-Ins > Rescan).
