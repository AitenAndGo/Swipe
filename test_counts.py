with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('const levels = ')
end = html.find('let currentLevelIndex')

if start != -1 and end != -1:
    levels_str = html[start+len('const levels = '):end].strip()
    if levels_str.endswith(';'):
        levels_str = levels_str[:-1]
    with open('temp_levels.py', 'w', encoding='utf-8') as tf:
        tf.write('lvls = ' + levels_str)
else:
    print("Could not find levels")

import sys
try:
    from temp_levels import lvls
except ImportError:
    print("Failed to import lvls")
    sys.exit(1)
    
print('Total levels in index.html:', len(lvls))

w1_count = 0
w2_count = 0
w3_count = 0

for lvl in lvls:
    has_g = any('G' in row or 'g' in row for row in lvl['layout'])
    has_2 = any(2 in row for row in lvl['layout'])
    if has_2:
        w3_count += 1
    elif has_g:
        w2_count += 1
    else:
        w1_count += 1

print(f'W1: {w1_count}, W2: {w2_count}, W3: {w3_count}')
