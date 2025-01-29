import webcolors
import colorthief

COLORS = [
    'gray',
    'white',
    'black',
    "green",
    "blue",
    "red",
    "purple",
    "orange",
    "yellow",
    "brown",
    "gold",
]

def closest_color(rgb_tuple):
    """Find the closest color name for the given RGB tuple."""
    min_diff = float('inf')
    closest_name = None
    for name, hex_code in webcolors.CSS3_NAMES_TO_HEX.items():
        r, g, b = webcolors.hex_to_rgb(hex_code)
        diff = (r - rgb_tuple[0]) ** 2 + (g - rgb_tuple[1]) ** 2 + (b - rgb_tuple[2]) ** 2
        if diff < min_diff:
            min_diff = diff
            closest_name = name
    return closest_name

def get_color_name(rgb_tuple):
    """Try to get the exact color name or return the closest color name."""
    try:
        # Check if the color has an exact name
        return webcolors.rgb_to_name(rgb_tuple)
    except ValueError:
        # Find the closest color if no exact match
        return closest_color(rgb_tuple)
    
def get_generic_color(color_name):
    # Define a dictionary mapping specific color names to generic ones
    color_map = {
        "red": "red",
        "crimson": "red",
        "scarlet": "red",
        "maroon": "red",
        "orange": "orange",
        "tangerine": "orange",
        "amber": "orange",
        "yellow": "yellow",
        "gold": "yellow",
        "lemon": "yellow",
        "green": "green",
        "lime": "green",
        "emerald": "green",
        "blue": "blue",
        "navy": "blue",
        "cyan": "blue",
        "indigo": "indigo",
        "violet": "purple",
        "lavender": "purple",
        "magenta": "purple",
        "purple": "purple"
    }

    # Normalize input to lowercase for case-insensitive matching
    color_name = color_name.lower()

    # Return the generic color name if found, otherwise "unknown"
    return color_map.get(color_name, "unknown")
    
def getProminentColors(image_file_location):
    ct = colorthief.ColorThief(image_file_location)
    palette = ct.get_palette(color_count=40, quality=1)
    top_colors, prom_colors = [], []
    for color in palette:
        top_colors.append(get_color_name(color))
    print(top_colors)
    # If a color name appears inside a color (e.g. 'gray' in 'dimgray') then add the simpler one to the list
    for color in top_colors:
        for preset_color in COLORS:
            if preset_color in color and preset_color not in prom_colors:
                prom_colors.append(preset_color)

    # Turn the list of colors into generic names
    for color in top_colors:
        gen = get_generic_color(color)
        if gen != "unknown" and gen not in prom_colors:
            prom_colors.append(gen)
    return prom_colors
