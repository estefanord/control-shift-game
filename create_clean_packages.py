#!/usr/bin/env python3
"""
Create clean Windows and Mac packages without README files
"""

import os
import zipfile
from pathlib import Path

def create_clean_packages():
    """Create Windows and Mac packages without README files"""
    print("📦 Creating clean packages without README files...")
    
    dist_dir = Path('dist')
    packages_dir = Path('packages')
    packages_dir.mkdir(exist_ok=True)
    
    # Windows package - NO README
    windows_dir = dist_dir / 'windows'
    if windows_dir.exists():
        with zipfile.ZipFile('packages/Control_Shift_Windows_PC.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in windows_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(windows_dir)
                    zf.write(file_path, arcname)
        print("✅ Clean Windows package created: packages/Control_Shift_Windows_PC.zip")
    
    # macOS package - NO README  
    mac_dir = dist_dir / 'mac'
    if mac_dir.exists():
        with zipfile.ZipFile('packages/Control_Shift_macOS.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in mac_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(mac_dir)
                    zf.write(file_path, arcname)
        print("✅ Clean macOS package created: packages/Control_Shift_macOS.zip")

if __name__ == "__main__":
    create_clean_packages() 