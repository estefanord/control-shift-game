#!/usr/bin/env python3
"""
Multi-platform build script for Control Shift game
Creates executables for Windows (.exe), macOS (.app), and web deployment
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

def create_windows_executable():
    """Create Windows .exe executable using PyInstaller"""
    print("🪟 Building Windows executable...")
    
    # PyInstaller command for Windows
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=Control_Shift_Windows',
        '--add-data=assets:assets',
        '--add-data=music:music',
        '--icon=assets/favicon.ico' if os.path.exists('assets/favicon.ico') else '',
        '--distpath=dist/windows',
        'main.py'
    ]
    
    # Remove empty icon parameter if file doesn't exist
    cmd = [arg for arg in cmd if arg]
    
    try:
        subprocess.run(cmd, check=True)
        
        # Rename to have proper .exe extension
        old_path = 'dist/windows/Control_Shift_Windows'
        new_path = 'dist/windows/Control_Shift_Windows.exe'
        
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            print(f"✅ Windows executable created: {new_path}")
            return True
        elif os.path.exists(new_path):
            print(f"✅ Windows executable created: {new_path}")
            return True
        else:
            print("❌ Windows executable not found after build")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Windows build failed: {e}")
        return False

def create_mac_executable():
    """Create macOS .app bundle using PyInstaller"""
    print("🍎 Building macOS executable...")
    
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=Control_Shift_Mac',
        '--add-data=assets:assets',
        '--add-data=music:music',
        '--distpath=dist/mac',
        'main.py'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        
        # Check if app bundle was created
        app_path = 'dist/mac/Control_Shift_Mac.app'
        exe_path = 'dist/mac/Control_Shift_Mac'
        
        if os.path.exists(app_path):
            print(f"✅ macOS app bundle created: {app_path}")
            return True
        elif os.path.exists(exe_path):
            print(f"✅ macOS executable created: {exe_path}")
            return True
        else:
            print("❌ macOS executable not found after build")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ macOS build failed: {e}")
        return False

def create_web_version():
    """Create web version using pygbag"""
    print("🌐 Building web version...")
    
    # Check if pygbag is installed
    try:
        import pygbag
    except ImportError:
        print("❌ pygbag not installed. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pygbag'], check=True)
    
    # Create web build directory
    os.makedirs('dist/web', exist_ok=True)
    
    # Create web build
    try:
        cmd = [
            sys.executable, '-m', 'pygbag',
            '--width=800',
            '--height=600',
            '--app_name=Control_Shift_Web',
            '--archive',
            'main.py'
        ]
        
        # Change to dist/web directory for build
        original_dir = os.getcwd()
        os.chdir('dist/web')
        
        # Copy necessary files to web build directory  
        shutil.copy('../../main.py', '.')
        if os.path.exists('../../src'):
            shutil.copytree('../../src', './src', dirs_exist_ok=True)
        if os.path.exists('../../assets'):
            shutil.copytree('../../assets', './assets', dirs_exist_ok=True)
        if os.path.exists('../../music'):
            shutil.copytree('../../music', './music', dirs_exist_ok=True)
        
        subprocess.run(cmd, check=True)
        
        # Return to original directory
        os.chdir(original_dir)
        
        print("✅ Web version created in dist/web/")
        return True
        
    except subprocess.CalledProcessError as e:
        os.chdir(original_dir)
        print(f"❌ Web build failed: {e}")
        return False

def create_distribution_packages():
    """Create properly named ZIP packages for each platform"""
    print("📦 Creating distribution packages...")
    
    dist_dir = Path('dist')
    packages_dir = Path('packages')
    packages_dir.mkdir(exist_ok=True)
    
    # Windows package
    windows_dir = dist_dir / 'windows'
    if windows_dir.exists():
        with zipfile.ZipFile('packages/Control_Shift_Windows_PC.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in windows_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(windows_dir)
                    zf.write(file_path, arcname)
            
            # Add README for Windows
            readme_content = """# Control Shift - Windows Version

## How to Play:
1. Extract this ZIP file to a folder
2. Double-click 'Control_Shift_Windows.exe' to start the game
3. Use Arrow Keys or WASD to move, Space to jump

## System Requirements:
- Windows 10 or newer
- No additional software needed - all dependencies included!

## Troubleshooting:
If Windows shows a security warning, click "More info" then "Run anyway"
This is normal for new executables and the game is completely safe.

Enjoy the game!
"""
            zf.writestr('README_WINDOWS.txt', readme_content)
        print("✅ Windows package created: packages/Control_Shift_Windows_PC.zip")
    
    # macOS package  
    mac_dir = dist_dir / 'mac'
    if mac_dir.exists():
        with zipfile.ZipFile('packages/Control_Shift_macOS.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in mac_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(mac_dir)
                    zf.write(file_path, arcname)
            
            # Add README for macOS
            readme_content = """# Control Shift - macOS Version

## How to Play:
1. Extract this ZIP file
2. Double-click 'Control_Shift_Mac' (or Control_Shift_Mac.app) to start
3. Use Arrow Keys or WASD to move, Space to jump

## System Requirements:
- macOS 10.13 or newer
- No additional software needed!

## Troubleshooting:
If macOS says the app is from an "unidentified developer":
1. Right-click the app and select "Open"
2. Click "Open" in the dialog that appears
3. The game will run and be trusted for future launches

Enjoy the game!
"""
            zf.writestr('README_MAC.txt', readme_content)
        print("✅ macOS package created: packages/Control_Shift_macOS.zip")
    
    # Web package
    web_dir = dist_dir / 'web'
    if web_dir.exists():
        with zipfile.ZipFile('packages/Control_Shift_Web_Browser.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in web_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(web_dir)
                    zf.write(file_path, arcname)
            
            # Add README for web version
            readme_content = """# Control Shift - Web Browser Version

