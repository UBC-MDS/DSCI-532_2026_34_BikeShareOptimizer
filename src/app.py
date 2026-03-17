from shiny import App, render, ui, reactive
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from shinywidgets import render_plotly, render_widget, output_widget
import plotly.express as px
import os
from dotenv import load_dotenv
import querychat
from chatlas import ChatAnthropic
# Add the parent directory of 'src' to the path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils import calculate_avg_trip_time
import plotly.graph_objects as go
from pathlib import Path
import ibis
from ibis import _

# Read Anthropic API key
load_dotenv()
API_KEY = os.environ.get("ANTHROPIC_API_KEY")

# -- Data setup (runs once at startup) ----------------------------------------
PARQUET = Path(__file__).parent / ".." / "data" / "processed" / "201306-citibike-tripdata.parquet"
if not PARQUET.exists():
    raise FileNotFoundError(
        "Missing parquet file. Run `python src/prep_data.py` first."
    )

con = ibis.duckdb.connect()
df = con.read_parquet(str(PARQUET))

df = df.mutate(
    starttime = df.starttime.cast("timestamp"),
    stoptime = df.stoptime.cast("timestamp")
)
df = df.mutate(start_hour = df['starttime'].hour())
df = df.mutate(end_hour = df['stoptime'].hour())
df = df.mutate(day_of_week = df['starttime'].day_of_week.full_name())
df = df.mutate(month = df['starttime'].strftime('%B'))
df = df.mutate(birth_year = df["birth year"].nullif('NULL').cast('int64'))
df = df.drop("birth year").rename({"birth year": "birth_year"})

# Initialize QueryChat
qc = querychat.QueryChat(
    df.execute(),
    "BikeShareOptimizer",
    greeting="👋 Hi! I'm your NYC BikeShare assistant. Ask me about trends in Citi Bike data!",
    data_description="""
    Citi Bike trip dataset for NYC.
    Columns:
    - starttime, stoptime: Datetimes
    - start_hour, end_hour: Integer (0-23)
    - birth year: Integer(nullable)
    - usertype: 'Subscriber' or 'Customer'
    - gender: 0 (Unknown), 1 (Male), 2 (Female)
    - start station name: String
    """,
    client=ChatAnthropic(model="claude-3-5-sonnet-latest", api_key=API_KEY),
)

# UI
app_ui = ui.page_navbar(
    ui.nav_panel("Main Dashboard", 
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
                        min=1899, 
                        max=1997, 
                        value=[1950, 1997], # Adjusted default to remove outliers
                        sep=''
                    )
                ),
                ui.input_slider(
                    id="start_time_slider",
                    label="Start Hour",
                    min=0,
                    max=23,
                    value=[0, 23],
                ),
                ui.input_selectize(
                    id="day_of_week_filter",
                    label="Day of Week",
                    choices=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    selected=[],
                    multiple=True,
                ),
                ui.input_selectize(
                    id="month_filter",
                    label="Month",
                    choices=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
                    selected=[],
                    multiple=True,
                ),
                ui.input_checkbox_group(
                    id="gender_checkbox",
                    label="User Gender",
                    choices={'0': "Unknown", '1': "Male", '2': "Female"},
                    selected=["0", "1", "2"],
                ),
                ui.input_action_button('apply', 'Apply Filters', class_='btn-primary'),
                ui.input_action_button("reset", "Reset Filter"),
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
                    output_widget("start_hour_barplot"),
                    full_screen=True,
                ),
                col_widths=[6, 6],
            ),
            ui.layout_columns(
                ui.card(
                    ui.card_header("NYC Station Map"),
                    output_widget("map"),
                    full_screen=True,
                )
            ),
        ),
    ),

    ui.nav_panel("AI Insights", 
        ui.layout_sidebar(
            qc.sidebar(),
            ui.layout_columns(
                ui.card(
                    ui.card_header("AI Filtered Data"),
                    ui.download_button("download_ai_data", "Download Data"),
                    ui.output_data_frame("ai_data_table")
                ),
                ui.card(
                    ui.card_header("AI Start Hour Trends"),
                    output_widget("ai_start_hour_plot"),
                    full_screen=True,
                ),
                ui.card(
                    ui.card_header("AI User Type Distribution"),
                    output_widget("ai_usertype_plot"),
                    full_screen=True,
                ),
                col_widths=[6,6]
            )
        )
    ),
    
    # Keyword arguments must go at the end of the page_navbar call
    title="Citi Bike NYC System Optimizer",
    id="tabs"
)


