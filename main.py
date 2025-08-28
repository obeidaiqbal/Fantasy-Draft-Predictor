from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd


def load_data():
    df24 = pd.read_csv("data/2024season.csv")
    df25 = pd.read_csv("data/2025season.csv")
    df24 = clean_data(df24, 24)
    df25 = clean_data(df25, 25)
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

def collapse_multiteam_rows(df):
    numeric_cols = df.select_dtypes(include=["number"]).columns
    df["_total_games"] = df["G"]
    for col in numeric_cols:
        if col not in ["G"]: 
            df[col] = df[col] * df["G"]
    grouped = df.groupby("Player", as_index=False).sum(numeric_only=True)
    for col in numeric_cols:
        if col not in ["G"]:  
            grouped[col] = grouped[col] / grouped["_total_games"]
    grouped.drop(columns="_total_games", inplace=True)
    return grouped

def get_fantasy_points(df):
    df["FPTS"] = (df["PTS"] + 1.5 * df["TRB"] + 2 * df["AST"] + 2 * df["STL"] + 2 * df["BLK"] - df["TOV"])
    return df

def merge_data(df24, df25):
    df = pd.merge(df24, df25[["Player", "FPTS"]], on="Player", suffixes=("_24", "_25"))
    return df

def calculate_regression(df):
    features = ["PTS", "FG%", "3P%", "FT%", "AST", "TRB", "STL", "BLK", "TOV", "G", "MP"]
    X = df[features]
    Y = df["FPTS_25"]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 42)
    model = LinearRegression()
    model.fit(X_train, Y_train)
    coeffs = pd.DataFrame({"Feature": X_train.columns, "Coefficient": model.coef_}).sort_values("Coefficient", ascending=False)
    Y_pred = model.predict(X_test)
    mse = mean_squared_error(Y_test, Y_pred)
    r2 = r2_score(Y_test, Y_pred)
    df["Predicted_FPTS_25"] = model.predict(X)
    ranking = df[["Player", "FPTS_25", "Predicted_FPTS_25"]].sort_values(
        "Predicted_FPTS_25", ascending=False
    )
    ranking.to_csv("data/2025season_predictions.csv", index=False)


def main():
    df24, df25 = load_data()
    df24 = collapse_multiteam_rows(df24)
    df25 = collapse_multiteam_rows(df25)
    df24 = get_fantasy_points(df24)
    df25 = get_fantasy_points(df25)
    df = merge_data(df24, df25)
    # print(df[df["Player"] == "Shai Gilgeous-Alexander"])
    calculate_regression(df)

if __name__=="__main__":
    main()