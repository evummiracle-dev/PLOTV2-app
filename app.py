 import streamlit as st

st.set_page_config(page_title="PLOTV2", page_icon="📜")
st.title("📜 PLOTV2 Generator")

if 'free_done' not in st.session_state:
    st.session_state.free_done = False
if 'paid_scenes' not in st.session_state:
    st.session_state.paid_scenes = False
if 'paid_pdf' not in st.session_state:
    st.session_state.paid_pdf = False
if 'all_scenes' not in st.session_state:
    st.session_state.all_scenes = []

title = st.text_input("Video Title", "My lost car")
language = st.selectbox("Language", ["English", "Twi", "Pidgin", "French"])
mood = st.selectbox("Mood", [
    "Drama","Comedy","Action","Romantic","Horror","Thriller","Tragedy","Mystery",
    "Adventure","Crime","Fantasy","Sci-Fi","Gospel","Family","Sports","War"
])

def make_scenes(lang, mood, title, total):
    s = [
        f"OPENING: The story of {title} starts. Main character worried.",
        f"PROBLEM: {title} goes missing. Search begins fast.",
        f"CONFLICT: Fight breaks out because of {title}.",
        f"TWIST: Secret about {title} comes out. Shock.",
        f"CLIFFHANGER: Call about {title}. To be continued...",
        f"INVESTIGATION: Looking for clues about {title}.",
        f"DANGER: Attack happens over {title}. Someone hurt.",
        f"HOSPITAL: Recovering. Thinks of {title} always.",
        f"BETRAYAL: Friend stole {title}. Trust broken.",
        f"PLAN: New plan to get {title} back. Team ready.",
        f"INFILTRATION: Sneak in for {title}. Alarm blows.",
        f"CAPTURE: Caught with {title}. Enemy wins round 1.",
        f"ESCAPE: Clever escape using {title}. Explosion.",
        f"FINAL BATTLE: Last fight for {title}. One wins.",
        f"ENDING: {title} found. Life changed forever."
    ]
    
    if lang == "Twi":
        s = [x.replace("because of", "ɛsiane").replace("for", "ma") for x in s]
    elif lang == "Pidgin":
        s = [x.replace("is", "dey").replace("are", "dey") for x in s]
    elif lang == "French":
        s = [x.replace("OPENING", "DÉBUT").replace("for", "pour").replace("of", "de") for x in s]
    
    return s[:total]

# FREE 5 SCENES
st.subheader("1. FREE - 5 Scenes")
if st.button("Get 5 Scenes FREE", disabled=st.session_state.free_done):
    st.session_state.free_done = True
    scenes = make_scenes(language, mood, title, 5)
    st.session_state.all_scenes = scenes
    for i, scene in enumerate(scenes, 1):
        st.write(f"**Scene {i}:** {scene}")

# PAY 10 CEDIS FOR 10 MORE
if st.session_state.free_done and not st.session_state.paid_scenes:
    st.subheader("2. PAY - 10 More Scenes = 10 GHS")
    st.info("MoMo: 0555834680 | Ref: PLOTV2")
    if st.button("I Paid 10 Cedis - Unlock"):
        st.session_state.paid_scenes = True
        st.rerun()

if st.session_state.paid_scenes:
    scenes = make_scenes(language, mood, title, 15)[5:]
    st.session_state.all_scenes.extend(scenes)
    for i, scene in enumerate(scenes, 6):
        st.write(f"**Scene {i}:** {scene}")

# SCRIPT TAB - FREE
if st.session_state.all_scenes:
    st.subheader("3. SCRIPT TAB - FREE")
    if st.button("Make Full Script"):
        script = f"TITLE: {title}\nLANGUAGE: {language}\nMOOD: {mood}\n\n"
        for i, scene in enumerate(st.session_state.all_scenes, 1):
            script += f"SCENE {i}\n{scene}\n\n"
        st.code(script)
        st.download_button("Download TXT", script, f"{title}.txt")

# PDF TAB - 10 CEDIS
if st.session_state.all_scenes and not st.session_state.paid_pdf:
    st.subheader("4. PDF TAB - 10 GHS")
    st.info("MoMo: 0555834680 | Ref: PDF")
    if st.button("I Paid 10 Cedis - Unlock PDF"):
        st.session_state.paid_pdf = True
        st.rerun()

if st.session_state.paid_pdf:
    pdf_text = "\n\n".join([f"SCENE {i+1}: {s}" for i, s in enumerate(st.session_state.all_scenes)])
    st.download_button("Download PDF", pdf_text, f"{title}.pdf")
