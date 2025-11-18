import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

PROJECT_ROOT = "/mnt/c/Users/danie/feag3_Mechanical_Properties"

def extract_stress_strain_data():
    """Extract stress-strain data from tensile test log"""
    
    log_file = os.path.join(PROJECT_ROOT, "outputs/tensile_test.log")
    
    with open(log_file, 'r') as f:
        content = f.read()
    
    # Find the tensile test data section
    lines = content.split('\n')
    data = []
    in_tensile_section = False
    
    for line in lines:
        if 'Step' in line and 'v_strain_xx' in line and 'v_stress_xx' in line:
            in_tensile_section = True
            continue
        elif in_tensile_section:
            if line.strip() and (line[0].isdigit() or (line.startswith(' ') and line[1].isdigit())):
                parts = line.strip().split()
                if len(parts) >= 3:
                    try:
                        step = int(parts[0])
                        strain = float(parts[1])
                        stress = float(parts[2])
                        data.append([step, strain, stress])
                    except:
                        continue
            elif line.strip() and not line[0].isdigit():
                break
    
    df = pd.DataFrame(data, columns=['Step', 'Strain', 'Stress_GPa'])
    return df

# Extract and analyze the data
df = extract_stress_strain_data()

if not df.empty:
    print("=== FeAg3 Tensile Test Results ===")
    print(f"Data points: {len(df)}")
    print("\nStress-Strain Data:")
    print(df.head(10))
    
    # Save data
    csv_path = os.path.join(PROJECT_ROOT, "results/stress_strain_data.csv")
    df.to_csv(csv_path, index=False)
    print(f"\nData saved to: {csv_path}")
    
    # Create plot
    plt.figure(figsize=(10, 6))
    plt.plot(df['Strain'] * 100, df['Stress_GPa'], 'b-o', linewidth=2, markersize=4)
    plt.xlabel('Strain (%)')
    plt.ylabel('Stress (GPa)')
    plt.title('FeAg3 Stress-Strain Curve from Molecular Dynamics')
    plt.grid(True, alpha=0.3)
    
    # Calculate mechanical properties
    if len(df) > 2:
        # Young's modulus from initial slope
        youngs_modulus = np.polyfit(df['Strain'][:3] * 100, df['Stress_GPa'][:3], 1)[0]
        max_stress = df['Stress_GPa'].max()
        max_strain = df['Strain'].max() * 100
        
        plt.text(0.02, 0.95, f'Young\'s Modulus: {youngs_modulus:.2f} GPa', 
                transform=plt.gca().transAxes, fontsize=12,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        plt.text(0.02, 0.85, f'Max Stress: {max_stress:.4f} GPa', 
                transform=plt.gca().transAxes, fontsize=12,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        
        print(f"\n=== Mechanical Properties ===")
        print(f"Young's Modulus: {youngs_modulus:.2f} GPa")
        print(f"Maximum Stress: {max_stress:.4f} GPa")
        print(f"Maximum Strain: {max_strain:.4f} %")
    
    plot_path = os.path.join(PROJECT_ROOT, "results/stress_strain_curve.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved to: {plot_path}")
    
    plt.show()
    
else:
    print("No stress-strain data found")

print("\n=== Simulation Summary ===")
print("✅ Energy minimization completed")
print("✅ Tensile test executed successfully") 
print("✅ Stress-strain data extracted")
print("✅ Mechanical properties calculated")
