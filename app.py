import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
from tavily import TavilyClient

# Load environment variables
load_dotenv()

# -------------------------------------------------------------------
# CLIENT INITIALIZATION
# -------------------------------------------------------------------
# AICredits uses standard OpenAI endpoints
client = OpenAI(
    base_url="https://api.aicredits.in/v1",
    api_key=os.getenv("AICREDITS_API_KEY")  # Reads sk-xxx key from .env
)

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Model configuration
MODEL_NAME = "gemini-2.0-flash-lite-001"

# Streamlit page configuration
st.set_page_config(
    page_title="YouTube Script Generator",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# -------------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------------
def get_realtime_info(query: str) -> tuple[str, str]:
    """
    Fetches web search data and attempts to summarize it using the LLM.
    Returns: (summary_text, raw_search_backup)
    """
    # Step 1: Tavily Search
    try:
        response = tavily_client.search(
            query=query,
            max_results=3,
            topic="general",
            search_depth="advanced"
        )
        results = response.get("results", []) if response else []

        if not results:
            return "", "No relevant search results found online."

        formatted_snippets = [
            f"### {res.get('title')}\n{res.get('content')}\n**Source:** {res.get('url')}"
            for res in results
        ]
        raw_source_info = "\n\n---\n\n".join(formatted_snippets)

    except Exception as e:
        st.error(f"❌ Search Error: Tavily API failed -> {str(e)}")
        return "", ""

    # Step 2: Gemini Summarization
    prompt = f"""You are a professional researcher. Summarize the following real-time data for '{query}'.

Requirements:
- Factual, concise, insightful (~200 words).
- Well-structured with bullet points or key takeaways.
- No self-references or fluff.
- don't give me anything like here is the summury etc.
- tone easy but professional.

Source Data:
{raw_source_info}
"""

    try:
        # Standard OpenAI chat completion payload
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        llm_summary = completion.choices[0].message.content.strip()
        return llm_summary, raw_source_info

    except Exception as e:
        # Clear failure message for user/developer debug
        st.warning(f"⚠️ LLM Summarizer Failed: {str(e)}. Displaying raw web data instead.")
        return "", raw_source_info


def generate_video_script(info_text: str) -> str:
    """Generates a high-retention short video script using the context."""
    prompt = f"""You are a Senior Scriptwriter for YouTube Shorts / Reels.
Transform this context into a production-ready script:

{info_text}

Rules:
1. Open mid-action with a strong visual/verbal hook.
2. Structure: Hook -> Frame -> Payload -> Outro with CTA.
3. Distinguish [Visual Cues] from (Spoken Words).
4. Output ONLY the production script.
"""

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return completion.choices[0].message.content.strip()

    except Exception as e:
        st.error(f"❌ Script Generation Failed: {str(e)}")
        return ""


# -------------------------------------------------------------------
# STREAMLIT UI LAYOUT
# -------------------------------------------------------------------
def main():
    st.title("🎬 YouTube Script Generator")
    st.write("Fetch real-time data and write scripts automatically.")
    st.markdown("---")

    query = st.text_input("Enter your topic or question:")

    if query:
        with st.spinner("Searching latest information..."):
            summary, raw_data = get_realtime_info(query)

        # Handle UI output based on what succeeded
        if summary:
            st.subheader("📌 AI Summary")
            st.markdown(summary)
            script_context = summary
        elif raw_data:
            st.subheader("🌐 Raw Web Results (Fallback)")
            st.markdown(raw_data)
            script_context = raw_data
        else:
            st.error("Unable to gather context for this topic.")
            return

        st.markdown("---")
        st.subheader("🎥 Generate Script")

        if st.button("Generate Short Video Script", type="primary"):
            with st.spinner("Crafting script..."):
                script = generate_video_script(script_context)

                if script:
                    st.subheader("📜 Production Script")
                    st.text_area("Script Content", script, height=350)

                    st.download_button(
                        label="Download Script (.txt)",
                        data=script,
                        file_name="video_script.txt",
                        mime="text/plain"
                    )

if __name__ == "__main__":
    main()