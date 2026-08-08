#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio, websockets, json, subprocess, time, os, signal

async def check_console():
    # 启动 Chrome
    proc = subprocess.Popen([
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        '--headless', '--disable-gpu', '--no-sandbox', '--disable-setuid-sandbox',
        '--remote-debugging-port=9223',
        'file:///D:/km/MultiUs/MultiUs/index.html'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3)
    
    try:
        # 获取页面 websocket URL
        import urllib.request
        with urllib.request.urlopen('http://127.0.0.1:9223/json/list') as resp:
            pages = json.loads(resp.read())
        if not pages:
            print('no pages')
            return
        ws_url = pages[0]['webSocketDebuggerUrl']
        
        async with websockets.connect(ws_url) as ws:
            # 启用 Runtime console
            await ws.send(json.dumps({'id':1,'method':'Runtime.enable'}))
            await ws.send(json.dumps({'id':2,'method':'Log.enable'}))
            
            # 等页面加载
            await asyncio.sleep(2)
            
            # 收集 console 消息
            logs = []
            try:
                while True:
                    msg = await asyncio.wait_for(ws.recv(), timeout=2)
                    data = json.loads(msg)
                    if data.get('method') in ('Runtime.consoleAPICalled', 'Log.entryAdded'):
                        logs.append(data)
            except asyncio.TimeoutError:
                pass
            
            if logs:
                print(f'CONSOLE MESSAGES ({len(logs)}):')
                for log in logs:
                    print(json.dumps(log, ensure_ascii=False)[:500])
            else:
                print('CONSOLE ZERO ERRORS (no messages)')
    finally:
        proc.terminate()
        proc.wait(timeout=5)

asyncio.run(check_console())
