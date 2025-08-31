from crewai import Agent
from tools import youtube_search, youtube_transcript_fetcher

# Research Agent
blog_researcher = Agent(
    role="YouTube Research Assistant",
    goal="Extract accurate context from a YouTube video for {topic} and prepare research notes.",
    verbose=True,
    backstory=(
        "You specialize in gathering clean, structured research from long-form media, "
        "summarizing key points, and preparing inputs for blog creation."
    ),
    tools=[youtube_search, youtube_transcript_fetcher],
    allow_delegation=True,
    memory=True,
)

# Blog Writer Agent
blog_writer = Agent(
    role="Blog Writer",
    goal=(
        "Write an appealing, engaging, and well-structured blog post based on the provided YouTube video {topic}. "
        "Make it lively, story-driven, and easy to read, while keeping it informative and polished."
    ),
    verbose=True,
    backstory=(
        "You are a skilled storyteller and content creator who knows how to transform transcripts and notes "
        "into blogs that hook readers from the first line, keep them engaged with relatable explanations, "
        "and leave them with actionable insights."
    ),
    tools=[youtube_search, youtube_transcript_fetcher],
    allow_delegation=True,
    memory=True,
)
