import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
    
match = re.search(r'const levels = (\[.*?\]);', html, flags=re.DOTALL)
if match:
    with open('t.py', 'w') as tf:
        tf.write('l = ' + match.group(1))

try:
    from t import l
    print('Levels length:', len(l))
    print('Level 0:', l[0])
    print('Level 21:', l[21])
    print('Level 42:', l[42])
except Exception as e:
    print('Error:', e)
