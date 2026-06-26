"""
手绘图标 Streamlit 集成助手
使用方法：
    from assets.handdrawn_icons_helper import render_icon, icon_html
    st.markdown(icon_html('robot', 24, '#ffffff'), unsafe_allow_html=True)
"""

import base64
import json
import os

# 图标 JS 文件路径
_ICONS_JS_PATH = os.path.join(os.path.dirname(__file__), 'handdrawn_icons.js')

# 缓存图标 SVG 字符串
_ICON_CACHE = {}


def _load_icons():
    """从 JS 文件中提取图标 SVG 字符串"""
    if _ICON_CACHE:
        return _ICON_CACHE
    
    # 由于 JS 文件包含对象字面量，这里用简单方法解析
    # 实际使用时建议将图标单独存为 SVG 文件或 JSON
    with open(_ICONS_JS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 简单解析：找到 HANDDRAWN_ICONS 对象
    # 这里返回一个空字典，实际使用时需要正确解析
    # 建议直接将图标保存为单独的 SVG 文件
    
    return _ICON_CACHE


def get_icon_svg(icon_name, size=24, color='currentColor'):
    """
    获取图标 SVG 字符串
    
    Args:
        icon_name: 图标名称（如 'robot', 'brain' 等）
        size: 图标尺寸（默认 24）
        color: 图标颜色（默认 'currentColor'，可用 'white', '#ffffff' 等）
    
    Returns:
        SVG 字符串
    """
    # 图标定义字典（从 JS 文件同步）
    # 注意：实际使用时请从 handdrawn_icons.js 正确导入
    icons = _parse_icons_from_js()
    
    if icon_name not in icons:
        return f'<span style="color:red;">Icon not found: {icon_name}</span>'
    
    svg = icons[icon_name]
    
    # 替换颜色
    if color != 'currentColor':
        svg = svg.replace('stroke="currentColor"', f'stroke="{color}"')
        svg = svg.replace('fill="currentColor"', f'fill="{color}"')
    
    # 设置尺寸
    if size != 24:
        svg = svg.replace('viewBox="0 0 24 24"', f'width="{size}" height="{size}" viewBox="0 0 24 24"')
    
    return svg


def icon_html(icon_name, size=24, color='#ffffff', valign='middle'):
    """
    生成可直接用于 st.markdown 的 HTML
    
    Args:
        icon_name: 图标名称
        size: 尺寸
        color: 颜色
        valign: 垂直对齐方式
    
    Returns:
        包含图标的 HTML span 标签
    """
    svg = get_icon_svg(icon_name, size, color)
    return f'<span style="display:inline-flex;align-items:{valign};vertical-align:{valign};">{svg}</span>'


def render_icon(st, icon_name, size=24, color='#ffffff'):
    """
    直接在 Streamlit 中渲染图标
    
    Args:
        st: streamlit 模块
        icon_name: 图标名称
        size: 尺寸
        color: 颜色
    """
    html = icon_html(icon_name, size, color)
    st.markdown(html, unsafe_allow_html=True)


def _parse_icons_from_js():
    """
    从 handdrawn_icons.js 解析图标
    
    注意：这是一个简化实现。
    生产环境建议将图标保存为 JSON 或单独 SVG 文件。
    """
    # 由于 JS 对象字面量解析较复杂，这里返回一个提示
    # 实际使用时，请将 handdrawn_icons.js 中的图标复制到此处
    # 或使用 Node.js 运行 JS 文件获取图标
    
    # 读取 JS 文件并尝试提取 SVG 字符串
    js_path = os.path.join(os.path.dirname(__file__), 'handdrawn_icons.js')
    
    if not os.path.exists(js_path):
        return {}
    
    # 简单提取：找到所有 `key: \`<svg ...></svg>\`` 模式
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    icons = {}
    # 使用正则提取图标名称和 SVG
    import re
    pattern = r"(\w+):\s*`(<svg[^>]*viewBox=\"0 0 24 24\"[^>]*>.*?</svg>)`"
    
    # 由于模板字符串可能跨多行，使用更灵活的方法
    lines = content.split('\n')
    current_key = None
    current_svg_lines = []
    in_svg = False
    
    for line in lines:
        if ': `<svg' in line or ': `<svg' in line.replace(' ', ''):
            # 新图标开始
            idx = line.find(': `')
            if idx > 0:
                current_key = line[:idx].strip().replace('  ', '').replace('// ', '')
                # 清理 key
                import re
                key_match = re.search(r'(\w+)$', current_key)
                if key_match:
                    current_key = key_match.group(1)
                current_svg_lines = [line[idx+3:]]  # 跳过 ": `"
                in_svg = True
        elif in_svg:
            current_svg_lines.append(line)
            if '</svg>`' in line:
                # 图标结束
                svg = '\n'.join(current_svg_lines).replace('</svg>`', '</svg>')
                icons[current_key] = svg
                current_key = None
                current_svg_lines = []
                in_svg = False
    
    return icons


# 图标名称列表（用于自动补全）
ICON_NAMES = [
    # 首页模块
    'robot', 'book_open', 'target', 'building', 'rocket', 'info',
    # 学习画像
    'brain', 'chat', 'user', 'card',
    # 资源生成
    'books', 'gear', 'lightning', 'download', 'file',
    # 路径规划
    'map', 'clock', 'chart_bar', 'flag',
    # 质量评估
    'check', 'chart_line', 'magnifier', 'star',
    # 侧边栏
    'nav_home', 'nav_brain', 'nav_book', 'nav_map', 'nav_check',
    # 补充
    'arrow_right', 'arrow_down', 'close', 'menu', 'search',
    'settings', 'bell', 'refresh', 'lock', 'cloud', 'heart',
    'pencil', 'bulb', 'link', 'warning',
]


if __name__ == '__main__':
    # 测试：打印所有图标名称
    print("可用图标列表：")
    for name in ICON_NAMES:
        print(f"  - {name}")
    
    # 测试：获取一个图标
    svg = get_icon_svg('robot', 24, 'white')
    print(f"\n机器人图标 SVG:\n{svg}")
