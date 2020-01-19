import json
import math


def get_coord(venue_name, venue_list):
    try:
        coord = venue_list[venue_name]['location']
        return coord['x'], coord['y']
    except KeyError:
        return 103.77459895804348, 1.2982161237100815


def find_distance(venue_a, venue_b, venue_list):
    (xa, ya) = get_coord(venue_a, venue_list)
    (xb, yb) = get_coord(venue_b, venue_list)
    return math.sqrt((xa - xb) ** 2 + (ya - yb) ** 2)


if __name__ == "__main__":
    with open('/home/bryanwhl/project/venues.json', 'r') as f:
        venues = json.load(f)

    print(find_distance("UT-AUD1", "UT-AUD2", venues))
    print(find_distance("AS4-0602", "E4A-06-07", venues))
    print(find_distance("S17-0512", "COM1-003", venues))
    print(get_coord("Y-AChemLab", venues))