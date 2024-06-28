import os
import time

from colorama import Fore, Style
from dotenv import load_dotenv
from loguru import logger

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


def print_ascii_art():
    print(
        """
   /================================================================================\
||     _                                    ____            __ _      _    ___  ||
||    | | ___  _   _ _ __ _ __   ___ _   _ / ___|_ __ __ _ / _| |_   / \  |_ _| ||
|| _  | |/ _ \| | | | '__| '_ \ / _ \ | | | |   | '__/ _` | |_| __| / _ \  | |  ||
||| |_| | (_) | |_| | |  | | | |  __/ |_| | |___| | | (_| |  _| |_ / ___ \ | |  ||
|| \___/ \___/ \__,_|_|  |_| |_|\___|\__, |\____|_|  \__,_|_|  \__/_/   \_\___| ||
||                                   |___/                                      ||
\================================================================================/
    """
    )


def main():
    agent_config = load_agent_config("./config/agent_config.yaml")

    llm_config = agent_config.get("llm_config", {})

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    llm_config["config_list"] = [
        {
            "model": "gpt-4o",
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
    start_time = time.time()
    print_ascii_art()
    main()
    logger.info("Execution time: {:.2f} seconds", time.time() - start_time)
