import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
matches = pd.read_csv("data/matches.csv")
deliveries = pd.read_csv("data/deliveries.csv")

# # Basic information
# print("===== MATCHES =====")
# print("Shape:", matches.shape)
# print("\nColumns:")
# print(matches.columns.tolist())

# print("\nData types:")
# print(matches.dtypes)

# print("\nMissing values:")
# print(matches.isnull().sum())

# print("\n===== DUPLICATES =====")

# print("Duplicate matches:", matches.duplicated().sum())
# print("Duplicate deliveries:", deliveries.duplicated().sum())


# print("\n===== UNIQUE SEASONS =====")
# print(matches["season"].unique())


# print("\n===== UNIQUE TEAMS =====")
# print("Team 1:")
# print(matches["team1"].unique())

# print("\nTeam 2:")
# print(matches["team2"].unique())


# print("\n===== MATCH RESULTS =====")
# print(matches["result"].value_counts(dropna=False))


# print("\n===== TOSS DECISIONS =====")
# print(matches["toss_decision"].value_counts(dropna=False))

# print(deliveries.columns.tolist())

# print(matches.isnull().sum())
# print('\n')
# print(deliveries.isnull().sum())
# print("\n")
# print(matches.duplicated().sum())
# print("\n")
# print(deliveries.duplicated().sum())


# print(pd.crosstab(matches["winner"], matches["result"], dropna = False))
# print("\n")

# print("matches with no winner") 
# print(matches[matches["winner"].isnull()][
#     ["team1", "team2", "result", "result_margin", "season"]
# ])()

# print( matches[matches["city"].isnull()][['venue','city','team1','team2','season']] )

# print(pd.read_csv("data/matches.csv"))
      
# df= matches['city'].isnull().sum()     
# print(df)

# Fill missing cities using venue
matches.loc[
    matches["venue"] == "Sharjah Cricket Stadium", "city"
] = "Sharjah"

matches.loc[
    matches["venue"] == "Dubai International Cricket Stadium", "city"
] = "Dubai"

# Check
print("Missing cities after cleaning:")
print(matches["city"].isnull().sum())

matches.loc[
     matches["venue"] == "Sharjah Cricket Stadium", "city"
 ] = "Sharjah"

print(matches.isnull().sum())

print(
  matches[matches["target_runs"].isnull()][["team1","team2","result","target_runs","target_overs"]]

)
print(
    matches[matches["target_overs"].isnull()][["team1","team2","result","target_runs","target_overs"]]

)
print("\n")
print(deliveries.isnull().sum())

#EDA

print(
    matches["season"].value_counts().sort_index()
)

print(
    matches["team1"].unique()
)

teams = pd.concat([
    matches["team1"],
    matches["team2"]
])

print(teams.unique())
print("Total unique team names:", teams.nunique())


team_name_mapping = {
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru",
    "Kings XI Punjab": "Punjab Kings",
    "Delhi Daredevils": "Delhi Capitals",
    "Rising Pune Supergiants": "Rising Pune Supergiant"
}

matches["team1"]=matches["team1"].replace(team_name_mapping)
matches["team2"]=matches["team2"].replace(team_name_mapping)
print("\n")
print(matches["team1"].unique())

deliveries["batting_team"] = deliveries["batting_team"].replace(team_name_mapping)
deliveries["bowling_team"] = deliveries["bowling_team"].replace(team_name_mapping)


print(
    deliveries["batting_team"].nunique()
)
print(
    deliveries["bowling_team"].nunique()
)

matches["toss_winner"]=matches["toss_winner"].replace(team_name_mapping)
matches["winner"]=matches["winner"].replace(team_name_mapping)

print(
    matches["toss_winner"].nunique()
)
print(
    matches["winner"].nunique()
)

print("\n===== FINAL CLEANING CHECK =====")

print("Duplicate matches:", matches.duplicated().sum())
print("Duplicate deliveries:", deliveries.duplicated().sum())

print("\nMissing values in matches:")
print(matches.isnull().sum())

print("\nMissing values in deliveries:")
print(deliveries.isnull().sum())

print("\nUnique teams:")
teams = pd.concat([matches["team1"], matches["team2"]])
print(teams.nunique())

matches.to_csv("data/matches_cleaned.csv", index=False)
deliveries.to_csv("data/deliveries_cleaned.csv", index=False)

print("Cleaned datasets saved successfully!")