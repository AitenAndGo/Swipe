import json
import re

# Read the original 60 levels
with open('generated_levels.json', 'r') as f:
    text = f.read()
    # Replace single quotes with double quotes so json.loads works? Or just eval
    levels = eval(text)

w1 = levels[0:20]
w2 = levels[20:40]
w3 = levels[40:60]

# Sort each world by the first star threshold (which is min_steps + 2)
w1.sort(key=lambda l: l['stars'][0])
w2.sort(key=lambda l: l['stars'][0])
w3.sort(key=lambda l: l['stars'][0])

w1_tut = {
    'stars': [2, 3],
    'layout': [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 'R', 0, 0, 0, 'r', 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 1],
        [1, 'B', 0, 0, 0, 'b', 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1]
    ]
}

w2_tut = {
    'stars': [3, 5],
    'layout': [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 'R', 0, 0, 0, 'r', 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1],
        [1, 'B', 0, 0, 0, 'b', 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1],
        [1, 'G', 0, 0, 0, 'g', 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1]
    ]
}

w3_tut = {
    'stars': [4, 6],
    'layout': [
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 'R', 0, 2, 0, 0, 'r', 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 'B', 0, 0, 0, 0, 'b', 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
}

new_levels = []
new_levels.append(w1_tut)
new_levels.extend(w1)
new_levels.append(w2_tut)
new_levels.extend(w2)
new_levels.append(w3_tut)
new_levels.extend(w3)

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Build levels_json string
levels_json = "[\n"
for i, level in enumerate(new_levels):
    levels_json += '  {\n'
    levels_json += f'    "stars": {json.dumps(level["stars"])},\n'
    levels_json += '    "layout": [\n'
    for j, row in enumerate(level['layout']):
        row_str = "[" + ", ".join(f"'{x}'" if isinstance(x, str) else str(x) for x in row) + "]"
        levels_json += f'      {row_str}{"," if j < len(level["layout"])-1 else ""}\n'
    levels_json += '    ]\n'
    levels_json += f'  }}{"," if i < len(new_levels)-1 else ""}\n'
levels_json += ']'

# Replace levels
pattern = r'const levels = \[.*?\];\n\n        let currentLevelIndex'
replacement = 'const levels = ' + levels_json + ';\n\n        let currentLevelIndex'
new_html = re.sub(pattern, replacement, html, flags=re.DOTALL)

# Ensure logic is correct for 21 levels
# In index.html, we check 21 levels per world.
# Replace all "20" with "21", "40" with "42", "60" with "63" in the relevant JS parts.
# Let's replace the showWorldsView and openWorld blocks if they are wrong.
import textwrap

js_logic = """
        function showWorldsView() {
            document.getElementById('levels-view').style.display = 'none';
            document.getElementById('worlds-view').style.display = 'block';

            let playerProgress = JSON.parse(sessionStorage.getItem('swipeProgress')) || {};

            let w1Stars = 0;
            for (let i = 0; i < 21; i++) w1Stars += (playerProgress[i] || 0);
            document.getElementById('w1-progress').textContent = `${w1Stars}/63 Stars`;

            let w2Stars = 0;
            for (let i = 21; i < 42; i++) w2Stars += (playerProgress[i] || 0);
            document.getElementById('w2-progress').textContent = `${w2Stars}/63 Stars`;

            let w3Stars = 0;
            for (let i = 42; i < 63; i++) w3Stars += (playerProgress[i] || 0);
            document.getElementById('w3-progress').textContent = `${w3Stars}/63 Stars`;

            const w2Card = document.getElementById('world-card-2');
            const w2Subtitle = document.getElementById('w2-subtitle');
            if (!DEV_UNLOCK_ALL && w1Stars < 42) {
                w2Card.classList.add('locked');
                w2Subtitle.innerHTML = `<span style="color: #ff6b6b; font-weight: bold;">Requires 42 stars in W1</span>`;
            } else {
                w2Card.classList.remove('locked');
                w2Subtitle.textContent = `3 Blocks - Advanced`;
            }

            const w3Card = document.getElementById('world-card-3');
            const w3Subtitle = document.getElementById('w3-subtitle');
            if (!DEV_UNLOCK_ALL && w2Stars < 42) {
                w3Card.classList.add('locked');
                w3Subtitle.innerHTML = `<span style="color: #ff6b6b; font-weight: bold;">Requires 42 stars in W2</span>`;
            } else {
                w3Card.classList.remove('locked');
                w3Subtitle.textContent = `Pushable Boxes`;
            }
        }

        function openWorld(worldId) {
            let playerProgress = JSON.parse(sessionStorage.getItem('swipeProgress')) || {};

            if (worldId === 2 && !DEV_UNLOCK_ALL) {
                let w1Stars = 0;
                for (let i = 0; i < 21; i++) w1Stars += (playerProgress[i] || 0);
                if (w1Stars < 42) {
                    const card = document.getElementById('world-card-2');
                    card.style.transform = 'translate(-5px, 0)';
                    setTimeout(() => card.style.transform = 'translate(5px, 0)', 50);
                    setTimeout(() => card.style.transform = 'translate(-5px, 0)', 100);
                    setTimeout(() => card.style.transform = 'translate(0, 0)', 150);
                    return;
                }
            }
            if (worldId === 3 && !DEV_UNLOCK_ALL) {
                let w2Stars = 0;
                for (let i = 21; i < 42; i++) w2Stars += (playerProgress[i] || 0);
                if (w2Stars < 42) {
                    const card = document.getElementById('world-card-3');
                    card.style.transform = 'translate(-5px, 0)';
                    setTimeout(() => card.style.transform = 'translate(5px, 0)', 50);
                    setTimeout(() => card.style.transform = 'translate(-5px, 0)', 100);
                    setTimeout(() => card.style.transform = 'translate(0, 0)', 150);
                    return;
                }
            }

            document.getElementById('worlds-view').style.display = 'none';
            document.getElementById('levels-view').style.display = 'block';
            document.getElementById('current-world-title').textContent = `World ${worldId}`;

            const container = document.getElementById('world-levels-container');
            container.innerHTML = '';

            levels.forEach((level, index) => {
                const isWorld1 = index < 21;
                const isWorld2 = index >= 21 && index < 42;
                const isWorld3 = index >= 42;

                if ((worldId === 1 && isWorld1) || (worldId === 2 && isWorld2) || (worldId === 3 && isWorld3)) {
                    const btn = document.createElement('button');
                    btn.className = 'btn-level' + (isWorld2 || isWorld3 ? ' world-2' : '');

                    let starsCount = playerProgress[index] || 0;
                    let starsText = '';
                    if (starsCount > 0) {
                        starsText = '<div class="level-stars">';
                        for (let i = 0; i < 3; i++) {
                            starsText += i < starsCount ? '★' : '☆';
                        }
                        starsText += '</div>';
                    }

                    let localIndex = index;
                    if (isWorld2) localIndex = index - 21;
                    if (isWorld3) localIndex = index - 42;
                    btn.innerHTML = `<div>${localIndex + 1}</div>${starsText}`;

                    btn.onclick = () => {
                        currentLevelIndex = index;
                        document.getElementById('main-menu').style.display = 'none';
                        initLevel();
                    };

                    container.appendChild(btn);
                }
            });
        }
"""
# Replace the JS logic functions
pattern_js = r'function showWorldsView\(\) \{.*function showMainMenu\(\)'
new_html = re.sub(pattern_js, js_logic.strip() + '\n\n        function showMainMenu()', new_html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
print('Done!')
