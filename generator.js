const fs = require('fs');

const DIRS = [
    {dx: 0, dy: -1}, // up
    {dx: 0, dy: 1},  // down
    {dx: -1, dy: 0}, // left
    {dx: 1, dy: 0}   // right
];

function serializeState(blocks, boxes) {
    let s = blocks.map(b => `${b.x},${b.y}`).join('|');
    if (boxes.length > 0) {
        let bstrs = boxes.map(b => `${b.x},${b.y}`);
        bstrs.sort();
        s += '#' + bstrs.join('|');
    }
    return s;
}

function copyState(state) {
    return {
        blocks: state.blocks.map(b => ({...b})),
        boxes: state.boxes.map(b => ({...b}))
    };
}

function solve(grid, startBlocks, startBoxes, targets) {
    const startState = {
        blocks: startBlocks,
        boxes: startBoxes
    };
    
    let queue = [{ state: startState, depth: 0 }];
    let visited = new Set();
    visited.add(serializeState(startState.blocks, startState.boxes));
    
    while (queue.length > 0) {
        let { state, depth } = queue.shift();
        
        // check win
        let win = true;
        for (let i = 0; i < targets.length; i++) {
            if (state.blocks[i].x !== targets[i].x || state.blocks[i].y !== targets[i].y) {
                win = false;
                break;
            }
        }
        if (win) {
            return depth; // optimal solution steps
        }
        
        if (depth >= 25) continue; // max depth
        
        // try moves
        for (let i = 0; i < state.blocks.length; i++) {
            for (let d = 0; d < DIRS.length; d++) {
                let dx = DIRS[d].dx;
                let dy = DIRS[d].dy;
                
                let nextState = copyState(state);
                let active = nextState.blocks[i];
                let moved = false;
                
                while (true) {
                    let nx = active.x + dx;
                    let ny = active.y + dy;
                    
                    if (ny < 0 || ny >= grid.length || nx < 0 || nx >= grid[0].length) break;
                    if (grid[ny][nx] === 1) break;
                    
                    let blockInWay = false;
                    for (let j = 0; j < nextState.blocks.length; j++) {
                        if (i !== j && nextState.blocks[j].x === nx && nextState.blocks[j].y === ny) {
                            blockInWay = true;
                            break;
                        }
                    }
                    if (blockInWay) break;
                    
                    let boxIndex = nextState.boxes.findIndex(b => b.x === nx && b.y === ny);
                    if (boxIndex !== -1) {
                        let bnx = nx + dx;
                        let bny = ny + dy;
                        if (bny < 0 || bny >= grid.length || bnx < 0 || bnx >= grid[0].length) break;
                        if (grid[bny][bnx] === 1) break;
                        
                        let bbiw = false;
                        for (let j = 0; j < nextState.blocks.length; j++) {
                            if (nextState.blocks[j].x === bnx && nextState.blocks[j].y === bny) {
                                bbiw = true;
                                break;
                            }
                        }
                        if (bbiw) break;
                        
                        if (nextState.boxes.some((b, idx) => idx !== boxIndex && b.x === bnx && b.y === bny)) break;
                        
                        nextState.boxes[boxIndex].x = bnx;
                        nextState.boxes[boxIndex].y = bny;
                    }
                    
                    active.x = nx;
                    active.y = ny;
                    moved = true;
                }
                
                if (moved) {
                    let s = serializeState(nextState.blocks, nextState.boxes);
                    if (!visited.has(s)) {
                        visited.add(s);
                        queue.push({ state: nextState, depth: depth + 1 });
                    }
                }
            }
        }
    }
    return -1;
}

function randomInt(max) {
    return Math.floor(Math.random() * max);
}

function generateMap(world) {
    // world: 1 (2 blocks), 2 (3 blocks), 3 (2 blocks + boxes)
    const W = 8 + randomInt(3);
    const H = 7 + randomInt(3);
    
    let grid = Array.from({length: H}, () => Array(W).fill(0));
    for (let x=0; x<W; x++) { grid[0][x] = 1; grid[H-1][x] = 1; }
    for (let y=0; y<H; y++) { grid[y][0] = 1; grid[y][W-1] = 1; }
    
    let numWalls = randomInt(5) + 3;
    for (let i=0; i<numWalls; i++) {
        let x = 1 + randomInt(W-2);
        let y = 1 + randomInt(H-2);
        grid[y][x] = 1;
    }
    
    let emptyCells = [];
    for (let y=1; y<H-1; y++) {
        for (let x=1; x<W-1; x++) {
            if (grid[y][x] === 0) emptyCells.push({x, y});
        }
    }
    
    // Shuffle
    for (let i = emptyCells.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [emptyCells[i], emptyCells[j]] = [emptyCells[j], emptyCells[i]];
    }
    
    let numBlocks = world === 2 ? 3 : 2;
    let numBoxes = world === 3 ? (randomInt(2) + 1) : 0;
    
    if (emptyCells.length < numBlocks * 2 + numBoxes) return null;
    
    let startBlocks = [];
    let targets = [];
    let startBoxes = [];
    
    let ptr = 0;
    for (let i=0; i<numBlocks; i++) {
        startBlocks.push(emptyCells[ptr++]);
        targets.push(emptyCells[ptr++]);
    }
    for (let i=0; i<numBoxes; i++) {
        startBoxes.push(emptyCells[ptr++]);
    }
    
    let minSteps = solve(grid, startBlocks, startBoxes, targets);
    if (minSteps >= (world === 1 ? 4 : (world === 2 ? 5 : 6))) {
        // Output format
        // 1=wall, 0=empty, R/B/G = start, r/b/g = target, 2 = box
        let layout = Array.from({length: H}, () => Array(W).fill(0));
        for (let y=0; y<H; y++) {
            for (let x=0; x<W; x++) {
                layout[y][x] = grid[y][x];
            }
        }
        layout[startBlocks[0].y][startBlocks[0].x] = 'R';
        layout[targets[0].y][targets[0].x] = 'r';
        layout[startBlocks[1].y][startBlocks[1].x] = 'B';
        layout[targets[1].y][targets[1].x] = 'b';
        if (world === 2) {
            layout[startBlocks[2].y][startBlocks[2].x] = 'G';
            layout[targets[2].y][targets[2].x] = 'g';
        }
        for (let b of startBoxes) {
            layout[b.y][b.x] = 2;
        }
        
        return {
            stars: [minSteps + 2, minSteps + 6],
            layout: layout
        };
    }
    return null;
}

let allLevels = [];
for (let w = 1; w <= 3; w++) {
    console.log(`Generating World ${w}...`);
    let count = 0;
    let wLevels = [];
    while (count < 20) {
        let level = generateMap(w);
        if (level) {
            wLevels.push(level);
            count++;
            console.log(`  Found level ${count}/20 for World ${w}`);
        }
    }
    allLevels = allLevels.concat(wLevels);
}

fs.writeFileSync('generated_levels.json', JSON.stringify(allLevels, null, 2));
console.log("Done generating 60 levels.");
