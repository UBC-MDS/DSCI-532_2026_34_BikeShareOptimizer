# Project Proposal: Bike Share Operational Dashboard

## Section 1: Motivation and Purpose

### Target Audience
We design this dashboard for **Bike Share Operations Managers** and **City Transportation Planners** who are responsible for maintaining balanced bike availability across stations and ensuring smooth system operation.

### Problem
Bike share systems experience uneven demand throughout the day and across locations. During peak commute hours, certain stations quickly run empty while others become full and cannot accept returns. This creates user frustration and requires costly manual redistribution. Currently, managers rely on static reports or delayed summaries, making it difficult to anticipate demand patterns and proactively allocate resources.

### Solution
This dashboard provides an interactive decision-support tool that allows users to explore bike usage patterns across time and stations. Using filters such as **date**, **hour of day**, and **rider type**, users can:
* Identify peak demand periods.
* Detect stations at risk of becoming empty or full.
* Compare weekday and weekend usage patterns.
* Monitor long-term trends.

This enables proactive redistribution and operational planning rather than reactive intervention.

---

## Section 2: Description of the Data

### Dataset Source
* **Dataset:** Citi Bike Trip History Dataset
* **Source:** [https://citibikenyc.com/system-data](https://citibikenyc.com/system-data)

### Data Structure
* **Unit of observation:** A single bike trip
* **Approximate size (after sampling):**
    * Rows: ~50,000 – 200,000
    * Columns: ~10–15

### Key Variables

| Variable | Description | Why relevant |
| :--- | :--- | :--- |
| `start_time` | Timestamp of trip start | Identifies peak demand hours |
| `start_station` | Origin station | Detects high-demand stations |
| `end_station` | Destination station | Identifies flow patterns |
| `trip_duration` | Length of ride | Understands usage behavior |
| `user_type` | Member vs casual | Distinguishes commuters vs tourists |

### Relevance to the Problem
Temporal variables allow analysis of demand fluctuations across hours and days, while station identifiers enable location-based operational decisions. Rider type helps distinguish commuter patterns from recreational usage. Together, these variables support actionable decisions such as prioritizing redistribution routes and scheduling staffing during peak demand periods.

---

## Section 3: Research Questions & Usage Scenarios

### Persona
* **Name:** Alex
* **Role:** Bike Share Operations Manager
* **Goal:** Ensure stations remain balanced and minimize service disruptions.
* **Context:** Alex reviews system usage daily and must decide where redistribution trucks should be sent before rush hour begins.

### Usage Scenario
At the start of the day, Alex opens the dashboard and filters to **weekday mornings**. The dashboard highlights stations with **high departure rates** and **low returns**. Alex identifies these high-risk stations and schedules redistribution trucks before peak commute time to replenish them. Later, Alex compares weekend patterns to understand recreational usage and adjust staffing levels accordingly.

### User Stories / Jobs To Be Done
1.  **User Story 1:** As an **operations manager**, I want to **identify stations with the highest departures during rush hour** so that I can **prioritize redistribution**.
2.  **User Story 2:** As an **operations manager**, I want to **compare weekday and weekend demand** so that I can **adjust staffing schedules**.
3.  **User Story 3:** As a **transportation planner**, I want to **analyze monthly usage trends** so that I can **evaluate whether the system requires expansion**.

---

## Section 4: Exploratory Data Analysis

> *To address User Story 1 (demands per start station and hour), we analyzed the count of start station and hour group.*
>
> **Analysis:** The trips_per_start_station_hour table in `notebooks/eda_analysis.ipynb` reveals that E 17 St & Broadway, Broadway & W 24 St and W 20 St & 11 Ave are the top 3 most bike in demand stations at 17 or 18'o clock.
>
> **Reflection:** This finding supprts the need for a targeted filter in the dashboard. By allowing bike share suppliers to select start station and hour, they can know how many bikes need to ready at which station before certain hour so that there won't be bike shortage. 

---

## Section 5: App Sketch & Description

![App Layout](image.png)

### Description
The dashboard is designed as a comprehensive control panel for operations managers and planners. It features a collapsible sidebar for filtering and a three-tiered layout for visualizing data.

#### 1. Sidebar Controls (Filters)
The left-hand sidebar allows the user to slice the data to find specific insights:
* **Birth Year:** A slider range (e.g., 1899–1997) to filter riders by age, allowing planners to analyze demographic usage patterns.
* **Start & End Hour:** Sliders (0–23) to isolate specific times of day, such as morning rush hours (7–9 AM) or late-night operations.
* **User Gender:** Checkboxes to filter by "Male", "Female", or "Unknown".
* **Reset Filter:** A quick action button to restore the global view.

#### 2. Key Performance Indicators (Top Row)
Four KPI cards provide an immediate snapshot of system health based on the selected filters:
* **Average Trip Time:** Monitors efficiency and usage behavior.
* **Subscriber to Customer Ratio:** Tracks the balance between daily commuters (subscribers) and tourists (customers).
* **Most Popular Start Station:** Identifies the highest-demand location needing attention.
* **Most Popular Start Hour:** Pinpoints the peak time of usage.

#### 3. Deep-Dive Visualizations (Middle & Bottom)
* **Distribution of Birth Years (Histogram):** Visualizes the age profile of riders, helping planners understand who is using the system.
* **Trip Counts by Start Hour (Bar Chart):** A temporal analysis showing demand peaks. This directly supports the Operations Manager's need to know *when* to schedule redistribution trucks (e.g., observing the spikes at 8 AM and 5 PM).
* **Map (Bottom Panel):** A geospatial view that plots station locations. This interactive map will update based on the sidebar filters to show where trips are originating and terminating during the selected hours.

#### 4. Interactivity
The dashboard is fully reactive. As the user adjusts the **Start Hour** slider in the sidebar, the **Map** and **KPI cards** will instantly update to reflect conditions during that specific window, allowing the manager to "play back" the day and see how demand shifts across the city.
