import concurrent.futures
import time

def part_One(file_path):
    
    def convert(seed, maps):
        num = seed
        for r in maps:
            for dest_start, source_start, length in r:
                if source_start <= num < source_start + length:
                    num = dest_start + (num - source_start)
                    break
        return num

    with open(file_path) as f:
        arr_paragraphs = f.read().split('\n\n')

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

def convert(seed, maps):
        num = seed
        for r in maps:
            for dest_start, source_start, length in r:
                if source_start <= num < source_start + length:
                    num = dest_start + (num - source_start)
                    break
        return num

def process_seed(seed_data):
    seed_start, seed_length, all_maps = seed_data
    min_location = float('inf')
    for seed_num in range(seed_start, seed_start + seed_length):
        location = convert(seed_num, all_maps)
        min_location = min(min_location, location)
    return min_location

def part_Two(file_path):

    with open(file_path) as f:
        arr_paragraphs = f.read().split('\n\n')

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

    # List of initial seeds
    seeds = [int(i) for i in arr_paragraphs[0].split(': ')[1].split()]
    pairs_seeds = [(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)]
    arr_paragraphs.pop(0)

    # Fill out all the maps
    for i, e in enumerate(arr_paragraphs):
        for k in e.split(':\n')[1].split('\n'):
            all_maps[i].append([int(i) for i in k.split()])

    # Find the lowest location number corresponding to any of the initial seeds

    # min_location = float('inf')
    # for seed_start, seed_length in pairs_seeds:
    #     for seed_num in range(seed_start, seed_start + seed_length):
    #         location = convert(seed_num, all_maps)
    #         min_location = min(min_location, location)
    start_time = time.time()

    min_location = float('inf')

    seed_data = [(seed_start, seed_length, all_maps) for seed_start, seed_length in pairs_seeds]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(process_seed, seed_data)
        min_location = min(results)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time / 60} minuts")

    return min_location

def main():
    # print('Part one:', part_One('day5/input.txt')) # 282277027
    print('Part two:', part_Two('day5/input.txt')) # 

if __name__ == "__main__":
    main()