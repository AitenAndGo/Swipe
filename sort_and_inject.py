import json
import re

with open('generated_levels.json', 'r', encoding='utf-8') as f:
    text = f.read()
    levels = eval(text)

w1 = levels[0:20]
w2 = levels[20:40]
w3 = levels[40:60]

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

levels_json = "[\n"
for i, level in enumerate(new_levels):
    levels_json += '        {\n'
    levels_json += f'            "stars": {json.dumps(level["stars"])},\n'
    levels_json += '            "layout": [\n'
    for j, row in enumerate(level['layout']):
        row_str = "[" + ", ".join(f"'{x}'" if isinstance(x, str) else str(x) for x in row) + "]"
        levels_json += f'                {row_str}{"," if j < len(level["layout"])-1 else ""}\n'
    levels_json += '            ]\n'
    levels_json += f'        }}{"," if i < len(new_levels)-1 else ""}\n'
levels_json += '    ]'

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = r'const levels = \[.*?\];'
replacement = 'const levels = ' + levels_json + ';'
html = re.sub(pattern, replacement, html, count=1, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Levels replaced!")
