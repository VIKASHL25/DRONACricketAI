# DRONA: Cricket Tactical Intelligence Engine

Drona is an advanced tactical support system designed for modern cricket analytics. By integrating real-time match data with predictive modeling, Drona provides actionable insights, win probability forecasts, and optimal field placement strategies for coaches and analysts.

## Key Capabilities

- **Live Match Center**: Real-time tracking of international and league matches with granular scorecards.
- **Predictive Engine**: Proprietary algorithm (`agents/simulator.py`) that calculates win probability based on required run rate, wickets in hand, and historical trends.
- **AI Strategy Coach**: LLM-powered strategic advice tailored to the specific match situation (powered by Llama 3 via Groq).
- **Dynamic Field Plotter**: Visualizes optimal fielding restrictions and placements based on pressure levels and batter constraints.

## Technical Architecture

The system is built on a modular Python architecture:
- **Frontend**: Streamlit with custom CSS.
- **Data Layer**: Integration with RapidAPI for real-time scores.
- **Intelligence**: 
  - Deterministic simulation for probability.
  - Generative AI for strategic context.
- **Visualization**: Matplotlib for field mapping.

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/drona-cricket-engine.git
   cd drona-cricket-engine
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   Create a `.env` file in the root directory:
   ```env
   CRICKET_API_KEY=your_rapidapi_key
   CRICKET_API_HOST=cricbuzz-cricket.p.rapidapi.com
   CRICKET_API_URL=https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live
   CRICKET_DETAIL_URL=https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1
   GROQ_API_KEY=your_groq_api_key
   ```

4. **Launch Application**
   ```bash
   streamlit run app.py
   ```

## Project Structure

```
├── agents/             # Intelligence modules (Coach, Scout, Simulator)
├── services/           # External API integrations
├── visuali/            # Visualization engines
├── app.py              # Main application entry point
├── requirements.txt    # Dependency manifest
└── .env                # Configuration (Git-ignored)
```

---
*Built for the future of sport.*
