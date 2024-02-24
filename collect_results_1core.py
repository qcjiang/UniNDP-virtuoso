#!/usr/bin/python3
import os
import csv

directories = ['CPU/1core', 'NDP/1core', 'CPU.test/1core', 'NDP.test/1core', 'CPU-no-translation/1core', 'NDP-no-translation/1core', 'CPU-no-translation.test/1core', 'NDP-no-translation.test/1core', 'NDP-common-ddr/1core', 'NDP-no-translation-common-ddr/1core', 'NDP-HBM/1core', 'NDP-no-translation-HBM/1core']
output_file = 'output_1core.csv'
frequency_ghz = 2.6

with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Directory', 'File', 'Total Cycles', 'Average PTW Latency (Cycles)'])

def calculate_average_ptw_latency(data, frequency_ghz):
    ptw_latency_fs = 0
    ptw_walks = 0
    for line in data.splitlines():
        if line.startswith('ptw_radix_0.page_level_latency'):
            ptw_latency_fs += float(line.split('=')[1].strip())
        elif line.startswith('PTW_0.page_walks'):
            ptw_walks = float(line.split('=')[1].strip())

    if ptw_walks != 0:
        average_ptw_latency_cycles = (ptw_latency_fs / ptw_walks) * (frequency_ghz / 1e6)
    else:
        average_ptw_latency_cycles = 'N/A'
    return average_ptw_latency_cycles

for directory in directories:
    for subdir in ['bc', 'bfs', 'cc', 'dlrm', 'gc', 'gen', 'pr', 'rnd', 'sssp', 'tc', 'xs']:
        out_path = os.path.join(directory, subdir, 'out')
        sim_out_path = os.path.join(directory, subdir, 'sim.out')
        average_ptw_latency_cycles = 'N/A'
        cycles = 'N/A'

        if os.path.exists(out_path):
            with open(out_path, 'r') as file:
                data = file.read()
                average_ptw_latency_cycles = calculate_average_ptw_latency(data, frequency_ghz)

        if os.path.exists(sim_out_path):
            with open(sim_out_path, 'r') as file:
                data = file.read()
                for line in data.splitlines():
                    if 'Cycles' in line:
                        cycles = line.split('|')[1].strip()

        with open(output_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([directory, subdir, cycles, average_ptw_latency_cycles])

print("Data extraction complete, results saved in", output_file)
