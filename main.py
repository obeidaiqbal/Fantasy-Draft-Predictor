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

def main():
    df24, df25 = load_data()
    df24 = clean_data(df24, 24)
    df25 = clean_data(df25, 25)
    print(df24.head())
    print(df25.head())

if __name__=="__main__":
    main()