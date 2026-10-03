import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_css = '''        :root {
            --cell-size: 45px;
            --bg-color: #f7f7f7;
            --text-color: #333333;
            --grid-line-color: #e8e8e8;
            
            /* Mini Metro Colors */
            --color-red: #eb5e5e;
            --color-blue: #4db8ff;
            --color-green: #68cc76;
            --color-box: #f5a623;
            --color-wall: #d6d6d6;
            
            --border-radius: 6px;
        }

        body {
            font-family: 'Inter', 'Segoe UI', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding-top: 20px;
            touch-action: none;
            overflow: hidden;
        }

        h1 {
            margin: 0 0 10px 0;
            font-weight: 700;
            font-size: 28px;
            letter-spacing: -0.5px;
            color: var(--text-color);
        }

        p {
            margin-bottom: 20px;
            font-size: 15px;
            color: #666;
            font-weight: 500;
        }

        #game-container {
            position: relative;
            background: #ffffff;
            padding: 15px;
            border-radius: var(--border-radius);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(0, 0, 0, 0.05);
        }

        #game-board {
            display: grid;
            position: relative;
            background-color: var(--bg-color);
            border-radius: 4px;
            overflow: hidden;
        }

        .cell {
            width: var(--cell-size);
            height: var(--cell-size);
            box-sizing: border-box;
            border: 1px solid var(--grid-line-color);
        }

        .wall {
            background-color: var(--color-wall);
            border: none;
            border-radius: 0;
        }

        .target {
            position: relative;
        }

        .target::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: calc(var(--cell-size) * 0.45);
            height: calc(var(--cell-size) * 0.45);
            border-radius: 50%;
            background-color: transparent;
            border-width: 4px;
            border-style: solid;
            box-sizing: border-box;
        }

        @keyframes pulse-target {
            0% { transform: translate(-50%, -50%) scale(1); }
            50% { transform: translate(-50%, -50%) scale(1.1); }
            100% { transform: translate(-50%, -50%) scale(1); }
        }

        .target.red-target::after {
            border-color: var(--color-red);
            animation: pulse-target 2s infinite ease-in-out;
        }

        .target.blue-target::after {
            border-color: var(--color-blue);
            animation: pulse-target 2s infinite ease-in-out 0.6s;
        }

        .target.green-target::after {
            border-color: var(--color-green);
            animation: pulse-target 2s infinite ease-in-out 1.2s;
        }

        .block {
            position: absolute;
            width: calc(var(--cell-size) - 14px);
            height: calc(var(--cell-size) - 14px);
            margin: 7px;
            border-radius: 50%;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
            z-index: 10;
            box-sizing: border-box;
        }

        .block.red { background-color: var(--color-red); }
        .block.blue { background-color: var(--color-blue); }
        .block.green { background-color: var(--color-green); }

        .block.active {
            transform: scale(1.3);
            z-index: 11;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }

        .movable-box {
            position: absolute;
            width: calc(var(--cell-size) - 6px);
            height: calc(var(--cell-size) - 6px);
            margin: 3px;
            border-radius: 4px;
            background-color: var(--color-box);
            transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
            z-index: 8;
            box-sizing: border-box;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            font-size: 16px;
        }
        
        .movable-box::after {
            content: '■';
            opacity: 0.4;
        }

        .controls {
            margin-top: 25px;
            display: flex;
            gap: 15px;
        }

        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 30px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.1s, opacity 0.2s, box-shadow 0.2s;
            color: white;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }

        .btn:active {
            transform: translateY(2px);
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .btn:hover { opacity: 0.9; }

        .btn-red { background-color: var(--color-red); }
        .btn-blue { background-color: var(--color-blue); }
        .btn-green { background-color: var(--color-green); }
        .btn-restart { background-color: #95a5a6; }

        #message {
            margin-top: 20px;
            font-size: 20px;
            font-weight: bold;
            color: var(--text-color);
            height: 30px;
        }

        @keyframes shake {
            0% { transform: translate(0, 0); }
            20% { transform: translate(-3px, 2px); }
            40% { transform: translate(3px, -2px); }
            60% { transform: translate(-3px, -2px); }
            80% { transform: translate(3px, 2px); }
            100% { transform: translate(0, 0); }
        }

        .shake { animation: shake 0.2s; }

        .swipe-trail {
            position: absolute;
            opacity: 0.6;
            z-index: 4;
            pointer-events: none;
            border-radius: 6px;
            transition: width 0.2s cubic-bezier(0.25, 0.8, 0.25, 1),
                height 0.2s cubic-bezier(0.25, 0.8, 0.25, 1),
                left 0.2s cubic-bezier(0.25, 0.8, 0.25, 1),
                top 0.2s cubic-bezier(0.25, 0.8, 0.25, 1),
                opacity 0.3s ease-out;
        }

        .swipe-trail.red { background: var(--color-red); }
        .swipe-trail.blue { background: var(--color-blue); }
        .swipe-trail.green { background: var(--color-green); }

        @keyframes shake-block {
            0% { transform: scale(1.05) translate(0, 0); }
            20% { transform: scale(1.05) translate(-1px, 1px); }
            40% { transform: scale(1.05) translate(1px, -1px); }
            60% { transform: scale(1.05) translate(-1px, -1px); }
            80% { transform: scale(1.05) translate(1px, 1px); }
            100% { transform: scale(1.05) translate(0, 0); }
        }

        .shake-block { animation: shake-block 0.15s; }

        .impact-particle {
            position: absolute;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            pointer-events: none;
            z-index: 12;
            transition: opacity 0.3s ease-out, transform 0.3s ease-out;
        }

        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(255, 255, 255, 0.9);
            z-index: 100;
            align-items: center;
            justify-content: center;
        }

        .modal-content {
            background: #ffffff;
            border: none;
            padding: 40px 50px;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.08);
            color: var(--text-color);
            transform: scale(0.9);
            opacity: 0;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }

        .modal.show { display: flex; }
        .modal.show .modal-content {
            transform: scale(1);
            opacity: 1;
        }

        .stars {
            font-size: 40px;
            color: #f1c40f;
            margin: 15px 0;
            letter-spacing: 5px;
        }

        .header-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            max-width: 450px;
            margin-bottom: 15px;
        }

        .header-info h1 {
            margin: 0;
            font-family: 'Inter', sans-serif;
            font-size: 24px;
        }

        .steps-counter {
            font-family: 'Inter', sans-serif;
            font-size: 16px;
            font-weight: 600;
            background: #e8e8e8;
            color: #333;
            padding: 8px 16px;
            border-radius: 30px;
        }

        .worlds-container {
            display: flex;
            flex-direction: column;
            gap: 15px;
            text-align: left;
            width: 100%;
        }

        .world-card {
            position: relative;
            height: 100px;
            border-radius: 12px;
            overflow: hidden;
            cursor: pointer;
            background: #ffffff;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.2s;
            border: 1px solid #eaeaea;
        }

        .world-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }

        .world-card-bg {
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 15px;
        }

        .world-card.locked {
            cursor: not-allowed;
            opacity: 0.6;
            filter: grayscale(100%);
        }

        .world-card.locked:hover {
            transform: none;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        }

        .locked-overlay {
            position: absolute;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 24px;
            color: #999;
            opacity: 0;
        }

        .world-card.locked .locked-overlay {
            opacity: 1;
        }

        .bg-world-1 { background-color: var(--color-blue); }
        .bg-world-2 { background-color: var(--color-green); }
        .bg-world-3 { background-color: var(--color-red); }

        .world-card-content {
            position: relative;
            padding: 15px 20px 15px 40px;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-sizing: border-box;
        }

        .world-card-content h2 {
            margin: 0 0 5px 0;
            font-size: 22px;
            color: var(--text-color);
            font-weight: 700;
        }

        .world-card-content p {
            margin: 0;
            font-size: 14px;
            color: #7f8c8d;
        }

        .progress-text {
            position: absolute;
            right: 20px;
            bottom: 20px;
            font-weight: 700;
            font-size: 14px;
            color: #95a5a6;
        }

        .btn-back {
            background: transparent;
            color: var(--text-color);
            border: none;
            padding: 8px 15px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            font-size: 16px;
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .btn-back:hover {
            background: rgba(0,0,0,0.05);
        }

        .level-grid {
            display: flex;
            gap: 12px;
            justify-content: center;
            flex-wrap: wrap;
            padding: 10px;
        }

        .btn-level {
            width: 65px;
            height: 65px;
            border-radius: 12px;
            background: #ffffff;
            color: var(--text-color);
            font-size: 20px;
            font-weight: 700;
            border: 2px solid #e0e0e0;
            cursor: pointer;
            transition: all 0.15s ease;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }

        .btn-level:hover {
            border-color: var(--color-blue);
            color: var(--color-blue);
            transform: translateY(-2px);
            box-shadow: 0 5px 12px rgba(77, 184, 255, 0.2);
        }

        .btn-level.world-2:hover {
            border-color: var(--color-green);
            color: var(--color-green);
            box-shadow: 0 5px 12px rgba(104, 204, 118, 0.2);
        }

        .level-stars {
            font-size: 12px;
            color: #f1c40f;
            margin-top: 4px;
            letter-spacing: 1px;
        }

        .btn-menu {
            background-color: var(--color-box);
            color: white;
        }'''

