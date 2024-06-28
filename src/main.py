import os

from colorama import Fore, Style
from dotenv import load_dotenv

from src.agents.agent_factory import organize_agents
from src.utility.helper import load_agent_config
from src.utility.prompt_template import task1
from src.utility.system_messages import (
    admin_system_message,
    critic_system_message,
    engineer_system_message,
    executor_system_message,
    planner_system_message,
    researcher_system_message,
)

load_dotenv()


def main():
    agent_config = load_agent_config("./config/agent_config.yaml")

    llm_config = agent_config.get("llm_config", {})

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    llm_config["config_list"] = [
        {
            "model": "gpt-4",
            "api_key": api_key,
        }
    ]
    code_execution_config = agent_config.get("code_execution_config", {})

    manager, groupchat, user_proxy, engineer, researcher, planner, executor, critic = (
        organize_agents(
            llm_config,
            code_execution_config,
            admin_system_message,
            engineer_system_message,
            researcher_system_message,
            planner_system_message,
            executor_system_message,
            critic_system_message,
        )
    )

    task2 = input("Please enter the new task description: ")

    # Apply colorama styling to task2
    highlighted_task2 = f"{Fore.YELLOW}{task2}{Style.RESET_ALL}"

    user_proxy.initiate_chat(
        manager,
        message=task1.format(task2=highlighted_task2),
    )


if __name__ == "__main__":
    main()
