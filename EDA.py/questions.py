import pandas as pd
matches = pd.read_csv("data/matches_cleaned.csv")
deliveries = pd.read_csv("data/deliveries_cleaned.csv")

print(matches.columns.tolist())

# print(matches.shape)
# print(deliveries.shape)

# #01
# print(
#     (matches.groupby("season")).size()
#     )
# #02
# print(
# matches.groupby("season")[["team1","team2"]].nunique()
# )

# #04
# print(
#     matches.groupby("venue").size().sort_values(ascending=False)
#     )

# #05

# print(
#     matches.groupby("city").size().sort_values(ascending=False)
# )

# print(
#     matches["target_runs"].mean()
# )
# print("\n")
# #06
# print(
#     matches.groupby("winner").size().sort_values(ascending=False).head(10)
# )
# print("\n")

# #07

# matches_played = pd.concat([
#     matches["team1"],
#     matches["team2"]
# ]).value_counts()

# df= matches.groupby("winner").size()

# percent = df*100/(matches_played)

# print(percent.sort_values(ascending=False).head(5))

# print("Team:", percent.idxmax())
# print("Win percentage:", round(percent.max(), 2))

# team_season_wins = (
#     matches.groupby(["season", "winner"])
#     .size()
#     .unstack(fill_value=0)
# )

# print(team_season_wins)

# #11
# print(
#     matches.groupby("toss_winner").size().sort_values(ascending=False).head(5)
# )
# print("teams_choosing_batting")
# print(matches[matches["toss_decision"]=="bat"].groupby("toss_winner").size().sort_values(ascending=False))
# print("teams_choosing_fielding")
# print(matches[matches["toss_decision"]=="field"].groupby("toss_winner").size().sort_values(ascending=False))

# print(matches.groupby("toss_decision").size())

# matches["toss_match_winner"] = (
#     matches["toss_winner"] == matches["winner"]
# )
# print(matches["toss_match_winner"].value_counts())

# print(
#     matches.groupby("result").size()
# )
# print(
#     deliveries.groupby("batter")["batsman_runs"].sum().sort_values(ascending=False).head(5)
# )

# bowler_wickets = deliveries[
#     deliveries["dismissal_kind"].isin([
#         "bowled",
#         "caught",
#         "caught and bowled",
#         "lbw",
#         "stumped",
#         "hit wicket"
#     ])
# ].groupby("bowler").size().sort_values(ascending=False)

# print(bowler_wickets.head(10))