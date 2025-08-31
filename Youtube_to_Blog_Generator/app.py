import os
import io
import streamlit as st
from dotenv import load_dotenv

# ✅ Load env BEFORE importing crew (so tools see the keys at import time)
load_dotenv()

from crew import crew  # after env is loaded

st.set_page_config(
    page_title="YouTube → Blog Generator",
    page_icon="📝",
    layout="centered"
)

# --- Header ---
st.title("📹 → 📝 YouTube to Blog Generator")
st.caption("Paste a YouTube video link or ID. The app will fetch the transcript (if available) and write a clean blog post.")

# --- Input Area ---
with st.form("yt_form", clear_on_submit=False):
    video_input = st.text_input(
        "YouTube Video URL or ID",
        placeholder="https://www.youtube.com/watch?v=XXXXXXXXXXX or just the 11-char ID"
    )
    col1, col2 = st.columns(2)
    with col1:
        target_words = st.slider("Target length (approx. words)", 600, 1500, 900, step=50)
    with col2:
        include_tldr = st.checkbox("Include TL;DR", True)

    submitted = st.form_submit_button("🚀 Generate Blog Post")

if submitted:
    if not video_input.strip():
        st.error("Please enter a valid YouTube URL or 11-character video ID.")
    else:
        with st.spinner("Processing video and generating your blog..."):
            # Pass optional guidance as part of the 'topic' string to keep your original structure
            guidance = f"{video_input}\n\n[Guidance] target_words={target_words}; include_tldr={include_tldr}"
            try:
                result = crew.kickoff(inputs={"topic": guidance})
            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.stop()

        # ✅ FIX: Extract output string properly
        blog_text = None
        if hasattr(result, "output"):
            blog_text = result.output
        elif isinstance(result, str):
            blog_text = result
        else:
            blog_text = str(result)

        if not blog_text.strip():
            st.error("No result was returned. Check logs for details.")
        else:
            st.success("✅ Blog post generated!")
            st.subheader("📝 Preview")
            st.markdown(blog_text)

            # Download buttons
            md_bytes = blog_text.encode("utf-8")
            st.download_button(
                label="📥 Download as Markdown",
                data=md_bytes,
                file_name="blog_post.md",
                mime="text/markdown"
            )

            # Optional: also offer plain text
            st.download_button(
                label="📥 Download as Text",
                data=md_bytes,
                file_name="blog_post.txt",
                mime="text/plain"
            )

# --- Sidebar: Tips & Status ---
with st.sidebar:
    st.header("Settings & Status")
    openai_ok = bool(os.getenv("OPENAI_API_KEY"))
    yt_ok = bool(os.getenv("YOUTUBE_API_KEY"))
    st.write(f"OpenAI Key: {'✅' if openai_ok else '❌'}")
    st.write(f"YouTube Key: {'✅' if yt_ok else '⚠️ Optional (used for search)'}")
    st.markdown("---")
    st.markdown(
        "Tips:\n"
        "- If transcript is disabled, the app will still write from metadata.\n"
        "- You can paste a full URL or just the 11-character video ID.\n"
        "- Adjust target words in the form for longer/shorter posts."
    )
