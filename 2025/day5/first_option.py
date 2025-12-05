ranges = []
ingredients = []

with open("2025/day5/input.txt", 'r') as f:
    for line in (line.strip() for line in f.readlines()):
        if "-" in line:
            start, end = (int(x) for x in line.split("-"))
            ranges.append(range(start, end + 1))
        elif line:
            ingredients.append(int(line))

print(f"Fresh ingredients: {sum(1 for i in ingredients if any((i in r) for r in ranges))}")

last_range = range(0, 0)
fresh = 0

# объединяем пересекающиеся диапазоны
for r in sorted(ranges, key=lambda r: r.start):
    if r.start in last_range:  # диапазоны пересекаются
        if r.stop > last_range.stop:
            fresh += r.stop - last_range.stop
            last_range = range(last_range.start, r.stop)
    else:
        fresh += len(r)
        last_range = r

print(f"Total fresh ingredients: {fresh}")
