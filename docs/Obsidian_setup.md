# Set up for the Weekly Calendar Summary Visualization in Obsidian

This guide provides step-by-step instructions to run the `dataviewjs` code that visualizes your weekly Google Calendar data in Obsidian.

## Prerequisites

Before running the code, ensure the following:

1. **Obsidian Installed:**
   - Download and install Obsidian from [obsidian.md](https://obsidian.md/).

2. **Required Community Plugins in Obsidian:**
   - **Dataview Plugin:**
     - Go to **Settings > Community Plugins > Browse**.
     - Search for `Dataview` and click **Install**.
     - Enable the plugin by toggling the switch.
     - Ensure **JavaScript Queries** are enabled under **Settings > Dataview**.

   - **Charts Plugin**:
     - Similarly, search for `Charts` in the Community Plugins browser and install it.
     - Enable the plugin.

---

## Folder and File Setup

1. **Weekly Tracker Folder:** Create a folder in your vault named `weekly_Tracker`. Files are added to this folder by the `create_summary_Google_calendar.py` script, with the naming convention `Weekly_Tracker_YYYY-MM-DD.md` for weekly summaries and `Weekly_Goals.md` for your goal data.

2. **Weekly Data File:** Generated automatically by `create_summary_Google_calendar.py` in the format:
     ```markdown
     ---
     Hobbies: '2'
     Learning: '10'
     Social: '12.50'
     Work: '40'
     Workout: '5'
     ---
     ```

3. **Weekly Goals File:** Has to be manually created by the user, with your desired goals in the format: 
     ```markdown
     ---
     Hobbies: 5
     Learning: 10
     Social: 10
     Work: 40
     Workout: 7
     ---
     ```

---

## Adding the Visualization Code

1. **Create a New Note:** Create a new note in Obsidian where you want to render the visualization.

2. **Insert the DataviewJS Code Block:** Add the following code block to your note:
     ```markdown
     ```dataviewjs
     // Paste the provided code in `scripts/plot_in_Obsidian.js`
     ```

3. **Customize the Code:**
   - Update the folder name (`weekly_Tracker`) if your folder name is different.
   - Update the `categories` array in the code to match your desired calendar categories.
   - Change the colors of the calendar categories in the plot if desired. 


## Running the Visualization

1. **Save the Note:** Save the note after adding the code.

2. **View the Rendered Chart:** Obsidian will execute the `dataviewjs` code and render a bar chart displaying your weekly actual hours, goals, and remaining hours.


## Example Output

Here’s an example of what the chart will look like:

- **Bar Chart:**
  - **X-Axis:** Categories (e.g., Hobbies, Learning, Social).
  - **Y-Axis:** Hours spent.
  - Two stacked series for:
    - Actual Hours: Shaded with 80% opacity.
    - Remaining Hours to Goal: Shaded with 20% opacity.

![[weekly_summary]](docs/Habit_summary_plot.png)

## Notes

**Error Handling:**
   - If the chart does not render or throws an error, ensure:
     - The `categories` in the code match the keys in your `Weekly_Tracker` and `Weekly_Goals` files.
     - All plugins are properly installed and enabled.
   - Use the Obsidian developer console (`Ctrl+Shift+I`) for debugging errors.
