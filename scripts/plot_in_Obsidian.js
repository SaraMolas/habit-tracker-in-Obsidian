
// 1. Fetch necessary files 
// Define the folder where your files are located 
const folder = "weekly_Tracker"; // change this parameter if it's in a different folder
const files = dv.pages(`"${folder}"`); // fetch all files in the folder

// Filter files that match the naming convention "Weekly_Tracker_YYYY-MM-DD" 
const weeklyFiles = files .where(f => f.file.name.match(/^Weekly_Tracker_\d{4}-\d{2}-\d{2}$/)); 

// Sort files by date (parsed from the file name) 
const sortedFiles = weeklyFiles.sort(f => Date.parse(f.file.name.match(/\d{4}-\d{2}-\d{2}$/)[0]) );

// Get the newest file (last in the sorted array) 
const weeklyData = sortedFiles[sortedFiles.length - 1];

// Get the file with the weekly goals
const weeklyGoals = dv.page("weekly_Tracker/Weekly_Goals");

// 2. Define categories - modify to match your own calendar categories, as listed in your weekly summary
const categories = ["Hobbies","Learning", "Social",  "Work", "Workout"];

// 3. Extract actual hours and goal hours, ensuring proper conversion to numbers 
const actualHours = categories.map(cat => parseFloat(weeklyData[cat]) || 0); 
const goalHours = categories.map(cat => parseFloat(weeklyGoals[cat]) || 0); 
const remainingHours = categories.map((cat, i) => Math.max(0, goalHours[i] - actualHours[i]));

// 4. Define base colors for each calendar - has to match your own calendar categories
const categoryColorMap = {
    "Hobbies": "rgba(199, 150, 255, TRANSPARENCY)",
    "Learning": "rgba(255, 225, 0, TRANSPARENCY)",
    "Social": "rgba(102, 204, 0, TRANSPARENCY)",
    "Work": "rgba(150, 50, 250, TRANSPARENCY)",
    "Workout": "rgba(255, 51, 51, TRANSPARENCY)"
};

// Use the mapping to get base colors
const baseColors = categories.map(cat => categoryColorMap[cat]);

// 5. Generate transparent colors for each dataset 
const actualColors = baseColors.map(color => color.replace("TRANSPARENCY", "0.8")); // 80% opacity 
const goalColors = baseColors.map(color => color.replace("TRANSPARENCY", "0.2")); // 20% opacity
					  
// 4. Generate chart-ready Markdown for the Charts plugin 
const chartBlock = `
\`\`\`chart
type: bar
labels: ${JSON.stringify(categories)} 
series: 
	  - label: "Actual Hours" 
	    data: ${JSON.stringify(actualHours)} 
		backgroundColor: ${JSON.stringify(actualColors)}
	  - label: "Weekly Goals" 
	    data: ${JSON.stringify(remainingHours)} 
		backgroundColor: ${JSON.stringify(goalColors)}
indexAxis: y 
stacked: true
legend: false
xTitle: "Hours"
\`\`\` 
`;

// 6. Render the chart block as raw Markdown 
dv.el("div", chartBlock);
