/**
 * 手绘速写风功能图标集
 * 风格：线条抖动、粗细不均、带毛边、局部断开
 * 全部白色单色线条，viewBox="0 0 24 24"
 */

const HANDDRAWN_ICONS = {

  // ========== 1. 首页模块图标（6个）==========

  // 机器人图标 - 头部方形带天线，身体矩形，线条抖动
  robot: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
    <!-- 天线 -->
    <line x1="9" y1="2" x2="7" y2="5" stroke-width="1.4"/>
    <line x1="15" y1="2" x2="17" y2="5" stroke-width="1.4"/>
    <circle cx="8" cy="2" r="1.2" stroke-width="1.1"/>
    <circle cx="16" cy="2" r="1.2" stroke-width="1.1"/>
    <!-- 头部 -->
    <path d="M5.5 5.5 C5.5 5, 6 4.5, 6.5 4.5 L17.5 4.5 C18 4.5, 18.5 5, 18.5 5.5 L18.5 11.5 C18.5 12, 18 12.5, 17.5 12.5 L6.5 12.5 C6 12.5, 5.5 12, 5.5 11.5 Z" stroke-width="1.9"/>
    <!-- 眼睛 -->
    <circle cx="9.5" cy="8" r="1.5" stroke-width="1.3"/>
    <circle cx="14.5" cy="8" r="1.5" stroke-width="1.3"/>
    <circle cx="9.5" cy="7.7" r="0.5" fill="currentColor" stroke="none"/>
    <circle cx="14.5" cy="7.7" r="0.5" fill="currentColor" stroke="none"/>
    <!-- 嘴巴 -->
    <path d="M9 10.5 Q12 12, 15 10.5" stroke-width="1.2"/>
    <!-- 身体 -->
    <path d="M8 13 L8 19 C8 20, 8.5 20.5, 9 20.5 L15 20.5 C15.5 20.5, 16 20, 16 19 L16 13" stroke-width="1.7"/>
    <!-- 手臂 -->
    <path d="M8 15 L4.5 17" stroke-width="1.6"/>
    <path d="M16 15 L19.5 17" stroke-width="1.6"/>
    <!-- 腿部 -->
    <path d="M10.5 20.5 L9.5 23" stroke-width="1.5"/>
    <path d="M13.5 20.5 L14.5 23" stroke-width="1.5"/>
  </svg>`,

  // 书籍图标（首页版）- 打开的书本，线条自然
  book_open: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <!-- 书脊 -->
    <path d="M12 3.5 C12 3.5, 11.8 12, 12 20.5" stroke-width="2.0"/>
    <!-- 左页 -->
    <path d="M11.8 4 C7 4.5, 3.5 6, 2.5 7.5 C2 8.2, 2 9, 2 9.5 L2 18 C2 19, 2.5 19.5, 3.5 19.5 C6 19.5, 9 19, 11.8 18.5" stroke-width="1.6"/>
    <!-- 右页 -->
    <path d="M12.2 4 C17 4.5, 20.5 6, 21.5 7.5 C22 8.2, 22 9, 22 9.5 L22 18 C22 19, 21.5 19.5, 20.5 19.5 C18 19.5, 15 19, 12.2 18.5" stroke-width="1.6"/>
    <!-- 左页横线 -->
    <path d="M4 10.5 L10.5 9.8" stroke-width="0.9"/>
    <path d="M4.2 13 L10.5 12.3" stroke-width="0.9"/>
    <path d="M5 15.5 L10 15" stroke-width="0.9"/>
    <!-- 右页横线 -->
    <path d="M13.5 9.8 L20 10.5" stroke-width="0.9"/>
    <path d="M13.5 12.3 L20 13" stroke-width="0.9"/>
    <path d="M14 15 L19 15.5" stroke-width="0.9"/>
  </svg>`,

  // 目标图标 - 靶心，线条不完美
  target: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
    <!-- 外圈 -->
    <circle cx="12" cy="12" r="10" stroke-width="1.8"/>
    <!-- 中圈 -->
    <circle cx="12" cy="12" r="6.5" stroke-width="1.5"/>
    <!-- 内圈 -->
    <circle cx="12.3" cy="11.8" r="3" stroke-width="1.3"/>
    <!-- 中心点 -->
    <circle cx="12.3" cy="11.8" r="0.8" fill="currentColor" stroke="none"/>
    <!-- 十字线 -->
    <line x1="12.3" y1="1.5" x2="12.3" y2="5" stroke-width="1.2"/>
    <line x1="12.3" y1="19" x2="12.3" y2="22.5" stroke-width="1.2"/>
    <line x1="1.5" y1="11.8" x2="5" y2="11.8" stroke-width="1.2"/>
    <line x1="19" y1="11.8" x2="22.5" y2="11.8" stroke-width="1.2"/>
  </svg>`,

  // 建筑图标 - 简易楼房，手绘感
  building: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <!-- 主楼体 -->
    <path d="M4 22 L4 6 C4 5, 4.5 4, 5.5 3.8 L12 2 L18.5 3.8 C19.5 4, 20 5, 20 6 L20 22" stroke-width="1.9"/>
    <!-- 楼层线 -->
    <line x1="4.3" y1="9" x2="19.7" y2="9" stroke-width="1.2"/>
    <line x1="4.5" y1="13.5" x2="19.5" y2="13.5" stroke-width="1.2"/>
    <line x1="4.8" y1="18" x2="19.2" y2="18" stroke-width="1.2"/>
    <!-- 窗户 -->
    <rect x="6" y="10" width="3" height="2.5" rx="0.2" stroke-width="1.1"/>
    <rect x="10.5" y="10" width="3" height="2.5" rx="0.2" stroke-width="1.1"/>
    <rect x="15" y="10" width="3" height="2.5" rx="0.2" stroke-width="1.1"/>
    <rect x="6" y="14.8" width="3" height="2.5" rx="0.2" stroke-width="1.1"/>
    <rect x="10.5" y="14.8" width="3" height="2.5" rx="0.2" stroke-width="1.1"/>
    <rect x="15" y="14.8" width="3" height="2.5" rx="0.2" stroke-width="1.1"/>
    <!-- 门 -->
    <path d="M10.5 22 L10.5 17.5 C10.5 16.5, 11 16, 11.5 16 L12.5 16 C13 16, 13.5 16.5, 13.5 17.5 L13.5 22" stroke-width="1.4"/>
  </svg>`,

  // 火箭图标 - 上升火箭，线条抖动
  rocket: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <!-- 箭体 -->
    <path d="M12 2 C11 3, 9.5 5, 9 7 L7.5 15 C7.3 16, 7.8 16.5, 8.5 16.3 L11 15.5 L12 22 L13 15.5 L15.5 16.3 C16.2 16.5, 16.7 16, 16.5 15 L15 7 C14.5 5, 13 3, 12 2Z" stroke-width="1.8"/>
    <!-- 窗户 -->
    <circle cx="12" cy="9" r="1.8" stroke-width="1.3"/>
    <circle cx="12" cy="9" r="0.6" fill="currentColor" stroke="none"/>
    <!-- 左翼 -->
    <path d="M9 15 L6.5 19 L8.5 18.5" stroke-width="1.5"/>
    <!-- 右翼 -->
    <path d="M15 15 L17.5 19 L15.5 18.5" stroke-width="1.5"/>
    <!-- 尾焰 -->
    <path d="M11 22 Q10.5 24, 9 25" stroke-width="1.2" stroke-dasharray="1 1.5"/>
    <path d="M13 22 Q13.5 24, 15 25" stroke-width="1.2" stroke-dasharray="1 1.5"/>
    <path d="M12 22 Q12 24.5, 12 26" stroke-width="1.0" stroke-dasharray="0.8 1.2"/>
  </svg>`,

  // 信息图标 - 圆圈内加i，手绘
  info: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <!-- 圆圈 -->
    <circle cx="12" cy="12" r="10" stroke-width="1.8"/>
    <!-- i的圆点 -->
    <circle cx="12" cy="8" r="1.2" fill="currentColor" stroke="none"/>
    <!-- i的竖线 -->
    <line x1="12" y1="11" x2="12" y2="17" stroke-width="1.8"/>
  </svg>`,

  // ========== 2. 学习画像模块图标（4个）==========

  // 大脑图标 - 不对称脑沟回
  brain: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
    <!-- 大脑外轮廓（不对称） -->
    <path d="M12 3.5 C8.5 3.5, 5.5 5.5, 5 8.5 C4.5 11, 5.5 12.5, 6 13.5 C5 14.5, 4.5 16, 5 17.5 C5.8 20, 8.5 21, 11 20.5 C11.5 21.5, 13 22, 14.5 21.5 C17 20.5, 18.5 18, 18.5 15.5 C19 13, 20 11, 18.5 9 C17.5 7, 15 4, 12 3.5Z" stroke-width="1.8"/>
    <!-- 左脑回 -->
    <path d="M8.5 7.5 Q7 9.5, 8 11.5" stroke-width="1.1"/>
    <path d="M7.5 12 Q6 14, 7.5 15.5" stroke-width="1.1"/>
    <path d="M9 10 Q7.5 11.5, 8.5 13" stroke-width="0.9"/>
    <!-- 右脑回 -->
    <path d="M15.5 7.5 Q17 9.5, 16 11.5" stroke-width="1.1"/>
    <path d="M16.5 12 Q18 14, 16.5 15.5" stroke-width="1.1"/>
    <path d="M15 10 Q16.5 11.5, 15.5 13" stroke-width="0.9"/>
    <!-- 脑中线 -->
    <path d="M12 4.5 Q11.8 9, 12.2 13 Q12.5 16, 12 19.5" stroke-width="1.0" stroke-dasharray="2 1"/>
  </svg>`,

  // 对话气泡图标 - 线条不均匀
  chat: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <!-- 气泡主体 -->
    <path d="M4 4.5 C4 3.5, 4.8 3, 5.5 3 L18.5 3 C19.2 3, 20 3.5, 20 4.5 L20 15.5 C20 16.5, 19.2 17, 18.5 17 L11 17 L6.5 20.5 L8 16.5 L5.5 16.5 C4.8 16.5, 4 16, 4 15 Z" stroke-width="1.8"/>
    <!-- 省略号 -->
    <circle cx="8.5" cy="9.5" r="1" fill="currentColor" stroke="none"/>
    <circle cx="12" cy="9.5" r="1" fill="currentColor" stroke="none"/>
    <circle cx="15.5" cy="9.5" r="1" fill="currentColor" stroke="none"/>
  </svg>`,

  // 用户图标 - 简笔画风格
  user: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <!-- 头部 -->
    <circle cx="12" cy="7" r="4.5" stroke-width="1.8"/>
    <!-- 身体 -->
    <path d="M4.5 22 C4.5 16.5, 7.5 13, 12 13 C16.5 13, 19.5 16.5, 19.5 22" stroke-width="1.8"/>
  </svg>`,

  // 卡片图标 - 带手绘阴影
  card: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
    <!-- 卡片主体 -->
    <path d="M3 4.5 C3 3.5, 3.8 3, 4.5 3 L19.5 3 C20.2 3, 21 3.5, 21 4.5 L21 19.5 C21 20.2, 20.2 21, 19.5 21 L4.5 21 C3.8 21, 3 20.2, 3 19.5 Z" stroke-width="1.8"/>
    <!-- 手绘阴影线 -->
    <path d="M4.5 21.5 L22 21.5" stroke-width="1.1" stroke-dasharray="0.8 0.5"/>
    <path d="M21.5 4.5 L22.2 22" stroke-width="1.1" stroke-dasharray="0.8 0.5"/>
    <!-- 芯片 -->
    <rect x="5" y="7" width="5" height="3.5" rx="0.3" stroke-width="1.2"/>
    <line x1="7.2" y1="7" x2="7.2" y2="10.5" stroke-width="0.8"/>
    <line x1="9.3" y1="7" x2="9.3" y2="10.5" stroke-width="0.8"/>
    <!-- 线条 -->
    <line x1="5" y1="14" x2="14" y2="14" stroke-width="1.2"/>
    <line x1="5" y1="16.5" x2="11" y2="16.5" stroke-width="1.0"/>
  </svg>`,

  // ========== 3. 资源生成模块图标（5个）==========

  // 书籍图标（资源版）- 堆叠书本，与首页差异化
  books: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
    <!-- 后侧书本 -->
    <path d="M3 6.5 C3 5.5, 3.8 5, 4.5 5 L12 4.5 C12.8 4.5, 13.5 5, 13.5 6 L13.5 19 C13.5 19.8, 12.8 20.5, 12 20.5 L4.5 20 C3.8 20, 3 19.5, 3 18.5 Z" stroke-width="1.5"/>
    <path d="M5 8.5 L11 8" stroke-width="0.8"/>
    <path d="M5.2 11 L11 10.5" stroke-width="0.8"/>
    <path d="M5.5 13.5 L10.5 13.2" stroke-width="0.8"/>
    <!-- 前侧书本 -->
    <path d="M10.5 5.5 C11.2 5.5, 12 5, 12.5 4.5 L19.5 4 C20.2 4, 21 4.5, 21 5.5 L21 18.5 C21 19.2, 20.2 20, 19.5 20 L12.5 19.5 C11.8 19.5, 11 19, 10.5 18 Z" stroke-width="1.7"/>
    <path d="M12.5 7.5 L19 7" stroke-width="0.8"/>
    <path d="M12.8 10 L19.2 9.5" stroke-width="0.8"/>
    <path d="M13 12.5 L18.5 12.2" stroke-width="0.8"/>
    <!-- 书签 -->
    <path d="M16 4.5 L16 9 L17.5 7.5 L19 9 L19 4.5" stroke-width="1.0"/>
  </svg>`,

  // 齿轮图标 - 齿轮齿不规则（简化手绘版）
  gear: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <!-- 内圈 -->
    <circle cx="12" cy="12" r="3.5" stroke-width="1.6"/>
    <!-- 齿（不规则分布） -->
    <line x1="12" y1="1.5" x2="12" y2="3.5" stroke-width="1.3"/>
    <line x1="17.5" y1="2.5" x2="16" y2="4.5" stroke-width="1.3"/>
    <line x1="21" y1="6" x2="19" y2="7.5" stroke-width="1.3"/>
    <line x1="22.5" y1="11" x2="20.5" y2="11" stroke-width="1.3"/>
    <line x1="21" y1="16" x2="19" y2="15" stroke-width="1.3"/>
    <line x1="17.5" y1="20" x2="16" y2="18" stroke-width="1.3"/>
    <line x1="12" y1="22.5" x2="12" y2="20.5" stroke-width="1.3"/>
    <line x1="7" y1="20.5" x2="8" y2="18" stroke-width="1.3"/>
    <line x1="3" y1="17" x2="5" y2="15.5" stroke-width="1.3"/>
    <line x1="1.5" y1="12" x2="3.5" y2="12" stroke-width="1.3"/>
    <line x1="3" y1="7" x2="5" y2="8.5" stroke-width="1.3"/>
    <line x1="6.5" y1="3.5" x2="8" y2="5.5" stroke-width="1.3"/>
    <!-- 外圈（手绘不规则） -->
    <path d="M12 3.5 L17.5 5 L21 11 L19 16 L16 18.5 L12 20.5 L8 19 L5 16 L3 11 L5.5 6 Z" stroke-width="1.1" stroke-dasharray="0.5 0.3"/>
    <!-- 中心点 -->
    <circle cx="12" cy="12" r="1" fill="currentColor" stroke="none"/>
  </svg>`,

  // 闪电图标 - 锯齿不均匀
  lightning: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
    <!-- 闪电形状 -->
    <path d="M13 1.5 L7.5 11.5 L11.5 11.2 L9 22.5 L19 10 L14.5 10.5 L17.5 1.5 Z" stroke-width="1.9"/>
    <!-- 手绘毛边 -->
    <path d="M10.5 11.3 L11.2 9.5" stroke-width="0.8" stroke-dasharray="0.5 0.5"/>
    <path d="M14 10.8 L15 8.5" stroke-width="0.8" stroke-dasharray="0.5 0.5"/>
  </svg>`,

  // 下载图标 - 箭头线条抖动
  download: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <!-- 方框 -->
    <path d="M4 3.5 C4 2.5, 4.8 2, 5.5 2 L18.5 2 C19.2 2, 20 2.5, 20 3.5 L20 20.5 C20 21.2, 19.2 22, 18.5 22 L5.5 22 C4.8 22, 4 21.5, 4 20.5 Z" stroke-width="1.8"/>
    <!-- 下载箭头 -->
    <path d="M12 6.5 L12 16" stroke-width="1.9"/>
    <path d="M8.5 13.5 L12 17 L15.5 13.5" stroke-width="1.7"/>
    <!-- 底部横线 -->
    <line x1="7" y1="19.5" x2="17" y2="19.5" stroke-width="1.4"/>
  </svg>`,

  // 文件图标 - 带褶皱效果
  file: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
    <!-- 文件主体 -->
    <path d="M5 2.5 C5 1.8, 5.5 1.5, 6 1.5 L14.5 1.5 L19 6 L19 21.5 C19 22, 18.5 22.5, 18 22.5 L6 22.5 C5.5 22.5, 5 22, 5 21.5 Z" stroke-width="1.7"/>
    <!-- 折角 -->
    <path d="M14.5 1.5 L14.5 6 L19 6" stroke-width="1.3"/>
    <!-- 褶皱线 -->
    <path d="M8 9.5 L16 9" stroke-width="1.0"/>
    <path d="M8 12.5 L15.5 12" stroke-width="1.0"/>
    <path d="M8 15.5 L16 15" stroke-width="1.0"/>
    <path d="M8 18.5 L13 18.2" stroke-width="0.9"/>
    <!-- 手绘褶皱 -->
    <path d="M7.5 5.5 Q8.5 5, 9.5 5.8" stroke-width="0.6" stroke-dasharray="0.5 0.8"/>
  </svg>`,

  // ========== 4. 路径规划模块图标（4个）==========

  // 地图图标 - 路线不规则
  map: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
    <!-- 地图折纸 -->
    <path d="M2.5 4.5 L7 2.5 L12 4.5 L17 2.5 L21.5 4.5 L21.5 19.5 L17 21.5 L12 19.5 L7 21.5 L2.5 19.5 Z" stroke-width="1.7"/>
    <!-- 路线 -->
    <path d="M7 7 Q10 5, 12 8 Q14 11, 12 14 Q10 17, 13 19.5" stroke-width="1.4" stroke-dasharray="2 1"/>
    <!-- 起点 -->
    <circle cx="6.5" cy="6.5" r="1.2" fill="currentColor" stroke="none"/>
    <!-- 终点 -->
    <path d="M16.5 18.5 L19.5 21.5 M19.5 18.5 L16.5 21.5" stroke-width="1.3"/>
    <!-- 定位标记 -->
    <path d="M17 12.5 C17 11, 18 10, 19.5 10 C21 10, 22 11, 22 12.5 C22 14.5, 19.5 17, 19.5 17 C19.5 17, 17 14.5, 17 12.5Z" stroke-width="1.2"/>
    <circle cx="19.5" cy="12" r="1" stroke-width="0.9"/>
  </svg>`,

  // 时钟图标 - 指针位置略偏
  clock: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
    <!-- 外圈 -->
    <circle cx="12" cy="12" r="10" stroke-width="1.8"/>
    <!-- 中心 -->
    <circle cx="12.3" cy="12.2" r="1" stroke-width="1.3"/>
    <!-- 时针（略偏） -->
    <line x1="12.3" y1="12.2" x2="12.3" y2="6.5" stroke-width="1.7"/>
    <!-- 分针（略偏） -->
    <line x1="12.3" y1="12.2" x2="18" y2="13" stroke-width="1.4"/>
    <!-- 秒针（抖动） -->
    <line x1="12.3" y1="12.2" x2="11" y2="19" stroke-width="0.8" stroke-dasharray="1 0.5"/>
    <!-- 刻度（不均匀） -->
    <line x1="12" y1="1.5" x2="12" y2="3" stroke-width="1.0"/>
    <line x1="21" y1="11" x2="22.5" y2="11" stroke-width="1.0"/>
    <line x1="12" y1="21" x2="12" y2="22.5" stroke-width="1.0"/>
    <line x1="1.5" y1="12" x2="3" y2="12" stroke-width="1.0"/>
    <line x1="4.5" y1="4.5" x2="5.5" y2="5.2" stroke-width="0.7"/>
    <line x1="19.5" y1="4.5" x2="18.5" y2="5.2" stroke-width="0.7"/>
  </svg>`,

  // 图表图标（路径规划版）- 柱状图柱子粗细不一
  chart_bar: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <!-- 坐标轴 -->
    <line x1="3" y1="21" x2="22" y2="21" stroke-width="1.4"/>
    <line x1="3" y1="21" x2="3" y2="2.5" stroke-width="1.4"/>
    <!-- 柱子1（细） -->
    <rect x="5" y="13" width="2.5" height="8" rx="0.2" stroke-width="1.3"/>
    <!-- 柱子2（粗） -->
    <rect x="9" y="8" width="3.2" height="13" rx="0.2" stroke-width="1.6"/>
    <!-- 柱子3（中） -->
    <rect x="13.5" y="4" width="2.8" height="17" rx="0.2" stroke-width="1.4"/>
    <!-- 柱子4（细高） -->
    <rect x="18" y="10" width="2.2" height="11" rx="0.2" stroke-width="1.2"/>
    <!-- 顶部横线（手绘，不直） -->
    <path d="M2.5 2.8 Q12 2, 22.5 2.5" stroke-width="0.9" stroke-dasharray="1.5 1"/>
  </svg>`,

  // 旗帜图标 - 飘带不规则
  flag: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
    <!-- 旗杆 -->
    <line x1="6" y1="2" x2="6" y2="22" stroke-width="1.5"/>
    <!-- 飘带（不规则） -->
    <path d="M6 3 C9 2.5, 13 2, 16 4 C19 6, 18 9, 15 10 C18 11, 20 13, 17 16 C15 18, 11 17.5, 8 16 L6 15.5 Z" stroke-width="1.7"/>
    <!-- 手绘阴影线 -->
    <path d="M8 6 Q12 5, 14 7" stroke-width="0.7" stroke-dasharray="0.5 0.8"/>
    <path d="M8.5 12 Q12 11, 14.5 13" stroke-width="0.7" stroke-dasharray="0.5 0.8"/>
    <!-- 旗杆顶部 -->
    <circle cx="6" cy="1.5" r="1" stroke-width="1.2"/>
  </svg>`,

  // ========== 5. 质量评估模块图标（4个）==========

  // 对勾图标 - 对勾线条不完美
  check: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.0" stroke-linecap="round" stroke-linejoin="round">
    <!-- 外圈 -->
    <circle cx="12" cy="12" r="10" stroke-width="1.7"/>
    <!-- 对勾（不完美） -->
    <path d="M7 12.5 Q9 15.5, 10.5 14.5 Q14 10, 18.5 6" stroke-width="2.0"/>
    <!-- 手绘毛边 -->
    <path d="M6.5 12.8 L7.5 11.8" stroke-width="0.7" stroke-dasharray="0.4 0.6"/>
  </svg>`,

  // 图表图标（评估版）- 折线图，与柱状图差异化
  chart_line: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
    <!-- 坐标轴 -->
    <line x1="3" y1="21" x2="22" y2="21" stroke-width="1.3"/>
    <line x1="3" y1="21" x2="3" y2="3" stroke-width="1.3"/>
    <!-- 折线（不完美） -->
    <path d="M4 18 Q6 17, 7.5 15 Q9 10, 11 12 Q13 14, 15 8 Q17 5, 20 7" stroke-width="1.7"/>
    <!-- 数据点 -->
    <circle cx="7.5" cy="15" r="1.2" fill="currentColor" stroke="none"/>
    <circle cx="11" cy="12" r="1.2" fill="currentColor" stroke="none"/>
    <circle cx="15" cy="8" r="1.2" fill="currentColor" stroke="none"/>
    <circle cx="20" cy="7" r="1.2" fill="currentColor" stroke="none"/>
    <!-- 网格线（手绘） -->
    <path d="M3 14.5 L22 14.5" stroke-width="0.5" stroke-dasharray="1 2"/>
    <path d="M3 8 L22 8" stroke-width="0.5" stroke-dasharray="1 2"/>
  </svg>`,

  // 放大镜图标 - 镜片略椭圆
  magnifier: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <!-- 镜片（略椭圆） -->
    <ellipse cx="10.5" cy="10.5" rx="7" ry="6.5" stroke-width="1.8"/>
    <!-- 手柄 -->
    <line x1="15.5" y1="15.5" x2="22" y2="22" stroke-width="1.9"/>
    <!-- 手绘反光 -->
    <path d="M7 7.5 Q8.5 6.5, 10 7" stroke-width="0.8" stroke-dasharray="0.5 0.5"/>
    <!-- 手柄毛边 -->
    <path d="M17 17.5 L18.5 19" stroke-width="0.6" stroke-dasharray="0.4 0.6"/>
  </svg>`,

  // 星星图标 - 角不均匀
  star: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
    <!-- 星星（角不均匀） -->
    <path d="M12 2 L14.5 8.5 L21.5 9.2 L16.2 13.8 L17.8 20.5 L12 17 L6.2 20.5 L7.8 13.8 L2.5 9.2 L9.5 8.5 Z" stroke-width="1.7"/>
    <!-- 内部短线（手绘装饰） -->
    <path d="M12 5 L12.5 7.5" stroke-width="0.7"/>
    <path d="M8 9.5 L10 9.2" stroke-width="0.6"/>
    <path d="M16 9.5 L14 9.2" stroke-width="0.6"/>
    <path d="M9.5 14.5 L11 13.5" stroke-width="0.6"/>
    <path d="M14.5 14.5 L13 13.5" stroke-width="0.6"/>
  </svg>`,

  // ========== 6. 侧边栏导航图标（5个）==========

  // 首页图标 - 房子线条手绘感
  nav_home: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
    <!-- 屋顶 -->
    <path d="M12 2.5 L2.5 12.5 L4.5 12.5" stroke-width="1.9"/>
    <path d="M12 2.5 L21.5 12.5 L19.5 12.5" stroke-width="1.9"/>
    <!-- 房体 -->
    <path d="M6 12 L6 20.5 C6 21, 6.5 21.5, 7 21.5 L17 21.5 C17.5 21.5, 18 21, 18 20.5 L18 12" stroke-width="1.7"/>
    <!-- 门 -->
    <path d="M10 21.5 L10 16 C10 15, 10.5 14.5, 11 14.5 L13 14.5 C13.5 14.5, 14 15, 14 16 L14 21.5" stroke-width="1.4"/>
    <!-- 窗户 -->
    <path d="M7.5 14 L9.2 14 L9.2 16.5 L7.5 16.5 Z" stroke-width="1.0"/>
    <path d="M14.8 14 L16.5 14 L16.5 16.5 L14.8 16.5 Z" stroke-width="1.0"/>
    <!-- 烟囱 -->
    <path d="M15.5 5.5 L15.5 2.5 L17.5 2.5 L17.5 7" stroke-width="1.3"/>
  </svg>`,

  // 画像图标 - 大脑简笔画
  nav_brain: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <!-- 简化大脑轮廓 -->
    <path d="M12 4 C7 4, 4 7, 4 11 C4 13.5, 5.5 15, 6.5 16 C5.5 17, 5 18.5, 5.5 20 C6.3 21.5, 8.5 22, 11 21.5 L12 21.5 L13 21.5 C15.5 22, 17.7 21.5, 18.5 20 C19 18.5, 18.5 17, 17.5 16 C18.5 15, 20 13.5, 20 11 C20 7, 17 4, 12 4Z" stroke-width="1.8"/>
    <!-- 简化脑回 -->
    <path d="M8 8 Q7 10, 8.5 12" stroke-width="1.1"/>
    <path d="M16 8 Q17 10, 15.5 12" stroke-width="1.1"/>
    <path d="M12 6.5 Q11 9, 12.5 12 Q13 15, 12 17.5" stroke-width="0.9" stroke-dasharray="1.5 1"/>
  </svg>`,

  // 资源图标 - 书籍简笔画
  nav_book: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
    <!-- 简化书本 -->
    <path d="M4 4 C4 3.5, 4.5 3, 5 3 L12 2.5 L19 3 C19.5 3, 20 3.5, 20 4 L20 20 C20 20.5, 19.5 21, 19 21 L12 20.5 L5 21 C4.5 21, 4 20.5, 4 20 Z" stroke-width="1.8"/>
    <!-- 书脊 -->
    <line x1="12" y1="2.5" x2="12" y2="20.5" stroke-width="1.5"/>
    <!-- 简化横线 -->
    <line x1="5" y1="8" x2="10.5" y2="7.8" stroke-width="0.9"/>
    <line x1="5.2" y1="11" x2="10.5" y2="10.8" stroke-width="0.9"/>
    <line x1="13.5" y1="7.8" x2="19" y2="8" stroke-width="0.9"/>
    <line x1="13.5" y1="10.8" x2="19" y2="11" stroke-width="0.9"/>
  </svg>`,

  // 路径图标 - 地图简笔画
  nav_map: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <!-- 简化地图折纸 -->
    <path d="M3 5 L8 3 L12 5 L17 3 L21 5 L21 19 L17 21 L12 19 L8 21 L3 19 Z" stroke-width="1.7"/>
    <!-- 简化路线 -->
    <path d="M8 8 Q10 6, 12 9 Q14 12, 12 15 Q10 18, 14 20" stroke-width="1.3" stroke-dasharray="1.5 0.8"/>
    <!-- 起点 -->
    <circle cx="7.5" cy="7.5" r="1" fill="currentColor" stroke="none"/>
    <!-- 终点 -->
    <path d="M17 18.5 L19 21 M19 18.5 L17 21" stroke-width="1.1"/>
  </svg>`,

  // 评估图标 - 对勾简笔画
  nav_check: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
    <!-- 简化圆圈 -->
    <circle cx="12" cy="12" r="9.5" stroke-width="1.7"/>
    <!-- 简化对勾 -->
    <path d="M7.5 12.5 Q9.5 15, 11 14 Q13.5 10.5, 18 6.5" stroke-width="1.9"/>
  </svg>`,

  // ========== 额外补充图标（用于hover/active状态）==========

  // 小箭头（右）
  arrow_right: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <line x1="4" y1="12" x2="19" y2="12" stroke-width="1.6"/>
    <path d="M14 7 L20 12 L14 17" stroke-width="1.6"/>
  </svg>`,

  // 小箭头（下）
  arrow_down: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <line x1="12" y1="4" x2="12" y2="19" stroke-width="1.6"/>
    <path d="M7 14 L12 20 L17 14" stroke-width="1.6"/>
  </svg>`,

  // 关闭图标
  close: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <line x1="5" y1="5" x2="19" y2="19" stroke-width="1.8"/>
    <line x1="19" y1="5" x2="5" y2="19" stroke-width="1.8"/>
  </svg>`,

  // 菜单图标
  menu: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <line x1="3" y1="6" x2="21" y2="6" stroke-width="1.8"/>
    <line x1="3" y1="12" x2="21" y2="12" stroke-width="1.8"/>
    <line x1="3" y1="18" x2="21" y2="18" stroke-width="1.8"/>
  </svg>`,

  // 搜索图标
  search: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="10.5" cy="10.5" rx="6.5" ry="6.5" stroke-width="1.7"/>
    <line x1="15" y1="15" x2="21.5" y2="21.5" stroke-width="1.8"/>
  </svg>`,

  // 设置图标（简化齿轮）
  settings: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="12" cy="12" r="3" stroke-width="1.5"/>
    <path d="M12 2 L12.8 4.5 L12 2 L11.2 4.5 Z" stroke-width="1.1"/>
    <path d="M22 12 L19.5 12.8 L22 12 L19.5 11.2 Z" stroke-width="1.1"/>
    <path d="M12 22 L11.2 19.5 L12 22 L12.8 19.5 Z" stroke-width="1.1"/>
    <path d="M2 12 L4.5 11.2 L2 12 L4.5 12.8 Z" stroke-width="1.1"/>
    <path d="M19.5 4.5 L17.5 6.5 L19.5 4.5 L17.5 6.5 Z" stroke-width="1.1"/>
    <path d="M4.5 19.5 L6.5 17.5 L4.5 19.5 L6.5 17.5 Z" stroke-width="1.1"/>
    <path d="M19.5 19.5 L17.5 17.5 L19.5 19.5 L17.5 17.5 Z" stroke-width="1.1"/>
    <path d="M4.5 4.5 L6.5 6.5 L4.5 4.5 L6.5 6.5 Z" stroke-width="1.1"/>
  </svg>`,

  // 通知图标
  bell: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
    <!-- 铃铛主体 -->
    <path d="M12 2.5 C8 2.5, 5 5.5, 5 9.5 C5 14, 3.5 15.5, 3.5 16.5 L20.5 16.5 C20.5 15.5, 19 14, 19 9.5 C19 5.5, 16 2.5, 12 2.5Z" stroke-width="1.7"/>
    <!-- 铃铛底部 -->
    <line x1="5" y1="17.5" x2="19" y2="17.5" stroke-width="1.5"/>
    <!-- 铃铛舌 -->
    <circle cx="12" cy="20" r="1.5" stroke-width="1.2"/>
    <!-- 顶部 -->
    <circle cx="12" cy="2" r="1" stroke-width="1.2"/>
  </svg>`,

  // 刷新图标
  refresh: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
    <!-- 圆弧1 -->
    <path d="M4 12 C4 7, 7.5 3, 12 3 C16.5 3, 20 6.5, 20 11" stroke-width="1.7"/>
    <!-- 箭头1 -->
    <path d="M18.5 2 L21 5.5 L17.5 5.5" stroke-width="1.5"/>
    <!-- 圆弧2 -->
    <path d="M20 12 C20 17, 16.5 21, 12 21 C7.5 21, 4 17.5, 4 13" stroke-width="1.7"/>
    <!-- 箭头2 -->
    <path d="M5.5 22 L3 18.5 L6.5 18.5" stroke-width="1.5"/>
  </svg>`,

  // 锁图标
  lock: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
    <!-- 锁体 -->
    <path d="M5 11 L5 20 C5 21, 5.5 21.5, 6 21.5 L18 21.5 C18.5 21.5, 19 21, 19 20 L19 11 C19 10, 18.5 9.5, 18 9.5 L6 9.5 C5.5 9.5, 5 10, 5 11Z" stroke-width="1.7"/>
    <!-- 锁扣 -->
    <path d="M8 9.5 L8 6 C8 3.5, 9.5 2, 12 2 C14.5 2, 16 3.5, 16 6 L16 9.5" stroke-width="1.5"/>
    <!-- 锁孔 -->
    <circle cx="12" cy="14.5" r="1.5" stroke-width="1.2"/>
    <line x1="12" y1="16" x2="12" y2="18.5" stroke-width="1.2"/>
  </svg>`,

  // 云图标
  cloud: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
    <!-- 云朵 -->
    <path d="M6 16 C3 16, 2 14, 2 12 C2 9.5, 4 8, 6 8.5 C7 5.5, 10 3.5, 13 4.5 C15.5 3, 18.5 4.5, 19 7.5 C21 8, 22 10, 22 12 C22 14, 20.5 16, 18 16 Z" stroke-width="1.7"/>
    <!-- 手绘毛边 -->
    <path d="M5.5 13.5 Q7 12.5, 8.5 13.5" stroke-width="0.6" stroke-dasharray="0.5 0.8"/>
  </svg>`,

  // 爱心图标
  heart: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <!-- 爱心 -->
    <path d="M12 21 C11 20, 5 16, 3 12 C1 8, 2.5 4, 6 3.5 C9 3, 11 5, 12 6.5 C13 5, 15 3, 18 3.5 C21.5 4, 23 8, 21 12 C19 16, 13 20, 12 21Z" stroke-width="1.7"/>
    <!-- 手绘装饰 -->
    <path d="M9 9 Q10 7.5, 11 9" stroke-width="0.7" stroke-dasharray="0.4 0.6"/>
    <path d="M13 9 Q14 7.5, 15 9" stroke-width="0.7" stroke-dasharray="0.4 0.6"/>
  </svg>`,

  // 铅笔图标
  pencil: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
    <!-- 铅笔主体 -->
    <path d="M15.5 2.5 L21.5 8.5 L11 19 L3 21.5 L5.5 13.5 Z" stroke-width="1.7"/>
    <!-- 铅笔尖端 -->
    <path d="M3 21.5 L2 23 L4.5 21.5" stroke-width="1.3"/>
    <!-- 橡皮 -->
    <path d="M15.5 2.5 L13 5 L18.5 10.5 L21.5 8.5" stroke-width="1.2" stroke-dasharray="0.8 0.5"/>
    <!-- 铅笔线 -->
    <line x1="13.5" y1="5.5" x2="17.5" y2="9.5" stroke-width="0.8"/>
  </svg>`,

  // 灯泡图标
  bulb: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
    <!-- 灯泡主体 -->
    <path d="M12 2 C7.5 2, 4 5.5, 4 9.5 C4 12.5, 5.5 15, 7.5 16.5 L7.5 19 C7.5 20, 8.5 21, 10 21.5 L14 21.5 C15.5 21, 16.5 20, 16.5 19 L16.5 16.5 C18.5 15, 20 12.5, 20 9.5 C20 5.5, 16.5 2, 12 2Z" stroke-width="1.7"/>
    <!-- 灯丝 -->
    <path d="M10 13 Q12 15, 14 13" stroke-width="1.1"/>
    <!-- 底座螺纹 -->
    <line x1="8.5" y1="19" x2="15.5" y2="19" stroke-width="1.0"/>
    <line x1="9" y1="20" x2="15" y2="20" stroke-width="0.9"/>
  </svg>`,

  // 链接图标
  link: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <!-- 链环1 -->
    <path d="M10.5 13.5 C8 11, 8 7, 10.5 4.5 C13 2, 17 2, 19.5 4.5 L17 7" stroke-width="1.6"/>
    <!-- 链环2 -->
    <path d="M13.5 10.5 C16 13, 16 17, 13.5 19.5 C11 22, 7 22, 4.5 19.5 L7 17" stroke-width="1.6"/>
  </svg>`,

  // 警告图标
  warning: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <!-- 三角形 -->
    <path d="M12 2 L22 20 L2 20 Z" stroke-width="1.8"/>
    <!-- 感叹号 -->
    <line x1="12" y1="9" x2="12" y2="15" stroke-width="1.8"/>
    <circle cx="12" cy="18" r="1" fill="currentColor" stroke="none"/>
  </svg>`,

};

// 导出兼容不同环境的格式
if (typeof module !== 'undefined' && module.exports) {
  module.exports = HANDDRAWN_ICONS;
}
if (typeof window !== 'undefined') {
  window.HANDDRAWN_ICONS = HANDDRAWN_ICONS;
}

/**
 * 获取图标 SVG 字符串（支持自定义尺寸和颜色）
 * @param {string} name - 图标名称
 * @param {number} size - 尺寸（默认 24）
 * @param {string} color - 颜色（默认 currentColor）
 * @returns {string} SVG 字符串
 */
function getIconSVG(name, size = 24, color = 'currentColor') {
  if (!HANDDRAWN_ICONS[name]) return '';
  let svg = HANDDRAWN_ICONS[name];
  if (size !== 24) {
    svg = svg.replace('viewBox="0 0 24 24"', `width="${size}" height="${size}" viewBox="0 0 24 24"`);
  }
  if (color !== 'currentColor') {
    svg = svg.replace(/stroke="currentColor"/g, `stroke="${color}"`);
    svg = svg.replace(/fill="currentColor"/g, `fill="${color}"`);
  }
  return svg;
}

/**
 * 获取图标 HTML（用于 Streamlit st.markdown 注入）
 * @param {string} name - 图标名称
 * @param {number} size - 尺寸
 * @param {string} color - 颜色
 * @returns {string} 可直接用于 st.markdown 的 HTML
 */
function getIconHTML(name, size = 24, color = '#ffffff') {
  const svg = getIconSVG(name, size, color);
  return `<span style="display:inline-flex;align-items:center;justify-content:center;width:${size}px;height:${size}px;">${svg}</span>`;
}

/**
 * 生成 Streamlit 使用示例代码
 */
const ICON_USAGE_EXAMPLES = {
  python: `
# 在 Streamlit 中使用手绘图标
import streamlit as st
import json

# 读取图标文件
with open('assets/handdrawn_icons.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# 方法1：直接嵌入 SVG
def render_icon(name, size=24, color='white'):
    # 从 HANDDRAWN_ICONS 对象中获取对应 SVG
    # 需要通过 st.components.v1.html 或 st.markdown 注入
    svg_html = f'<span style="display:inline-flex;">{HANDDRAWN_ICONS[name]}</span>'
    st.markdown(svg_html, unsafe_allow_html=True)

# 方法2：使用 base64 编码
import base64
def get_icon_data_uri(name, color='white'):
    svg = HANDDRAWN_ICONS[name]
    svg = svg.replace('currentColor', color)
    encoded = base64.b64encode(svg.encode()).decode()
    return f'data:image/svg+xml;base64,{encoded}'

# 在侧边栏使用
st.sidebar.markdown(
    getIconHTML('nav_home', 20) + ' 首页',
    unsafe_allow_html=True
)
  `,
  js: `
// 在 JavaScript/React 中使用
import { HANDDRAWN_ICONS } from './assets/handdrawn_icons.js';

// 直接插入 SVG
document.getElementById('icon-container').innerHTML = HANDDRAWN_ICONS.robot;

// 带自定义颜色
const svg = HANDDRAWN_ICONS.brain.replace(/currentColor/g, '#ff6b6b');
document.getElementById('icon-container').innerHTML = svg;
  `
};

// 导出辅助函数
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    HANDDRAWN_ICONS,
    getIconSVG,
    getIconHTML,
    ICON_USAGE_EXAMPLES
  };
}
