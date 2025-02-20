from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.custom_tool import StockDataTool

@CrewBase
class FinancialAnalysisCrew():
    """FinancialAnalysisCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    ollama_llm = LLM(
        model='ollama/deepseek-r1:1.5b',  # Use a valid model name
        base_url='http://localhost:11434',  # Ensure Ollama is running here
        temperature=0.2
    )

    def __init__(self):
        self.stock_tool = StockDataTool()

    @agent
    def financial_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_analyst'],
            verbose=True,
            llm=self.ollama_llm,
            tools=[self.stock_tool]  # Register the tool here
        )

    @agent
    def research_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['research_analyst'],
            verbose=True,
            llm=self.ollama_llm
        )

    @agent
    def investment_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['investment_advisor'],
            verbose=True,
            llm=self.ollama_llm
        )

    @task
    def financial_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['financial_analysis'],
            agent=self.financial_analyst()  # Assign the task to the financial_analyst agent
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research'],
            agent=self.research_analyst()  # Assign the task to the research_analyst agent
        )

    @task
    def filings_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['filings_analysis'],
            agent=self.research_analyst()  # Assign the task to the research_analyst agent
        )

    @task
    def stock_action_prediction_task(self) -> Task:
        return Task(
            config=self.tasks_config['stock_action_prediction'],
            agent=self.investment_advisor()  # Assign the task to the investment_advisor agent
        )

    @task
    def recommend_task(self) -> Task:
        return Task(
            config=self.tasks_config['recommend'],
            agent=self.investment_advisor(),  # Assign the task to the investment_advisor agent
            output_file='recommendation_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the FinancialAnalysisCrew crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )