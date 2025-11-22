import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# Set the project root path
PROJECT_ROOT = "/mnt/c/Users/danie/feag3_Mechanical_Properties"

def parse_lammps_log(log_file):
    """Parse LAMMPS log file and extract thermo data"""
    
    with open(log_file, 'r') as f:
        lines = f.readlines()
    
    # Find thermo data section
    thermo_start = False
    thermo_data = []
    headers = []
    
    for line in lines:
        if 'Step' in line and 'PotEng' in line and 'TotEng' in line:
            headers = line.strip().split()
            thermo_start = True
            continue
        
        if thermo_start:
            if line.strip() and not line.startswith('Loop') and not line.startswith('Minimization'):
                # Check if line contains numeric data
                import re
                if re.match(r'^\s*\d', line):
                    values = line.strip().split()
                    if len(values) == len(headers):
                        thermo_data.append([float(x) for x in values])
            elif line.startswith('Minimization'):
                break
    
    df = pd.DataFrame(thermo_data, columns=headers)
    return df

def parse_lammps_data(data_file):
    """Parse LAMMPS data file and extract atom positions"""
    
    with open(data_file, 'r') as f:
        lines = f.readlines()
    
    atoms_section = False
    atoms = []
    
    for i, line in enumerate(lines):
        if 'Atoms' in line:
            atoms_section = True
            continue
        elif atoms_section and line.strip() and not line.startswith('#'):
            parts = line.strip().split()
            if len(parts) >= 5:
                atom_id = int(parts[0])
                atom_type = int(parts[1])
                x, y, z = float(parts[2]), float(parts[3]), float(parts[4])
                atoms.append({'type': atom_type, 'x': x, 'y': y, 'z': z})
    
    return atoms

def create_minimization_plot():
    """Create energy minimization plot"""
    
    log_file = os.path.join(PROJECT_ROOT, "outputs/minimization.log")
    
    if not os.path.exists(log_file):
        print(f"Log file not found: {log_file}")
        return None
    
    df = parse_lammps_log(log_file)
    
    if df.empty:
        print("No thermo data found in log file")
        return None
    
    plt.figure(figsize=(12, 8))
    
    # Plot energy evolution
    plt.subplot(2, 2, 1)
    plt.plot(df['Step'], df['PotEng'], 'b-', linewidth=2)
    plt.xlabel('Step')
    plt.ylabel('Potential Energy (eV)')
    plt.title('Energy Minimization')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 2)
    plt.plot(df['Step'], df['Press'], 'r-', linewidth=2)
    plt.xlabel('Step')
    plt.ylabel('Pressure (GPa)')
    plt.title('Pressure Evolution')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 3)
    plt.plot(df['Step'], df['Volume'], 'g-', linewidth=2)
    plt.xlabel('Step')
    plt.ylabel('Volume (Å³)')
    plt.title('Volume Evolution')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    plot_path = os.path.join(PROJECT_ROOT, "results/minimization_progress.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Minimization plot saved to: {plot_path}")
    return df

def create_structure_plot():
    """Create 3D structure visualization"""
    
    data_file = os.path.join(PROJECT_ROOT, "outputs/feag3_minimized.lmp")
    
    if not os.path.exists(data_file):
        print(f"Structure file not found: {data_file}")
        return
    
    atoms = parse_lammps_data(data_file)
    
    if not atoms:
        print("No atoms found in data file")
        return
    
    # Separate Fe and Ag atoms
    fe_positions = [[a['x'], a['y'], a['z']] for a in atoms if a['type'] == 1]
    ag_positions = [[a['x'], a['y'], a['z']] for a in atoms if a['type'] == 2]
    
    fe_positions = np.array(fe_positions)
    ag_positions = np.array(ag_positions)
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot atoms
    if len(fe_positions) > 0:
        ax.scatter(fe_positions[:, 0], fe_positions[:, 1], fe_positions[:, 2], 
                  c='red', s=200, label='Fe', alpha=0.8, edgecolors='black')
    
    if len(ag_positions) > 0:
        ax.scatter(ag_positions[:, 0], ag_positions[:, 1], ag_positions[:, 2], 
                  c='silver', s=150, label='Ag', alpha=0.8, edgecolors='black')
    
    ax.set_xlabel('X (Å)')
    ax.set_ylabel('Y (Å)')
    ax.set_zlabel('Z (Å)')
    ax.set_title('FeAg3 Crystal Structure (Minimized)')
    ax.legend()
    
    plot_path = os.path.join(PROJECT_ROOT, "results/structure_3d.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Structure plot saved to: {plot_path}")
    print(f"Total atoms: {len(atoms)}")
    print(f"Fe atoms: {len(fe_positions)}")
    print(f"Ag atoms: {len(ag_positions)}")

if __name__ == "__main__":
    print("Creating visualization plots...")
    
    # Create results directory
    os.makedirs(os.path.join(PROJECT_ROOT, "results"), exist_ok=True)
    
    # Create minimization plot
    df = create_minimization_plot()
    
    if df is not None and not df.empty:
        print("\nMinimization Summary:")
        print(f"Initial Energy: {df['PotEng'].iloc[0]:.2f} eV")
        print(f"Final Energy: {df['PotEng'].iloc[-1]:.2f} eV")
        print(f"Energy Change: {df['PotEng'].iloc[-1] - df['PotEng'].iloc[0]:.2f} eV")
        print(f"Final Volume: {df['Volume'].iloc[-1]:.2f} Å³")
        
        # Save data to CSV
        csv_path = os.path.join(PROJECT_ROOT, "results/minimization_data.csv")
        df.to_csv(csv_path, index=False)
        print(f"Data saved to: {csv_path}")
    
    # Create structure plot
    create_structure_plot()
    
    print("\nAll visualizations completed!")
