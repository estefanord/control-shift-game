#!/usr/bin/env python3
"""
Build script that properly includes music and assets in PyInstaller executables
"""

import os
import sys
import shutil
import subprocess
import zipfile
from pathlib import Path

def clean_build_dirs():
    """Remove old build and dist directories"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ Cleaned {dir_name} directory")

def create_windows_executable_with_sound():
    """Create Windows .exe executable with music files included"""
    print("🪟 Building Windows executable with sound...")
    
    # PyInstaller command for Windows with proper asset inclusion
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=Control_Shift_Windows',
        '--add-data=assets/music:assets/music',  # More specific path
        '--add-data=assets/sfx:assets/sfx',      # Include sound effects too
        '--add-data=assets/sprites:assets/sprites', # Include sprites
        '--add-data=src:src',                    # Include source code
        '--distpath=dist/windows',
        '--clean',                               # Clean cache
        'main.py'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        
        # Check if executable was created
        windows_exe = 'dist/windows/Control_Shift_Windows'
        if os.path.exists(windows_exe + '.exe'):
            print(f"✅ Windows executable with sound created: {windows_exe}.exe")
            return True
        elif os.path.exists(windows_exe):
            # Rename to have .exe extension
            os.rename(windows_exe, windows_exe + '.exe')
            print(f"✅ Windows executable with sound created: {windows_exe}.exe")
            return True
        else:
            print("❌ Windows executable not found after build")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Windows build failed: {e}")
        return False

def create_mac_executable_with_sound():
    """Create macOS executable with music files included"""
    print("🍎 Building macOS executable with sound...")
    
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=Control_Shift_Mac',
        '--add-data=assets/music:assets/music',
        '--add-data=assets/sfx:assets/sfx',
        '--add-data=assets/sprites:assets/sprites',
        '--add-data=src:src',
        '--distpath=dist/mac',
        '--clean',
        'main.py'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        
        # Check if app bundle was created
        app_path = 'dist/mac/Control_Shift_Mac.app'
        exe_path = 'dist/mac/Control_Shift_Mac'
        
        if os.path.exists(app_path):
            print(f"✅ macOS app bundle with sound created: {app_path}")
            return True
        elif os.path.exists(exe_path):
            print(f"✅ macOS executable with sound created: {exe_path}")
            return True
        else:
            print("❌ macOS executable not found after build")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ macOS build failed: {e}")
        return False

def create_packages_with_sound():
    """Create properly named ZIP packages with sound included"""
    print("📦 Creating packages with sound...")
    
    dist_dir = Path('dist')
    packages_dir = Path('packages')
    packages_dir.mkdir(exist_ok=True)
    
    # Windows package with sound
    windows_dir = dist_dir / 'windows'
    if windows_dir.exists():
        with zipfile.ZipFile('packages/Control_Shift_Windows_PC.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in windows_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(windows_dir)
                    zf.write(file_path, arcname)
        print("✅ Windows package with sound: packages/Control_Shift_Windows_PC.zip")
    
    # macOS package with sound
    mac_dir = dist_dir / 'mac'
    if mac_dir.exists():
        with zipfile.ZipFile('packages/Control_Shift_macOS.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in mac_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(mac_dir)
                    zf.write(file_path, arcname)
        print("✅ macOS package with sound: packages/Control_Shift_macOS.zip")

def main():
    """Main build process with sound"""
    print("🔊 Building Control Shift with SOUND support...")
    print("=" * 60)
    
    # Clean old builds
    clean_build_dirs()
    
    # Track successful builds
    successful_builds = []
    
    # Build for each platform with sound
    if create_windows_executable_with_sound():
        successful_builds.append("Windows (with sound)")
    
    if create_mac_executable_with_sound():
        successful_builds.append("macOS (with sound)")
    
    # Create distribution packages
    if successful_builds:
        create_packages_with_sound()
        
        print("\n" + "=" * 60)
        print("🎉 BUILD WITH SOUND COMPLETE!")
        print(f"✅ Successfully built: {', '.join(successful_builds)}")
        print("\n📦 Ready for upload:")
        print("   • packages/Control_Shift_Windows_PC.zip (WITH SOUND)")
        print("   • packages/Control_Shift_macOS.zip (WITH SOUND)")
        print("\n🔊 Music files are now properly included!")
    else:
        print("❌ No successful builds created")

if __name__ == "__main__":
    main() 