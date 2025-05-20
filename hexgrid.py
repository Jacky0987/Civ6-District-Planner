import math
import pygame

class HexGrid:
    """六边形网格系统"""
    
    def __init__(self, radius, grid_width, grid_height):
        """
        初始化六边形网格
        
        参数:
            radius: 六边形的半径（像素）
            grid_width: 网格的宽度（六边形数量）
            grid_height: 网格的高度（六边形数量）
        """
        self.radius = radius
        self.width = grid_width
        self.height = grid_height
        self.hex_width = self.radius * 2
        self.hex_height = math.sqrt(3) * self.radius
        self.horizontal_distance = self.hex_width * 3/4
        self.vertical_distance = self.hex_height
        
        # 初始化网格数据
        self.grid = {}
        for q in range(self.width):
            for r in range(self.height):
                self.grid[(q, r)] = None
    
    def pixel_to_hex(self, x, y, offset_x=0, offset_y=0, scale=1.0):
        """将屏幕坐标转换为六边形网格坐标（考虑偏移和缩放）"""
        # 调整坐标以考虑偏移和缩放
        adjusted_x = (x - offset_x) / scale
        adjusted_y = (y - offset_y) / scale
        
        # 转换为网格坐标
        q = (adjusted_x / self.horizontal_distance)
        r = (adjusted_y / self.vertical_distance - 0.5 * (int(q) % 2))
        
        # 四舍五入到最近的六边形
        q_round = round(q)
        r_round = round(r)
        
        # 确保坐标在网格范围内
        if 0 <= q_round < self.width and 0 <= r_round < self.height:
            return q_round, r_round
        return None
    
    def hex_to_pixel(self, q, r):
        """将六边形网格坐标转换为屏幕坐标（六边形中心）"""
        x = q * self.horizontal_distance
        y = r * self.vertical_distance + (q % 2) * self.vertical_distance / 2
        return x, y
    
    def get_hex_corners(self, q, r, offset_x=0, offset_y=0, scale=1.0):
        """获取六边形的六个角的坐标（考虑偏移和缩放）"""
        center_x, center_y = self.hex_to_pixel(q, r)
        # 应用缩放和偏移
        center_x = center_x * scale + offset_x
        center_y = center_y * scale + offset_y
        scaled_radius = self.radius * scale
        
        corners = []
        for i in range(6):
            angle_rad = math.pi / 3 * i
            x = center_x + scaled_radius * math.cos(angle_rad)
            y = center_y + scaled_radius * math.sin(angle_rad)
            corners.append((x, y))
        return corners
    
    def get_neighbors(self, q, r):
        """获取六边形的相邻六边形坐标"""
        # 偶数列的相邻坐标
        even_directions = [
            (0, -1), (1, -1), (1, 0), 
            (0, 1), (-1, 0), (-1, -1)
        ]
        # 奇数列的相邻坐标
        odd_directions = [
            (0, -1), (1, 0), (1, 1), 
            (0, 1), (-1, 1), (-1, 0)
        ]
        
        directions = odd_directions if q % 2 else even_directions
        neighbors = []
        
        for direction in directions:
            neighbor_q = q + direction[0]
            neighbor_r = r + direction[1]
            
            if 0 <= neighbor_q < self.width and 0 <= neighbor_r < self.height:
                neighbors.append((neighbor_q, neighbor_r))
                
        return neighbors
    
    def place_district(self, q, r, district):
        """在指定位置放置区域"""
        if (q, r) in self.grid:
            self.grid[(q, r)] = district
            return True
        return False
    
    def remove_district(self, q, r):
        """移除指定位置的区域"""
        if (q, r) in self.grid:
            self.grid[(q, r)] = None
            return True
        return False
    
    def get_district(self, q, r):
        """获取指定位置的区域"""
        if (q, r) in self.grid:
            return self.grid[(q, r)]
        return None
    
    def draw(self, surface, colors, font=None, offset_x=0, offset_y=0, scale=1.0):
        """绘制六边形网格（考虑偏移和缩放）"""
        for q in range(self.width):
            for r in range(self.height):
                corners = self.get_hex_corners(q, r, offset_x, offset_y, scale)
                
                # 绘制六边形
                district = self.grid[(q, r)]
                color = colors['empty']
                if district:
                    color = district.color
                
                pygame.draw.polygon(surface, color, corners)
                pygame.draw.polygon(surface, colors['border'], corners, 1)
                
                # 如果有区域，绘制区域名称
                if district and font:
                    center_x, center_y = self.hex_to_pixel(q, r)
                    # 应用缩放和偏移
                    center_x = center_x * scale + offset_x
                    center_y = center_y * scale + offset_y
                    
                    # 分割文本行
                    lines = district.short_name.split('\n')
                    line_height = font.get_height()
                    
                    # 计算文本块的总高度
                    total_height = line_height * len(lines)
                    
                    # 绘制每一行
                    for i, line in enumerate(lines):
                        text = font.render(line, True, colors['text'])
                        text_rect = text.get_rect(
                            center=(center_x, 
                                   center_y - total_height/2 + line_height/2 + i*line_height)
                        )
                        surface.blit(text, text_rect)