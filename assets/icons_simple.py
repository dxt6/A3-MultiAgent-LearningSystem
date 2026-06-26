"""
简化版手绘图标系统 - 使用更可靠的渲染方式
"""

def get_icon_html(icon_name, size=24, color="#ffffff"):
    """
    获取手绘图标的HTML代码（简化版 - 使用emoji作为备用）
    如果SVG渲染有问题，可以切换到emoji模式
    """
    
    # SVG图标映射（简化版，只保留核心图标）
    svg_icons = {
        'robot': f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><circle cx="9" cy="10" r="1.5" fill="{color}"/><circle cx="15" cy="10" r="1.5" fill="{color}"/><path d="M8 16 Q12 19 16 16"/></svg>',
        
        'brain': f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round"><path d="M12 3 C8 3,5 6,5 10 C5 13,7 15,8 16 C7 17,7 19,9 20 C11 21,12 20,12 19 C12 20,13 21,15 20 C17 19,17 17,16 16 C17 15,19 13,19 10 C19 6,16 3,12 3Z"/></svg>',
        
        'book_open': f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.7" stroke-linecap="round"><path d="M12 3 L12 21 M12 4 C7 5,2 7,2 10 L2 18 C2 19,7 21,12 20 M12 4 C17 5,22 7,22 10 L22 18 C22 19,17 21,12 20"/></svg>',
        
        'gear': f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.7" stroke-linecap="round"><circle cx="12" cy="12" r="3"/><path d="M12 2 L12 6 M12 18 L12 22 M2 12 L6 12 M18 12 L22 12 M4.5 4.5 L7 7 M17 17 L19.5 19.5 M19.5 4.5 L17 7 M7 17 L4.5 19.5"/></svg>',
        
        'map': f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.7" stroke-linecap="round"><path d="M1 6 L1 22 L8 18 L16 21 L23 17 L23 1 L16 5 L8 2 Z"/><path d="M8 2 L8 18 M16 5 L16 21"/></svg>',
        
        'check': f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round"><path d="M4 12 L9 17 L20 6"/></svg>',
        
        'target': f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2" fill="{color}"/></svg>',
        
        'chat': f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.7" stroke-linecap="round"><path d="M21 15 C21 16,20 17,19 17 L8 17 C7 17,6 18,6 19 L6 21 L9 19 L19 19 C20 19,21 18,21 17 Z M3 3 L21 3 C22 3,23 4,23 5 L23 15 C23 16,22 17,21 17 L5 17 L3 19 L3 5 C3 4,4 3,5 3 Z"/></svg>',
    }
    
    # 如果图标存在，返回SVG
    if icon_name in svg_icons:
        return f'<span style="display:inline-flex;align-items:center;">{svg_icons[icon_name]}</span>'
    
    # 备用：使用emoji
    emoji_fallback = {
        'robot': '🤖', 'brain': '🧠', 'book_open': '📖', 
        'gear': '⚙️', 'map': '🗺️', 'check': '✅',
        'target': '🎯', 'chat': '💬'
    }
    
    if icon_name in emoji_fallback:
        return f'<span style="font-size:{size}px;">{emoji_fallback[icon_name]}</span>'
    
    # 默认返回一个简单的圆形
    return f'<span style="display:inline-flex;align-items:center;"><svg width="{size}" height="{size}" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8" fill="{color}" opacity="0.5"/></svg></span>'


# 为了兼容原有代码，提供相同的接口
def icon_html(icon_name, size=24, color="#ffffff"):
    """原有接口 - 调用新的简化函数"""
    return get_icon_html(icon_name, size, color)


HANDDRAWN_ICONS_PY = {
    'robot': icon_html('robot'),
    'brain': icon_html('brain'),
    'book_open': icon_html('book_open'),
    'gear': icon_html('gear'),
    'map': icon_html('map'),
    'check': icon_html('check'),
    'target': icon_html('target'),
    'chat': icon_html('chat'),
}
