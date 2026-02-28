from shiny import App, render, ui, reactive
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from shinywidgets import render_plotly, render_widget, output_widget

df = pd.read_csv("data/raw/201306-citibike-tripdata.csv", parse_dates=['starttime', 'stoptime'])
df['start_hour'] = df['starttime'].dt.hour
df['end_hour'] = df['stoptime'].dt.hour
df['birth year'] = df['birth year'].astype('Int64')
df['day_of_week'] = df['starttime'].dt.day_name()
df['month'] = df['starttime'].dt.month_name()

app_ui = ui.page_fluid(
    ui.tags.style("body { font-size: 0.6em; }"),
    ui.panel_title("Citi Bikes"),
    ui.layout_sidebar(
            ui.sidebar(
            ui.input_checkbox_group(
                id="usertype_checkbox",
                label="User Type",
                choices=["Subscriber", "Customer"],
                selected=["Subscriber"],
            ),
            ui.panel_conditional(
                "!input.usertype_checkbox.includes('Customer')",
                ui.input_slider(
                    id="birth_year_slider",
                    label="User Birth Year (Subscribers Only)",
                    min=int(df['birth year'].min()),
                    max=int(df['birth year'].max()),
                    value=[int(df['birth year'].min()), int(df['birth year'].max())],
                )
            ),
            ui.input_slider(
                id="start_time_slider",
                label="Start Hour",
                min=0,
                max=23,
                value=[0, 23],
            ),ui.input_selectize(
                id="day_of_week_filter",
                label="Day of Week",
                choices=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                selected=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                multiple=True,
            ),
            ui.input_selectize(
                id="month_filter",
                label="Month",
                choices=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
                selected=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
                multiple=True,
            ),
            ui.input_checkbox_group(
                id="gender_checkbox",
                label="User Gender",
                choices={
                    '0': "Unknown",
                    '1': "Male",
                    '2': "Female",
                },
                selected=[
                    "0", "1", "2"
                ],
            ),
            ui.input_action_button("reset", "Reset filter"),
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
    @reactive.calc
    def filtered_df():
        # Convert sidebar options to variables
        s_min, s_max = input.start_time_slider()
        genders = [int(g) for g in input.gender_checkbox()]
        usertypes = input.usertype_checkbox()
        days = input.day_of_week_filter()
        months = input.month_filter()

        # Mask
        m = (df['start_hour'].between(s_min, s_max) &
             df['gender'].isin(genders) &
             df['usertype'].isin(usertypes) &
             df['day_of_week'].isin(days) &
             df['month'].isin(months))

        if "Customer" not in usertypes:
            b_min, b_max = input.birth_year_slider()
            m_birth = df['birth year'].between(b_min, b_max)
            m = m & m_birth

        return df[m]

    @reactive.effect
    @reactive.event(input.reset)
    def _():
        ui.update_checkbox_group('usertype_checkbox', selected=["Subscriber"])
        ui.update_slider("birth_year_slider", value=[int(df['birth year'].min()), int(df['birth year'].max())])
        ui.update_slider("start_time_slider", value=[0, 23])
        ui.update_checkbox_group("gender_checkbox", selected=['0', '1', '2'])
        ui.update_selectize("day_of_week_filter", selected=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        ui.update_selectize("month_filter", selected=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

    @render.text
    def avg_trip_time():
        d = filtered_df()
        if d.empty: return "N/A"
        avg = d['tripduration'].mean() / 60
        return f"{avg:.1f} mins"

    @render.text
    def s_to_c_ratio():
        d = filtered_df()
        if d.empty:
            return "N/A"

        subscribers = (d["usertype"] == "Subscriber").sum()
        customers = (d["usertype"] == "Customer").sum()

        if customers == 0:
            return "∞"

        ratio = subscribers / customers
        return f"{ratio:.2f}"

    @render.text
    def pop_start_id():
        d = filtered_df()
        if d.empty:
            return "N/A"

        station = d["start station name"].value_counts().idxmax()
        return station

    @render.text
    def pop_start_hour():
        d = filtered_df()
        if d.empty: return "N/A"
        return '?'
    
    
# Create app
app = App(app_ui, server)