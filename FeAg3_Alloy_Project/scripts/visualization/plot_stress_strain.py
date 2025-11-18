import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

PROJECT_ROOT = "/mnt/c/Users/danie/feag3_Mechanical_Properties"

def parse_tensile_data(log_file):
    """Parse tensile test data from LAMMPS log file"""
    
    with open(log_file, 'r') as f:
        lines = f.readlines()
    
    data = []
    capture = False
    
    for line in lines:
        if 'Step' in line and 'v_strain_xx' in line and 'v_stress_xx' in line:
            capture = True
            continue
        elif capture and line.strip():
            if line[0].isdigit() or (line[0] == ' ' and line[1].isdigit()):
                parts = line.strip().split()
                if len(parts) >= 5:
                    try:
                        step = int(parts[0])
                        strain = float(parts[1])
                        stress = float(parts[2])
                        data.append([step, strain, stress])
                    except:
                        continue
            else:
                break
    
    df = pd.DataFrame(data, columns=['Step', 'Strain', 'Stress_GPa'])
    return df

def plot_stress_strain(df, save_path=None):
    """Plot stress-strain curve"""
    
    plt.figure(figsize=(10, 6))
    plt.plot(df['Strain'] * 100, df['Stress_GPa'], 'b-', linewidth=2, marker='o', markersize=4)
    plt.xlabel('Strain (%)')
    plt.ylabel('Stress (GPa)')
    plt.title('FeAg3 Stress-Strain Curve from MD Simulation')
    plt.grid(True, alpha=0.3)
    
    # Calculate Young's modulus from linear region
    if len(df) > 5:
        youngs_modulus = np.polyfit(df['Strain'][:5] * 100, df['Stress_GPa'][:5], 1)[0]
        plt.text(0.6, 0.9, f'Young\'s Modulus: {youngs_modulus:.2f} GPa', 
                transform=plt.gca().transAxes, fontsize=12,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Stress-strain plot saved to: {save_path}")
    
    plt.show()
    
    return df

# Parse and plot the data
log_file = os.path.join(PROJECT_ROOT, "outputs/tensile_test.log")
df = parse_tensile_data(log_file)

if not df.empty:
    print("Stress-Strain Data:")
    print(df.head(10))
    print(f"\nTotal data points: {len(df)}")
    
    # Save data to CSV
    csv_path = os.path.join(PROJECT_ROOT, "results/stress_strain_data.csv")
    df.to_csv(csv_path, index=False)
    print(f"Data saved to: {csv_path}")
    
    # Create plot
    plot_path = os.path.join(PROJECT_ROOT, "results/stress_strain_curve.png")
    plot_stress_strain(df, plot_path)
    
    # Calculate mechanical properties
    youngs_modulus = np.polyfit(df['Strain'][:5] * 100, df['Stress_GPa'][:5], 1)[0]
    yield_strength = df['Stress_GPa'].max() * 0.9  # Approximate yield strength
    
    print(f"\nMechanical Properties:")
    print(f"Young's Modulus: {youngs_modulus:.2f} GPa")
    print(f"Maximum Stress: {df['Stress_GPa'].max():.4f} GPa")
    print(f"Maximum Strain: {df['Strain'].max() * 100:.4f} %")
else:
    print("No stress-strain data found in log file")
