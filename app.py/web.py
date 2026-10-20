import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

matches = pd.read_csv("data/matches_cleaned.csv")
deliveries = pd.read_csv("data/deliveries_cleaned.csv")

st.set_page_config(
    page_title="IPL Data Analysis Project",
    page_icon="🏏",
    layout="wide"
)

st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# ================= Team Color Map=================     

map = {
    "Chennai Super Kings": "#FFFF3C",
    "Mumbai Indians": "#004BA0",
    "Royal Challengers Bengaluru": "#EC1C24",
    "Kolkata Knight Riders": "#3A225D",
    "Delhi Capitals": "#282968",
    "Sunrisers Hyderabad": "#FF822A",
    "Punjab Kings": "#ED1B24",
    "Rajasthan Royals": "#EA1A85",
    "Gujarat Titans": "#1B2133",
    "Lucknow Super Giants": "#00A9E0",
    "Rising Pune Supergiant": "#D71920",
    "Gujarat Lions": "#F46B29",
    "Pune Warriors": "#1B458F",
    "Kochi Tuskers Kerala": "#E36C2F",
    "Deccan Chargers": "#B02A30"
}


# ================= SIDEBAR =================     
with st.sidebar:
    st.title("Navigation")
    st.markdown("---")
    page=st.radio(
        "Navigate",
          [
            "🏠 Home",
            "🏆 Team Analysis",
            "👤 Player Analysis",
            
            
        ]
    )
    st.markdown("---")

    st.caption("Explore IPL statistics, trends and performances.")  

# ================= HOME =================

if page == "🏠 Home":

        st.title("𝗦𝗰𝗼𝗿𝗲𝗦𝗲𝗻𝘀𝗲",text_alignment="center")
        st.markdown("<br>",unsafe_allow_html=True)
        st.write(
            "Welcome to the IPL Data Analysis Dashboard — an interactive platform "
            "designed to explore and understand the rich history of the Indian Premier League. "
            "Analyze team and player performances, season-wise trends," 
             "batting and bowling statistics, and many more "
            "through interactive visualizations and data-driven analysis."
        )

        st.subheader("Quick stats",text_alignment="center")
        st.markdown("<br>",unsafe_allow_html=True)

        col1, col2, col3, col4,col5= st.columns(5)
        with col1:
            st.metric("Total_matches",len(matches))

        with col2:
            st.metric("Total Teams",pd.concat([matches["team1"],matches["team2"]]).nunique())
        with col3:
            st.metric("Total Seasons", matches["season"].nunique())

        with col4:
            st.metric("Total Venues", matches["venue"].nunique())

        with col5:
            st.metric("Players Participated", pd.concat([deliveries["batter"],deliveries["non_striker"],deliveries["bowler"]]).nunique())   



        st.subheader("🏆 Most Successful Teams")

        win= matches.groupby("winner").size().reset_index(name="wins").sort_values("wins", ascending=False)
        fig=px.bar(win, x = "wins", y = "winner", orientation ="h",color = "winner",color_discrete_map=map)      
        st.plotly_chart(fig,use_container_width=True)


        st.subheader("🔥Players to Watch")
        col1, col2, col3, col4= st.columns(4)

        with col1:
         
            st.write("🏏 Top Batsmen")

            top_batsmen = [
                "Virat Kohli",
                "Rohit Sharma",
                "MS Dhoni",
                "Chris Gayle",
                "AB de Villiers"
            ]

            st.dataframe(
                pd.DataFrame({"Icons": top_batsmen}),
                hide_index=True,
                use_container_width=True
            )


        with col2:
            st.write("🎯 Best Bowlers")
    
            best_bowlers = [
                "Jasprit Bumrah",
                "Lasith Malinga",
                "Rashid Khan",
                "Sunil Narine",
                "Bhuvneshwar Kumar"
            ]

            st.dataframe(
                pd.DataFrame({"Icons": best_bowlers}),
                hide_index=True,
                use_container_width=True
            )


        with col3:
            st.write("🔄 Best All-Rounders")

            best_all_rounders = [
                "Ravindra Jadeja",
                "Hardik Pandya",
                "Andre Russell",
                "Shane Watson",
                "Kieron Pollard"
            ]

            st.dataframe(
                pd.DataFrame({"Icons": best_all_rounders}),
                hide_index=True,
                use_container_width=True
            )


        with col4:

            st.write("🧤 Best Fielders")
    
            best_fielders = [
                "Ravindra Jadeja",
                "Suresh Raina",
                "AB de Villiers",
                "Kieron Pollard",
                "David Miller"
            ]

            st.dataframe(
                pd.DataFrame({"Icons": best_fielders}),
                hide_index=True,
                use_container_width=True
            )


        st.subheader("👑 Champions")
 
        df = matches.sort_values("match_date").groupby("season").last()
        p = df["winner"]

        champions = p.value_counts().reset_index()
        champions.columns = ["Team", "Titles"]

        fig = px.bar(
        champions,
        x="Team",
        y="Titles",
        color="Team",
        color_discrete_map = map
    )

        st.plotly_chart(fig, use_container_width=True)



