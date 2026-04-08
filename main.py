import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}

os.makedirs("output", exist_ok=True)


def get_standings(competition="PL"):
    url = f"{BASE_URL}/competitions/{competition}/standings"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    table = response.json()["standings"][0]["table"]
    rows = []
    for entry in table:
        rows.append({
            "position": entry["position"],
            "team": entry["team"]["shortName"],
            "played": entry["playedGames"],
            "won": entry["won"],
            "draw": entry["draw"],
            "lost": entry["lost"],
            "goals_for": entry["goalsFor"],
            "goals_against": entry["goalsAgainst"],
            "goal_diff": entry["goalDifference"],
            "points": entry["points"],
        })
    return pd.DataFrame(rows)


def get_top_scorers(competition="PL", limit=10):
    url = f"{BASE_URL}/competitions/{competition}/scorers?limit={limit}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    scorers = response.json()["scorers"]
    rows = []
    for entry in scorers:
        rows.append({
            "player": entry["player"]["name"],
            "team": entry["team"]["shortName"],
            "goals": entry["goals"],
            "assists": entry.get("assists") or 0,
            "played": entry.get("playedMatches") or 0,
        })
    return pd.DataFrame(rows)


def plot_standings(df):
    top10 = df.head(10).copy()

    fig, ax = plt.subplots(figsize=(12, 6))

    colors = []
    for pos in top10["position"]:
        if pos <= 4:
            colors.append("#3b82f6")   # Champions League — blue
        elif pos == 5:
            colors.append("#f59e0b")   # Europa League — amber
        else:
            colors.append("#6b7280")   # Rest — grey

    bars = ax.barh(top10["team"][::-1], top10["points"][::-1], color=colors[::-1], edgecolor="white", height=0.65)

    for bar, pts in zip(bars, top10["points"][::-1]):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                str(pts), va="center", fontsize=10, color="#111827")

    legend_patches = [
        mpatches.Patch(color="#3b82f6", label="Champions League (Top 4)"),
        mpatches.Patch(color="#f59e0b", label="Europa League (5th)"),
        mpatches.Patch(color="#6b7280", label="Rest"),
    ]
    ax.legend(handles=legend_patches, loc="lower right", fontsize=9)

    ax.set_xlabel("Points", fontsize=11)
    ax.set_title("Premier League — Top 10 Standings", fontsize=14, fontweight="bold", pad=15)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_facecolor("#f9fafb")
    fig.patch.set_facecolor("#ffffff")

    plt.tight_layout()
    path = "output/standings.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  Saved {path}")


def plot_top_scorers(df):
    fig, ax = plt.subplots(figsize=(12, 6))

    bars = ax.barh(df["player"][::-1], df["goals"][::-1],
                   color="#ef4444", edgecolor="white", height=0.65)

    for bar, goals in zip(bars, df["goals"][::-1]):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                str(goals), va="center", fontsize=10, color="#111827")

    ax.set_xlabel("Goals", fontsize=11)
    ax.set_title("Premier League — Top Scorers", fontsize=14, fontweight="bold", pad=15)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_facecolor("#f9fafb")
    fig.patch.set_facecolor("#ffffff")

    plt.tight_layout()
    path = "output/top_scorers.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  Saved {path}")


def print_summary(standings, scorers):
    print("\n=== Premier League Standings (Top 10) ===\n")
    print(standings.head(10).to_string(index=False))

    print("\n=== Top Scorers ===\n")
    print(scorers.to_string(index=False))


def main():
    if not API_KEY:
        print("Error: FOOTBALL_API_KEY not set. Add it to your .env file.")
        return

    print("Fetching Premier League standings...")
    standings = get_standings()

    print("Fetching top scorers...")
    scorers = get_top_scorers()

    print("Generating charts...")
    plot_standings(standings)
    plot_top_scorers(scorers)

    print_summary(standings, scorers)
    print("\nDone. Charts saved to output/")


if __name__ == "__main__":
    main()
