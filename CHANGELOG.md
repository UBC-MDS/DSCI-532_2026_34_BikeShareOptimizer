# Changelog

All notable changes to this project will be documented in this file.

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