html = re.sub(r':root\s*\{.*?</style>', new_css + '\n    </style>', html, flags=re.DOTALL)

# Inline style removals using precise strings matching the actual file contents.
html = html.replace('style="background: radial-gradient(circle at center, #1b2838 0%, #000000 100%); z-index: 200;"', 'style="z-index: 200;"')
html = html.replace('style="width: 100%; max-width: 650px; padding: 40px 30px; transform: scale(1); opacity: 1; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 20px 60px rgba(0,0,0,0.9), inset 0 2px 10px rgba(255,255,255,0.05); background: rgba(20, 30, 40, 0.85); backdrop-filter: blur(20px);"', 'style="width: 100%; max-width: 650px; padding: 40px 30px;"')
html = html.replace('style="font-size: 48px; margin-bottom: 10px; color: #fff; text-shadow: 0 0 20px rgba(52, 152, 219, 0.6), 0 5px 10px rgba(0,0,0,0.8); font-family: \'Orbitron\', sans-serif; letter-spacing: 4px;"', 'style="font-size: 48px; margin-bottom: 10px; color: var(--text-color); font-weight: 800; letter-spacing: -2px;"')
html = html.replace('style="color: #bdc3c7; margin-bottom: 40px; font-weight: 300; font-size: 18px; letter-spacing: 1px;"', 'style="color: #666; margin-bottom: 40px; font-weight: 500; font-size: 18px;"')
html = html.replace('style="margin: 0; font-size: 28px; color: #fff; text-shadow: 0 2px 5px rgba(0,0,0,0.5); font-family: \'Orbitron\', sans-serif;"', 'style="margin: 0; font-size: 24px; color: var(--text-color); font-weight: 700;"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
