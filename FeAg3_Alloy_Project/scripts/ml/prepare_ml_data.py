import pandas as pd
import numpy as np

# Load our stress-strain data
df = pd.read_csv('results/stress_strain_data.csv')

print("=== FeAg3 Data for Machine Learning ===")
print(f"Dataset shape: {df.shape}")
print("\nFirst few rows:")
print(df.head())

# Calculate additional features for ML
youngs_modulus = 1.23  # GPa from our calculation
yield_strength = df['Stress_GPa'].max() * 0.9  # Approximate yield strength
ultimate_strength = df['Stress_GPa'].max()

# Create ML-ready dataset
ml_data = pd.DataFrame({
    'composition_Fe': [0.25],  # FeAg3 = 1 Fe : 3 Ag
    'composition_Ag': [0.75],
    'temperature_K': [300],    # Simulation temperature
    'strain_rate': [0.0001],   # Simulation strain rate
    'lattice_parameter_a': [5.77704618],
    'lattice_parameter_c': [4.63966600],
    'volume': [134.10007696],
    'youngs_modulus': [youngs_modulus],
    'yield_strength': [yield_strength],
    'ultimate_strength': [ultimate_strength],
    'max_strain': [df['Strain'].max()]
})

print(f"\n=== ML Training Data ===")
print(ml_data)

# Save for ML training
ml_data.to_csv('data/processed/ml_training_data.csv', index=False)
print(f"\nML data saved to: data/processed/ml_training_data.csv")

print(f"\n=== Next Steps for ML ===")
print("1. Generate more data with varying parameters")
print("2. Add features (temperature, strain rate, composition)")
print("3. Train regression models (Random Forest, Neural Networks)")
print("4. Predict mechanical properties from structure")
