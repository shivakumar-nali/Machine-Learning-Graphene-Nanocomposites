import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Manual extraction of the data we saw in the log
data = [
    [522, 0.000000, 0.17317181],
    [600, 0.000008, 0.17412217],
    [700, 0.000018, 0.17535622],
    [800, 0.000028, 0.17659004],
    [900, 0.000038, 0.17782364],
    [1000, 0.000048, 0.17905702],
    [1100, 0.000058, 0.18029018],
    [1200, 0.000068, 0.18152311],
    [1300, 0.000078, 0.18275582],
    [1400, 0.000088, 0.18398830],
    [1500, 0.000098, 0.18522057],
    [1522, 0.000100, 0.18549163]
]

df = pd.DataFrame(data, columns=['Step', 'Strain', 'Stress_GPa'])

print("=== FeAg3 Tensile Test Results ===")
print(df)
print(f"\nTotal data points: {len(df)}")

# Save data
df.to_csv('results/stress_strain_data.csv', index=False)
print("Data saved to: results/stress_strain_data.csv")

# Create plot
plt.figure(figsize=(10, 6))
plt.plot(df['Strain'] * 100, df['Stress_GPa'], 'b-o', linewidth=2, markersize=6)
plt.xlabel('Strain (%)')
plt.ylabel('Stress (GPa)')
plt.title('FeAg3 Stress-Strain Curve from Molecular Dynamics')
plt.grid(True, alpha=0.3)

# Calculate mechanical properties
youngs_modulus = np.polyfit(df['Strain'][:5] * 100, df['Stress_GPa'][:5], 1)[0]
max_stress = df['Stress_GPa'].max()
max_strain = df['Strain'].max() * 100

plt.text(0.02, 0.95, f'Young\'s Modulus: {youngs_modulus:.2f} GPa', 
        transform=plt.gca().transAxes, fontsize=12,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
plt.text(0.02, 0.85, f'Max Stress: {max_stress:.4f} GPa', 
        transform=plt.gca().transAxes, fontsize=12,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

plt.savefig('results/stress_strain_curve.png', dpi=300, bbox_inches='tight')
print("Plot saved to: results/stress_strain_curve.png")

print(f"\n=== Mechanical Properties ===")
print(f"Young's Modulus: {youngs_modulus:.2f} GPa")
print(f"Maximum Stress: {max_stress:.4f} GPa")
print(f"Maximum Strain: {max_strain:.4f} %")

plt.show()
