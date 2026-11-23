
#!/usr/bin/env python3
"""
Interactive station maps
------------------------------------------------
LEFT PANEL:
    Europe

RIGHT TOP PANEL:
    Netherlands (large inset with province borders)

RIGHT BOTTOM PANEL:
    Brazil

Features
--------
- Brown land / blue water
- Clear country borders
- Dutch province borders
- Clickable station URLs
- Hover tooltips
- Custom marker styles/colors
- Automatic label positioning without additional packages
"""

import webbrowser
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import mplcursors


# ============================================================
# STATION CONFIGURATION
# ============================================================

stations = [
    {
        "name": "Duivendaal",
        "period": "1920-1963",
        "lat": 51.9664,
        "lon": 5.6594,
        "marker": "o",
        "color": "purple",
        "size": 140,
        "url": "https://maq-observations.nl/wp-content/uploads/duivendaal_maq_data_overview.docx",
        "country": "Netherlands"
    },
    {
        "name": "Haarweg",
        "period": "1963-2012",
        "lat": 51.970719,
        "lon": 5.642652,
        "marker": "o",
        "color": "purple",
        "size": 140,
        "url": "https://maq-observations.nl/wp-content/uploads/haarweg_maq_data_overview.docx",
        "country": "Netherlands"
    },
    {
        "name": "Veenkampen",
        "period": "2011-now",
        "lat": 51.9812,
        "lon": 5.6201,
        "marker": "o",
        "color": "purple",
        "size": 140,
        "url": "https://maq-observations.nl/wp-content/uploads/veenkampen_maq_data_overview.docx",
        "country": "Netherlands"
    },
    {
        "name": "Loobos",
        "period": "1996-now",
        "lat": 52.166581,
        "lon": 5.743556,
        "marker": "o",
        "color": "green",
        "size": 140,
        "url": "https://maq-observations.nl/wp-content/uploads/loobos_maq_data_overview.docx",
        "country": "Netherlands"
    },
    {
        "name": "Amsterdam",
        "period": "2018-now",
        "lat": 52.366648,
        "lon": 4.892913,
        "marker": "o",
        "color": "red",
        "size": 140,
        "url": "https://maq-observations.nl/wp-content/uploads/amsterdam_maq_data_overview.docx",
        "country": "Netherlands"
    },
    {
        "name": "Scintillometry",
        "period": "2018-now",
        "lat": 51.970221,
        "lon": 4.926187,
        "marker": "o",
        "color": "blue",
        "size": 140,
        "url": "https://maq-observations.nl/wp-content/uploads/scintillometry_maq_data_overview.docx",
        "country": "Netherlands"
    },
    {
        "name": "CloudRoots",
        "period": "August 2022",
        "lat": -2.1458,
        "lon": -59.0055,
        "marker": "^",
        "color": "orange",
        "size": 140,
        "url": "https://maq-observations.nl/wp-content/uploads/cloudroots_maq_data_overview.docx",
        "country": "Spain"
    },
    {
        "name": "LIAISE",
        "period": "April-September 2021",
        "lat": 41.6882,
        "lon": 0.94001,
        "marker": "^",
        "color": "yellow",
        "size": 140,
        "url": "https://maq-observations.nl/wp-content/uploads/liase_maq_data_overview.docx",
        "country": "Spain"
    },
]


# ============================================================
# COLORS
# ============================================================

LAND_COLOR = "#b58b5a"
WATER_COLOR = "#7ec8e3"


# ============================================================
# FIGURE LAYOUT
# ============================================================

fig = plt.figure(figsize=(18, 10))

# Left large panel: Europe
ax_eu = fig.add_axes(
    [0.05, 0.08, 0.52, 0.84],
    projection=ccrs.PlateCarree()
)

# Right top: Netherlands
ax_nl = fig.add_axes(
    [0.62, 0.53, 0.33, 0.39],
    projection=ccrs.PlateCarree()
)

# Right bottom: Brazil
ax_br = fig.add_axes(
    [0.62, 0.08, 0.33, 0.34],
    projection=ccrs.PlateCarree()
)


# ============================================================
# EXTENTS
# ============================================================

ax_eu.set_extent(
    [-15, 35, 35, 72],
    crs=ccrs.PlateCarree()
)

nl_extent = [3.0, 7.5, 50.5, 53.8]

ax_nl.set_extent(
    nl_extent,
    crs=ccrs.PlateCarree()
)

ax_br.set_extent(
    [-75, -30, -35, 10],
    crs=ccrs.PlateCarree()
)


# ============================================================
# MAP STYLING FUNCTION
# ============================================================

