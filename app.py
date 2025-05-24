import streamlit as st
import pandas as pd

# Load data
users = pd.read_csv("data/users.csv")
resources = pd.read_csv("data/resources.csv")
interactions = pd.read_csv("data/interactions.csv")
quiz_scores = pd.read_csv("data/quiz_scores.csv")

st.title("📚 Personalized Learning Recommender")

# 1. User selection
selected_user = st.selectbox("Select your name", users["user_name"])

def get_user_id(user_name):
    return users[users['user_name'] == user_name]['user_id'].values[0]

user_id = get_user_id(selected_user)

# 2. Learning preferences
st.subheader("🧭 Choose your learning preference")
topic_pref = st.radio("Select a topic", ["Python", "ML"])

# 3. Recommendation logic
def recommend(user_id, topic_pref):
    user_rated = interactions[interactions['user_id'] == user_id]['resource_id'].tolist()
    
    # Filter resources by topic preference
    filtered_resources = resources[resources['topic'] == topic_pref]

    # Resources user has already rated from that topic
    rated_in_topic = filtered_resources[filtered_resources['resource_id'].isin(user_rated)]['resource_id'].tolist()

    # Recommend resources in the topic that user hasn't rated yet
    recommended = filtered_resources[~filtered_resources['resource_id'].isin(rated_in_topic)]
    
    return recommended

recs = recommend(user_id, topic_pref)

st.subheader("🔍 Recommended For You")
if not recs.empty:
    for index, row in recs.iterrows():
        st.markdown(f"**{row['title']}** ({row['topic']} - {row['difficulty']})")
        st.markdown(f"[Open]({row['url']}) - Type: {row['type']}")
        st.markdown("---")
else:
    st.write("No new recommendations right now.")

# 4. Quiz scores section
st.subheader("📊 Your Quiz Scores")

user_scores = quiz_scores[quiz_scores['user_id'] == user_id]

if not user_scores.empty:
    st.bar_chart(user_scores.set_index("topic")["score"])
    st.write(user_scores[["topic", "score"]])
else:
    st.write("No quiz scores available.")

# 5. Rating input
st.subheader("⭐ Rate a Resource")

def add_rating(user_id):
    global interactions

    resource_to_rate = st.selectbox("Select a resource to rate", resources["title"])

    resource_id_to_rate = resources[resources["title"] == resource_to_rate]["resource_id"].values[0]

    rating = st.slider("Your rating (1-5)", 1, 5, 3)

    if st.button("Submit Rating"):
        new_entry = pd.DataFrame({
            "user_id": [user_id],
            "resource_id": [resource_id_to_rate],
            "rating": [rating]
        })
        interactions = pd.concat([interactions, new_entry], ignore_index=True)
        interactions.to_csv("data/interactions.csv", index=False)
        st.success(f"Thanks for rating '{resource_to_rate}' with {rating} stars!")

add_rating(user_id)
