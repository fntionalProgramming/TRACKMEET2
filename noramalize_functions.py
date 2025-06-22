'''
functions for normalizing the sssad and track events into one same format to make it easier to parse the data
because there is a ctually a crazy ammount of inconsistency in both data
'''

from typing import Optional, Tuple
'''
soem time in sssad category rows some time it is like this
"SG/IG/IB" instead of a normal category string like "SG"
so this function will basically just parse it
'''
def normalize_sssad_category(s: str) -> list[str]:
    s = s.split('/')
    if isinstance(s, str):
        s = [s]
    return s

'''
this function a sssad event string like LJ - (NW Pit)
'''
def normalize_sssad_events(word: str) -> Tuple[str, Optional[str]]:
    location_aliases = {
        'n': 'north',
        's': 'south',
        'e': 'east',
        'w': 'west',
        'ne': 'northeast',
        'nw': 'northwest',
        'se': 'southeast',
        'sw': 'southwest',
        'north': 'north',
        'south': 'south',
        'east': 'east',
        'west': 'west',
    }

    sssad_prefix_map = {
        "lj": "longjump",
        "tj": "triplejump",
        "hj": "highjump",
        "pv": "polevault",
        "sp": "shotput",
        "jv": "javelin",
    }
    pit = False
    word = word.lower()
    if "pit" in word:
        word = word.replace("pit", "")
        pit = True
    word = word.replace("(", "")
    word = word.replace(")", "")
    word = word.replace("-", "")
    word = word.strip()
    word = word.split(' ')
    word = [w for w in word if w != '']
    location = None
    if len(word) == 2 and word[1] in location_aliases:
        location = location_aliases[word[1]]
        if pit:
            location += " pit"
        word = word[0]
    word = "".join(word)
    if word in sssad_prefix_map:
        word = sssad_prefix_map[word]
    return word, location

def normalize_trackie_events(word: str) -> str:
    event_map_trackie = {
        # track events
        "100m",
        "200m",
        "400m",
        "800m",
        "1500m",
        "3000m",
        "hurdles",
        "4x100m",
        # fields events
        "longjump",
        "polevault",
        "triplejump",
        "highjump",
        "shot",
        "discus",
        "javelin"
    }
    word = word.lower()
    word = word.split(" ")
    if len(word) == 2 and word[1] in event_map_trackie:
        word = word[1]
    elif len(word) == 2 and word[0] in event_map_trackie:
        word = word[0]
    return "".join(word)

'''
main function to test the inputs
these inputs are directly taken from SSSAD and Trackie events
'''
if __name__ == "__main__":
    examples = [
        "100 M",
        "800 M",
        "Pole Vault",
        "HJ - North",
        "LJ - NW",
        "Shot (EAST)",
        "3000 M",
        "4 x 100 M",
        "Medley",
        "Javelin (S)",
        "1500 M",
        "Discus",
        "400 M",
        "200 M",
        "Hurdles",
        "Hurdles",
        "TJ - NW Pit"
    ]
    for event in examples:
        print(f"Input: {event}")
        event, location = normalize_sssad_events(event)
        print(f"Nromalized: {event} Location: {location}")
        print("-" * 40)
    
    print("\n=== normalize_trackie_data ===")
    trackie_examples = [
        "100m",
        "800m",
        "Pole Vault",
        "High Jump",
        "Long Jump",
        "Shot Put",
        "3000m",
        "4x100m",
        "Medley",
        "Javelin Throw",
        "1500m",
        "Discus Throw",
        "400m",
        "200m",
        "80m Hurdles",
        "100m Hurdles",
        "Triple Jump",
    ]
    for event in trackie_examples:
        normalized = normalize_trackie_events(event)
        print(f"Input: {event}")
        print(f"Normalized: {normalized}")
        print("-" * 40)
    print("\n=== Comparison Between SSSAD and Trackie ===")
    for sssad_event in examples:
        sssad_norm, sssad_location = normalize_sssad_events(sssad_event)
        for trackie_event in trackie_examples:
            trackie_norm = normalize_trackie_events(trackie_event)

            if sssad_norm == trackie_norm:
                print(f"✅\nSSSAD:    {sssad_event} -> {sssad_norm} | {sssad_location}\nTrackie:  {trackie_event} -> {trackie_norm}")
                print("-" * 60)

