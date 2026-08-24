# -*- coding: utf-8 -*-
"""
Production builder for GATE Tracker Pro index.html
"""

import os

def build():
    with open('create_complete_app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    marker = '<!-- ======================================================== -->\n  <!-- GATE TRACKER PRO COMPLETE CORE ENGINE SCRIPT -->'
    js_start = content.find(marker)
    end_marker = '</script>\n</body>\n</html>'
    js_end = content.rfind(end_marker)

    if js_start == -1 or js_end == -1:
        print("Error locating JS block in create_complete_app.py", js_start, js_end)
        return

    js_block = content[js_start:js_end + len(end_marker)]

    with open('create_app.py', 'r', encoding='utf-8') as f:
        app_content = f.read()

    html_start = app_content.find('<!DOCTYPE html>')
    html_marker = '<!-- Core App Logic Script Included in Part 2 -->'
    html_end = app_content.find(html_marker)

    if html_start == -1 or html_end == -1:
        print("Error locating HTML block in create_app.py", html_start, html_end)
        return

    html_block = app_content[html_start:html_end]

    full_output = html_block + "\n" + js_block

    target = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
    with open(target, 'w', encoding='utf-8') as f:
        f.write(full_output)

    print(f"Clean index.html built successfully: {len(full_output)} bytes ({full_output.count(chr(10))} lines)")

if __name__ == '__main__':
    build()
