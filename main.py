from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd


def load_data(season, year):
    df = pd.read_csv(season)
    df = clean_data(df, year)
    df = collapse_multiteam(df)
    df["FPTS"] = (df["PTS"] + 1.5 * df["TRB"] + 2 * df["AST"] + 2 * df["STL"] + 2 * df["BLK"] - df["TOV"])
    return df

def clean_data(df, season):
    df["Season"] = season
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass
    columns = ["Player", "Age", "Team", "Pos", "PTS", "FG%", "3P%", "FT%", "AST", "TRB", "STL", "BLK", "TOV", "G", "GS", "MP", "Season"]
    return df[columns]

def collapse_multiteam(df):
    numeric_cols = df.select_dtypes(include = ["number"]).columns
    df["_total_games"] = df["G"]
    for col in numeric_cols:
        if col not in ["G"]: 
            df[col] = df[col] * df["G"]
    grouped = df.groupby("Player", as_index = False).sum(numeric_only = True)
    for col in numeric_cols:
        if col not in ["G"]:  
            grouped[col] = grouped[col] / grouped["_total_games"]
    grouped.drop(columns = "_total_games", inplace = True)
    return grouped

def main():
    years = [21, 22, 23, 24, 25]
    seasons = {}
    for y in years:
        path = f"data/20{y}season.csv"
        seasons[y] = load_data(path, y)
    
    print(seasons[25][seasons[25]["Player"] == "LeBron James"])
    print(seasons[24][seasons[24]["Player"] == "LeBron James"])
    print(seasons[23][seasons[23]["Player"] == "LeBron James"])
    print(seasons[22][seasons[22]["Player"] == "LeBron James"])
    print(seasons[21][seasons[21]["Player"] == "LeBron James"])

if __name__=="__main__":
    main()