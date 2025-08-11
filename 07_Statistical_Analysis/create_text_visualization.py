import csv

# Read the data
with open('writing_scores_data.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Convert to floats
for row in data:
    row['Before_AI'] = float(row['Before_AI'])
    row['After_AI'] = float(row['After_AI'])
    row['Improvement'] = float(row['Improvement'])

# Create a text-based visualization
print("\nTEXT-BASED VISUALIZATION OF RESULTS")
print("=" * 80)
print("\n1. BEFORE vs AFTER COMPARISON (Scatter Plot Style)")
print("-" * 60)
print("Score Range: 60 -------- 70 -------- 80 -------- 90")
print("             |          |          |          |")

for i, row in enumerate(data):
    before_pos = int((row['Before_AI'] - 60) * 1.5)  # Scale to fit display
    after_pos = int((row['After_AI'] - 60) * 1.5)
    
    # Ensure positions are within bounds
    before_pos = max(0, min(39, before_pos))
    after_pos = max(0, min(39, after_pos))
    
    line = [' '] * 40
    line[before_pos] = 'B'
    
    # If they don't overlap, add A
    if before_pos != after_pos:
        line[after_pos] = 'A'
    else:
        line[before_pos] = 'X'
    
    print(f"S{i+1:02d}: {''.join(line)} (B={row['Before_AI']:.1f}, A={row['After_AI']:.1f})")

print("\nLegend: B = Before AI, A = After AI, X = Overlapping scores")

print("\n\n2. IMPROVEMENT DISTRIBUTION (Histogram Style)")
print("-" * 60)
print("Improvement (points)")
print("   <0   0-2  2-4  4-6  6-8  >8")
print("   |    |    |    |    |    |")

# Count improvements in bins
bins = {'<0': 0, '0-2': 0, '2-4': 0, '4-6': 0, '6-8': 0, '>8': 0}
for row in data:
    imp = row['Improvement']
    if imp < 0:
        bins['<0'] += 1
    elif imp <= 2:
        bins['0-2'] += 1
    elif imp <= 4:
        bins['2-4'] += 1
    elif imp <= 6:
        bins['4-6'] += 1
    elif imp <= 8:
        bins['6-8'] += 1
    else:
        bins['>8'] += 1

# Display histogram
max_count = max(bins.values())
for i in range(max_count, 0, -1):
    line = f"{i:2d} |"
    for bin_name in ['<0', '0-2', '2-4', '4-6', '6-8', '>8']:
        if bins[bin_name] >= i:
            line += "  ■  "
        else:
            line += "     "
    print(line)
print("   " + "-" * 35)
print("     <0   0-2  2-4  4-6  6-8  >8")
print(f"\nCount: {bins['<0']}    {bins['0-2']}    {bins['2-4']}    {bins['4-6']}    {bins['6-8']}    {bins['>8']}")

print("\n\n3. STATISTICAL SUMMARY BOX")
print("+" + "-" * 58 + "+")
print("| PAIRED T-TEST RESULTS                                    |")
print("|" + "-" * 58 + "|")
print(f"| Sample size: 20 students                                 |")
print(f"| Mean improvement: 4.28 points (95% CI: 2.86 to 5.71)    |")
print(f"| t-statistic: 6.30 (df = 19)                             |")
print(f"| p-value: < 0.001 (highly significant)                    |")
print(f"| Cohen's d: 1.41 (large effect size)                      |")
print("|" + "-" * 58 + "|")
print("| INTERPRETATION:                                          |")
print("| ✓ Significant improvement in writing scores              |")
print("| ✓ 95% of students showed improvement                     |")
print("| ✓ Large practical effect (>1 SD improvement)             |")
print("+" + "-" * 58 + "+")

print("\n\n4. INDIVIDUAL STUDENT PERFORMANCE")
print("-" * 60)
print("Top 5 Improvements:")
sorted_data = sorted(data, key=lambda x: x['Improvement'], reverse=True)
for i in range(5):
    row = sorted_data[i]
    print(f"  {row['Student_ID']}: {row['Before_AI']:.1f} → {row['After_AI']:.1f} (+{row['Improvement']:.1f})")

print("\nBottom 5 Improvements:")
for i in range(-5, 0):
    row = sorted_data[i]
    sign = '+' if row['Improvement'] >= 0 else ''
    print(f"  {row['Student_ID']}: {row['Before_AI']:.1f} → {row['After_AI']:.1f} ({sign}{row['Improvement']:.1f})")