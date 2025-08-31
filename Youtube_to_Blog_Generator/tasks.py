from crewai import Task
from agents import blog_researcher, blog_writer

research_task = Task(
    description=(
        "Given a YouTube video URL or ID: {topic}\n"
        "- Use the YouTube Transcript Fetcher tool to get the transcript and metadata.\n"
        "- Produce structured research notes with: Title, Channel, Date, Link, Key Points (bulleted), "
        "Notable quotes (if any), and a concise 5-7 sentence summary. "
        "If the transcript is not available, rely on the video metadata and general knowledge."
    ),
    agent=blog_researcher,
    expected_output=(
        "Structured research notes including: Title, Channel, Date, Link, Key Points, Quotes (optional), "
        "and a summary paragraph."
    )
)

writing_task = Task(
    description=(
        "Write a well-structured and engaging blog post based on the research notes for {topic}.\n"
        "Requirements:\n"
        "- Catchy title\n"
        "- Short TL;DR\n"
        "- Intro (why it matters / set the stage)\n"
        "- 3–6 clear sections with subheadings\n"
        "- Bullet points where helpful\n"
        "- Conversational yet professional tone\n"
        "- A short conclusion with a call-to-action\n"
        "- SEO-friendly but human tone; 700–1200 words\n"
    ),
    agent=blog_writer,
    expected_output="A polished and engaging blog post in Markdown."
)
