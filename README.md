# Jacky's Civilization VI District Planner
## Project Overview
The Civilization VI District Planner is a tool developed with Python and Pygame that helps players plan their city district layouts to maximize adjacency bonuses. This tool simulates the district placement mechanics in Civilization VI, allowing players to plan ahead before actual gameplay to optimize their city development strategies.

### Key Features
- Hexagonal grid system simulating the Civilization VI game map
- Support for all major district types (Campus, Commercial Hub, Industrial Zone, etc.)
- Display of district adjacency rules and effects
- Interactive interface with map dragging and zooming capabilities
- Real-time display of district information and adjacency bonuses
### Technical Highlights
- Graphics rendering using Pygame
- Hexagonal grid algorithm implementation
- Modular design for easy expansion
## Installation and Usage
### Requirements
- Python 3.6+
- Pygame 2.0+
### Installation Steps
1. Clone the repository
```
git clone https://github.com/Jacky0987/Civ6-District-Planner
cd Civ6Planner
```
2. Install dependencies
```
pip install pygame
```
3. Run the program
```
python main.py
```
### Usage Instructions
- Left area: Displays the hexagonal grid map
- Right panel: District selector and information display
- Click to select a district type, then click on a hexagon on the map to place the district
- Hold Shift key and drag the mouse to move the map
- Use the mouse wheel to zoom in and out
- Bottom panel displays detailed information about the currently selected district
## Development Roadmap
- Add more terrain types (forests, mountains, rivers, etc.)
- Implement save and load functionality
- Add more civilization-specific districts
- Optimize UI interface for better user experience
## Contribution Guidelines
Contributions and suggestions are welcome! Please follow these steps:

1. Fork this repository
2. Create a new branch ( git checkout -b feature/your-feature )
3. Commit your changes ( git commit -m 'Add some feature' )
4. Push to the branch ( git push origin feature/your-feature )
5. Create a Pull Request
## License
This project is licensed under the MIT License - see the LICENSE file for details