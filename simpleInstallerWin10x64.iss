; Script Inno Setup corrigé pour ThonnySc
; Support pour Python 3.13.3, PyInstaller, et Plugins personnalisés

#define PythonVersion major+"."+minor+"."+patch
#define PythonStrictVersion major+minor

#define arch "amd64"
#define PythonLocalInstallDir "%localappdata%\Programs\Python\Python"+PythonStrictVersion+"\"
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
Name: "python_installer"; Description: "Python {#PythonVersion}: Ne décocher cette case que si vous vouler utiliser une autre version de python"; Types: full  custom;
Name: "editors"; Description: "Editeurs Python(Thonny seulement pour le moment )"; Types: full compact custom;
Name: "editors\ps_flag_thonny"; Description: "Drapeau Palestinian au lieu de Ukranian dans Thonny"; Types: full compact custom;
Name: "editors\thonny_autosave"; Description: "Enregistrer automatiqement dans Thonny"; Types: full compact custom;
Name: "editors\thonny_tunisiaschools" ; Description: "Générer le code PyQt5 dans Thonny / Dossier par défaut(thonny_tunisiaschools)"; Types: full compact custom;
Name: "editors\friendly" ; Description: "Afficher une explication des erreurs dans l'assistant Thonny (thonny_friendly)"; Types: full compact custom;
Name: "bac_sc"; Description: "Bibliothèques pour bac scientifiques / bac informatiques : PyQt5 / Numpy / Designer "; Types: full compact custom;
Name: "editors\edulint"; Description: "Installer thonny-edulint (Linter pédagogique)"; Types: full compact custom;

[Tasks]
Name: "ThonnyDesktopIcon"; Description: "Créer icone bureau pour Thonny"; Components: "editors"
Name: "DesignerDesktopIcon"; Description: "Créer icone bureau pour Designer"; Components: "bac_sc"

[Files]
Source: "thonny_french_traceback.py"; DestDir: "{localappdata}\Programs\Python\Python{#PythonStrictVersion}\Lib\site-packages\thonny\plugins"; Flags: ignoreversion
Source: "thonny_quick_switch\__init__.py"; DestDir: "{localappdata}\Programs\Python\Python{#PythonStrictVersion}\Lib\site-packages\thonny\plugins"; DestName: "thonny_quick_switch.py"; Flags: ignoreversion
Source: "thonny_simple_autocomplete\*"; DestDir: "{localappdata}\Programs\Python\Python{#PythonStrictVersion}\Lib\site-packages\thonny\plugins\thonny_simple_autocomplete"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "thonny_export_exe\*"; DestDir: "{localappdata}\Programs\Python\Python{#PythonStrictVersion}\Lib\site-packages\thonny\plugins\thonny_export_exe"; Flags: ignoreversion recursesubdirs createallsubdirs

; FIX : Copier le fichier requirements.txt pour l'installation groupée
Source: "requirements.txt"; DestDir: "{tmp}"; Flags: ignoreversion

Source: "python-{#PythonVersion}-{#arch}.exe"; DestDir: "{tmp}"; Flags: ignoreversion ; Components: "python_installer"
Source: "RefreshEnv.cmd"; DestDir: "{tmp}";
Source: "depsx64\*.whl" ; DestDir: "{tmp}\deps\";
Source: "depsx64\*.tar.gz" ; DestDir: "{tmp}\deps\";

[Icons]
Name: "{group}\Thonny"; Filename: "{#PythonLocalInstallDir}\Scripts\thonny.exe"; IconFilename: "{#PythonLocalInstallDir}\Lib\site-packages\thonny\res\thonny.ico" ; Components: "editors"
Name: "{group}\QT Designer"; Filename: "{#PythonLocalInstallDir}\Lib\site-packages\PyQt5\Qt5\bin\designer.exe" ; Components: "bac_sc" 
Name: "{autodesktop}\Thonny"; Filename: "{#PythonLocalInstallDir}\Scripts\thonny.exe"; IconFilename: "{#PythonLocalInstallDir}\Lib\site-packages\thonny\res\thonny.ico" ; Tasks: "ThonnyDesktopIcon" 
Name: "{autodesktop}\Qt Designer"; Filename: "{#PythonLocalInstallDir}\Scripts\pyqt5_qt5_designer.exe"; IconFilename: "{#PythonLocalInstallDir}\Lib\site-packages\PyQt5\Qt5\bin\Designer.exe"; Tasks: "DesignerDesktopIcon"

[Registry]
Root: HKCU; Subkey: "Environment"; ValueType: string; ValueName: "FRIENDLY_LANGUAGE"; ValueData: "fr"; Flags: preservestringtype

[Run]
; 1. Installation de Python (inchangé)
Filename: "{tmp}\python-{#PythonVersion}-{#arch}.exe"; Parameters: "/passive PrependPath=1 Include_launcher=1"; StatusMsg: "Installation de Python {#PythonVersion}..."; Components: "python_installer"

; 2. NOUVELLE MÉTHODE : Installation forcée via le chemin absolu
; On utilise {localappdata}\Programs\Python\Python{#PythonStrictVersion}\python.exe pour être certain de l'environnement
Filename: "{localappdata}\Programs\Python\Python{#PythonStrictVersion}\python.exe"; \
    Parameters: "-m pip install pyinstaller thonny numpy pyqt5_qt5_designer --upgrade --no-index --find-links {tmp}\deps --prefer-binary"; \
    StatusMsg: "Installation de PyInstaller et des bibliothèques (Mode Forcé)..."; \
    Components: "editors"

; 3. Installation des plugins spécifiques restants
Filename: "cmd.exe"; \
    Parameters: "/q /c mode 80,5 && {tmp}\RefreshEnv.cmd && py.exe -m pip install thonny_palestine_flag thonny-autosave thonny-tunisiaschools --upgrade --no-index --prefer-binary --find-links {tmp}\deps >> {tmp}\innosetup.log"; \
    StatusMsg: "Configuration finale des plugins..."; \
    Components: "editors"

[Code]
procedure InitializeWizard;
begin
  WizardForm.LicenseMemo.Font.Name:='Consolas'
end;

