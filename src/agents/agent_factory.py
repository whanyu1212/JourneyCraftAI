import autogen


def organize_agents(
    llm_config,
    code_execution_config,
    admin_system_message,
    engineer_system_message,
    researcher_system_message,
    planner_system_message,
    executor_system_message,
    critic_system_message,
):
    user_proxy = autogen.UserProxyAgent(
        name="Admin",
        system_message=admin_system_message,
        code_execution_config=code_execution_config,
    )

    engineer = autogen.AssistantAgent(
        name="Engineer",
        llm_config=llm_config,
        system_message=engineer_system_message,
    )

    researcher = autogen.AssistantAgent(
        name="Researcher",
        llm_config=llm_config,
        system_message=researcher_system_message,
    )

    planner = autogen.AssistantAgent(
        name="Planner",
        system_message=planner_system_message,
        llm_config=llm_config,
    )

    executor = autogen.UserProxyAgent(
        name="Executor",
        system_message=executor_system_message,
        human_input_mode="NEVER",
        code_execution_config=code_execution_config,
    )
    critic = autogen.AssistantAgent(
        name="Critic",
        system_message=critic_system_message,
        llm_config=llm_config,
    )
    groupchat = autogen.GroupChat(
        agents=[user_proxy, engineer, researcher, planner, executor, critic],
        messages=[],
        max_round=50,
    )
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    return (
        manager,
        groupchat,
        user_proxy,
        engineer,
        researcher,
        planner,
        executor,
        critic,
    )
