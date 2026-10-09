import csv
import sys

INPUT_CSV = "/home/agiuser/Documents/qd_new_code/legged_gym/resources/robots/T1-V2-URDF/Q410100005401_T1-V2.SLDASM/urdf/Q410100005401_T1-V2.SLDASM.csv"
OUTPUT_CSV = "/home/agiuser/Documents/qd_new_code/legged_gym/resources/robots/T1-V2-URDF/Q410100005401_T1-V2.SLDASM/urdf/Q410100005401_T1-V2_inertia_summary.csv"

REQUIRED_COLS = [
    "Link Name",
    "Mass",
    "Moment Ixx", "Moment Ixy", "Moment Ixz",
    "Moment Iyy", "Moment Iyz", "Moment Izz"
]

with open(INPUT_CSV, newline="", encoding="utf-8") as fin, \
     open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as fout:
    
    reader = csv.reader(fin)
    writer = csv.writer(fout)

    # 读取表头
    header = next(reader)
    header = [h.strip() for h in header]

    # 动态获取列索引
    col_indices = {}
    for col_name in REQUIRED_COLS:
        if col_name not in header:
            raise ValueError(f"Column '{col_name}' not found in CSV header.")
        col_indices[col_name] = header.index(col_name)

    idx_link = col_indices["Link Name"]
    idx_mass = col_indices["Mass"]
    idx_ixx = col_indices["Moment Ixx"]
    idx_ixy = col_indices["Moment Ixy"]
    idx_ixz = col_indices["Moment Ixz"]
    idx_iyy = col_indices["Moment Iyy"]
    idx_iyz = col_indices["Moment Iyz"]
    idx_izz = col_indices["Moment Izz"]

    # 写入表头
    writer.writerow([
        "link_name", "mass",
        "ixx", "ixy", "ixz", "iyy", "iyz", "izz"
    ])

    for row in reader:
        if not row or len(row) <= idx_izz:
            continue

        link_name = row[idx_link].strip()
        if not link_name:
            continue

        try:
            mass = float(row[idx_mass])
            ixx  = float(row[idx_ixx])
            ixy  = float(row[idx_ixy])
            ixz  = float(row[idx_ixz])
            iyy  = float(row[idx_iyy])
            iyz  = float(row[idx_iyz])
            izz  = float(row[idx_izz])
        except ValueError:
            print(f"Warning: skipping row with invalid numeric data: {row}", file=sys.stderr)
            continue

        writer.writerow([link_name, mass, ixx*1e-3, ixy*1e-3, ixz*1e-3, iyy*1e-3, iyz*1e-3, izz*1e-3])

print(f"Done. Output written to: {OUTPUT_CSV}")