#define MyAppName "PaddleOCR-json"
#define MyAppVersion "1.4.1"

[Setup]
AppId={{3D35D8FC-65D6-40F9-A087-2D5DB50A0622}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\{#MyAppName}
OutputDir=output
OutputBaseFilename=PaddleOCR-json_setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ChangesEnvironment=yes
CreateAppDir=yes

[Files]
Source: "..\PaddleOCR-json_v1.4.1_windows_x64\PaddleOCR-json_v1.4.1\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Code]
procedure EnvAddPath(Path: string);
var
  Paths: string;
begin
  if RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'Path', Paths) then
  begin
    if Pos(';' + Uppercase(Path) + ';', ';' + Uppercase(Paths) + ';') = 0 then
      RegWriteStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'Path', Paths + ';' + Path);
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then 
    EnvAddPath(ExpandConstant('{app}'));
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  Path, Paths: string;
  P: Integer;
begin
  if (CurUninstallStep = usUninstall) and RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'Path', Paths) then
  begin
    Path := ExpandConstant('{app}');
    P := Pos(';' + Uppercase(Path) + ';', ';' + Uppercase(Paths) + ';');
    if P > 0 then
    begin
      Delete(Paths, P, Length(Path) + 1);
      RegWriteStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'Path', Paths);
    end;
  end;
end; 