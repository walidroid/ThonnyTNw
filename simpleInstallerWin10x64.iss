; Script Inno Setup corrigé pour ThonnySc
; Support pour Python 3.13.3, PyInstaller, et Plugins personnalisés

#define PythonVersion major+"."+minor+"."+patch
#define PythonStrictVersion major+minor

#define arch "amd64"
#define PythonLocalInstallDir "%localappdata%\Programs\Python\Python"+PythonStrictVersion+"\"
#define PythonFullInstallationExe "python-{#PythonVersion}.exe"
#define MyAppName "ThonnySc"
#define MyAppVersion tag
#define MyAppPublisher "Walid Jadla"
#define MyAppURL "https://bacalgo.de"

[Setup]
AppId={{10E0D286-4928-469E-A6F1-F5A213737C86}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
CreateAppDir=no
ChangesAssociations=yes
DefaultGroupName=ThonnyTN
PrivilegesRequiredOverridesAllowed=commandline
OutputBaseFilename={#MyAppName}_{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
LicenseFile=license-for-win-installer.txt

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Components]
Name: "python_installer"; Description: "Python {#PythonVersion}: Ne décocher cette case que si vous voulez utiliser une autre version de python"; Types: full custom;
Name: "editors"; Description: "Editeur Thonny et Plugins (Autocomplétion, Export EXE, French Traceback)"; Types: full compact custom;
Name: "editors\ps_flag_thonny"; Description: "Drapeau Palestinien dans Thonny"; Types: full compact custom;
Name: "editors\thonny_autosave"; Description: "Enregistrement automatique"; Types: full compact custom;
Name: "bac_sc"; Description: "Bibliothèques Scientifiques (PyQt5, Numpy, Designer)"; Types: full compact custom;
Name: "editors\edulint"; Description: "Linter pédagogique (thonny-edulint)"; Types: full compact custom;

; --- AJOUT DE LA SECTION MANQUANTE ---
[Tasks]
Name: "ThonnyDesktopIcon"; Description: "Créer une icône sur le bureau pour Thonny"; Components: "editors"
Name: "DesignerDesktopIcon"; Description: "Créer une icône sur le bureau pour Designer"; Components: "bac_sc"

[Files]
; --- Plugins Thonny ---
; Diagnostic des erreurs en français
Source: "thonny_french_traceback.py"; DestDir: "{localappdata}\Programs\Python\Python{#PythonStrictVersion}\Lib\site-packages\thonny\plugins"; Flags: ignoreversion
; Sélecteur d'interprète (Python 3 / ESP32)
Source: "thonny_quick_switch\__init__.py"; DestDir: "{localappdata}\Programs\Python\Python{#PythonStrictVersion}\Lib\site-packages\thonny\plugins"; DestName: "thonny_quick_switch.py"; Flags: ignoreversion
; Autocomplétion et Snippets
Source: "thonny_simple_autocomplete\*"; DestDir: "{localappdata}\Programs\Python\Python{#PythonStrictVersion}\Lib\site-packages\thonny\plugins\thonny_simple_autocomplete"; Flags: ignoreversion recursesubdirs createallsubdirs
; Exportation en .EXE
Source: "thonny_export_exe\*"; DestDir: "{localappdata}\Programs\Python\Python{#PythonStrictVersion}\Lib\site-packages\thonny\plugins\thonny_export_exe"; Flags: ignoreversion recursesubdirs createallsubdirs

; --- Fichiers système et Dépendances ---
Source: "requirements.txt"; DestDir: "{tmp}"; Flags: ignoreversion 
Source: "python-{#PythonVersion}-{#arch}.exe"; DestDir: "{tmp}"; Flags: ignoreversion; Components: "python_installer"
Source: "RefreshEnv.cmd"; DestDir: "{tmp}";
Source: "depsx64\*.whl"; DestDir: "{tmp}\deps\";
Source: "depsx64\*.tar.gz"; DestDir: "{tmp}\deps\";

[Icons]
Name: "{group}\Thonny"; Filename: "{#PythonLocalInstallDir}\Scripts\thonny.exe"; IconFilename: "{#PythonLocalInstallDir}\Lib\site-packages\thonny\res\thonny.ico"; Components: "editors"
Name: "{group}\QT Designer"; Filename: "{#PythonLocalInstallDir}\Lib\site-packages\PyQt5\Qt5\bin\designer.exe"; Components: "bac_sc"
; Correction de la tâche ici
Name: "{autodesktop}\Thonny"; Filename: "{#PythonLocalInstallDir}\Scripts\thonny.exe"; IconFilename: "{#PythonLocalInstallDir}\Lib\site-packages\thonny\res\thonny.ico"; Tasks: "ThonnyDesktopIcon"
Name: "{autodesktop}\Qt Designer"; Filename: "{#PythonLocalInstallDir}\Scripts\pyqt5_qt5_designer.exe"; IconFilename: "{#PythonLocalInstallDir}\Lib\site-packages\PyQt5\Qt5\bin\Designer.exe"; Tasks: "DesignerDesktopIcon"

[Registry]
Root: HKCU; Subkey: "Environment"; ValueType: string; ValueName: "FRIENDLY_LANGUAGE"; ValueData: "fr"; Flags: preservestringtype

[Run]
; 1. Installation de Python
Filename: "{tmp}\python-{#PythonVersion}-{#arch}.exe"; Parameters: "/passive PrependPath=1 Include_launcher=1"; StatusMsg: "Installation de Python {#PythonVersion}..."; Components: "python_installer"

; 2. Installation groupée via requirements.txt (Thonny, PyInstaller, Numpy, etc.)
Filename: "cmd.exe"; Parameters: "/q /c mode 80,5 && title Installation des composants ... && {tmp}\RefreshEnv.cmd && py.exe -m pip install -r {tmp}\requirements.txt --upgrade --no-index --find-links {tmp}\deps --prefer-binary >> {tmp}\innosetup.log"; StatusMsg: "Installation de Thonny, PyInstaller et des bibliothèques..."; Components: "editors"

; 3. Installation des plugins spécifiques
Filename: "cmd.exe"; Parameters: "/q /c mode 80,5 && title Installation des outils spécifiques ... && {tmp}\RefreshEnv.cmd && py.exe -m pip install thonny-tunisiaschools thonny-autosave --upgrade --no-index --prefer-binary --find-links {tmp}\deps >> {tmp}\innosetup.log"; StatusMsg: "Configuration des plugins Thonny..."; Components: "editors"

[Code]
procedure InitializeWizard;
begin
  WizardForm.LicenseMemo.Font.Name:='Consolas';
end;