def style_map(ax):

    ax.add_feature(
        cfeature.OCEAN,
        facecolor=WATER_COLOR,
        zorder=0
    )

    ax.add_feature(
        cfeature.LAND,
        facecolor=LAND_COLOR,
        edgecolor="black",
        linewidth=0.6,
        zorder=1
    )

    ax.add_feature(
        cfeature.BORDERS,
        edgecolor="black",
        linewidth=0.8,
        zorder=2
    )

    ax.coastlines(linewidth=0.8)


style_map(ax_eu)
style_map(ax_nl)
style_map(ax_br)


# ============================================================
# TITLES
# ============================================================

ax_eu.set_title("Europe", fontsize=18)
ax_nl.set_title("Netherlands", fontsize=18)
ax_br.set_title("Brazil", fontsize=18)


# ============================================================
# NETHERLANDS BOX ON EUROPE MAP
# ============================================================

rect_lons = [
    nl_extent[0],
    nl_extent[1],
    nl_extent[1],
    nl_extent[0],
    nl_extent[0],
]

rect_lats = [
    nl_extent[2],
    nl_extent[2],
    nl_extent[3],
    nl_extent[3],
    nl_extent[2],
]

ax_eu.plot(
    rect_lons,
    rect_lats,
    color="black",
    linewidth=2,
    transform=ccrs.PlateCarree(),
    zorder=30,
)


# ============================================================
# LOAD DUTCH PROVINCES
# ============================================================

province_url = (
    "https://cartomap.github.io/nl/wgs84/provincie_2023.geojson"
)

try:

    import geopandas as gpd

    provinces = gpd.read_file(province_url)

    provinces.boundary.plot(
        ax=ax_nl,
        edgecolor="black",
        linewidth=0.8,
        zorder=40,
        transform=ccrs.PlateCarree(),
    )

    print("Province borders loaded successfully.")

except Exception as e:

    print("Could not load province borders.")
    print(e)


# ============================================================
# FIX IJSSELMEER / INTERNAL WATER BODIES
# ============================================================

ax_nl.add_feature(
    cfeature.LAKES,
    facecolor=WATER_COLOR,
    edgecolor="black",
    linewidth=0.4,
    zorder=5
)

ax_nl.add_feature(
    cfeature.RIVERS,
    edgecolor=WATER_COLOR,
    linewidth=0.5,
    zorder=6
)


# ============================================================
# STATION PLOTTING
# ============================================================

scatter_objects = []
station_labels = []


def add_station(ax, station, initial_offset=(12, 12)):

    label = f"{station['name']} ({station['period']})"

    # Station marker
    sc = ax.scatter(
        station["lon"],
        station["lat"],
        s=station["size"],
        marker=station["marker"],
        color=station["color"],
        edgecolor="black",
        transform=ccrs.PlateCarree(),
        zorder=100,
    )


    # Set label position
    if station["name"] == "Scintillometry":
        label_offset = (-35, -25)  # Bottom left
    else:
        label_offset = (12, 12)    # Default: top right
        
    # Special initial position for LIAISE:
    # move it away from the Europe legend.
    if station["name"] == "LIAISE" and ax is ax_eu:
        label_offset = (35, 35)

        

    # Annotation: label offset is measured in screen points.
    # This keeps the label separated from the marker at every map scale.
    annotation = ax.annotate(
        label,
        xy=(station["lon"], station["lat"]),
        xycoords=ccrs.PlateCarree()._as_mpl_transform(ax),
        xytext=label_offset,
        textcoords="offset points",
        fontsize=8,
        ha="left",
        va="bottom",
        arrowprops=dict(
            arrowstyle="-",
            color="black",
            linewidth=0.6,
            shrinkA=3,
            shrinkB=6,
        ),
        bbox=dict(
            facecolor="white",
            edgecolor="none",
            alpha=0.8,
            pad=1.5
        ),
        zorder=101,
    )

    scatter_objects.append((sc, station))
    station_labels.append((ax, annotation, station))


for station in stations:
    # Skip labels for these two stations
    if station["name"] in ["Haarweg", "Duivendaal"]:
        continue

    # Europe:
    # Explicitly exclude all Dutch stations.
    if (
        station["country"] != "Netherlands"
        and -15 <= station["lon"] <= 35
        and 35 <= station["lat"] <= 72
    ):
        add_station(ax_eu, station)

    # Netherlands:
    # Dutch stations are displayed only here.
    if (
        station["country"] == "Netherlands"
        and nl_extent[0] <= station["lon"] <= nl_extent[1]
        and nl_extent[2] <= station["lat"] <= nl_extent[3]
    ):
        add_station(
            ax_nl,
            station,
            initial_offset=(12, 12)
        )

    # Brazil
    if (
        -75 <= station["lon"] <= -30
        and -35 <= station["lat"] <= 10
    ):
        add_station(
            ax_br,
            station,
            initial_offset=(12, 12)
        )


