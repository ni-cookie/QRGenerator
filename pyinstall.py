import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--windowed',
    '--noconsole',
    '--name=QRGen',
    '--icon=images/QRGenLOGO_512x512.icns',
    '--add-data=images:images', 
])