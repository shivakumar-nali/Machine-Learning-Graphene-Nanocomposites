import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def parse_lammps_data(data_file):
    """Parse LAMMPS data file and extract atom positions"""
    
    with open(data_file, 'r') as f:
        lines = f.readlines()
    
    atoms_section = False
    masses_section = False
    atoms = []
    masses = {}
    
    for i, line in enumerate(lines):
        if 'Masses' in line:
            masses_section = True
            continue
        elif 'Atoms' in line:
            masses_section = False
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

def plot_structure(data_file, save_path=None):
    """Plot 3D atomic structure"""
    
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
    ax.set_title('FeAg3 Crystal Structure')
    ax.legend()
    
    # Set equal aspect ratio
    max_range = max([ax.get_xlim()[1] - ax.get_xlim()[0],
                     ax.get_ylim()[1] - ax.get_ylim()[0],
                     ax.get_zlim()[1] - ax.get_zlim()[0]])
    
    mid_x = np.mean(ax.get_xlim())
    mid_y = np.mean(ax.get_ylim())
    mid_z = np.mean(ax.get_zlim())
    
    ax.set_xlim(mid_x - max_range/2, mid_x + max_range/2)
    ax.set_ylim(mid_y - max_range/2, mid_y + max_range/2)
    ax.set_zlim(mid_z - max_range/2, mid_z + max_range/2)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Structure plot saved to: {save_path}")
    
    plt.show()
    
    print(f"Total atoms: {len(atoms)}")
    print(f"Fe atoms: {len(fe_positions)}")
    print(f"Ag atoms: {len(ag_positions)}")

if __name__ == "__main__":
    # Visualize minimized structure
    data_file = "../../outputs/feag3_minimized.lmp"
    plot_structure(data_file, "../../results/structure_3d.png")
