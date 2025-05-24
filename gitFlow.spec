# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['gitFlow.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['readchar', 'keyboard', 'git', 'git.cmd', 'git.db', 'git.exc', 'git.objects', 'git.refs', 'git.remote', 'git.repo', 'git.util', 'requests', 'importlib.metadata'],
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='gitFlow',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
