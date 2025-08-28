from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
pd.options.display.float_format = "{:.1f}".format


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

def build_training_data(seasons):
    rows = []
    for year in range(21, 25):
        current = seasons[year]
        nxt = seasons[year+1][["Player", "FPTS"]]
        merged = current.merge(nxt, on="Player", suffixes=("", "_next"))
        rows.append(merged)
    return pd.concat(rows, ignore_index=True)

def calculate_regression(data, seasons):
    features = ["PTS", "FG%", "3P%", "FT%", "AST", "TRB", "STL", "BLK", "TOV", "G", "MP"]
    X = data[features]
    y = data["FPTS_next"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    # print("MSE:", mean_squared_error(y_test, y_pred))
    # print("R^2:", r2_score(y_test, y_pred))
    X_2025 = seasons[25][features]
    pred_2026 = model.predict(X_2025)
    seasons[25]["FPTS_26"] = pred_2026
    print(seasons[25][["Player", "FPTS", "FPTS_26"]].sort_values("FPTS_26", ascending = False).head(20))
    sorted = (seasons[25][["Player", "FPTS", "FPTS_26"]].sort_values("FPTS_26", ascending = False))
    sorted.to_csv("data/2025season_predictions.csv", index = False)

def main():
    years = [21, 22, 23, 24, 25]
    seasons = {}
    for y in years:
        path = f"data/20{y}season.csv"
        seasons[y] = load_data(path, y)
    data = build_training_data(seasons)
    calculate_regression(data, seasons)

if __name__=="__main__":
    main()