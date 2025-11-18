import pandas as pd
import matplotlib.pyplot as plt
import re

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
                if re.match(r'^\s*\d', line):
                    values = line.strip().split()
                    if len(values) == len(headers):
                        thermo_data.append([float(x) for x in values])
            elif line.startswith('Minimization'):
                break
    
    df = pd.DataFrame(thermo_data, columns=headers)
    return df

def plot_minimization(log_file, save_path=None):
    """Plot energy minimization progress"""
    
    df = parse_lammps_log(log_file)
    
    if df.empty:
        print("No thermo data found in log file")
        return
    
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
    
    plt.subplot(2, 2, 4)
    plt.plot(df['Step'], df['Lx'], 'm-', label='Lx', linewidth=2)
    plt.plot(df['Step'], df['Ly'], 'c-', label='Ly', linewidth=2)
    plt.plot(df['Step'], df['Lz'], 'y-', label='Lz', linewidth=2)
    plt.xlabel('Step')
    plt.ylabel('Lattice Parameters (Å)')
    plt.title('Lattice Parameters')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    
    plt.show()
    
    return df

if __name__ == "__main__":
    # Parse our minimization log
    log_file = "../../outputs/minimization.log"
    df = plot_minimization(log_file, "../../results/minimization_plot.png")
    
    if df is not None and not df.empty:
        print("\nMinimization Summary:")
        print(f"Initial Energy: {df['PotEng'].iloc[0]:.2f} eV")
        print(f"Final Energy: {df['PotEng'].iloc[-1]:.2f} eV")
        print(f"Energy Change: {df['PotEng'].iloc[-1] - df['PotEng'].iloc[0]:.2f} eV")
        print(f"Final Volume: {df['Volume'].iloc[-1]:.2f} Å³")
        
        # Save data to CSV for further analysis
        df.to_csv("../../results/minimization_data.csv", index=False)
        print("Data saved to: ../../results/minimization_data.csv")
