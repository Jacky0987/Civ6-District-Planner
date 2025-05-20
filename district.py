class District:
    """文明6区域类"""
    
    def __init__(self, name, short_name, color, adjacency_rules, description=""):
        """
        初始化区域
        
        参数:
            name: 区域全名
            short_name: 区域简称（用于显示）
            color: 区域颜色（RGB元组）
            adjacency_rules: 相邻加成规则字典
            description: 区域描述
        """
        self.name = name
        self.short_name = short_name
        self.color = color
        self.adjacency_rules = adjacency_rules
        self.description = description
    
    def get_adjacency_bonus(self, adjacent_district):
        """
        计算与相邻区域的加成
        
        参数:
            adjacent_district: 相邻的区域对象
            
        返回:
            (加成类型, 加成值)
        """
        if not adjacent_district:
            return None
        
        # 检查是否有特定区域加成规则
        if adjacent_district.name in self.adjacency_rules:
            return self.adjacency_rules[adjacent_district.name]
        
        # 检查是否有通用区域加成规则
        if 'any_district' in self.adjacency_rules:
            return self.adjacency_rules['any_district']
        
        return None

# 定义文明6中的主要区域
def create_districts():
    """创建文明6中的主要区域"""
    districts = {}
    
    # 定义区域颜色
    BLUE = (66, 135, 245)
    RED = (235, 64, 52)
    GREEN = (46, 204, 113)
    PURPLE = (155, 89, 182)
    ORANGE = (230, 126, 34)
    YELLOW = (241, 196, 15)
    BROWN = (160, 64, 0)
    GRAY = (149, 165, 166)
    WHITE = (255, 255, 255)  # 添加白色
    ORANGE_YELLOW = (245, 171, 53)  # 添加黄色和橙色之间的颜色
    
    # 学院区（原校园区）
    districts['campus'] = District(
        name='学院区',
        short_name='学院\nCampus',
        color=BLUE,
        adjacency_rules={
            '雨林': ('+1科技值', 1),
            '山脉': ('+1科技值', 1),
            '礁石': ('+1科技值', 1),
            '图书馆区': ('+1科技值', 1),
            'any_district': ('+0.5科技值', 0.5)
        },
        description="学院区提供科技值，相邻山脉、雨林和礁石时获得加成。"
    )
    
    # 商业中心
    districts['commercial_hub'] = District(
        name='商业中心',
        short_name='商业\nCommercial',
        color=YELLOW,
        adjacency_rules={
            '河流': ('+2金币', 2),
            '港口区': ('+2金币', 2),
            'any_district': ('+0.5金币', 0.5)
        },
        description="商业中心提供金币，相邻河流和港口时获得加成。"
    )
    
    # 工业区
    districts['industrial_zone'] = District(
        name='工业区',
        short_name='工业\nIndustrial',
        color=ORANGE,
        adjacency_rules={
            '矿山': ('+1生产力', 1),
            '采石场': ('+1生产力', 1),
            'any_district': ('+0.5生产力', 0.5)
        },
        description="工业区提供生产力，相邻矿山和采石场时获得加成。"
    )
    
    # 剧院广场
    districts['theater_square'] = District(
        name='剧院广场',
        short_name='剧院\nTheater',
        color=PURPLE,
        adjacency_rules={
            '奇观': ('+2文化值', 2),
            'any_district': ('+0.5文化值', 0.5)
        },
        description="剧院广场提供文化值，相邻奇观时获得加成。"
    )
    
    # 圣地
    districts['holy_site'] = District(
        name='圣地',
        short_name='圣地\nHoly Site',  # 添加英文名称
        color=WHITE,  # 修改为白色
        adjacency_rules={
            '山脉': ('+1信仰值', 1),
            '自然奇观': ('+2信仰值', 2),
            '森林': ('+0.5信仰值', 0.5),
            'any_district': ('+0.5信仰值', 0.5)
        },
        description="圣地提供信仰值，相邻山脉、自然奇观和森林时获得加成。"
    )
    
    # 娱乐中心
    districts['entertainment_complex'] = District(
        name='娱乐中心',
        short_name='娱乐\nEntertainment',  # 添加英文名称
        color=ORANGE_YELLOW,  # 修改为黄色和橙色之间的颜色
        adjacency_rules={
            'any_district': ('+0宜居度', 0)
        },
        description="娱乐中心提供宜居度，帮助城市增长。"
    )
    
    # 港口
    districts['harbor'] = District(
        name='港口',
        short_name='港口\nHarbor',
        color=GREEN,
        adjacency_rules={
            '海洋资源': ('+1金币', 1),
            '商业中心': ('+2金币', 2),
            'any_district': ('+0.5金币', 0.5)
        },
        description="港口提供金币和贸易路线，相邻海洋资源和商业中心时获得加成。"
    )
    
    # 宫殿（城市中心）
    districts['city_center'] = District(
        name='城市中心',
        short_name='中心\nCity Center',
        color=GRAY,
        adjacency_rules={},
        description="城市中心是每个城市的核心，提供基础产出。"
    )
    
    return districts