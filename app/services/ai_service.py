from crewai import Agent, Task, Crew
from dotenv import load_dotenv
import os
from app.tools.content_tool import ContentTool

load_dotenv()

def create_crewai_setup(prompt):
    content_tool = ContentTool()

    content_creator = Agent(
        role='Content Creator',
        goal='Create high-quality, engaging content based on the given prompt',
        backstory='''You are an expert content creator with extensive experience in digital marketing. 
        Your goal is to create compelling content that resonates with the target audience and aligns 
        with marketing objectives.''',
        verbose=True,
        allow_delegation=False,
        tools=[content_tool]
    )

    seo_optimizer = Agent(
        role='SEO Optimizer',
        goal='Optimize content for search engines while maintaining readability and engagement',
        backstory='''You are an SEO expert with a deep understanding of search engine algorithms and 
        content optimization techniques. Your goal is to enhance content visibility and ranking 
        without compromising its quality or user experience.''',
        verbose=True,
        allow_delegation=False,
        tools=[content_tool]
    )

    task_create_content = Task(
        description=f'''Create engaging content based on the following prompt: {prompt}
        Ensure the content is informative, engaging, and aligns with marketing best practices.''',
        agent=content_creator,
        expected_output="A well-structured, engaging piece of content that addresses the given prompt and follows marketing best practices. The output should be in markdown format."
    )

    task_optimize_seo = Task(
        description='''Optimize the created content for search engines. 
        Ensure proper keyword usage, meta descriptions, and overall SEO best practices are applied.''',
        agent=seo_optimizer,
        expected_output="An SEO-optimized version of the input content, including suggested meta descriptions, optimized headings, and a list of incorporated keywords. The output should be in markdown format with SEO recommendations clearly marked."
    )

    crew = Crew(
        agents=[content_creator, seo_optimizer],
        tasks=[task_create_content, task_optimize_seo],
        verbose=True
    )

    result = crew.kickoff()

    return result

def generate_content(prompt: str) -> dict:
    result = create_crewai_setup(prompt)
    # Extract the relevant information from the CrewOutput object
    content = result.raw
    return {
        "title": prompt[:50],  # Use the first 50 characters of the prompt as the title
        "body": content
    }