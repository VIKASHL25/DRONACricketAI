import streamlit as st
from services.cricket_api import get_live_matches, get_match_details
from agents.simulator import simulate_over
from agents.coach import coach_agent
from visuali.field_plot import draw_field

st.set_page_config(
    page_title="DRONA Cricket AI",
    layout="wide",
    page_icon="🏏"
)

st.title("🏏 DRONA – Cricket Tactical Intelligence Engine")

mode=st.radio(
    "Select Mode",
    ["📡 Live Match Mode", " Manual Scenario Mode"]
)

if mode=="📡 Live Match Mode":

    try:
        matches=get_live_matches()

        if not matches:
            st.warning("No live matches available.")
            st.stop()

        match_dict={
            f"{m['name']} | {m['status']}": m
            for m in matches
        }

        selected_label=st.selectbox(
            "Select Live Match",
            list(match_dict.keys())
        )

        selected_match=match_dict[selected_label]

    except Exception as e:
        st.error("Live API Error")
        st.text(str(e))
        st.stop()

    try:
        match_details=get_match_details(selected_match["match_id"])

        match_header=match_details.get("matchHeader", {})
        match_score=match_details.get("matchScore", {})
        miniscore=match_details.get("miniscore", {})

        status=match_header.get("status") or selected_match.get("status", "")
        match_format=match_header.get("matchFormat", "T20")

        st.subheader("📊 Match Information")
        st.write(f"**Status:** {status}")
        st.write(f"**Format:** {match_format}")

        if any(word in status.lower() for word in ["won", "match over", "abandoned", "tied"]):

            st.success("🏆 Match Completed")

            team1=match_header.get("team1", {}).get("teamName", "Team 1")
            team2=match_header.get("team2", {}).get("teamName", "Team 2")

            team1_score=match_score.get("team1Score", {})
            team2_score=match_score.get("team2Score", {})

            st.subheader("📊 Final Scorecard")

            def extract_score(score_dict):
                if not score_dict:
                    return None

                for value in score_dict.values():
                    if isinstance(value, dict):
                        runs=value.get("runs")
                        wickets=value.get("wickets")
                        overs=value.get("overs")

                        if runs is not None:
                            return runs, wickets, overs

                return None

            col1, col2=st.columns(2)

            with col1:
                result=extract_score(team1_score)
                if result:
                    runs, wickets, overs=result
                    st.metric(team1, f"{runs}/{wickets}")
                    st.caption(f"Overs: {overs}")
                else:
                    st.metric(team1, "Score Not Available")

            with col2:
                result=extract_score(team2_score)
                if result:
                    runs, wickets, overs=result
                    st.metric(team2, f"{runs}/{wickets}")
                    st.caption(f"Overs: {overs}")
                else:
                    st.metric(team2, "Score Not Available")

            st.subheader(" Result")
            st.info(status)

        elif miniscore:

            current_score=miniscore.get("score", 0)
            wickets=miniscore.get("wickets", 0)
            overs=float(miniscore.get("overs", 0))
            target=miniscore.get("target", 0)

            striker_data=miniscore.get("striker", {})
            striker=striker_data.get("batName", "Unknown")
            striker_runs=striker_data.get("runs", 0)
            striker_balls=striker_data.get("balls", 1)

            bowler=miniscore.get("bowlerStriker", {}).get("bowlName", "Unknown")

            total_overs=50 if match_format=="ODI" else 20

            balls_left=int((total_overs-overs)*6)
            required_runs=target-current_score if target else 0
            wickets_in_hand=10-wickets

            col1, col2, col3=st.columns(3)
            col1.metric("Score", f"{current_score}/{wickets}")
            col2.metric("Overs", overs)
            col3.metric("Target", target if target else "N/A")

            st.write(f"**Striker:** {striker} ({striker_runs} off {striker_balls})")
            st.write(f"**Bowler:** {bowler}")
            st.write(f"**Wickets in Hand:** {wickets_in_hand}")

            if required_runs > 0 and balls_left > 0:

                win_prob=simulate_over(
                    required_runs,
                    balls_left,
                    aggression=1.2,
                    batsman_runs=striker_runs,
                    balls_faced=striker_balls,
                    wickets_in_hand=wickets_in_hand
                )

                strategy=coach_agent(
                    f"Need {required_runs} in {balls_left} balls. "
                    f"Striker: {striker} ({striker_runs} off {striker_balls}). "
                    f"Bowler: {bowler}. "
                    f"Wickets in hand: {wickets_in_hand}.",
                    win_prob
                )

                st.subheader("Predicted Win Probability")
                st.metric("Winning Chance", f"{win_prob * 100:.4f}%")

                st.subheader("Strategy Recommendation")
                st.write(strategy)

                st.subheader("🏟 Recommended Field Placement")

                fig = draw_field(
                    required_runs,
                    balls_left,
                    wickets_in_hand
                )

                colA, colB, colC=st.columns([1, 2, 1])
                with colB:
                    st.pyplot(fig)

        else:
            st.info("Match has not started yet.")
            st.write(status)

    except Exception as e:
        st.error("Error processing match data")
        st.text(str(e))
        st.stop()

else:

    st.subheader("Enter Custom Match Scenario")

    col1, col2=st.columns(2)

    with col1:
        striker=st.text_input("Striker Name")
        required_runs=st.number_input("Runs Needed", min_value=1)
        batsman_runs=st.number_input("Batsman Current Runs", min_value=0)

    with col2:
        bowler=st.text_input("Bowler Name")
        balls_left=st.number_input("Balls Remaining", min_value=1)
        balls_faced=st.number_input("Balls Faced", min_value=1)

    wickets_in_hand=st.slider("Wickets In Hand", 1, 10, 6)
    aggression=st.slider("Aggression Level", 0.5, 2.0, 1.0)

    if st.button("Generate Strategy"):

        win_prob=simulate_over(
            required_runs,
            balls_left,
            aggression,
            batsman_runs,
            balls_faced,
            wickets_in_hand
        )

        strategy=coach_agent(
            f"Need {required_runs} in {balls_left} balls. "
            f"Striker: {striker} ({batsman_runs} off {balls_faced}). "
            f"Wickets in hand: {wickets_in_hand}. "
            f"Bowler: {bowler}.",
            win_prob
        )

        st.subheader("Predicted Win Probability")
        st.metric("Winning Chance", f"{win_prob * 100:.4f}%")

        st.subheader("Strategy Recommendation")
        st.write(strategy)

        st.subheader("Recommended Field Placement")

        fig=draw_field(
            required_runs,
            balls_left,
            wickets_in_hand
        )

        colA, colB, colC=st.columns([1, 2, 1])
        with colB:
            st.pyplot(fig)
