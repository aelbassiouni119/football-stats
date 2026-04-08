# Football Stats Analyzer

A Python tool that fetches live Premier League data and generates visual stats — standings, top scorers, and goal analysis.

Built with Python, pandas, matplotlib, and the [football-data.org](https://www.football-data.org/) API.

## Charts

### Standings
![Standings](output/standings.png)

### Top Scorers
![Top Scorers](output/top_scorers.png)

## Features

- Live Premier League standings (Top 10)
- Top scorers leaderboard
- Color-coded standings chart (Champions League, Europa League zones)
- Charts auto-saved to `output/`

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/YOURUSERNAME/football-stats
cd football-stats
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your API key**

Get a free key at [football-data.org](https://www.football-data.org/client/register).

```bash
cp .env.example .env
# then open .env and paste your key
```

**4. Run**
```bash
python main.py
```

Charts are saved to `output/`.

## Tech Stack

- **Python 3** — core language
- **requests** — API calls
- **pandas** — data wrangling
- **matplotlib** — visualizations
- **football-data.org** — free football data API

## Author

[Amin El Bassiouni](https://linkedin.com/in/amin-elbassiouni)
