import pandas as pd


def load_data():
    df24 = pd.read_csv("data/2024season.csv")
    df25 = pd.read_csv("data/2025season.csv")
    return df24, df25

def clean_data(df, season):
    df["Season"] = season
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass
    columns = ["Player", "Age", "Team", "Pos", "PTS", "FG%", "3P%", "FT%", "AST", "TRB", "STL", "BLK", "TOV", "G", "GS", "MP", "Season"]
    return df[columns]

def get_fantasy_points(df):
    df["FPTS"] = (df["PTS"] + 1.5 * df["TRB"] + 2 * df["AST"] + 2 * df["STL"] + 2 * df["BLK"] - df["TOV"])
    return df

def main():
    df24, df25 = load_data()
    df24 = clean_data(df24, 24)
    df25 = clean_data(df25, 25)
    df24 = get_fantasy_points(df24)
    df25 = get_fantasy_points(df24)
    print(df24.head())
    print(df25.head())

if __name__=="__main__":
    main()