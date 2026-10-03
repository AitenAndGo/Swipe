import json
import re

with open('generated_levels.json', 'r') as f:
    text = f.read()
    # It has valid JS/Python syntax (with single quotes). eval works for parsing it!
    levels = eval(text)

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
new_levels.extend(levels[0:20])
new_levels.append(w2_tut)
new_levels.extend(levels[20:40])
new_levels.append(w3_tut)
new_levels.extend(levels[40:60])

with open('generated_levels_new.json', 'w') as f:
    f.write('[\n')
    for i, level in enumerate(new_levels):
        f.write('  {\n')
        f.write(f'    "stars": {json.dumps(level["stars"])},\n')
        f.write('    "layout": [\n')
        for j, row in enumerate(level['layout']):
            row_str = "[" + ", ".join(f"'{x}'" if isinstance(x, str) else str(x) for x in row) + "]"
            f.write(f'      {row_str}{"," if j < len(level["layout"])-1 else ""}\n')
        f.write('    ]\n')
        f.write(f'  }}{"," if i < len(new_levels)-1 else ""}\n')
    f.write(']\n')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('generated_levels_new.json', 'r') as f:
    levels_json = f.read()

pattern = r'const levels = \[.*?\];\n\n        let currentLevelIndex'
replacement = 'const levels = ' + levels_json + ';\n\n        let currentLevelIndex'
new_html = re.sub(pattern, replacement, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
print('Done!')
