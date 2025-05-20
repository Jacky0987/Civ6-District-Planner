# 文明6区域规划模拟器 (Civilization VI District Planner)
## 项目简介
文明6区域规划模拟器是一个基于Python和Pygame开发的工具，帮助玩家规划城市区域布局，以最大化相邻加成效果。该工具模拟了文明6中的区域放置机制，让玩家可以在实际游戏前进行规划，从而优化城市发展策略。

### 主要功能
- 六边形网格系统，模拟文明6游戏地图
- 支持所有主要区域类型（学院区、商业中心、工业区等）
- 显示区域相邻加成规则和效果
- 交互式界面，支持拖动和缩放地图
- 实时显示区域信息和相邻加成
### 技术特点
- 使用Pygame进行图形渲染
- 六边形网格算法实现
- 模块化设计，便于扩展
## 安装与使用
### 环境要求
- Python 3.6+
- Pygame 2.0+
### 安装步骤
1. 克隆仓库到本地
```
git clone https://github.com/yourusername/
Civ6Planner.git
cd Civ6Planner
```
2. 安装依赖
```
pip install pygame
```
3. 运行程序
```
python main.py
```
### 使用说明
- 左侧区域：显示六边形网格地图
- 右侧面板：区域选择器和信息显示
- 点击选择区域类型，然后点击地图上的六边形放置区域
- 按住Shift键并拖动鼠标可移动地图
- 使用鼠标滚轮可缩放地图
- 底部面板显示当前选中区域的详细信息
## 开发计划
- 添加更多地形类型（森林、山脉、河流等）
- 实现保存和加载功能
- 添加更多文明特色区域
- 优化UI界面，提升用户体验
## 贡献指南
欢迎贡献代码或提出建议！请遵循以下步骤：

1. Fork 本仓库
2. 创建新分支 ( git checkout -b feature/your-feature )
3. 提交更改 ( git commit -m 'Add some feature' )
4. 推送到分支 ( git push origin feature/your-feature )
5. 创建 Pull Request
## 许可证
本项目采用 MIT 许可证 - 详情请参阅 LICENSE 文件