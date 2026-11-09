import os
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

RAR = r"C:\Program Files\WinRAR\Rar.exe"
REPO_ROOT = Path(r"C:\Users\PC MARKET\Documents\GitHub\CURRICULUM-EDITOR")
DESKTOP_APP = REPO_ROOT / "desktop_app"
DEST_DIR = Path(r"F:\CV_MAKER")

assert os.path.exists(RAR), "WinRAR Rar.exe not found"
DEST_DIR.mkdir(parents=True, exist_ok=True)

# 1. Prepare web_version inside desktop_app
web_ver_dir = DESKTOP_APP / "web_version"
if web_ver_dir.exists():
    shutil.rmtree(web_ver_dir)
web_ver_dir.mkdir(parents=True, exist_ok=True)

shutil.copyfile(REPO_ROOT / "index.html", web_ver_dir / "index.html")
shutil.copytree(REPO_ROOT / "css", web_ver_dir / "css")
shutil.copytree(REPO_ROOT / "js", web_ver_dir / "js")
shutil.copytree(REPO_ROOT / "assets", web_ver_dir / "assets")
print("[OK] Synchronized web_version into desktop_app.")

# 2. Build Installateur_CV_Maker_Leger.exe
print("\n--- Building Installateur_CV_Maker_Leger.exe ---")
out_leger = DEST_DIR / "Installateur_CV_Maker_Leger.exe"
tmp_leger = DESKTOP_APP / "tmp_leger.exe"
if tmp_leger.exists():
    tmp_leger.unlink()

cmd_leger = [
    RAR, "a", "-sfx",
    "-zsfx_config_leger.txt",
    "-iiconcv_icon.ico",
    "-m5", "-r", "-y",
    "-x*\\__pycache__\\*",
    "-x*.pyc",
    "-xoffline_runtime.exe",
    "-xSetup_*.exe",
    "-xtmp_*.exe",
    "-x*.rar",
    "-x*.zip",
    "-x*.lnk",
    "-xbuild_*.py",
    "-xcreate_*.py",
    str(tmp_leger),
    "cv_docx_gen.py", "cv_editor_ui.py", "cv_html_gen.py", "cv_icon.ico",
    "cv_icons.py", "cv_models.py", "cv_pdf_gen.py", "cv_translations.py",
    "LANCER_CV_EDITOR.bat", "post_install_generic.vbs", "post_install.vbs",
    "requirements.txt", "run_silent.vbs", "web_version"
]

res = subprocess.run(cmd_leger, cwd=DESKTOP_APP, capture_output=True, text=True)
if tmp_leger.exists():
    if out_leger.exists():
        out_leger.unlink()
    shutil.move(str(tmp_leger), str(out_leger))
    print(f"[OK] Installateur_CV_Maker_Leger.exe generated: {out_leger.stat().st_size:,} bytes")
else:
    print("[ERROR] Failed to build Leger installer:")
    print(res.stderr or res.stdout)
    exit(1)

# 3. Build Installateur_CV_Maker_Complet.exe (Including offline_runtime.exe)
print("\n--- Building Installateur_CV_Maker_Complet.exe ---")
out_complet = DEST_DIR / "Installateur_CV_Maker_Complet.exe"
tmp_complet = DESKTOP_APP / "tmp_complet.exe"
if tmp_complet.exists():
    tmp_complet.unlink()

cmd_complet = [
    RAR, "a", "-sfx",
    "-zsfx_config_complet.txt",
    "-iiconcv_icon.ico",
    "-m5", "-r", "-y",
    "-x*\\__pycache__\\*",
    "-x*.pyc",
    "-xSetup_*.exe",
    "-xtmp_*.exe",
    "-x*.rar",
    "-x*.zip",
    "-x*.lnk",
    "-xbuild_*.py",
    "-xcreate_*.py",
    str(tmp_complet),
    "cv_docx_gen.py", "cv_editor_ui.py", "cv_html_gen.py", "cv_icon.ico",
    "cv_icons.py", "cv_models.py", "cv_pdf_gen.py", "cv_translations.py",
    "LANCER_CV_EDITOR.bat", "offline_runtime.exe", "post_install_generic.vbs",
    "post_install.vbs", "requirements.txt", "run_silent.vbs", "web_version"
]

res = subprocess.run(cmd_complet, cwd=DESKTOP_APP, capture_output=True, text=True)
if tmp_complet.exists():
    if out_complet.exists():
        out_complet.unlink()
    shutil.move(str(tmp_complet), str(out_complet))
    print(f"[OK] Installateur_CV_Maker_Complet.exe generated: {out_complet.stat().st_size:,} bytes")
else:
    print("[ERROR] Failed to build Complet installer:")
    print(res.stderr or res.stdout)
    exit(1)

# 4. Build ADMIN_BACKUP_CV_MAKER_FULL_20261109.rar
print("\n--- Building ADMIN_BACKUP_CV_MAKER_FULL_20261109.rar ---")
today_str = datetime.now().strftime("%Y%m%d")
backup_rar_name = f"ADMIN_BACKUP_CV_MAKER_FULL_{today_str}.rar"
out_backup = DEST_DIR / backup_rar_name
tmp_backup = REPO_ROOT / f"tmp_{backup_rar_name}"
if tmp_backup.exists():
    tmp_backup.unlink()

cmd_backup = [
    RAR, "a", "-m5", "-r", "-rr5p", "-y",
    "-x*\\__pycache__\\*",
    "-x*.pyc",
    "-x*.rar",
    "-x*.zip",
    "-x*tmp_*",
    str(tmp_backup),
    "*"
]

res = subprocess.run(cmd_backup, cwd=REPO_ROOT, capture_output=True, text=True)
if tmp_backup.exists():
    if out_backup.exists():
        out_backup.unlink()
    shutil.move(str(tmp_backup), str(out_backup))
    print(f"[OK] {backup_rar_name} generated: {out_backup.stat().st_size:,} bytes")
else:
    print("[ERROR] Failed to build backup archive:")
    print(res.stderr or res.stdout)
    exit(1)

print("\n=== All tasks in F:\\CV_MAKER completed successfully! ===")
