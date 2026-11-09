' ==============================================================================
' Post-installation Silencieuse - Curriculum Vitae Studio (Osiris Edition)
' ==============================================================================
Option Explicit

Dim WshShell, fso, scriptDir, desktopDir, shortcut, iconPath, programsDir, cvFolder

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
iconPath = scriptDir & "\cv_icon.ico"

' 1. Creation du raccourci sur le Bureau
On Error Resume Next
desktopDir = WshShell.SpecialFolders("Desktop")
If desktopDir <> "" Then
    Set shortcut = WshShell.CreateShortcut(desktopDir & "\Curriculum Vitae Studio.lnk")
    shortcut.TargetPath = "wscript.exe"
    shortcut.Arguments = "//B //nologo " & chr(34) & scriptDir & "\run_silent.vbs" & chr(34)
    shortcut.WorkingDirectory = scriptDir
    If fso.FileExists(iconPath) Then
        shortcut.IconLocation = iconPath & ",0"
    End If
    shortcut.Description = "Curriculum Vitae Studio (Osiris Edition)"
    shortcut.Save
End If

' 2. Creation du raccourci dans le Menu Demarrer
programsDir = WshShell.SpecialFolders("Programs")
If programsDir <> "" Then
    cvFolder = programsDir & "\Curriculum Vitae Studio"
    If Not fso.FolderExists(cvFolder) Then fso.CreateFolder(cvFolder)
    Set shortcut = WshShell.CreateShortcut(cvFolder & "\Curriculum Vitae Studio.lnk")
    shortcut.TargetPath = "wscript.exe"
    shortcut.Arguments = "//B //nologo " & chr(34) & scriptDir & "\run_silent.vbs" & chr(34)
    shortcut.WorkingDirectory = scriptDir
    If fso.FileExists(iconPath) Then
        shortcut.IconLocation = iconPath & ",0"
    End If
    shortcut.Description = "Curriculum Vitae Studio (Osiris Edition)"
    shortcut.Save
End If
On Error GoTo 0

' 3. Lancement automatique de l'application
WshShell.CurrentDirectory = scriptDir
WshShell.Run "wscript.exe //B //nologo " & chr(34) & scriptDir & "\run_silent.vbs" & chr(34), 0, False
