import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math


BOUNDARY_RADIUS = 65
SAFE_RADIUS = 62   # Keep small margin inside rope


def clamp_to_boundary(x, y):
    """Ensure fielder stays inside boundary circle."""
    distance = math.sqrt(x**2 + y**2)

    if distance > SAFE_RADIUS:
        scale = SAFE_RADIUS / distance
        x *= scale
        y *= scale

    return x, y


def draw_field(required_runs,
               balls_left,
               wickets_in_hand):

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_facecolor('#2E7D32')

    # Ground
    ax.add_patch(patches.Circle((0, 0), 65, color='#388E3C'))
    ax.add_patch(patches.Circle((0, 0), 65,
                                fill=False,
                                color='white',
                                linewidth=2))

    # 30-yard circle
    ax.add_patch(patches.Circle((0, 0), 30,
                                fill=False,
                                linestyle='--',
                                color='white'))

    # Pitch
    ax.add_patch(patches.Rectangle((-1.5, -10),
                                   3, 20,
                                   color='#E8D5B5'))

    overs_left = balls_left / 6
    rrr = required_runs / overs_left if overs_left > 0 else 0

    if rrr <= 8:
        situation = "Low Pressure"
    elif rrr <= 12:
        situation = "Moderate Pressure"
    else:
        situation = "High Pressure"

    # Base inside
    base_inside = {
        "Bowler": (0, -15),
        "Keeper": (0, 15),
        "Point": (-25, 20),
        "Cover": (-20, -5),
        "Mid-off": (-20, -25),
        "Mid-on": (20, -25),
    }

    if situation == "Low Pressure":

        outside = {
            "Third Man": (-50, 50),
            "Fine Leg": (50, 50),
            "Long-off": (-30, -55),
            "Long-on": (30, -55)
        }

        inside_extra = {
            "Square Leg": (25, 10)
        }

    elif situation == "Moderate Pressure":

        outside = {
            "Third Man": (-50, 50),
            "Fine Leg": (50, 50),
            "Long-off": (-30, -55),
            "Long-on": (30, -55),
            "Deep Mid-wkt": (50, -30)
        }

        inside_extra = {}

    else:

        outside = {
            "Third Man": (-55, 50),
            "Fine Leg": (55, 50),
            "Long-off": (-30, -60),
            "Long-on": (30, -60),
            "Deep Mid-wkt": (55, -35)
        }

        inside_extra = {}

    # Enforce max 5 outside
    outside = dict(list(outside.items())[:5])

    positions = {**base_inside, **inside_extra, **outside}

    safe_positions = {}
    for name, (x, y) in positions.items():
        x, y = clamp_to_boundary(x, y)
        safe_positions[name] = (x, y)

    
    for name, (x, y) in safe_positions.items():
        ax.plot(x, y, 'o',
                color='white',
                markersize=8,
                markeredgecolor='black')
        ax.text(x, y - 5,
                name,
                fontsize=6,
                color='white',
                ha='center')

    ax.set_xlim(-70, 70)
    ax.set_ylim(-70, 70)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.set_title(f"{situation} Field Setup",
                 color='white',
                 fontsize=9)

    return fig
