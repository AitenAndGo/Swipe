import json
import random
from collections import deque
import sys

DIRS = [
    (0, -1), # up
    (0, 1),  # down
    (-1, 0), # left
    (1, 0)   # right
]

def serialize_state(blocks, boxes):
    s = "|".join(f"{b[0]},{b[1]}" for b in blocks)
    if boxes:
        s += "#" + "|".join(f"{b[0]},{b[1]}" for b in sorted(boxes))
    return s

def copy_state(state):
    return {
        'blocks': [list(b) for b in state['blocks']],
        'boxes': [list(b) for b in state['boxes']]
    }

def solve(grid, start_blocks, start_boxes, targets):
    H = len(grid)
    W = len(grid[0])
    
    start_state = {
        'blocks': start_blocks,
        'boxes': start_boxes
    }
    
    queue = deque([(start_state, 0)])
    visited = set()
    visited.add(serialize_state(start_state['blocks'], start_state['boxes']))
    
    while queue:
        state, depth = queue.popleft()
        
        # Check win
        win = True
        for i in range(len(targets)):
            if state['blocks'][i][0] != targets[i][0] or state['blocks'][i][1] != targets[i][1]:
                win = False
                break
        if win:
            return depth
            
        if depth >= 15: # Limit search depth for speed
            continue
            
        # Try moves
        for i in range(len(state['blocks'])):
            for dx, dy in DIRS:
                next_state = copy_state(state)
                active = next_state['blocks'][i]
                moved = False
                
                while True:
                    nx = active[0] + dx
                    ny = active[1] + dy
                    
                    if ny < 0 or ny >= H or nx < 0 or nx >= W:
                        break
                    if grid[ny][nx] == 1:
                        break
                        
                    block_in_way = False
                    for j in range(len(next_state['blocks'])):
                        if i != j and next_state['blocks'][j][0] == nx and next_state['blocks'][j][1] == ny:
                            block_in_way = True
                            break
                    if block_in_way:
                        break
                        
                    box_idx = -1
                    for j, b in enumerate(next_state['boxes']):
                        if b[0] == nx and b[1] == ny:
                            box_idx = j
                            break
                            
                    if box_idx != -1:
                        bnx = nx + dx
                        bny = ny + dy
                        
                        if bny < 0 or bny >= H or bnx < 0 or bnx >= W:
                            break
                        if grid[bny][bnx] == 1:
                            break
                            
                        bbiw = False
                        for j in range(len(next_state['blocks'])):
                            if next_state['blocks'][j][0] == bnx and next_state['blocks'][j][1] == bny:
                                bbiw = True
                                break
                        if bbiw:
                            break
                            
                        box_in_way = False
                        for j, b in enumerate(next_state['boxes']):
                            if j != box_idx and b[0] == bnx and b[1] == bny:
                                box_in_way = True
                                break
                        if box_in_way:
                            break
                            
                        next_state['boxes'][box_idx][0] = bnx
                        next_state['boxes'][box_idx][1] = bny
                        
                    active[0] = nx
                    active[1] = ny
                    moved = True
                    
                if moved:
                    s = serialize_state(next_state['blocks'], next_state['boxes'])
                    if s not in visited:
                        visited.add(s)
                        queue.append((next_state, depth + 1))
                        
    return -1

def generate_map(world):
    W = 8
    H = 8
    
    grid = [[0 for _ in range(W)] for _ in range(H)]
    for x in range(W):
        grid[0][x] = 1
        grid[H-1][x] = 1
    for y in range(H):
        grid[y][0] = 1
        grid[y][W-1] = 1
        
    num_walls = random.randint(3, 5)
    for _ in range(num_walls):
        x = random.randint(1, W-2)
        y = random.randint(1, H-2)
        grid[y][x] = 1
        
    empty_cells = []
    for y in range(1, H-1):
        for x in range(1, W-1):
            if grid[y][x] == 0:
                empty_cells.append([x, y])
                
    random.shuffle(empty_cells)
    
    num_blocks = 3 if world == 2 else 2
    num_boxes = random.randint(1, 2) if world == 3 else 0
    
    if len(empty_cells) < num_blocks * 2 + num_boxes:
        return None
        
    start_blocks = []
    targets = []
    start_boxes = []
    
    ptr = 0
    for i in range(num_blocks):
        start_blocks.append(empty_cells[ptr])
        ptr += 1
        targets.append(empty_cells[ptr])
        ptr += 1
        
    for i in range(num_boxes):
        start_boxes.append(empty_cells[ptr])
        ptr += 1
        
    min_steps = solve(grid, start_blocks, start_boxes, targets)
    
    required_steps = 3 if world == 1 else (4 if world == 2 else 5)
    
    if min_steps >= required_steps:
        layout = [[grid[y][x] for x in range(W)] for y in range(H)]
        
        layout[start_blocks[0][1]][start_blocks[0][0]] = 'R'
        layout[targets[0][1]][targets[0][0]] = 'r'
        layout[start_blocks[1][1]][start_blocks[1][0]] = 'B'
        layout[targets[1][1]][targets[1][0]] = 'b'
        
        if world == 2:
            layout[start_blocks[2][1]][start_blocks[2][0]] = 'G'
            layout[targets[2][1]][targets[2][0]] = 'g'
            
        for b in start_boxes:
            layout[b[1]][b[0]] = 2
            
        return {
            'stars': [min_steps + 2, min_steps + 5],
            'layout': layout
        }
    return None

all_levels = []
for w in range(1, 4):
    print(f"Generating World {w}...", flush=True)
    w_levels = []
    count = 0
    while count < 20:
        lvl = generate_map(w)
        if lvl:
            w_levels.append(lvl)
            count += 1
            print(f"  Found level {count}/20 for World {w}", flush=True)
    all_levels.extend(w_levels)

with open('generated_levels.json', 'w') as f:
    import json
    f.write('[\n')
    for i, level in enumerate(all_levels):
        f.write('  {\n')
        f.write(f'    "stars": {json.dumps(level["stars"])},\n')
        f.write('    "layout": [\n')
        for j, row in enumerate(level['layout']):
            row_str = "[" + ", ".join(f"'{x}'" if isinstance(x, str) else str(x) for x in row) + "]"
            f.write(f'      {row_str}{"," if j < len(level["layout"])-1 else ""}\n')
        f.write('    ]\n')
        f.write(f'  }}{"," if i < len(all_levels)-1 else ""}\n')
    f.write(']\n')

print("Done generating 60 levels.", flush=True)
