import os

import autogen
from autogen.coding import LocalCommandLineCodeExecutor


class TripAgents:
    def __init__(self):
        self.assistant = autogen.AssistantAgent(
            name="assistant",
            system_message="""
    You are an expert travel planner. Your task is to:
    1. Process user's request for a travel itinerary.
    2. Research and create a detailed travel itinerary that includes:
    - Daily schedule with activities, times, and locations.
    - Transportation options between destinations.
    - Meal suggestions.
    3. Then create a Pandas DataFrame with columns: order of visit, name, latitude,
    longitude, description, and transportation_to_next.
    4. Save the DataFrame as a CSV file in the current directory as 'itinerary.csv'.
    5. Use folium to create a map with markers for each location in the itinerary.
    Connect the points with Antpath to show the travel route. Save the map as 'map.html'.
    6. Finally, provide a summary of the itinerary to the user.
    """,
            llm_config={
                "cache_seed": 41,
                "config_list": [
                    {"model": "gpt-4o", "api_key": os.getenv("OPENAI_API_KEY")}
                ],
                "temperature": 0,
            },
        )

        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=5,
            is_termination_msg=lambda x: x.get("content", "")
            .rstrip()
            .endswith("TERMINATE"),
            code_execution_config={
                "executor": LocalCommandLineCodeExecutor(work_dir="coding"),
            },
        )
