import pygame

class Button:
    """按钮类"""
    
    def __init__(self, x, y, width, height, text, color, hover_color, text_color, font):
        """
        初始化按钮
        
        参数:
            x, y: 按钮左上角坐标
            width, height: 按钮尺寸
            text: 按钮文本
            color: 按钮颜色
            hover_color: 鼠标悬停时的颜色
            text_color: 文本颜色
            font: 字体对象
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font
        self.is_hovered = False
        
    def draw(self, surface):
        """绘制按钮"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)  # 边框
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def update(self, mouse_pos):
        """更新按钮状态"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos, mouse_clicked):
        """检查按钮是否被点击"""
        return self.rect.collidepoint(mouse_pos) and mouse_clicked

class Panel:
    """信息面板类"""
    
    def __init__(self, x, y, width, height, color, border_color):
        """
        初始化面板
        
        参数:
            x, y: 面板左上角坐标
            width, height: 面板尺寸
            color: 面板背景色
            border_color: 边框颜色
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.border_color = border_color
        self.content = []
        
    def draw(self, surface, font):
        """绘制面板"""
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        
        y_offset = 10
        for text, color in self.content:
            text_surface = font.render(text, True, color)
            surface.blit(text_surface, (self.rect.x + 10, self.rect.y + y_offset))
            y_offset += 25
            
    def set_content(self, content):
        """设置面板内容"""
        self.content = content
        
    def clear(self):
        """清空面板内容"""
        self.content = []

class StatusBar:
    """状态栏类"""
    
    def __init__(self, x, y, width, height, color, border_color, font):
        """初始化状态栏"""
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.border_color = border_color
        self.font = font
        self.content = []
        
    def update(self, mouse_pos, hex_coords, hex_grid):
        """更新状态栏内容"""
        self.content = []
        
        # 显示鼠标坐标
        self.content.append((f"鼠标: ({mouse_pos[0]}, {mouse_pos[1]})", (0, 0, 0)))
        
        # 显示六边形坐标
        if hex_coords:
            q, r = hex_coords
            self.content.append((f"六边形: ({q}, {r})", (0, 0, 0)))
            
            # 显示区域信息
            district = hex_grid.get_district(q, r)
            if district:
                self.content.append((f"区域: {district.name}", (0, 0, 0)))
        
    def draw(self, surface):
        """绘制状态栏"""
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        
        # 绘制标题
        title = self.font.render("状态栏", True, (0, 0, 0))
        surface.blit(title, (self.rect.x + 10, self.rect.y + 5))
        
        # 绘制内容
        y_offset = 30
        for text, color in self.content:
            # 检查文本是否需要换行
            if self.font.size(text)[0] > self.rect.width - 20:
                # 分割文本以适应面板宽度
                words = text.split()
                lines = []
                current_line = ""
                
                for word in words:
                    test_line = current_line + word + " "
                    # 检查添加这个词后是否会超出面板宽度
                    if self.font.size(test_line)[0] < self.rect.width - 20:
                        current_line = test_line
                    else:
                        lines.append(current_line)
                        current_line = word + " "
                
                # 添加最后一行
                if current_line:
                    lines.append(current_line)
                
                # 绘制文本行
                for line in lines:
                    text_surface = self.font.render(line, True, color)
                    surface.blit(text_surface, (self.rect.x + 10, self.rect.y + y_offset))
                    y_offset += 20
            else:
                # 不需要换行的文本直接绘制
                text_surface = self.font.render(text, True, color)
                surface.blit(text_surface, (self.rect.x + 10, self.rect.y + y_offset))
                y_offset += 20
                
            # 防止文本超出面板底部
            if y_offset > self.rect.height - 10:
                break

class DistrictSelector:
    """区域选择器类"""
    
    def __init__(self, x, y, width, height, districts, font):
        """
        初始化区域选择器
        
        参数:
            x, y: 选择器左上角坐标
            width, height: 选择器尺寸
            districts: 区域字典
            font: 字体对象
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.districts = districts
        self.font = font
        self.buttons = []
        self.selected_district = None
        
        # 创建区域按钮
        button_height = 30
        button_width = width - 20
        button_x = x + 10
        button_y = y + 40  # 留出空间给标题
        
        # 添加区域按钮
        for key, district in districts.items():
            button = Button(
                button_x, 
                button_y, 
                button_width, 
                button_height, 
                f"{district.name} ({district.short_name.split()[0]})", 
                district.color, 
                (min(255, district.color[0] + 50), 
                 min(255, district.color[1] + 50), 
                 min(255, district.color[2] + 50)), 
                (0, 0, 0), 
                font
            )
            self.buttons.append((key, button))
            button_y += button_height + 5
        
        # 添加删除按钮
        delete_button = Button(
            button_x, 
            button_y, 
            button_width, 
            button_height, 
            "删除区域", 
            (200, 200, 200), 
            (230, 230, 230), 
            (255, 0, 0), 
            font
        )
        self.buttons.append(("delete", delete_button))
    
    def update(self, mouse_pos):
        """更新按钮状态"""
        for _, button in self.buttons:
            button.update(mouse_pos)
    
    def handle_click(self, mouse_pos, mouse_clicked):
        """处理点击事件"""
        for key, button in self.buttons:
            if button.is_clicked(mouse_pos, mouse_clicked):
                if key == "delete":
                    self.selected_district = "delete"
                else:
                    self.selected_district = self.districts[key]
                return True
        return False
    
    def draw(self, surface):
        """绘制区域选择器"""
        pygame.draw.rect(surface, (240, 240, 240), self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        
        # 绘制标题
        title = self.font.render("区域选择", True, (0, 0, 0))
        surface.blit(title, (self.rect.x + 10, self.rect.y + 10))
        
        # 绘制按钮
        for _, button in self.buttons:
            button.draw(surface)

class DescriptionPanel:
    """区域描述面板类"""
    
    def __init__(self, x, y, width, height, color, border_color, font):
        """初始化描述面板"""
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.border_color = border_color
        self.font = font
        self.district = None
        
    def set_district(self, district):
        """设置当前显示的区域"""
        self.district = district
        
    def clear(self):
        """清空面板内容"""
        self.district = None
        
    def draw(self, surface):
        """绘制描述面板"""
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        
        # 绘制标题
        title = self.font.render("区域描述", True, (0, 0, 0))
        surface.blit(title, (self.rect.x + 10, self.rect.y + 5))
        
        # 绘制区域描述
        if self.district:
            # 分割描述文本以适应面板宽度
            words = self.district.description.split()
            lines = []
            current_line = ""
            
            for word in words:
                test_line = current_line + word + " "
                # 检查添加这个词后是否会超出面板宽度
                if self.font.size(test_line)[0] < self.rect.width - 20:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "
            
            # 添加最后一行
            if current_line:
                lines.append(current_line)
            
            # 绘制文本行
            y_offset = 30
            for line in lines:
                text_surface = self.font.render(line, True, (0, 0, 0))
                surface.blit(text_surface, (self.rect.x + 10, self.rect.y + y_offset))
                y_offset += 20
                
                # 防止文本超出面板底部
                if y_offset > self.rect.height - 10:
                    break