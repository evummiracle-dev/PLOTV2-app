import streamlit as st
from datetime import datetime

st.set_page_config(page_title="PLOTV2 Scene Generator", page_icon="🎬", layout="centered")

if 'scenes_5' not in st.session_state:
    st.session_state.scenes_5 = []
if 'scenes_10' not in st.session_state:
    st.session_state.scenes_10 = []
if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False

st.title("🎬 PLOTV2 Scene Generator")
st.caption("Generate scenes in English, Twi, French or Pidgin. Pick your mood. Get your script.")
st.divider()

col1, col2 = st.columns(2)
with col1:
    title = st.text_input("Video Title", placeholder="e.g. The Lost Phone")
with col2:
    language = st.selectbox("Language", ["English", "Twi", "French", "Pidgin"])

user_script = st.text_area("Or Paste Your Script", placeholder="Paste script here if you have one...", height=100)

moods = [
    "Dark", "Comedy", "Romantic", "Action", "Horror", "Drama", "Thriller", "Mystery",
    "Adventure", "Sci-Fi", "Fantasy", "Documentary", "Motivational", "Sad", "Suspense", "Cinematic"
]
mood = st.selectbox("Choose Mood", moods)
st.divider()

def generate_scenes(title, script, language, mood, count):
    base = title if title else "Your Story"
    if script:
        base = f"Story based on: {script[:40]}..."

    templates = {
        "English": "Scene {n}: In a {mood} tone, {base}. The main character faces a challenge.",
        "Twi": "Scene {n}: {mood} kwan so, {base}. Nipa titiriw no hyia haw bi.",
        "French": "Scène {n}: Sur un ton {mood}, {base}. Le personnage principal fait face à un défi.",
        "Pidgin": "Scene {n}: For {mood} mood, {base}. Main person dey face problem."
    }

    scenes = []
    for i in range(1, count + 1):
        scene = templates[language].format(n=i, mood=mood.lower(), base=base)
        scenes.append(scene)
    return scenes

if st.button("🎯 Generate 5 Scenes - FREE", type="primary", use_container_width=True):
    if not title and not user_script:
        st.error("Please enter a Title OR paste a Script first")
    else:
        st.session_state.scenes_5 = generate_scenes(title, user_script, language, mood, 5)
        st.session_state.scenes_10 = []
        st.session_state.unlocked = False

if st.session_state.scenes_5:
    st.subheader(f"Your 5 {language} Scenes - {mood} Mood")
    for scene in st.session_state.scenes_5:
        st.write(scene)
    st.divider()

    st.subheader("Unlock More")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔓 Unlock 10 Scenes - 10 GHS", use_container_width=True):
            st.info("""
            **Send 10 GHS MoMo to: 0555834680**
            **Reference:** PLOTV2-10SCENES
            **Then DM screenshot to unlock**

            You will receive 10 full scenes after payment confirmation.
            """)
            if not title and not user_script:
                pass
            else:
                st.session_state.scenes_10 = generate_scenes(title, user_script, language, mood, 10)
                st.session_state.unlocked = True

    with col2:
        if st.button("📄 Save as PDF - 10 GHS", use_container_width=True):
            st.info("""
            **Send 10 GHS MoMo to: 0555834680**
            **Reference:** PLOTV2-PDF
            **Then DM screenshot to unlock**

            You will receive PDF download after payment confirmation.
            """)

if st.session_state.unlocked and st.session_state.scenes_10:
    st.divider()
    st.success("✅ Payment Instructions Shown Above. Send screenshot to unlock these scenes:")
    st.subheader(f"Your 10 {language} Scenes - {mood} Mood")
    for scene in st.session_state.scenes_10:
        st.write(scene)

    st.divider()
    st.subheader("🎁 Bonus: Convert to Full Script - FREE")
    if st.button("Convert These 10 Scenes to Script"):
        full_script = "\n\n".join(st.session_state.scenes_10)
        st.text_area("Your Full Script", full_script, height=300)
        st.download_button("Download Script.txt", full_script, file_name=f"PLOTV2_{title or 'script'}.txt")

st.divider()
st.caption("PLOTV2 © 2026 | Questions? DM @Miracle | MoMo: 0555834680")
