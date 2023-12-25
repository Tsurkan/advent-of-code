def convert(seed, maps):
        num = seed
        for r in maps:
            for dest_start, source_start, length in r:
                if source_start <= num < source_start + length:
                    num = dest_start + (num - source_start)
                    break
        return num

def card_announcement():

    # Define the mappings for each conversion step
    seed_to_soil_map = []
    soil_to_fertilizer_map = []
    fertilizer_to_water_map = []
    water_to_light_map = []
    light_to_temperature_map = []
    temperature_to_humidity_map = []
    humidity_to_location_map = []

    # Combine all the maps
    all_maps = [
        seed_to_soil_map, soil_to_fertilizer_map, fertilizer_to_water_map,
        water_to_light_map, light_to_temperature_map, temperature_to_humidity_map,
        humidity_to_location_map
    ]

    return all_maps

def task1(file_path):
    with open(file_path) as f:
        arr_paragraphs = f.read().split('\n\n')

    all_maps = card_announcement()

    # List of initial seeds
    seeds = [int(i) for i in arr_paragraphs[0].split(': ')[1].split()]
    arr_paragraphs.pop(0)

    # Fill out all the maps
    for i, e in enumerate(arr_paragraphs):
        for k in e.split(':\n')[1].split('\n'):
            all_maps[i].append([int(i) for i in k.split()])
            
    # Find the lowest location number corresponding to any of the initial seeds
    min_location = float('inf')
    for seed in seeds:
        location = convert(seed, all_maps)
        min_location = min(min_location, location)

    return min_location

def read_input(file_path):
    with open(file_path) as f:
        sections = f.read().split('\n\n')

    # Extract seeds from the first section and convert them into a list of integers
    seeds = [int(i) for i in sections[0].split(': ')[1].split()]
    sections.pop(0) # Remove the first section with seeds

    # Create intervals from pairs of seeds, specifying the start and end point of each interval
    intervals = [(a, a + b) for a, b in zip(seeds[::2], seeds[1::2])]
    return sections, intervals

def calculate_intervals(rows, intervals):

    # Initialize variables to store start points and offsets
    i_start = [-1]
    offsets = [0]
    latest_end = -1

    # Iterate through each row and calculate the end point of the interval
    for row in rows:
        latest_end = max(latest_end, row[1] + row[2])
        offset = row[0] - row[1]
        
        # Update start point and offset if they match the previous ones
        if i_start and i_start[-1] == row[1]:
            i_start[-1] = row[1]
            offsets[-1] = offset
        else:
            i_start.append(row[1])
            offsets.append(offset)
        
        i_start.append(row[1] + row[2])
        offsets.append(0)
    
    out = []
    
    # Calculate intervals based on given intervals and offsets
    for interval in intervals:
        splits = [interval[0]]
        start_index = None
        
        # Find suitable points to split the interval
        for idx, post in enumerate(i_start):
            if post <= splits[-1]:
                continue
            if start_index is None:
                start_index = idx - 1
            if post < interval[1]:
                if post != interval[1]:
                    splits.append(post)
            else:
                break
        
        splits.append(interval[1])
        start_index = start_index or len(offsets)
        
        # Apply offset to intervals
        for a, b in zip(splits, splits[1:]):
            dx = offsets[min(start_index or float('inf'), len(offsets) - 1)]
            start_index += 1
            out.append((a + dx, b + dx))
    
    return out

def task2(file_path):
    # Read input data and get sections and intervals
    sections, intervals = read_input(file_path)
    
    # For each table in sections, calculate intervals
    for table in sections:
        rows = [tuple(map(int, row.split())) for row in table.split('\n')[1:]]
        rows.sort(key=lambda row: row[1]) # Sort table rows based on the second element (intervals)
        intervals = calculate_intervals(rows, intervals) # Calculate intervals
    
    # Return the minimum start point of an interval
    return min(c[0] for c in intervals)

def main():
    file_path = '2023/day5/input.txt'
    print('Part one:', task1(file_path)) # 282277027
    print('Part two:', task2(file_path)) # 11554135

if __name__ == "__main__":
    main()