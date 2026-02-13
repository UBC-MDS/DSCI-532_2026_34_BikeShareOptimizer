from shiny import App, render, ui, reactive
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from shinywidgets import render_plotly, render_widget, output_widget

df = pd.read_csv("../data/raw/201306-citibike-tripdata.csv", parse_dates=['starttime', 'stoptime'])
df['start_hour'] = df['starttime'].dt.hour
df['end_hour'] = df['stoptime'].dt.hour

app_ui = ui.page_fluid(
    ui.tags.style("body { font-size: 0.6em; }"),
    ui.panel_title("Citi Bikes"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_slider(
                id="birth_year_slider",
                label="Birth Year",
                min=df['birth year'].min(),
                max=df['birth year'].max(),
                value=[df['birth year'].min(), df['birth year'].max()],
            ),
            ui.input_slider(
                id="start_time_slider",
                label="Start Hour",
                min=df['start_hour'].min(),
                max=df['start_hour'].max(),
                value=[df['start_hour'].min(), df['start_hour'].max()],
            ),
            ui.input_slider(
                id="end_time_slider",
                label="End Hour",
                min=df['end_hour'].min(),
                max=df['end_hour'].max(),
                value=[df['end_hour'].min(), df['end_hour'].max()],
            ),
            ui.input_checkbox_group(
                id="checkbox_group",
                label="User Gender",
                choices={
                    '0': "Unknown",
                    '1': "Male",
                    '2': "Female",
                },
                selected=[
                    "Unknown", "Male", "Female"
                ],
            ),
            ui.input_action_button("action_button", "Reset filter"),
            open="desktop",
        ),
        ui.layout_columns(
            ui.value_box("Average Trip Time", ui.output_text("avg_trip_time")),
            ui.value_box("Subscriber to Customer Ratio", ui.output_text("s_to_c_ratio")),
            ui.value_box("Most Popular Start Station", ui.output_text("pop_start_id")),
            ui.value_box('Most Popular Start Hour', ui.output_text("pop_start_hour")),
            fill=False,
        ),
        ui.layout_columns(
            ui.card(
                ui.card_header("Distribution of Birth Years"),
                output_widget("barplot1"),
                full_screen=True,
            ),
            ui.card(
                ui.card_header("Trip Counts by Start Hour"),
                output_widget("barplot"),
                full_screen=True,
            ),
            col_widths=[6, 6],
        ),
        ui.layout_columns(
            ui.card(
                ui.card_header("Map"),
                output_widget("map"),
                full_screen=True,
            )
        ),
    ),
)

# Server
def server(input, output, session):
    pass


# Create app
app = App(app_ui, server)