# ============================================================
# AUTOMATIC LABEL ADJUSTMENT
# ============================================================

def adjust_labels(fig, labels, iterations=300, gap=5):

    """
    Separate overlapping annotation labels.

    Label positions are adjusted in screen points, not geographic
    coordinates. The station markers remain fixed.

    Only labels on the same map are compared.
    """

    if not labels:
        return

    points_per_pixel = 72.0 / fig.dpi

    for iteration in range(iterations):

        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()

        moved = False

        for i in range(len(labels)):

            ax1, ann1, station1 = labels[i]

            for j in range(i + 1, len(labels)):

                ax2, ann2, station2 = labels[j]

                # Only compare labels on the same map.
                if ax1 is not ax2:
                    continue

                box1 = ann1.get_window_extent(
                    renderer
                ).expanded(1.02, 1.10)

                box2 = ann2.get_window_extent(
                    renderer
                ).expanded(1.02, 1.10)

                # No overlap.
                if not box1.overlaps(box2):
                    continue

                # Calculate overlap in display pixels.
                overlap_x = min(box1.x1, box2.x1) - max(
                    box1.x0, box2.x0
                )

                overlap_y = min(box1.y1, box2.y1) - max(
                    box1.y0, box2.y0
                )

                if overlap_x <= 0 or overlap_y <= 0:
                    continue

                # Move apart along the direction requiring
                # the smallest displacement.
                cx1 = (box1.x0 + box1.x1) / 2
                cy1 = (box1.y0 + box1.y1) / 2

                cx2 = (box2.x0 + box2.x1) / 2
                cy2 = (box2.y0 + box2.y1) / 2

                if overlap_x <= overlap_y:

                    direction = 1 if cx1 >= cx2 else -1

                    # Deterministic direction if centres coincide.
                    if abs(cx1 - cx2) < 0.1:
                        direction = 1 if i % 2 == 0 else -1

                    shift_x = (
                        overlap_x / 2 + gap
                    ) * points_per_pixel * direction

                    shift_y = 0

                else:

                    direction = 1 if cy1 >= cy2 else -1

                    if abs(cy1 - cy2) < 0.1:
                        direction = 1 if i % 2 == 0 else -1

                    shift_x = 0

                    shift_y = (
                        overlap_y / 2 + gap
                    ) * points_per_pixel * direction

                # Annotation positions are in points.
                x1, y1 = ann1.get_position()
                x2, y2 = ann2.get_position()

                ann1.set_position((
                    x1 + shift_x,
                    y1 + shift_y
                ))

                ann2.set_position((
                    x2 - shift_x,
                    y2 - shift_y
                ))

                moved = True

        if not moved:
            break

    fig.canvas.draw()


# Run label adjustment after all station labels have been created.
adjust_labels(fig, station_labels)


# ============================================================
# INTERACTIVE HOVER
# ============================================================

artists = [x[0] for x in scatter_objects]

cursor = mplcursors.cursor(
    artists,
    hover=True
)


@cursor.connect("add")
def on_hover(sel):

    artist = sel.artist

    for sc, station in scatter_objects:

        if sc is artist:

            label = (
                f"{station['name']} "
                f"({station['period']})"
            )

            sel.annotation.set_text(
                f"{label}\nClick to open webpage"
            )

            break


# ============================================================
# CLICKABLE URLS
# ============================================================

def on_click(event):

    for sc, station in scatter_objects:

        contains, _ = sc.contains(event)

        if contains:

            print(f"Opening: {station['url']}")

            webbrowser.open(
                station["url"]
            )

            break


fig.canvas.mpl_connect(
    "button_press_event",
    on_click
)


# ============================================================
# LEGEND
# ============================================================

legend_elements = []

for station in stations:

    legend_elements.append(
        Line2D(
            [0],
            [0],
            marker=station["marker"],
            color="w",
            label=f"{station['name']} ({station['period']})",
            markerfacecolor=station["color"],
            markeredgecolor="black",
            markersize=8,
        )
    )


ax_eu.legend(
    handles=legend_elements,
    loc="lower left",
    fontsize=8,
    framealpha=0.9,
    ncol=1,
    borderpad=0.7,
    labelspacing=0.5,
)


# ============================================================
# FINAL TITLE
# ============================================================

plt.suptitle(
    "Monitoring Stations & Field Campaigns",
    fontsize=22,
)

plt.savefig("MAQ-Obs_map.png",dpi=300)
plt.show()
