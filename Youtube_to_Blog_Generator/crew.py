from crewai import Crew, Process
from tasks import research_task, writing_task
from agents import blog_researcher, blog_writer

crew = Crew(
    agents=[blog_researcher, blog_writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    verbose=True
)
