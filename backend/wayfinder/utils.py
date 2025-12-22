import numpy as np
import colorsys
import logging


log = logging.getLogger(__name__)


def remove_locations_during_visit(locations_df, visits_df):
    # Create a mask
    mask = np.zeros(len(locations_df), dtype=bool)

    # Mark locations during visits
    for _, visit in visits_df.iterrows():
        mask |= (locations_df["time"] >= visit["arrival_date"]) & (
            locations_df["time"] <= visit["departure_date"]
        )

    return locations_df[~mask]


def color_trips(locations_df, visits_df):

    log.info("Coloring trips...")

    # Sort dataframes by time
    log.debug("Sorting dataframes by time...")
    locations_df = locations_df.sort_values("time")
    visits_df = visits_df.sort_values("arrival_date")

    # Initialize color column with NaN values
    log.debug("Initializing color column with NaN values...")
    locations_df["color"] = np.nan

    # Calculate number of colors needed
    log.debug("Calculating number of colors needed...")
    n_colors = len(visits_df) + 1  # +1 for the initial trip segment

    # Generate colors
    log.debug("Generating colors...")
    colors = [colorsys.hsv_to_rgb(i / n_colors, 0.8, 0.8) for i in range(n_colors)]
    colors = [
        "rgb({},{},{})".format(int(r * 255), int(g * 255), int(b * 255))
        for r, g, b in colors
    ]

    # Color the initial segment (before the first visit)
    log.debug("Coloring the initial segment...")
    mask = locations_df["time"] < visits_df.iloc[0]["arrival_date"]
    locations_df.loc[mask, "color"] = colors[0]

    # Color segments between visits
    log.debug("Coloring segments between visits...")
    for i in range(len(visits_df) - 1):
        departure = visits_df.iloc[i]["departure_date"]
        next_arrival = visits_df.iloc[i + 1]["arrival_date"]
        mask = (locations_df["time"] > departure) & (
            locations_df["time"] < next_arrival
        )
        locations_df.loc[mask, "color"] = colors[i + 1]

    # Color the final segment (after the last visit)
    log.debug("Coloring the final segment...")
    mask = locations_df["time"] > visits_df.iloc[-1]["departure_date"]
    locations_df.loc[mask, "color"] = colors[-1]

    return locations_df
