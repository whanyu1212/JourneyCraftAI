## Transcendent
 My AI co-pilot on the journey of self-improvement and discovery, meticulously tracking my progress, illuminating insights, and guiding me to unlock more potential. The UI is designed to look like a dynamic activity feed showcasing the journey.

## TO DO:
<details>
<summary>Click to expand To-Do List</summary>

- [x] Architecture: Team of agents
- [ ] Setting up credentials and API keys
- [ ] Literature review on LangGraphCrewAI and AutoGen
- [ ] Test integration with tourism related sites (webbasedloader or scraper)
</details>


## Travel Planner Outline:
<details>
<summary>Click to expand To-Do List</summary>

- [ ] what kind of planner (from scratch or?)
- [ ] geospatial -> graph (connecting the different stops)
- [ ] itenary (mitosheet?)
- [ ] multi-agent workflow
- [ ] calendar + items 
- [ ] single tab with multiple containers
</details>



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


