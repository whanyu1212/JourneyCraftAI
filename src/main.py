import os

from src.agents.agent_factory import organize_agents
from src.utility.helper import load_agent_config
from src.utility.system_messages import (
    admin_system_message,
    critic_system_message,
    engineer_system_message,
    executor_system_message,
    planner_system_message,
    researcher_system_message,
)


def main():
    agent_config = load_agent_config("./config/agent_config.yaml")

    llm_config = agent_config.get("llm_config", {})
    llm_config["config_list"] = [
        {"model": "gpt-4o", "api_key": os.getenv("OPENAI_API_KEY")}
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
    user_proxy.initiate_chat(
        manager,
        message=input("Enter your message: "),
    )


if __name__ == "__main__":
    main()