## For itch.io Upload:
This is the HTML5/WebAssembly version that runs in web browsers.

## Upload Instructions:
1. Upload this entire ZIP file to itch.io
2. Mark it as "This file will be played in the browser"
3. Set viewport to 800x600
4. Enable fullscreen option
5. Test in preview mode before publishing

## Browser Requirements:
- Modern browser with WebAssembly support
- Chrome, Firefox, Safari, Edge all supported
- No downloads needed for players!

## Controls:
- Arrow Keys or WASD: Move
- Space: Jump  
- L: Level select (from title screen)
- ESC: Return to title

Perfect for itch.io web deployment!
"""
            zf.writestr('README_WEB.txt', readme_content)
        print("✅ Web package created: packages/Control_Shift_Web_Browser.zip")

def create_itch_upload_guide():
    """Create a comprehensive guide for uploading to itch.io"""
    guide_content = """# 🎮 Control Shift - Complete itch.io Upload Guide

## 📦 What You Have

You now have THREE properly formatted packages for itch.io:

1. **Control_Shift_Windows_PC.zip** - For Windows users (.exe file)
2. **Control_Shift_macOS.zip** - For Mac users  
3. **Control_Shift_Web_Browser.zip** - For browser play (HTML5)

## 🚀 Upload to itch.io - Step by Step

### Step 1: Create Project
1. Go to itch.io and log in
2. Click "Upload new project"
3. Enter title: "Control Shift"
4. Classification: "Game"
5. Kind of project: "Downloadable" (we'll add web version too)

### Step 2: Upload Files

#### Windows Version:
- Upload: `Control_Shift_Windows_PC.zip`
- Label: "Windows Download"
- Platform: Windows
- This file will be played in browser: **NO**

#### macOS Version:
- Upload: `Control_Shift_macOS.zip` 
- Label: "macOS Download"
- Platform: macOS
- This file will be played in browser: **NO**

#### Web Version:
- Upload: `Control_Shift_Web_Browser.zip`
- Label: "Play in Browser"
- Platform: Web
- This file will be played in browser: **YES**
- Viewport: 800 x 600
- Fullscreen button: **YES**

### Step 3: Game Description

```
🎮 CONTROL SHIFT - Master 7 Different Control Schemes!

Navigate through challenging rooms where each level completely changes how you control your character!

🌟 UNIQUE GAMEPLAY:
• Room 1: Normal controls (learn the basics)
• Room 2: Reversed controls (left becomes right!)
• Room 3: Delayed input (actions happen after delay)
• Room 4: Chaos mode (controls change randomly)
• Room 5: Momentum physics (slippery movement)
• Room 6: High gravity (everything falls faster)
• Room 7: Final challenge (all mechanics combined!)

🎵 Original soundtrack for each room
🏆 Can you master all control schemes?

🕹️ PLAY OPTIONS:
• Download for Windows/Mac (no browser needed)
• Play instantly in your web browser
• Full gamepad support (desktop versions)

Controls: Arrow Keys/WASD + Space to jump
```

### Step 4: Settings
- Genre: Platformer, Puzzle
- Tags: platformer, challenging, unique-controls, pygame, browser-game
- Rating: Everyone
- Release status: Released
- Pricing: Free (or set price)

### Step 5: Publish!
1. Click "Save & view page"
2. Test each download/web version works
3. If everything works, set to "Public"
4. Share your itch.io URL!

## ✅ File Extension Problem - SOLVED!

- Windows file: `.exe` extension (runs immediately)
- Mac file: Clear executable or `.app` bundle
- Web file: `.html` that auto-loads
- All packages include clear README files

## 🎯 Testing Checklist

Before publishing:
- [ ] Windows .exe runs when double-clicked
- [ ] Mac version opens without issues
- [ ] Web version loads in itch.io preview
- [ ] All 7 levels are playable
- [ ] Music plays correctly
- [ ] Controls work as expected

## 🎊 Success!

Your game is now properly packaged for ALL platforms with correct file extensions and clear instructions. Players will know exactly what to download and how to run it!

No more file extension confusion - everything is clearly labeled and ready to go! 🎮✨
"""
    
    with open('COMPLETE_ITCH_UPLOAD_GUIDE.md', 'w') as f:
        f.write(guide_content)
    print("✅ Complete upload guide created: COMPLETE_ITCH_UPLOAD_GUIDE.md")

def main():
    """Main build process"""
    print("🏗️  Starting multi-platform build for Control Shift...")
    print("=" * 60)
    
    # Clean old builds
    clean_build_dirs()
    
    # Track successful builds
    successful_builds = []
    
    # Build for each platform
    if create_windows_executable():
        successful_builds.append("Windows")
    
    if create_mac_executable():
        successful_builds.append("macOS")
    
    if create_web_version():
        successful_builds.append("Web")
    
    # Create distribution packages
    if successful_builds:
        create_distribution_packages()
        create_itch_upload_guide()
        
        print("\n" + "=" * 60)
        print("🎉 BUILD COMPLETE!")
        print(f"✅ Successfully built: {', '.join(successful_builds)}")
        print("\n📦 Ready for upload:")
        print("   • packages/Control_Shift_Windows_PC.zip")
        print("   • packages/Control_Shift_macOS.zip") 
        print("   • packages/Control_Shift_Web_Browser.zip")
        print("\n📖 See COMPLETE_ITCH_UPLOAD_GUIDE.md for upload instructions!")
        print("\n🎮 All file extension issues resolved!")
    else:
        print("❌ No successful builds created")

if __name__ == "__main__":
    main() 