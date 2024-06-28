task1 = """
This recipe is available for you to reuse..

<begin recipe>
**Goal:** Help the users to plan the travel itinerary for a trip to the place that the user wants.

**Steps:**
1. Collect the must-visit places from web search.
2. For the shortlisted locations, find their respective latitude and longitude coordinates. If the coordinates are not available, drop the location from the list.
3. Plan the order of visit based on the distance between the locations and the available transportation options.
4. Use Python to create a detailed write up about the trip itinerary, including the places to visit, the order of visit, the distance between the locations and why the locations were chosen. Save the file as `trip_itinerary.md`.
5. Create a csv file with the order of visit, location name, latitude, longitude coordinates, transport to next place and description. Save the file as `itinerary_table.csv`.
6. Given the coordinates, plot the locations on a map using the `folium` library. Make sure you mark out the places to visit and then connect them with a Antpath line. Mouse over should show the order and place name. Save the map as `trip_map.html`.

</end recipe>

Here is a new task:

{task2}
"""