# ================= PLAYER ANALYSIS =================


if page ==  "👤 Player Analysis":

    st.title("Player Analytics", text_alignment="center")

    st.write( "Dive into individual IPL performances with interactive, data-driven analytics. Select a player to explore their batting and bowling statistics, career milestones, performance trends, and scoring patterns across seasons.") 

    players = sorted(set(
        deliveries["batter"].dropna()
    ) | set(
        deliveries["bowler"].dropna()
    ))
    player = st.selectbox(
          "Search for a Player:",
          players,
          index = None,
          placeholder = "Choose any Player")

    
    if player:
       
        st.success( f"You selected : {player}")
        

        runs = deliveries.groupby("batter")["batsman_runs"].sum()
        player_runs = runs[player]

        wickets = deliveries[deliveries["dismissal_kind"].isin([
           "bowled",
           "caught",
           "caught and bowled",
           "lbw",
           "stumped",
           "hit wicket"
        ])].groupby("bowler").size()
        player_wickets = wickets.get(player,0)

        if(player_runs > 1000 and player_wickets > 50):
            category = "All-Rounder"

        elif (player_runs > 1000):
                       category = "Batsman"
        elif (player_wickets > 60):
                       category = "Bowler"
        else:
             category = "Miscellaneous"

        batting_matches = deliveries[
        deliveries["batter"] == player]["match_id"]

        bowling_matches = deliveries[
        deliveries["bowler"] == player]["match_id"]

        matches_played = pd.concat([
        batting_matches,
        bowling_matches]).nunique()

        total_runs = deliveries[
            deliveries["batter"] == player
        ]["batsman_runs"].sum()
       
        
        wickets = deliveries[deliveries["dismissal_kind"].isin([
           "bowled",
           "caught",
           "caught and bowled",
           "lbw",
           "stumped",
           "hit wicket"
        ])].groupby("bowler").size()
        player_wickets = wickets.get(player,0)

        total_runs = deliveries[
        deliveries["batter"] == player
        ]["batsman_runs"].sum()

        dismissals = deliveries[
        deliveries["player_dismissed"] == player
        ].shape[0]

        if dismissals > 0:
            batting_average = total_runs / dismissals
        else:
            batting_average = 0

        df = deliveries[deliveries["batter"]== player]
        p=df["batsman_runs"].sum()
        q= df.shape[0]
        sr = (p*100)/q
        strike_rate = round(sr,2)


        player_bowling = deliveries[deliveries["bowler"] == player]

        runs_conceded = player_bowling["total_runs"].sum()

        legal_balls = player_bowling[
            player_bowling["extras_type"].isna() |
            ~player_bowling["extras_type"].isin(["wides", "noballs"])
        ].shape[0]

        if legal_balls > 0:
            overs = legal_balls / 6
            economy_rate = runs_conceded / overs
        else:
            economy_rate = 0

        p=deliveries[deliveries["bowler"]== player]
        q = p[p["is_wicket"]==1].shape[0]  
        bowling_avg = round(runs_conceded/q,2)

        df = deliveries[deliveries["batter"] == player].groupby("match_id")["batsman_runs"].sum()
        centuries = (df>= 100).sum()
         

        df = deliveries[deliveries["batter"] == player].groupby("match_id")["batsman_runs"].sum()
        hc = (df>= 50).sum()

        # Best Bowling Figures

        bowling_by_match = player_bowling.groupby("match_id").agg(
            runs=("total_runs", "sum"),
            wickets=("is_wicket", "sum")
        )
        bowling_by_match = bowling_by_match[
            bowling_by_match["wickets"] > 0
        ]

        # Sort: most wickets first, then fewest runs
        bowling_by_match = bowling_by_match.sort_values(
            ["wickets", "runs"],
            ascending=[False, True]
        )

        if len(bowling_by_match) > 0:
            best_wickets = bowling_by_match.iloc[0]["wickets"]
            best_runs = bowling_by_match.iloc[0]["runs"]

            best_bowling = f"{int(best_wickets)}/{int(best_runs)}"
        else:
            best_bowling = "—"

        wickets = deliveries[deliveries["dismissal_kind"].isin([
           "bowled",
           "caught",
           "caught and bowled",
           "lbw",
           "stumped",
           "hit wicket"
        ])]

        df = wickets[wickets["bowler"] == player]
        c = df.groupby("match_id")["is_wicket"].sum()
        hauls = (c>=5).sum()    


       


        col1,col2,col3,col4 = st.columns(4)

        if category == "Batsman":
            if player == "Virat Kohli":
                st.info("🔥 Top Batsman")
            with col1:
                 st.metric("Category",category) 
            with col2:
                st.metric("Matches Played", matches_played)
            with col3:
                st.metric("Total Runs",total_runs) 
            
            with col4:
                st.metric("Average",round(batting_average,2))

            col5,col6,col7,col8 = st.columns(4)        
            with col5:
                st.metric("Strike Rate",strike_rate)
            with col6:
                 st.metric("Centuries",centuries)
            with col7:
                 st.metric("Half Centuries",hc)            
            with col8:
                 st.metric("Total Wickets",player_wickets)  

                # Get selected player's deliveries
            player_deliveries = deliveries[
                deliveries["batter"] == player
            ].copy()

            # Get match IDs in the same order as they appear in deliveries
            match_ids = deliveries["match_id"].unique()

            # Deliveries dataset contains matches only up to Season 17
            matches_for_mapping = matches[
                matches["season"] <= 17
            ].copy()

            # Create match_id -> season mapping
            match_season = {}

            start = 0

            for season, group in matches_for_mapping.groupby("season", sort=True):

                number_of_matches = len(group)

                season_match_ids = match_ids[
                    start:start + number_of_matches
                ]

                for match_id in season_match_ids:
                    match_season[match_id] = season

                start += number_of_matches

            # Add season to player's deliveries
            player_deliveries["season"] = (
                player_deliveries["match_id"].map(match_season)
            )

            # Calculate total runs in each season
            season_runs = (
                player_deliveries
                .groupby("season")["batsman_runs"]
                .sum()
                .reset_index()
            )

            # Rename column for readability
            season_runs = season_runs.rename(
                columns={
                    "batsman_runs": "Runs_Scored"
                }
            )

            # Plot
            


            run_distribution = (
                 
            player_deliveries
            .groupby("batsman_runs")["batsman_runs"]
            .count()
            .reset_index(name="Count")
            )

            run_distribution = run_distribution[
                run_distribution["batsman_runs"].isin([1, 2, 3, 4, 6])
            ]

            run_distribution["Scoring"] = run_distribution["batsman_runs"].astype(str) + " Runs"

 

            col9,col10 = st.columns(2)  
            with col9:
                 fig = px.bar(
                        season_runs,
                        x="season",
                        y="Runs_Scored",
                        title=f"{player} : Runs per Season"
                             )
                 st.plotly_chart(
                fig,
                use_container_width=True )

            with col10:
                fig = px.pie(
                run_distribution,
                names="Scoring",
                values="Count",
                title=f"{player} : Scoring Pattern"
            )

                st.plotly_chart(fig, use_container_width=True)

            col11,col12 = st.columns(2)      
            with col11:     
                df = (player_deliveries.groupby("season").agg( 
                    Runs=("batsman_runs","sum"),
                    Balls = ("batsman_runs","count") 
                ) 
                .reset_index()
                )

                df["Strike_rate"]  =(df["Runs"]/df["Balls"])*100 

                fig = px.scatter(
                    df,
                    x="Strike_rate",
                    y="season",
                    hover_data = ["season"],
                    title = f"{player} : Runs vs Strike_rate"
                )
                st.plotly_chart(fig, use_container_width=True)
            with col12:
                 # Strike Rate per Season

                fig = px.line(
                    df,
                    x="season",
                    y="Strike_rate",
                    markers=True,
                    title=f"{player} : Strike Rate per Season"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )
        elif category == "Bowler":
            with col1:
                 st.metric("Category",category)
            with col2:
                st.metric("Matches Played", matches_played)

            with col3:
                st.metric("Total Wickets", player_wickets)

            with col4:
                st.metric("Economy Rate",round(economy_rate,2) )

            col5,col6,col7,col8 = st.columns(4)    

            with col5:
                st.metric("Bowling Average", bowling_avg)
            with col6:
                 st.metric("Best Figures",best_bowling)
            with col7:
                 st.metric("5 Wicket Hauls", hauls)         
            with col8:
                st.metric("Total Runs", total_runs)

            col9,col10 = st.columns(2)

            # Bowler's deliveries
            player_bowling = deliveries[
                deliveries["bowler"] == player
            ].copy()

            # Map match IDs to seasons
            match_ids = deliveries["match_id"].unique()

            matches_for_mapping = matches[
                matches["season"] <= 17
            ].copy()

            match_season = {}
            start = 0

            for season, group in matches_for_mapping.groupby("season", sort=True):

                number_of_matches = len(group)

                season_match_ids = match_ids[
                    start:start + number_of_matches
                ]

                for match_id in season_match_ids:
                    match_season[match_id] = season

                start += number_of_matches



            player_bowling["season"] = (
                player_bowling["match_id"].map(match_season)
            )

            wickets_by_season = (
                player_bowling[
                player_bowling["dismissal_kind"].isin([
            "bowled",
            "caught",
            "caught and bowled",
            "lbw",
            "stumped",
            "hit wicket"
                ])  ]
                .groupby("season")
                .size()
                .reset_index(name="Wickets")
            )

            with col9 :
                 fig = px.bar(
                wickets_by_season,
                x="season",
                y="Wickets",
                title=f"{player} : Wickets per Season"
            )
            st.plotly_chart(
                    fig,
                    use_container_width=True
                )
            # Economy Rate per Season

            economy_by_season = (
                    player_bowling
                    .groupby("season")
                    .apply(
                        lambda x: (
                            x["total_runs"].sum() /
                            (
                                x[
                                    x["extras_type"].isna() |
                                    ~x["extras_type"].isin(["wides", "noballs"])
                                ].shape[0] / 6
                            )
                        )
                    )
                    .reset_index(name="Economy_Rate")
                )

            with col10:
                 fig = px.line(
                    economy_by_season,
                    x = "season",
                    y = "Economy_Rate",
                    markers = True,
                    title= f"{player} : Economy Rate Per Season"
            )
            st.plotly_chart(fig, use_container_width= True)

            col11,col12 = st.columns(2)

                                     

        elif category == "All-Rounder":
            with col1:
                 st.metric("Category",category)
            with col2:
                st.metric("Matches Played", matches_played)
            with col3:
                st.metric("Total Runs", total_runs)

            with col4:
                st.metric("Strike Rate", strike_rate)
                
            col5,col6,col7,col8 = st.columns(4)        
            with col5:
                 st.metric("Centuries",centuries)
            with col6:
                  st.metric("Half Centuries",hc)            
            with col7:
                st.metric("Economy Rate", round(economy_rate,2))
            with col8:
                st.metric("Total Wickets", player_wickets)   

            # Prepare player batting and bowling data
            player_deliveries = deliveries[
                deliveries["batter"] == player
            ].copy()

            player_bowling = deliveries[
                deliveries["bowler"] == player
            ].copy()

            # Create match ID-to-season mapping
            match_ids = sorted(deliveries["match_id"].unique())

            matches_for_mapping = (
                matches[matches["season"] <= 17]
                .sort_values(
                    ["season", "match_date", "match_number"]
                )
                .copy()
            )

            if len(match_ids) != len(matches_for_mapping):
                st.error("Match counts do not match. Season mapping needs checking.")
            else:
                match_season = dict(
                    zip(match_ids, matches_for_mapping["season"])
                )

                player_deliveries["season"] = (
                    player_deliveries["match_id"].map(match_season)
                )

                player_bowling["season"] = (
                    player_bowling["match_id"].map(match_season)
                )

                # Graph 1: Runs per Season
                st.subheader("🏏 Runs per Season")

                season_runs = (
                    player_deliveries
                    .groupby("season")["batsman_runs"]
                    .sum()
                    .reset_index(name="Runs")
                    .sort_values("season")
                )

                fig_runs = px.bar(
                    season_runs,
                    x="season",
                    y="Runs",
                    title=f"{player} — Runs per Season",
                    labels={
                        "season": "IPL Season",
                        "Runs": "Total Runs"
                    }
                )

                st.plotly_chart(
                    fig_runs,
                    use_container_width=True
                )

                # Graph 2: Wickets per Season
                st.subheader("🎯 Wickets per Season")

                bowler_wickets = player_bowling[
                    player_bowling["dismissal_kind"].isin([
                        "bowled",
                        "caught",
                        "caught and bowled",
                        "lbw",
                        "stumped",
                        "hit wicket"
                    ])
                ]

                season_wickets = (
                    bowler_wickets
                    .groupby("season")
                    .size()
                    .reset_index(name="Wickets")
                    .sort_values("season")
                )

                fig_wickets = px.bar(
                    season_wickets,
                    x="season",
                    y="Wickets",
                    title=f"{player} — Wickets per Season",
                    labels={
                        "season": "IPL Season",
                        "Wickets": "Total Wickets"
                    }
                )

                st.plotly_chart(
                    fig_wickets,
                    use_container_width=True
                )
                     
                
        elif category == "Miscellaneous":
                    
            with col1:
                st.metric("Category",category)
            with col2:
                st.metric("Matches Played", matches_played)
            with col3:
                st.metric("Total Runs", total_runs)  
            with col4:
                st.metric("Strike Rate", strike_rate)

            col5,col6,col7,col8 = st.columns(4)    
            with col5:
                 st.metric("Centuries",centuries)
            with col6:
                 st.metric("Half Cenuries",hc)     
            with col7:
                st.metric("Total Wickets", player_wickets)
            with col8:
                st.metric("Economy Rate", round(economy_rate,2))
                # Prepare player batting and bowling data
            player_deliveries = deliveries[
                deliveries["batter"] == player
            ].copy()

            player_bowling = deliveries[
                deliveries["bowler"] == player
            ].copy()


            # Map match IDs to seasons
            match_ids = sorted(deliveries["match_id"].dropna().unique())

            matches_for_mapping = matches[
                matches["season"] <= 17
            ].copy()

            matches_for_mapping["match_date"] = pd.to_datetime(
                matches_for_mapping["match_date"],
                errors="coerce"
            )

            matches_for_mapping = matches_for_mapping.sort_values(
                ["season", "match_date", "match_number"]
            )

            if len(match_ids) != len(matches_for_mapping):

                st.error(
                    "Match counts do not match. "
                    "Please check the match ID-to-season mapping."
                )

            else:

                match_season = dict(
                    zip(
                        match_ids,
                        matches_for_mapping["season"]
                    )
                )

                player_deliveries["season"] = (
                    player_deliveries["match_id"].map(match_season)
                )

                player_bowling["season"] = (
                    player_bowling["match_id"].map(match_season)
                )


                # =====================================
                # GRAPH 1: RUNS PER SEASON
                # =====================================

                st.subheader("🏏 Runs per Season")

                season_runs = (
                    player_deliveries
                    .groupby("season")["batsman_runs"]
                    .sum()
                    .reset_index(name="Runs")
                    .sort_values("season")
                )

                # Make the x-axis categorical to prevent decimal ticks
                season_runs["season"] = (
                    season_runs["season"].astype(int).astype(str)
                )

                fig_runs = px.bar(
                    season_runs,
                    x="season",
                    y="Runs",
                    title=f"{player} — Runs per Season",
                    labels={
                        "season": "IPL Season",
                        "Runs": "Total Runs"
                    }
                )

                fig_runs.update_layout(
                    xaxis=dict(
                        type="category",
                        title="IPL Season"
                    ),
                    yaxis_title="Total Runs"
                )

                st.plotly_chart(
                    fig_runs,
                    use_container_width=True
                )


                # =====================================
                # GRAPH 2: WICKETS PER SEASON
                # =====================================

                st.subheader("🎯 Wickets per Season")

                bowler_wickets = player_bowling[
                    player_bowling["dismissal_kind"].isin([
                        "bowled",
                        "caught",
                        "caught and bowled",
                        "lbw",
                        "stumped",
                        "hit wicket"
                    ])
                ]

                season_wickets = (
                    bowler_wickets
                    .groupby("season")
                    .size()
                    .reset_index(name="Wickets")
                    .sort_values("season")
                )

                # Make the x-axis categorical to prevent decimal ticks
                season_wickets["season"] = (
                    season_wickets["season"].astype(int).astype(str)
                )

                fig_wickets = px.bar(
                    season_wickets,
                    x="season",
                    y="Wickets",
                    title=f"{player} — Wickets per Season",
                    labels={
                        "season": "IPL Season",
                        "Wickets": "Total Wickets"
                    }
                )

                fig_wickets.update_layout(
                    xaxis=dict(
                        type="category",
                        title="IPL Season"
                    ),
                    yaxis_title="Total Wickets"
                )

                st.plotly_chart(
                    fig_wickets,
                    use_container_width=True
                )   





            
if page ==  "🏆 Team Analysis":

     st.title("Team Analytics", text_alignment= "center", width= "stretch")  
     st.write(
    "Explore the performance, achievements, and competitive journey of IPL teams "
    "through interactive, data-driven analytics. Analyze team wins, win percentages, "
    "matches played, season-wise performance, championship records, and overall "
    "consistency across different IPL seasons. Compare teams to understand their "
    "strengths, dominance, and performance trends throughout the history of the league."
    ) 
     
