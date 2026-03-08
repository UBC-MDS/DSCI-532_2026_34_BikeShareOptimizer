# M2 App Specification: Citi Bike Dashboard

## 2.1 Updated Job Stories

| # | Job Story | Status | Notes |
| :--- | :--- | :--- | :--- |
| 1 | When I analyze Citi Bike data, I want to filter by user type and time, so I can see usage patterns for Subscribers vs Customers. | ✅ Implemented | Sidebar filter setup complete. |
| 2 | When I am a city planner, I want to filter by user demographics (age/gender), so I can see who is using the service. | ✅ Implemented | Added sliders/checkboxes for demographics. |
| 3 | When I am exploring station usage, I want to see the geographic map, so I can identify high-traffic areas. | ✅ Implemented | Map added. |
| 4 | When I analyze Citi Bike data, I want to analyze the Distribution of Birth Years of our subscribers, so I can see their usage patterns. | ✅ Implemented | Distribution of Birth Years component added. |
| 5 | When I analyze Citi Bike data, I want to analyze the start hour of the trips, so I can see their usage patterns. | ✅ Implemented | Most popular Start Hour component and Distribution of Start Hour component added. |

## 2.2 Component Inventory

| ID | Type | Shiny widget / renderer | Depends on | Job story |
| :--- | :--- | :--- | :--- | :--- |
| `usertype_checkbox` | Input | `ui.input_checkbox_group()` | — | #1 |
| `birth_year_slider` | Input | `ui.input_slider()` | `usertype_checkbox` | #2 |
| `start_time_slider` | Input | `ui.input_slider()` | — | #1 |
| `day_of_week_filter`| Input | `ui.input_selectize()` | — | #1 |
| `month_filter` | Input | `ui.input_selectize()` | — | #1 |
| `gender_checkbox` | Input | `ui.input_checkbox_group()` | — | #2 |
| `qc` | Input | `querychat.QueryChat()` | — | #1, #2, #3, #4, #5 |
| `filtered_df` | Reactive calc | `@reactive.calc` | All Inputs | #1, #2, #3, #4, #5 |
| `ai_df` | Reactive calc | `@reactive.calc` | `qc` | #1, #2, #3, #4, #5 |
| `avg_trip_time` | Output | `@render.text` | `filtered_df` | #1 |
| `s_to_c_ratio` | Output | `@render.text` | `filtered_df` | #1 |
| `pop_start_id` | Output | `@render.text` | `filtered_df` | #3 |
| `barplot1` | Output | `output_widget` | `filtered_df` | #4 |
| `map` | Output | `output_widget` | `filtered_df` | #4 |
| `pop_start_hour` | Output | `@render.text` | `filtered_df` | #5 |
| `start_hour_barplot` | Output | `output_widget` | `filtered_df` | #5 |
| `ai_data_table` | Output | `ui.output_data_frame()` | `ai_df` | #1, #2, #3, #4, #5 |

## 2.3 Reactivity Diagram


```mermaid
graph TD
    %% Inputs
    In1[/User Type/] --> Filter{{filtered_df}}
    In2[/Birth Year/] --> Filter
    In3[/Start Hour/] --> Filter
    In4[/Day/Month/] --> Filter
    In5[/Gender/] --> Filter
    In5[/Query Chat/] --> AI{{ai_df}}

    %% Reactive Calc
    Filter --> Out1([Avg Trip Time])
    Filter --> Out2([S to C Ratio])
    Filter --> Out3([Most Pop Station])
    Filter --> Out4([Birth Year Plot])
    Filter --> Out5([Map])
    Filter --> Out6([Most Popular Start Hour])
    Filter --> Out7([Trip Counts by Start Hour])
    AI --> Out8([AI Data Table])
```


## 2.4 Calculation Details

* **`filtered_df` (@reactive.calc)**:
    * **Dependencies**: All sidebar inputs (`usertype_checkbox`, `birth_year_slider`, `start_time_slider`, `day_of_week_filter`, `month_filter`, `gender_checkbox`).
    * **Transformation**: Performs a boolean mask on the primary DataFrame. It includes specific conditional logic: if "Customer" is excluded from `usertype_checkbox`, the `birth_year_slider` filter is applied to the result set. It returns the subsetted DataFrame.
    * **Outputs**: This calculation is consumed by all summary value boxes (`avg_trip_time`, `s_to_c_ratio`, `pop_start_id`, `pop_start_hour`) and all interactive plot/map outputs (`barplot1`, `map`, `start_hour_barplot`).
* **`ai_df` (@reactive.calc)**:
    * **Dependencies**: Query chat server response.
    * **Outputs**: A data table. 

## Reflection/Notes

* **Performance Note**: To ensure the map and bar charts perform well, the map component aggregates data using `.groupby()` on station names. This prevents the browser from attempting to render thousands of individual data points simultaneously.


