// Control Shift - Pure JavaScript Version
// Completely self-contained, no external dependencies

class Game {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.canvas.width = 800;
        this.canvas.height = 600;
        
        // Game state
        this.currentRoom = 0;
        this.gameState = 'TITLE'; // TITLE, PLAYING, LEVEL_SELECT, ENDING
        this.titleScreen = true;
        this.levelSelectScreen = false;
        
        // Player
        this.player = {
            x: 50,
            y: 300,
            width: 20,
            height: 30,
            velX: 0,
            velY: 0,
            onGround: false,
            color: '#FFB6C1' // Pink pastel
        };
        
        // Constants
        this.GRAVITY = 0.8;
        this.PLAYER_SPEED = 5;
        this.JUMP_STRENGTH = -12;
        this.FPS = 60;
        
        // Room effects
        this.roomEffects = {
            gravity: false,
            momentum: false,
            reversed: false,
            random: false,
            delayed: false,
            final: false
        };
        
        // Input handling
        this.keys = {};
        this.setupInput();
        
        // Room definitions
        this.rooms = this.createRooms();
        
        // Background stars
        this.stars = [];
        this.generateStars();
        
        // Game loop
        this.lastTime = 0;
        this.requestAnimationFrame = this.gameLoop.bind(this);
        this.gameLoop(0);
    }
    
    setupInput() {
        document.addEventListener('keydown', (e) => {
            this.keys[e.code] = true;
            
            if (this.titleScreen) {
                if (e.code === 'Space') {
                    this.titleScreen = false;
                    this.gameState = 'PLAYING';
                } else if (e.code === 'KeyL') {
                    this.titleScreen = false;
                    this.levelSelectScreen = true;
                    this.gameState = 'LEVEL_SELECT';
                }
            } else if (this.levelSelectScreen) {
                if (e.code === 'Escape') {
                    this.levelSelectScreen = false;
                    this.titleScreen = true;
                    this.gameState = 'TITLE';
                } else if (e.code >= 'Digit1' && e.code <= 'Digit7') {
                    const level = parseInt(e.code.charAt(5)) - 1;
                    this.setRoom(level);
                    this.levelSelectScreen = false;
                    this.gameState = 'PLAYING';
                }
            }
        });
        
        document.addEventListener('keyup', (e) => {
            this.keys[e.code] = false;
        });
    }
    
    createRooms() {
        return [
            {
                name: "Normal Room",
                platforms: [
                    {x: 0, y: 550, width: 800, height: 50},
                    {x: 200, y: 450, width: 100, height: 20},
                    {x: 400, y: 350, width: 100, height: 20},
                    {x: 600, y: 250, width: 100, height: 20}
                ],
                goal: {x: 750, y: 250, width: 30, height: 30},
                effect: 'normal'
            },
            {
                name: "High Gravity",
                platforms: [
                    {x: 0, y: 550, width: 800, height: 50},
                    {x: 150, y: 450, width: 80, height: 20},
                    {x: 300, y: 350, width: 80, height: 20},
                    {x: 450, y: 250, width: 80, height: 20},
                    {x: 600, y: 150, width: 80, height: 20}
                ],
                goal: {x: 620, y: 120, width: 30, height: 30},
                effect: 'gravity'
            },
            {
                name: "Momentum",
                platforms: [
                    {x: 0, y: 550, width: 800, height: 50},
                    {x: 100, y: 450, width: 60, height: 20},
                    {x: 250, y: 350, width: 60, height: 20},
                    {x: 400, y: 250, width: 60, height: 20},
                    {x: 550, y: 150, width: 60, height: 20},
                    {x: 700, y: 100, width: 60, height: 20}
                ],
                goal: {x: 720, y: 70, width: 30, height: 30},
                effect: 'momentum'
            },
            {
                name: "Reversed Controls",
                platforms: [
                    {x: 0, y: 550, width: 800, height: 50},
                    {x: 250, y: 450, width: 100, height: 20},
                    {x: 450, y: 350, width: 100, height: 20}
                ],
                goal: {x: 470, y: 320, width: 30, height: 30},
                effect: 'reversed'
            },
            {
                name: "Random Platforms",
                platforms: [
                    {x: 0, y: 550, width: 800, height: 50}
                ],
                goal: {x: 750, y: 250, width: 30, height: 30},
                effect: 'random'
            },
            {
                name: "Delayed Input",
                platforms: [
                    {x: 0, y: 550, width: 800, height: 50},
                    {x: 200, y: 450, width: 100, height: 20},
                    {x: 400, y: 350, width: 100, height: 20},
                    {x: 100, y: 250, width: 100, height: 20},
                    {x: 600, y: 200, width: 100, height: 20}
                ],
                goal: {x: 620, y: 170, width: 30, height: 30},
                effect: 'delayed'
            },
            {
                name: "Final Challenge",
                platforms: [
                    {x: 0, y: 550, width: 800, height: 50},
                    {x: 100, y: 450, width: 80, height: 20},
                    {x: 250, y: 380, width: 80, height: 20},
                    {x: 400, y: 310, width: 80, height: 20},
                    {x: 550, y: 240, width: 80, height: 20},
                    {x: 350, y: 170, width: 80, height: 20},
                    {x: 200, y: 100, width: 80, height: 20}
                ],
                goal: {x: 220, y: 50, width: 30, height: 30},
                effect: 'final'
            }
        ];
    }
    
    generateStars() {
        this.stars = [];
        for (let i = 0; i < 50; i++) {
            this.stars.push({
                x: Math.random() * 800,
                y: Math.random() * 600,
                size: Math.random() * 2 + 1,
                brightness: Math.random() * 155 + 100
            });
        }
    }
    
    setRoom(roomIndex) {
        if (roomIndex >= 0 && roomIndex < this.rooms.length) {
            this.currentRoom = roomIndex;
            this.player.x = 50;
            this.player.y = 300;
            this.player.velX = 0;
            this.player.velY = 0;
            this.player.onGround = false;
            
            // Reset room effects
            this.roomEffects = {
                gravity: false,
                momentum: false,
                reversed: false,
                random: false,
                delayed: false,
                final: false
            };
            
            // Set current room effect
            const effect = this.rooms[roomIndex].effect;
            if (effect !== 'normal') {
                this.roomEffects[effect] = true;
            }
            
            if (effect === 'random') {
                this.generateRandomPlatforms();
            }
        }
    }
    
    generateRandomPlatforms() {
        const room = this.rooms[this.currentRoom];
        room.platforms = [{x: 0, y: 550, width: 800, height: 50}]; // Keep ground
        
        for (let i = 0; i < 5; i++) {
            room.platforms.push({
                x: Math.random() * 650 + 50,
                y: Math.random() * 300 + 200,
                width: Math.random() * 60 + 60,
                height: 20
            });
        }
    }
    
    update(deltaTime) {
        if (this.gameState !== 'PLAYING') return;
        
        const room = this.rooms[this.currentRoom];
        
        // Handle different room effects
        this.updatePlayer(room);
        
        // Check goal collision
        if (this.checkCollision(this.player, room.goal)) {
            if (this.currentRoom < this.rooms.length - 1) {
                this.setRoom(this.currentRoom + 1);
            } else {
                this.gameState = 'ENDING';
            }
        }
        
        // Random platforms effect
        if (this.roomEffects.random && Math.random() < 0.01) {
            this.generateRandomPlatforms();
        }
    }
    
    updatePlayer(room) {
        let effectiveKeys = {...this.keys};
        
        // Reversed controls effect
        if (this.roomEffects.reversed) {
            const tempLeft = effectiveKeys.ArrowLeft || effectiveKeys.KeyA;
            const tempRight = effectiveKeys.ArrowRight || effectiveKeys.KeyD;
            
            effectiveKeys.ArrowLeft = tempRight;
            effectiveKeys.KeyA = tempRight;
            effectiveKeys.ArrowRight = tempLeft;
            effectiveKeys.KeyD = tempLeft;
        }
        
        // Handle input
        if (effectiveKeys.ArrowLeft || effectiveKeys.KeyA) {
            this.player.velX = -this.PLAYER_SPEED;
        } else if (effectiveKeys.ArrowRight || effectiveKeys.KeyD) {
            this.player.velX = this.PLAYER_SPEED;
        } else {
            this.player.velX = 0;
        }
        
        if ((effectiveKeys.Space || effectiveKeys.ArrowUp || effectiveKeys.KeyW) && this.player.onGround) {
            this.player.velY = this.JUMP_STRENGTH;
        }
        
        // Apply gravity (modified by room effects)
        let gravity = this.GRAVITY;
        if (this.roomEffects.gravity || this.roomEffects.final) {
            gravity *= 2;
        }
        
        this.player.velY += gravity;
        if (this.player.velY > 15) {
            this.player.velY = 15;
        }
        
        // Apply momentum effect
        if (this.roomEffects.momentum || this.roomEffects.final) {
            this.player.velX *= 0.8;
        }
        
        // Update position
        this.player.x += this.player.velX;
        this.player.y += this.player.velY;
        
        // Screen bounds
        if (this.player.x < 0) this.player.x = 0;
        if (this.player.x > 800 - this.player.width) this.player.x = 800 - this.player.width;
        
        // Reset if fallen
        if (this.player.y > 600) {
            this.player.x = 50;
            this.player.y = 300;
            this.player.velX = 0;
            this.player.velY = 0;
        }
        
        // Platform collision
        this.player.onGround = false;
        for (const platform of room.platforms) {
            if (this.checkCollision(this.player, platform) && this.player.velY > 0) {
                this.player.y = platform.y - this.player.height;
                this.player.velY = 0;
                this.player.onGround = true;
                break;
            }
        }
    }
    
    checkCollision(rect1, rect2) {
        return rect1.x < rect2.x + rect2.width &&
               rect1.x + rect1.width > rect2.x &&
               rect1.y < rect2.y + rect2.height &&
               rect1.y + rect1.height > rect2.y;
    }
    
    render() {
        // Clear screen
        this.ctx.fillStyle = '#000000';
        this.ctx.fillRect(0, 0, 800, 600);
        
        // Draw stars
        for (const star of this.stars) {
            this.ctx.fillStyle = `rgb(${star.brightness}, ${star.brightness}, ${star.brightness})`;
            this.ctx.beginPath();
            this.ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
            this.ctx.fill();
        }
        
        if (this.titleScreen) {
            this.renderTitleScreen();
        } else if (this.levelSelectScreen) {
            this.renderLevelSelect();
        } else if (this.gameState === 'PLAYING') {
            this.renderGame();
        } else if (this.gameState === 'ENDING') {
            this.renderEnding();
        }
    }
    
    renderTitleScreen() {
        this.ctx.fillStyle = '#FFB6C1';
        this.ctx.font = 'bold 48px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('Control Shift', 400, 250);
        
        this.ctx.fillStyle = '#FFFFFF';
        this.ctx.font = '24px Arial';
        this.ctx.fillText('Press SPACE to start', 400, 320);
        this.ctx.fillText('Press L for level select', 400, 350);
    }
    
    renderLevelSelect() {
        this.ctx.fillStyle = '#FFB6C1';
        this.ctx.font = 'bold 48px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('Level Select', 400, 100);
        
        this.ctx.fillStyle = '#FFFFFF';
        this.ctx.font = '24px Arial';
        
        const levelNames = [
            '1. Normal Room',
            '2. High Gravity',
            '3. Momentum',
            '4. Reversed Controls',
            '5. Random Platforms',
            '6. Delayed Input',
            '7. Final Challenge'
        ];
        
        for (let i = 0; i < levelNames.length; i++) {
            this.ctx.fillText(levelNames[i], 400, 200 + i * 40);
        }
        
        this.ctx.fillStyle = '#888888';
        this.ctx.fillText('Press ESC to return', 400, 500);
    }
    
    renderGame() {
        const room = this.rooms[this.currentRoom];
        
        // Draw platforms
        this.ctx.fillStyle = '#666666';
        for (const platform of room.platforms) {
            this.ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
        }
        
        // Draw goal
        this.ctx.fillStyle = '#00FF00';
        this.ctx.fillRect(room.goal.x, room.goal.y, room.goal.width, room.goal.height);
        
        // Draw player
        this.ctx.fillStyle = this.player.color;
        this.ctx.fillRect(this.player.x, this.player.y, this.player.width, this.player.height);
        
        // Draw player head
        this.ctx.fillStyle = '#FFFF99';
        this.ctx.beginPath();
        this.ctx.arc(this.player.x + this.player.width/2, this.player.y + 5, 5, 0, Math.PI * 2);
        this.ctx.fill();
        
        // Draw UI
        this.ctx.fillStyle = '#FFFFFF';
        this.ctx.font = '20px Arial';
        this.ctx.textAlign = 'left';
        this.ctx.fillText(`Room ${this.currentRoom + 1}/7: ${room.name}`, 10, 30);
        
        if (this.roomEffects.final) {
            this.ctx.fillText('Effect: All combined!', 10, 60);
        }
    }
    
    renderEnding() {
        this.ctx.fillStyle = '#FFB6C1';
        this.ctx.font = 'bold 48px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('Congratulations!', 400, 250);
        
        this.ctx.fillStyle = '#FFFFFF';
        this.ctx.font = '24px Arial';
        this.ctx.fillText('You completed all rooms!', 400, 320);
        this.ctx.fillText('Press SPACE to restart', 400, 350);
        
        if (this.keys.Space) {
            this.titleScreen = true;
            this.gameState = 'TITLE';
            this.setRoom(0);
        }
    }
    
    gameLoop(currentTime) {
        const deltaTime = currentTime - this.lastTime;
        this.lastTime = currentTime;
        
        this.update(deltaTime);
        this.render();
        
        requestAnimationFrame(this.requestAnimationFrame);
    }
}

// Initialize game when page loads
window.addEventListener('load', () => {
    new Game();
}); 