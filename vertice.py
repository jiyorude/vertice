import struct
import shutil
import zipfile
import glob
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, PageBreak, Spacer, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
import os
import sys

LUMP_ENTITIES = 0
LUMP_MODELS = 14
HEADER_LUMPS = 17
LUMP_SIZE = 8
HEADER_SIZE = 4 + HEADER_LUMPS * LUMP_SIZE

time = datetime.now().strftime("%b_%d-%H_%M_%S")
time_full = datetime.now().strftime(("%A %d %B %Y - %H:%M:%S"))
map_count = 0

def read_lump_info(file, lump_index):
    file.seek(HEADER_SIZE + lump_index * LUMP_SIZE)
    offset, length = struct.unpack('ii', file.read(LUMP_SIZE))
    return offset, length

def parse_entities(file, offset, length):
    file.seek(offset)
    entities_data = file.read(length).decode('utf-8', errors='ignore')
    spawn_points = []
    for entity in entities_data.split('}'):
        if '"classname" "info_player_deathmatch"' in entity:
            lines = entity.split('\n')
            for line in lines:
                if '"origin"' in line:
                    coords = line.split('"')[3]
                    x, y, z = map(float, coords.split(' '))
                    spawn_points.append((x, y, z))
                    break
    return spawn_points

def calculate_map_dimensions(spawn_points):
    print("...Calculating map dimensions.")
    min_x = min_y = min_z = float('inf')
    max_x = max_y = max_z = float('-inf')
    for x, y, z in spawn_points:
        min_x, max_x = min(min_x, x), max(max_x, x)
        min_y, max_y = min(min_y, y), max(max_y, y)
        min_z, max_z = min(min_z, z), max(max_z, z)
    return (min_x, max_x), (min_y, max_y), (min_z, max_z)

def process_map(bsp_path):
    print("...Processing spawn points.")
    global map_count
    map_count += 1
    with open(bsp_path, 'rb') as bsp_file:
        output = []
        entities_offset, entities_length = read_lump_info(bsp_file, LUMP_ENTITIES)
        spawn_points = parse_entities(bsp_file, entities_offset, entities_length)
        if not spawn_points:
            output.append("No spawn points found in map. Skipped.")
            print("...No spawn points found in map. Skipped.")
            return
        (min_x, max_x), (min_y, max_y), (min_z, max_z) = calculate_map_dimensions(spawn_points)
        output.append(f"Map {map_count} - {os.path.basename(bsp_path)}")
        output.append(f"Map Dimensions:")
        output.append("X Axis:")
        output.append(f"{min_x}")
        output.append(f"{max_x}")
        output.append("Y Axis:")
        output.append(f"{min_y}")
        output.append(f"{max_y}")
        output.append("Z Axis:")
        output.append(f"{min_z}")
        output.append(f"{max_z}")
        output.append("Spawn Points:")
        for idx, (x, y, z) in enumerate(spawn_points, start=1):
            move_left = x - min_x
            move_right = max_x - x
            move_forward = max_y - y
            move_backward = y - min_y
            move_up = max_z - z
            move_down = z - min_z
            output.append(f"Spawn Point {idx}")
            output.append(f"Spawn Position")
            output.append("X Axis")
            output.append(f"{x}")
            output.append("Y Axis")
            output.append(f"{y}")
            output.append("Z Axis")
            output.append(f"{z}")
            output.append(f"Space until void:")
            output.append(f"{move_left}")
            output.append(f"{move_right}")
            output.append(f"{move_forward}")
            output.append(f"{move_backward}")
            output.append(f"{move_up}")
            output.append(f"{move_down}")
            output.append("")
        print()
        return output

def generate_pdf(report_data, filename=f"output/vertice_output_{time}.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    Story = []
    
    Story.append(Paragraph("Vertice (Quake III Map Boundary Analysis Tool)", styles['Heading1']))
    Story.append(Spacer(1, 12))
    Story.append(Paragraph(f"Report generated at: {time_full}", styles['Normal']))
    Story.append(Spacer(1, 12))

    for data in report_data:
        if isinstance(data, list) and len(data) > 1:
            Story.append(Paragraph(f"{data[0]}", styles['Heading2']))
            Story.append(Spacer(1, 12))
            dimension_data = [
                ['Dimension', 'Min Value', 'Max Value'],
                ['X Axis', data[3], data[4]],
                ['Y Axis', data[6], data[7]],
                ['Z Axis', data[9], data[10]]
            ]
            dimension_table = Table(dimension_data, colWidths=[100, 100, 100], hAlign='LEFT')
            dimension_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.gray),
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ]))
            Story.append(dimension_table)
            Story.append(Spacer(1, 12))
            idx = 11
            while idx + 15 < len(data): 
                spawn_details = [
                    [data[idx+1], 'Value'],
                    ['X Axis', data[idx+4]],
                    ['Y Axis', data[idx+6]],
                    ['Z Axis', data[idx+8]],
                    [data[idx+9], ''],
                    ['Left', data[idx+10]],
                    ['Right', data[idx+11]],
                    ['Forward', data[idx+12]],
                    ['Backward', data[idx+13]],
                    ['Upward', data[idx+14]],
                    ['Downward', data[idx+15]]
                ]
                sp_table = Table(spawn_details, colWidths=[150, 150], hAlign='LEFT')
                sp_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.lightgrey), 
                    ('BACKGROUND', (0,4), (-1,4), colors.lightgrey), 
                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                ]))
                Story.append(sp_table)
                Story.append(Spacer(1, 12))
                idx += 16 
    doc.build(Story)


def extract_and_process_pk3(pk3_path, temp_extract_dir="temp_maps"):
    with zipfile.ZipFile(pk3_path, 'r') as zip_ref:
        bsp_files = [file for file in zip_ref.namelist() if file.lower().startswith("maps/") and file.lower().endswith(".bsp")]
        for bsp_file in bsp_files:
            zip_ref.extract(bsp_file, temp_extract_dir)
    maps_dir = os.path.join(temp_extract_dir, "maps")
    if not os.path.exists(maps_dir): 
        maps_dir = os.path.join(temp_extract_dir, "MAPS")
    if os.path.exists(maps_dir):
        bsp_paths = [os.path.join(maps_dir, file) for file in os.listdir(maps_dir) if file.endswith(".bsp")]
        for bsp_path in bsp_paths:
            yield process_map(bsp_path)
    else:
        print(f"...PK3 archive does not contain 'maps' folder. Skipped.")
    shutil.rmtree(temp_extract_dir)

def main(input_dir='input'):
    map_files = glob.glob(os.path.join(input_dir, '*.bsp')) + glob.glob(os.path.join(input_dir, '*.pk3'))
    report_data = []
    for map_file in map_files:
        filename = os.path.basename(map_file)
        if filename.endswith(".pk3"):
            print("...PK3 archive found.")
            print("...Extracting BSP from PK3 archive.")
            for output in extract_and_process_pk3(map_file):
                report_data.append(output)
        elif filename.endswith(".bsp"):
            print('...BSP file found.')
            map_output = process_map(map_file)
            report_data.append(map_output)
    generate_pdf(report_data)

if __name__ == "__main__":
    print("...Running Vertice.\n")
    main()
    print("...Done! Check the 'output' folder.")
    sys.exit(0)