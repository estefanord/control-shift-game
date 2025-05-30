# Control Shift - Web Deployment

## About the Game
Control Shift is a platformer game where each level introduces a different control mechanic that challenges the player's expectations. Navigate through 7 unique rooms, each with its own twist on traditional platformer controls.

## Game Features
- **7 Unique Levels**: Each with different control mechanics
- **Progressive Difficulty**: From normal controls to complex combinations
- **Level Select**: Press 'L' on the title screen to jump to any level
- **Web-Optimized**: Runs smoothly in modern web browsers

## Controls
- **Arrow Keys** or **WASD**: Move and jump
- **Space**: Jump (alternative)
- **L**: Level select (on title screen)
- **ESC**: Return to title (from level select)
- **1-7**: Jump to specific levels (in level select)

## Level Descriptions
1. **Normal Room**: Standard platformer controls
2. **High Gravity**: Increased gravity makes jumping more challenging
3. **Momentum**: Slippery controls with momentum-based movement
4. **Reversed Controls**: Left becomes right, right becomes left
5. **Random Platforms**: Platforms change position every few seconds
6. **Delayed Input**: Your inputs are delayed by half a second
7. **Final Challenge**: All effects cycle through automatically

## Deployment Instructions for itch.io

### Option 1: Upload the ZIP file (Recommended)
1. Go to your itch.io dashboard
2. Create a new project or edit an existing one
3. Set the project type to "HTML"
4. Upload the `web.zip` file from the `build` directory
5. Check "This file will be played in the browser"
6. Set the viewport dimensions to **800x600**
7. Enable fullscreen if desired
8. Publish your game!

### Option 2: Upload individual files
1. Extract the contents of `web.zip`
2. Upload all files (`index.html`, `web_deployment.apk`, `favicon.png`)
3. Set `index.html` as the main file
4. Configure viewport to **800x600**

## Technical Details
- Built with pygame and pygbag for web compatibility
- Uses WebAssembly for optimal performance
- Includes background music (7 different tracks)
- Responsive to different screen sizes
- No external dependencies required

## File Structure
```
build/
├── web.zip                 # Complete web deployment package
└── web/
    ├── index.html         # Main HTML file
    ├── web_deployment.apk # Game assets and code
    └── favicon.png        # Game icon
```

## Browser Compatibility
- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge
- Most modern browsers with WebAssembly support

## Troubleshooting
- If the game doesn't load, ensure the browser supports WebAssembly
- For audio issues, make sure the browser allows autoplay
- If controls feel unresponsive, try clicking on the game area first

Enjoy playing Control Shift! 