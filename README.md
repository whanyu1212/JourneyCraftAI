## JourneyCraftAI
JourneyCraftAI is an AI-powered travel planning agent that crafts personalized itineraries, suggests destinations tailored to your interests, and offers up-to-date travel advice..

## Workflow

```mermaid
graph LR

    Admin(("Admin<br>A human admin")) -->|Directs| Planner(("Planner<br>Suggest and revise plan"))
    Critic(("Critic<br>Provides feedback")) -->|Feedback to| Planner
    Critic -->|Evaluates| Engineer(("Engineer<br>Writes code"))
    Critic -->|Assesses| Researcher(("Researcher<br>Analyzes results"))
    Planner -->|Plans for| Engineer
    Planner -->|Guides| Researcher
    Engineer -->|Implements| Executor(("Executor<br>Executes code"))
    Executor -->|Results to| Critic
    Researcher -->|Supports| Planner

    subgraph "Core Components"
        Admin
        Critic
        Planner
        Engineer
        Executor
        Researcher
    end

    subgraph "Communication Layer"
        GroupChat(("GroupChat<br>Facilitates communication"))
        GroupChatManager(("GroupChatManager<br>Manages chat"))
    end

    %% Correctly connecting GroupChat to individual nodes within "Core Components"
    GroupChat -->|Manages communication for| Admin
    GroupChat -->|Manages communication for| Critic
    GroupChat -->|Manages communication for| Planner
    GroupChat -->|Manages communication for| Engineer
    GroupChat -->|Manages communication for| Executor
    GroupChat -->|Manages communication for| Researcher

    GroupChatManager --> GroupChat

    %% Additional Styles
    classDef human fill:#bbf,stroke:#333,stroke-width:2px;
    classDef automated fill:#fbf,stroke:#333,stroke-width:2px;
    classDef communication fill:#ff9,stroke:#333,stroke-width:2px;
    class Admin,Executor human
    class Engineer,Planner,Researcher,Critic automated
    class GroupChat,GroupChatManager communication

    %% Comments and Notes
    %% This flowchart represents the interaction between different components of the automated system.
    %% Admin and Executor are human-proxy agents, while Engineer, Planner, Researcher, and Critic are automated agents.
    %% GroupChat and GroupChatManager facilitate and manage communications among agents.
```


## Environment set up

1. **Install Poetry:** 
   For most users, run the following command in your terminal:
     ```bash
     curl -sSL [https://install.python-poetry.org](https://install.python-poetry.org) | python3 -
     ```

   If you're using **macOS** and have Homebrew, you can also choose to install with:
     ```bash
     brew install poetry
     ```

2. **Verify Installation:** Check if Poetry is installed correctly:
   ```bash
   poetry --version
   ```

3. **Install Pre-defined Dependencies:** From pyproject.toml & poetry.lock
    ```bash
    poetry install
    ```
4. **Activate Virtual Environment:**
    ```bash
    poetry shell
    ```
5. **Install Jupyter Kernel:**
    ```bash
    # name it base on your own preference
    python -m ipykernel install --user --name other-env --display-name "Python (other-env)"
    ```




## TO DO:
<details>
<summary>Click to expand To-Do List</summary>
- [ ] Test integration with Panel for display
- [ ] Look for ways to reduce cost
- [ ] Test Gemini's performance
</details>

