const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Game variables
let bird = {
    x: 100,
    y: 200,
    velocity: 0,
    gravity: 0.5,
    jump: -6
};

let pipes = [];
let score = 0;
let level = 1;
let gameOver = false;    
let frameCount = 0;
let gameSpeed = 2;

// Load images
const birdImg = new Image();
birdImg.src = 'images/avion.jpeg';
const pipeImg = new Image();
pipeImg.src = 'images/pipe.png';

// Load sounds
const wingSound = new Audio('audio/wing.mp3');
const pointSound = new Audio('audio/point.mp3');
const hitSound = new Audio('audio/hit.mp3');

function createPipe() {
    let gap = 125;
    let minHeight = 50;
    let maxHeight = canvas.height - gap - minHeight;
    let height = Math.floor(Math.random() * (maxHeight - minHeight)) + minHeight;
    
    pipes.push({
        x: canvas.width,
        topHeight: height,
        bottomHeight: canvas.height - height - gap,
        width: 50,
        passed: false
    });
}

function drawBird() {
    ctx.drawImage(birdImg, bird.x, bird.y, 50, 50);
}

function drawPipes() {
    for (let pipe of pipes) {
        ctx.drawImage(pipeImg, pipe.x, 0, pipe.width, pipe.topHeight);
        ctx.drawImage(pipeImg, pipe.x, canvas.height - pipe.bottomHeight, pipe.width, pipe.bottomHeight);
    }
}

function drawScore() {
    ctx.fillStyle = 'white';
    ctx.font = '20px Arial';
    ctx.fillText(`Score: ${score}  Level: ${level}`, 10, 30);
}

function updateScore() {
    for (let pipe of pipes) {
        if (bird.x > pipe.x + pipe.width && !pipe.passed) {
            score++;
            pipe.passed = true;
            pointSound.play();
            if (score % 5 === 0) {
                level++;
                gameSpeed += 0.5;
            }
        }
    }
}

function update() {
    if (gameOver) return;

    bird.velocity += bird.gravity;
    bird.y += bird.velocity;

    if (bird.velocity > 10) {
        bird.velocity = 10;
    }

    if (bird.y + 50 > canvas.height || bird.y < 0) {
        gameOver = true;
        hitSound.play();
    }

    if (frameCount % 100 === 0) {
        createPipe();
    }

    for (let pipe of pipes) {
        pipe.x -= gameSpeed;

        if (pipe.x + pipe.width < 0) {
            pipes.shift();
        }
    }

    updateScore();

    if (checkCollision()) {
        gameOver = true;
        hitSound.play();
    }

    frameCount++;
}

function checkCollision() {
    for (let pipe of pipes) {
        if (bird.x + 50 > pipe.x && bird.x < pipe.x + pipe.width &&
            (bird.y < pipe.topHeight || bird.y + 50 > canvas.height - pipe.bottomHeight)) {
            return true;
        }
    }
    return false;
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawBird();
    drawPipes();
    drawScore();

    if (gameOver) {
        ctx.fillStyle = 'white';
        ctx.font = '30px Arial';
        ctx.fillText('Game Over!', canvas.width / 2 - 70, canvas.height / 2);
        ctx.fillText(`Final Score: ${score}  Level: ${level}`, canvas.width / 2 - 120, canvas.height / 2 + 40);
    }
}

function gameLoop() {
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

function resetGame() {
    bird.y = 200;
    bird.velocity = 0;
    pipes = [];
    score = 0;
    level = 1;
    gameSpeed = 2;
    gameOver = false;
    frameCount = 0;
}

// Cambiar el evento de clic por un evento de teclado
document.addEventListener('keydown', function(event) {
    if (event.code === 'Space') {
        event.preventDefault();
        if (gameOver) {
            resetGame();
        } else {
            bird.velocity = bird.jump;
            wingSound.play();
        }
    }
});

gameLoop();