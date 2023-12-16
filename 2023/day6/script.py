def count_ways_to_beat_record(race_duration, record_distance):
    ways_to_beat_record = 0
    
    # iterating only up to race_duration // 2 and multiplying the count by 2 at the end 
    # if the race duration is even.
    for duration in range(1, (race_duration // 2) + 1):
        if duration * (race_duration - duration) > record_distance:
            ways_to_beat_record += 2

    if race_duration % 2 == 0:
        ways_to_beat_record -= 1
    
    return ways_to_beat_record

    # return sum(1 for duration in range(race_duration) if duration * (race_duration - duration) > record_distance)

def task1(file_path):
    with open(file_path, "r") as file:
        race_durations, record_distances = [list(map(int, line.strip().split(": ")[1].split())) for line in file.readlines()]

    total_ways = 1
    for duration, distance in zip(race_durations, record_distances):
        total_ways *= count_ways_to_beat_record(duration, distance)

    return total_ways

def task2(file_path):
    with open(file_path, "r") as file:
        race_durations, record_distances = [int(line.split(": ")[1].replace(' ', '').strip()) for line in file.readlines()]
   
    return count_ways_to_beat_record(race_durations, record_distances)

def main():
    file_path = '2023/day6/input.txt'
    print('Part one:', task1(file_path)) # 800280
    print('Part two:', task2(file_path)) # 45128024

if __name__ == "__main__":
    main()