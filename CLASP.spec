# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for CLASP

import sys
from pathlib import Path

block_cipher = None

# Get the project root directory
root_dir = Path(SPECPATH)

a = Analysis(
    ['clasp/main.py'],
    pathex=[str(root_dir)],
    binaries=[],
    datas=[
        ('images/clasp-icon.png', 'images'),
        ('images/clasp-screenshot.png', 'images'),
        ('docs/', 'docs'),
        ('examples/', 'examples'),
    ],
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtWidgets',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CLASP',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='images/clasp-icon.png',  # Application icon
)
