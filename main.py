import pygame
import sys
from hexgrid import HexGrid
from district import create_districts
from ui import Panel, DistrictSelector, StatusBar, DescriptionPanel

# 初始化Pygame
pygame.init()

# 设置窗口尺寸
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("文明6区域规划模拟器")

# 设置颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 240)

# 设置字体
font = pygame.font.SysFont('SimHei', 16)
title_font = pygame.font.SysFont('SimHei', 24)

# 创建六边形网格
HEX_RADIUS = 30
GRID_WIDTH = 15
GRID_HEIGHT = 15
hex_grid = HexGrid(HEX_RADIUS, GRID_WIDTH, GRID_HEIGHT)

# 地图偏移和缩放
map_offset_x = 0
map_offset_y = 0
map_scale = 1.0
dragging = False
drag_start = None

# 创建区域
districts = create_districts()

# 创建UI组件
district_selector = DistrictSelector(
    WINDOW_WIDTH - 250, 
    10, 
    240, 
    400, 
    districts, 
    font
)

info_panel = Panel(
    WINDOW_WIDTH - 250,
    420,
    240,
    170,
    LIGHT_GRAY,
    BLACK
)

# 添加状态栏
status_bar = StatusBar(
    WINDOW_WIDTH - 250,
    600,
    240,
    100,  # 将高度从80增加到100
    LIGHT_GRAY,
    BLACK,
    font
)

# 添加描述面板
description_panel = DescriptionPanel(
    0,  # 从窗口左侧开始
    WINDOW_HEIGHT - 80,  # 位于窗口底部
    WINDOW_WIDTH,  # 宽度等于窗口宽度
    100,  # 高度保持100像素
    LIGHT_GRAY,
    BLACK,
    font
)

# 颜色定义
colors = {
    'empty': (200, 200, 200),
    'border': (0, 0, 0),
    'text': (0, 0, 0),
    'highlight': (255, 255, 0, 128)  # 半透明黄色
}

# 游戏主循环
def main():
    global map_offset_x, map_offset_y, map_scale, dragging, drag_start
    
    clock = pygame.time.Clock()
    selected_hex = None
    
    while True:
        mouse_clicked = False
        mouse_pos = pygame.mouse.get_pos()
        
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    # 检查是否在地图区域内
                    if mouse_pos[0] < WINDOW_WIDTH - 250:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            # 按住Shift键拖动地图
                            dragging = True
                            drag_start = mouse_pos
                        else:
                            mouse_clicked = True
                    else:
                        mouse_clicked = True
                elif event.button == 4:  # 鼠标滚轮向上滚动
                    # 放大地图
                    if mouse_pos[0] < WINDOW_WIDTH - 250:
                        map_scale = min(2.0, map_scale + 0.1)
                elif event.button == 5:  # 鼠标滚轮向下滚动
                    # 缩小地图
                    if mouse_pos[0] < WINDOW_WIDTH - 250:
                        map_scale = max(0.5, map_scale - 0.1)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # 左键释放
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    # 拖动地图
                    dx = mouse_pos[0] - drag_start[0]
                    dy = mouse_pos[1] - drag_start[1]
                    map_offset_x += dx
                    map_offset_y += dy
                    drag_start = mouse_pos
        
        # 更新UI
        district_selector.update(mouse_pos)
        
        # 处理区域选择
        if district_selector.handle_click(mouse_pos, mouse_clicked):
            # 更新描述面板
            if district_selector.selected_district and district_selector.selected_district != "delete":
                description_panel.set_district(district_selector.selected_district)
            else:
                description_panel.clear()
        
        # 调整鼠标位置以考虑地图偏移和缩放
        adjusted_mouse_pos = (
            (mouse_pos[0] - map_offset_x) / map_scale,
            (mouse_pos[1] - map_offset_y) / map_scale
        )
        
        # 处理网格点击
        hex_coords = hex_grid.pixel_to_hex(mouse_pos[0], mouse_pos[1], map_offset_x, map_offset_y, map_scale)
        
        # 更新状态栏
        status_bar.update(mouse_pos, hex_coords, hex_grid)
        
        if hex_coords:
            # 如果点击了网格并且选择了区域
            if mouse_clicked and district_selector.selected_district and mouse_pos[0] < WINDOW_WIDTH - 250:
                if district_selector.selected_district == "delete":
                    hex_grid.remove_district(*hex_coords)
                else:
                    hex_grid.place_district(*hex_coords, district_selector.selected_district)
                selected_hex = hex_coords
        
        # 更新信息面板
        update_info_panel(selected_hex)
        
        # 绘制
        screen.fill(WHITE)
        
        # 绘制网格（考虑偏移和缩放）
        hex_grid.draw(screen, colors, font, map_offset_x, map_offset_y, map_scale)
        
        # 绘制UI组件
        district_selector.draw(screen)
        info_panel.draw(screen, font)
        status_bar.draw(screen)
        description_panel.draw(screen)
        
        # 绘制标题
        title = title_font.render("文明6区域规划模拟器", True, BLACK)
        screen.blit(title, (10, 10))
        
        # 显示当前选择的区域
        if district_selector.selected_district and district_selector.selected_district != "delete":
            current_selection = font.render(f"当前选择: {district_selector.selected_district.name}", True, BLACK)
            screen.blit(current_selection, (10, 50))
        elif district_selector.selected_district == "delete":
            current_selection = font.render("当前选择: 删除区域", True, BLACK)
            screen.blit(current_selection, (10, 50))
        
        # 显示地图缩放信息
        scale_info = font.render(f"缩放: {map_scale:.1f}x", True, BLACK)
        screen.blit(scale_info, (10, 80))
        
        # 显示操作提示
        controls = font.render("按住Shift+鼠标左键拖动地图，鼠标滚轮缩放", True, BLACK)
        screen.blit(controls, (10, 110))
        
        # 更新显示
        pygame.display.flip()
        clock.tick(60)

def update_info_panel(hex_coords):
    """更新信息面板内容"""
    info_panel.clear()
    
    if not hex_coords:
        info_panel.set_content([
            ("选择一个六边形格子", BLACK)
        ])
        return
    
    q, r = hex_coords
    district = hex_grid.get_district(q, r)
    
    if district:
        info_panel.set_content([
            (f"位置: ({q}, {r})", BLACK),
            (f"区域: {district.name}", BLACK),
            ("", BLACK),
            ("相邻加成:", BLACK)
        ])
        
        # 计算相邻加成
        neighbors = hex_grid.get_neighbors(q, r)
        total_bonuses = {}
        
        for neighbor_q, neighbor_r in neighbors:
            neighbor_district = hex_grid.get_district(neighbor_q, neighbor_r)
            if neighbor_district:
                bonus = district.get_adjacency_bonus(neighbor_district)
                if bonus:
                    bonus_type, bonus_value = bonus
                    if bonus_type in total_bonuses:
                        total_bonuses[bonus_type] += bonus_value
                    else:
                        total_bonuses[bonus_type] = bonus_value
        
        # 显示加成
        for bonus_type, bonus_value in total_bonuses.items():
            info_panel.content.append((f"{bonus_type}: +{bonus_value}", (0, 100, 0)))
    else:
        info_panel.set_content([
            (f"位置: ({q}, {r})", BLACK),
            ("空地", BLACK)
        ])

if __name__ == "__main__":
    main()