# Server
def server(input, output, session):
    qc_vals = qc.server()
    selected_stations = reactive.Value([])

    @reactive.calc
    def ai_df():
        try:
            d = qc_vals.df()
            if d is None or not isinstance(d, pd.DataFrame):
                return pd.DataFrame()
            return d
        except Exception:
            return pd.DataFrame()

    @render.data_frame
    def ai_data_table():
        d = ai_df()
        if d.empty:
            return render.DataGrid(pd.DataFrame({"Message": ["Ask the AI a question to generate data"]}))
        return render.DataGrid(d)
    
    @render.download(filename="ai_filtered_data.csv")
    def download_ai_data():
        d = ai_df()
        if d.empty:
            yield "No data available"
            return
        yield d.to_csv(index=False)

    @reactive.calc
    def base_filtered_df():
        s_min, s_max = input.start_time_slider()
        genders = [int(g) for g in input.gender_checkbox()]
        usertypes = input.usertype_checkbox()
        days = input.day_of_week_filter()
        months = input.month_filter()

        if not days:
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        if not months:
            months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

        m = (df['start_hour'].between(s_min, s_max) &
             df['gender'].isin(genders) &
             df['usertype'].isin(usertypes) &
             df['day_of_week'].isin(days) &
             df['month'].isin(months))

        if "Customer" not in usertypes:
            b_min, b_max = input.birth_year_slider()
            m_birth = df['birth year'].between(b_min, b_max)
            m = m & m_birth

        return df.filter(m)

    @reactive.calc
    def filtered_df():
        d = base_filtered_df().execute()
        stations = selected_stations.get()
        if stations:
            d = d[d['start station name'].isin(stations)]
        return d

    @reactive.effect
    @reactive.event(input.reset)
    def _():
        ui.update_checkbox_group('usertype_checkbox', selected=["Subscriber"])
        ui.update_slider("birth_year_slider", value=[1950, 1997])
        ui.update_slider("start_time_slider", value=[0, 23])
        ui.update_checkbox_group("gender_checkbox", selected=['0', '1', '2'])
        ui.update_selectize("day_of_week_filter", selected=[])
        ui.update_selectize("month_filter", selected=[])
        selected_stations.set([])

    @render.text
    def avg_trip_time():
        if not input.usertype_checkbox():
            return 'Please select a User Type'
        d = filtered_df()
        if d.empty: return "N/A"
        avg = calculate_avg_trip_time(d)
        if avg is None:
            return "N/A"
        return f"{avg:.1f} mins"

    @render.text
    def s_to_c_ratio():
        if not input.usertype_checkbox():
            return 'Please select a User Type'
        d = filtered_df()
        if d.empty:
            return "N/A"

        subscribers = (d["usertype"] == "Subscriber").sum()
        customers = (d["usertype"] == "Customer").sum()

        if customers == 0:
            return "N/A (No Customers)"

        ratio = subscribers / customers
        return f"{ratio:.2f}"

    @render.text
    def pop_start_id():
        if not input.usertype_checkbox():
            return 'Please select a User Type'
        d = filtered_df()
        if d.empty:
            return "N/A"
        return d["start station name"].value_counts().idxmax()

    @render.text
    def pop_start_hour():
        if not input.usertype_checkbox():
            return 'Please select a User Type'
        d = filtered_df()
        if d.empty: return "N/A"
        
        # Convert military time to AM/PM format
        start_hour = int(d['start_hour'].mode()[0])
        am_pm = "AM" if start_hour < 12 else "PM"
        display_hour = start_hour if start_hour <= 12 else start_hour - 12
        if display_hour == 0: display_hour = 12
        
        return f"{display_hour}:00 {am_pm}"

    @render_plotly
    def start_hour_barplot():
        empty_df = pd.DataFrame({'start_hour': [], 'trip_count': []})

        if not input.usertype_checkbox():
            return px.bar(empty_df, x='start_hour', y='trip_count').update_layout(title="Please select a User Type")

        d = filtered_df()
        if d.empty:
            return px.bar(empty_df, x='start_hour', y='trip_count').update_layout(title="No data available")

        trips_per_start_hour = d.groupby(['start_hour']).size().reset_index(name='trip_count')

        fig = px.bar(
            trips_per_start_hour, x='start_hour', y='trip_count',
            template="plotly_white", color_discrete_sequence=['#6C5CE7']
        )
        fig.update_traces(marker_line_color='white', marker_line_width=1.5, opacity=0.8)
        # Removed Plotly title to fix double-title issue
        fig.update_layout(
            xaxis_title="Start Hour", yaxis_title="Count of Trips",
            bargap=0.1, hovermode="x unified", margin=dict(l=20, r=20, t=20, b=20)
        )
        return fig
    
    @render_plotly
    def barplot1():
        empty_df = pd.DataFrame({'birth year': []})
        
        # Fixed blank plot confusion
        if "Subscriber" not in input.usertype_checkbox():
            return px.histogram(empty_df, x="birth year").update_layout(
                title="Data unavailable (Subscribers only)",
                xaxis_title="Birth Year", yaxis_title="Count of Trips"
            )

        d = filtered_df()
        if d.empty:
            return px.histogram(empty_df, x="birth year").update_layout(title="No data available")
            
        fig = px.histogram(
            d, x="birth year", nbins=40,
            template="plotly_white", color_discrete_sequence=['#6C5CE7']
        )
        fig.update_traces(marker_line_color='white', marker_line_width=1.5, opacity=0.8)
        # Removed Plotly title
        fig.update_layout(
            xaxis_title="Birth Year", yaxis_title="Count of Trips",
            bargap=0.1, hovermode="x unified", margin=dict(l=20, r=20, t=20, b=20)
        )
        return fig

    @render_widget
    def map():
        if not input.usertype_checkbox():
            return px.scatter_mapbox(lat=[0], lon=[0], zoom=0).update_layout(title="Please select a User Type")

        d = base_filtered_df().execute()
        if d.empty:
            return px.scatter_mapbox(lat=[0], lon=[0], zoom=0).update_layout(title="No data available")
        
        station_agg = d.groupby("start station name").agg(
            latitude=("start station latitude", "first"),
            longitude=("start station longitude", "first"),
            trip_count=("start station name", "size")
        ).reset_index()

        fig = px.scatter_mapbox(
            station_agg, lat="latitude", lon="longitude",
            color_discrete_sequence=['#1e1e1e'], zoom=11,
        )
        fig.update_traces(marker=dict(size=8), hoverinfo='skip', hovertemplate=None)

        fig2 = px.scatter_mapbox(
            station_agg, lat="latitude", lon="longitude",
            color="trip_count", color_continuous_scale='plasma',
            hover_name="start station name",
            hover_data={'latitude': False, 'longitude': False, "trip_count": True},
            labels={"trip_count": "Trips"}
        )

        fig.add_trace(fig2.data[0])
        fig.update_layout(
            mapbox_style="carto-positron",
            margin={"r":0,"t":0,"l":0,"b":0},
            coloraxis_colorbar=dict(title='Trip Count'),
            clickmode='event+select'
        )
        
        fw = go.FigureWidget(fig)

        def handle_selection(trace, points, state):
            if points.point_inds:
                stations = station_agg.iloc[points.point_inds]["start station name"].tolist()
                selected_stations.set(stations)
            else:
                selected_stations.set([])

        def handle_deselect(*args, **kwargs):
            selected_stations.set([])

        fw.data[1].on_selection(handle_selection)
        fw.data[1].on_click(handle_selection)
        fw.data[1].on_deselect(handle_deselect)

        return fw
    
    @render_plotly
    def ai_start_hour_plot():
        d = ai_df()
        if len(d) > 20000: d = d.sample(20000)
        if d.empty: return px.bar().update_layout(title="No AI filtered data available")

        agg = d.groupby("start_hour").size().reset_index(name="trip_count")
        fig = px.bar(
                agg, x="start_hour", y="trip_count",
                template="plotly_white", color_discrete_sequence=['#6C5CE7']
        )
        fig.update_layout(xaxis_title="Start Hour", yaxis_title="Trip Count", hovermode="x unified", margin=dict(t=20))
        return fig
    
    @render_plotly
    def ai_usertype_plot():
        d = ai_df()
        if len(d) > 20000: d = d.sample(20000)
        if d.empty: return px.bar().update_layout(title="No AI filtered data available")

        agg = d.groupby("usertype").size().reset_index(name="trip_count")
        fig = px.bar(
            agg, x="usertype", y="trip_count",
            template="plotly_white", color="usertype"
        )
        fig.update_layout(xaxis_title="User Type", yaxis_title="Trip Count", hovermode="x unified", margin=dict(t=20))
        return fig
    
app = App(app_ui, server)