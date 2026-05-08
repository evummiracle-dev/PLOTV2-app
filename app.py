 import streamlit as st
import os
import tempfile
import requests
from openai import OpenAI
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

st.set_page_config(page_title="PlotV2", layout="centered")

# We'll put the API key in Streamlit secrets later, not here
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🎬 PlotV2 - AI Story Video Generator")
st.write("Paste 15 scenes, one per line. I’ll generate images, audio, and stitch the video.")

story_title = st.text_input("Story Title", "The Boy in Kumasi Market")
story_input = st.text_area("15 Scenes - one per line", height=300,
                           placeholder="Scene 1: A boy wakes up in Kumasi...\nScene 2: He goes to the market...")

def make_video(scenes_text):
    temp_dir = tempfile.mkdtemp()
    all_clips = []

    for i, scene_text in enumerate(scenes_text):
        st.write(f"🎞️ Scene {i+1}/15: Generating image + audio...")

        # 1. Generate image with DALL-E 3
        img_path = os.path.join(temp_dir, f"scene_{i}.png")
        img_res = client.images.generate(
            model="dall-e-3",
            prompt=f"Cinematic 16:9 still, {scene_text}",
            size="1792x1024",
            quality="standard",
            n=1
        )
        img_data = requests.get(img_res.data[0].url).content
        with open(img_path, "wb") as f:
            f.write(img_data)

        # 2. Generate audio with OpenAI TTS - works great for Twi
        audio_path = os.path.join(temp_dir, f"scene_{i}.mp3")
        audio_res = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=scene_text
        )
        audio_res.stream_to_file(audio_path)

        # 3. Combine image + audio with moviepy
        audio_clip = AudioFileClip(audio_path)
        img_clip = ImageClip(img_path).set_duration(audio_clip.duration)
        img_clip = img_clip.set_audio(audio_clip)
        all_clips.append(img_clip)

    # 4. Stitch final video
    st.write("🔗 Stitching final video...")
    final_video = concatenate_videoclips(all_clips, method="compose")
    output_path = os.path.join(temp_dir, "plotv2_final.mp4")
    final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    return output_path

if st.button("Generate Video"):
    scenes = [s.strip() for s in story_input.split("\n") if s.strip()]

    if len(scenes)!= 15:
        st.error("You need exactly 15 scenes, one per line")
    else:
        with st.spinner("Creating video... takes 3-5 mins"):
            video_path = make_video(scenes)
            st.success("Done!")
            st.video(video_path)
            st.download_button("Download MP4", open(video_path, "rb"), file_name=f"{story_title}.mp4")
