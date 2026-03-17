# Changelog

All notable changes to this project will be documented in this file.

## [0.4.0] - 2026-03-17 (Milestone 4)

### Added
* **Data ETL Pipeline**: Added `src/prep_data.py` to filter and convert raw CSV data into a highly compressed Parquet format.
* **Automated Testing**: Integrated `pytest` for unit testing helper functions and `playwright` for end-to-end behavioral testing of the UI.
* **Modular Architecture**: Added `src/utils.py` to decouple business logic (like trip time calculations) from the main `app.py` server logic.

### Changed
* **Database Backend**: Migrated from in-memory Pandas dataframes to a DuckDB + Ibis backend to drastically improve filtering performance and reduce server memory load.
* **UI Defaults**: Adjusted the `Birth Year` slider to default to 1950 (instead of 1899) to prevent historical outliers from visually skewing the initial histogram load.
* **Contextual Framing**: Updated the main dashboard title to `Citi Bike NYC System Optimizer` to clarify the geographic scope for end-users.

### Deprecated
* **None**

### Removed
* **Redundant UI Elements**: Removed Plotly-generated chart titles that duplicated the Shiny `ui.card_header` text to clean up the visual layout.

### Fixed
* **AI Memory Crashes**: Fixed the "Error code 5" infinite spinning bug by sampling the dataframe before passing it to `QueryChat` and correctly handling the Ibis-to-Pandas `.execute()` conversion.
* **Division by Zero Error**: Fixed the "Subscriber to Customer Ratio" displaying `Infinity` when no customers are selected; it now cleanly displays `N/A (No Customers)`.
* **Military Time Formatting**: Converted the "Most Popular Start Hour" KPI from a raw 24-hour integer (e.g., `18`) into a user-friendly 12-hour AM/PM format (e.g., `6:00 PM`).
* **Blank Plot Confusion**: Added an explicit `Data unavailable (Subscribers only)` placeholder to the Birth Year histogram when the Subscriber checkbox is unselected.
* **Deployment Import Paths**: Fixed the `No module named 'utils'` crash on Posit Connect Cloud by updating absolute import paths (`from src.utils import...`).

### Security
* **API Key Protection**: Enforced `.env` variable loading for the Anthropic API key to ensure credentials are never hardcoded into the repository or exposed in client-side code.

### Reflection
* **Milestone 4 Takeaway**: Transitioning to a DuckDB backend and modularizing our code was a steep learning curve, but it fundamentally transformed our app from a prototype into a production-ready dashboard. Writing tests for `utils.py` and implementing GitHub collaboration norms kept our team aligned and prevented the last-minute merge conflicts we experienced in M3.

---

## [0.3.0] - 2026-03-07 (Milestone 3)

### Added
* **Tabs**: Added `AI Insights` tab and put the previous page into `Citi Bikes - Main Dashboard` tab. 
* **Component Inventory**:
    * **Chat Boxes**: Implemented AI chat box. PR #34. 
    * **Data Frame Table**: Added `AI Filtered Data` to show results of chat box queries.
* **Deployment**: Configured Posit Connect Cloud with separate `main` (stable) and `dev` (preview) pipelines.
* **Documentation**: Created `reports/m3_spec.md` with Reactivity Diagram and Component Inventory.

### Changed
* **Default Logic**: Update filtered_df logic to default of empty.
* **Default Values**: Update reset logic to new default values.
* **Remove Definitions**: Remove excess definitions from app.py.
* **User Type Prompts**: Add prompts to select user type in app.py.

### Fixed
* **Font Size**: Fixed font size of the dashboard. 
* **Selected Years**: Change display of selected years in slider.
* **Default Empty**: Change the default selection of month and Day of Week to be empty.
* **Consistent Schema**: Fix color schema inconsistencies between plots. 
* **Map Box**: Improve mapbox aggregation and empty-data handling


### Known Issues
* **None**

### Reflection
* **Publishing**: Publishing sometimes can get unexpected errors and requirement.txt needs to specify version for certain dependencies. 

---

## [0.2.0] - 2026-02-28 (Milestone 2)

### Added
* **Interactive Dashboard Skeleton**: Migrated from a static skeleton to a fully reactive dashboard.
* **Component Inventory**:
    * **Sidebar**: Added global filters for `User Type`, `Birth Year`, `Start Hour`, `Day of Week`, `Month`, and `Gender`.
    * **Value Boxes**: Implemented KPIs for `Average Trip Time`, `Subscriber/Customer Ratio`, and `Most Popular Start Station`.
    * **Visualizations**: Added `Distribution of Birth Years` (Histogram) and a `Citi Bike Station Map` using `plotly`.
* **Deployment**: Configured Posit Connect Cloud with separate `main` (stable) and `dev` (preview) pipelines.
* **Documentation**: Created `reports/m2_spec.md` with Reactivity Diagram and Component Inventory.

### Changed
* **Reactivity Architecture**: Centralized all data filtering into a single `@reactive.calc` (`filtered_df`) to optimize performance and data flow.
* **UI Layout**: Optimized sidebar layout to include conditional rendering for the Birth Year slider (visible only when subscribers are selected).
* **Dependencies**: Cleaned up `requirements.txt` to remove obsolete build-system packages (`altgraph`, `bdist-mpkg`) and added `anywidget` to support interactive plots.

### Fixed
* **Installation Errors**: Resolved `Pip subprocess` errors caused by hardcoded/outdated versions of system build tools.
* **Widget Rendering**: Fixed `FigureWidget` missing renderer error by adding `anywidget` and `shinywidgets`.

### Known Issues
* **Placeholder**: `Most Popular Start Hour` currently displays a placeholder (`?`) while waiting for frequency distribution logic in M3.

### Reflection
* **Job Stories**: All initial job stories identified in M1 are fully implemented. We refined the "filter by demographic" story (Job Story #2) to handle conditional logic, ensuring the birth year slider only appears for Subscribers.
* **Layout Evolution**: The final layout is very close to our M1 sketch. The main deviation was moving the "Start Hour" and "Month" filters to the sidebar to keep the main dashboard area clean, following the "5-second rule" for dashboard effectiveness.
* **Reactivity Learning**: Implementing the `@reactive.calc` was the biggest hurdle. We learned that chaining outputs to one calculation is much more efficient than having each output filter the dataframe independently.

---

## [0.1.0] - 2026-01-30 (Milestone 1)

### Added
* Initial project proposal and skeleton application setup.
* Basic UI layout for Citi Bike dashboard.
