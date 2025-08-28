import pandas as pd


def load_data():
    df24 = pd.read_csv("2024season.csv")
    df25 = pd.read_csv("2025season.csv")
    return df24, df25

def clean_data(df, season):
    df["Season"] = season
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass
    columns = [
        "Player", "Age", "Team", "Pos", "G", "GS", "MP",
        "FG%", "3P%", "FT%",
        "TRB", "AST", "STL", "BLK", "TOV", "PTS",
        "Season"
    ]
    return df[columns]

def main():
    df24, df25 = load_data()
    df24 = clean_data(df24, 24)
    df25 = clean_data(df25, 25)
    print(df25.head())

if __name__=="__main__":
    main()