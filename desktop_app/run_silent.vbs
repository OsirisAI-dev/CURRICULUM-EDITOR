' ==============================================================================
' Lanceur Intelligent & Silencieux - Curriculum Vitae Studio
' - Compatible Windows 7 SP1, Windows 8, Windows 8.1, Windows 10, Windows 11 (32/64-bit)
' - Mode 0-flicker (aucun écran noir console)
' - Si offline_runtime.exe est présent et que runtime\ n'est pas extrait, extraction silencieuse
' - Détection et exécution automatique de pythonw.exe
' - Secours automatique : si aucun environnement Python n'est disponible, ouverture
'   instantanée de la version Web Studio (100% autonome, zéro dépendance) dans le navigateur.
' ==============================================================================
Option Explicit

Dim WshShell, fso, scriptDir, localPyW, localPy, offlinePkg, sysPy, sysPyW, rc
Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = scriptDir

localPyW = scriptDir & "\runtime\pythonw.exe"
localPy  = scriptDir & "\runtime\python.exe"
offlinePkg = scriptDir & "\offline_runtime.exe"

Function IsValidPythonExe(pyPath)
    IsValidPythonExe = False
    On Error Resume Next
    If pyPath = "" Then Exit Function
    If Not fso.FileExists(pyPath) Then Exit Function
    If InStr(1, LCase(pyPath), "\windowsapps\", vbTextCompare) > 0 Then Exit Function
    If fso.GetFile(pyPath).Size < 10240 Then Exit Function
    IsValidPythonExe = True
    On Error GoTo 0
End Function

Function FindSystemPython()
    FindSystemPython = ""
    On Error Resume Next
    Dim execObj, line, localAppData, progFiles, progFiles86, subDir, cand
    Set execObj = WshShell.Exec("cmd.exe /c where python.exe 2>nul")
    Do While Not execObj.StdOut.AtEndOfStream
        line = Trim(execObj.StdOut.ReadLine())
        If IsValidPythonExe(line) Then
            FindSystemPython = line
            Exit Function
        End If
    Loop

    localAppData = WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%")
    progFiles = WshShell.ExpandEnvironmentStrings("%ProgramFiles%")
    progFiles86 = WshShell.ExpandEnvironmentStrings("%ProgramFiles(x86)%")

    Dim searchRoots(4), rIdx
    searchRoots(0) = localAppData & "\Programs\Python"
    searchRoots(1) = localAppData & "\Python"
    searchRoots(2) = progFiles
    searchRoots(3) = progFiles86
    searchRoots(4) = "C:\"

    For rIdx = 0 To 4
        If fso.FolderExists(searchRoots(rIdx)) Then
            For Each subDir In fso.GetFolder(searchRoots(rIdx)).SubFolders
                If Left(LCase(subDir.Name), 6) = "python" Then
                    cand = subDir.Path & "\python.exe"
                    If IsValidPythonExe(cand) Then
                        FindSystemPython = cand
                        Exit Function
                    End If
                End If
            Next
        End If
    Next
    On Error GoTo 0
End Function

Function CheckPythonFullReady(pyExe)
    CheckPythonFullReady = False
    On Error Resume Next
    If Not IsValidPythonExe(pyExe) Then Exit Function
    Dim cmd, code
    cmd = chr(34) & pyExe & chr(34) & " -c " & chr(34) & "import sys; assert sys.version_info >= (3,8); import tkinter, customtkinter, PIL, docx, reportlab, pypdf" & chr(34)
    code = WshShell.Run(cmd, 0, True)
    If Err.Number = 0 And code = 0 Then
        CheckPythonFullReady = True
    End If
    On Error GoTo 0
End Function

' 1. Si le runtime autonome local est déjà extrait et prêt
If fso.FileExists(localPyW) Then
    If fso.FileExists(offlinePkg) Then
        On Error Resume Next
        fso.DeleteFile offlinePkg, True
        On Error GoTo 0
    End If
    WshShell.Run chr(34) & localPyW & chr(34) & " " & chr(34) & scriptDir & "\cv_editor_ui.py" & chr(34), 0, False
    WScript.Quit 0
End If

' 2. Si le pack hors-ligne est présent (Setup Complet), extraction automatique
If fso.FileExists(offlinePkg) Then
    rc = WshShell.Run(chr(34) & offlinePkg & chr(34) & " -s", 0, True)
    If fso.FileExists(localPyW) Then
        On Error Resume Next
        fso.DeleteFile offlinePkg, True
        On Error GoTo 0
        WshShell.Run chr(34) & localPyW & chr(34) & " " & chr(34) & scriptDir & "\cv_editor_ui.py" & chr(34), 0, False
        WScript.Quit 0
    End If
End If

' 3. Vérifier si Python système est prêt
sysPy = FindSystemPython()
If sysPy <> "" Then
    If CheckPythonFullReady(sysPy) Then
        sysPyW = fso.GetParentFolderName(sysPy) & "\pythonw.exe"
        If Not fso.FileExists(sysPyW) Then sysPyW = sysPy
        WshShell.Run chr(34) & sysPyW & chr(34) & " " & chr(34) & scriptDir & "\cv_editor_ui.py" & chr(34), 0, False
        WScript.Quit 0
    Else
        ' Tenter d'installer les dépendances manquantes si pip disponible
        WshShell.Run chr(34) & sysPy & chr(34) & " -m pip install -r " & chr(34) & scriptDir & "\requirements.txt" & chr(34) & " --quiet", 0, True
        If CheckPythonFullReady(sysPy) Then
            sysPyW = fso.GetParentFolderName(sysPy) & "\pythonw.exe"
            If Not fso.FileExists(sysPyW) Then sysPyW = sysPy
            WshShell.Run chr(34) & sysPyW & chr(34) & " " & chr(34) & scriptDir & "\cv_editor_ui.py" & chr(34), 0, False
            WScript.Quit 0
        End If
    End If
End If

' 4. Secours automatique transparent : lancer la version Web Studio (0 dépendance !)
If fso.FileExists(scriptDir & "\web_version\index.html") Then
    WshShell.Run chr(34) & scriptDir & "\web_version\index.html" & chr(34), 1, False
    WScript.Quit 0
End If

' 5. Si aucun composant disponible
MsgBox "Impossible d'initialiser l'application. Veuillez exécuter l'installateur complet.", vbCritical, "Curriculum Vitae Studio"
WScript.Quit 1
