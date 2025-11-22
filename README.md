Machine Learning–Guided Prediction of Mechanical Properties of Fe–Ag₃ Alloy

Molecular Dynamics + ML Hybrid Approach

1. Project Overview

This project presents a hybrid computational framework that combines Molecular Dynamics (MD) simulations and Machine Learning (ML) techniques to accurately predict the mechanical properties of Fe–Ag₃ alloy, including:

Young’s Modulus

Ultimate Tensile Strength (UTS)

Maximum Strain

MD simulations provide atomistic deformation data but are computationally expensive when analyzing multiple scenarios. To overcome this, MD-generated stress–strain curves are used to train ML models, enabling fast and scalable prediction of material properties.

2. Objectives

Extract mechanical properties from MD-based stress–strain data

Train supervised ML models to predict these properties

Compare model performance and identify the best regression model

Reduce computational complexity and enable quick alloy evaluations

3. Methodology Workflow
[Molecular Dynamics Simulation (LAMMPS)]
          ↓
[Stress–Strain Curve Extraction]
          ↓
[Preprocessing & Feature Engineering]
          ↓
[ML Model Training and Prediction]


ML Models Evaluated:

Model	Performance Summary
Random Forest Regressor	Best accuracy (selected)
Gradient Boosting Regressor	Good, needs fine-tuning
Support Vector Machine (SVM)	Moderate performance
4. Folder Structure
FeAg3_Alloy_Project/
│── 01_References/           
│── 02_ML_Model/             
│── 03_MD_Simulation/       
│   ├── data/               
│   ├── inputs/              
│   └── potentials/         
│── 04_Results/              
│   ├── graphs/              
│   └── visualization_scripts/  
│── 05_Report/              
│   ├── mlmi_report.pdf
│   └── mlmi_report.docx
│── MLMI.pptx               
│── README.md               

5. How to Run the Project
Run ML Training
python 02_ML_Model/prepare_ml_data.py

Run Tensile Simulation (LAMMPS)
lammps < 03_MD_Simulation/inputs/05_tensile_test.in

Plot Stress–Strain Graphs
python 04_Results/visualization_scripts/plot_stress_strain.py

6. Key Outcomes

Random Forest achieved the best prediction performance (highest R² value, lowest error).

ML effectively captured nonlinear brittle deformation behavior.

The framework significantly reduces the computational load required for MD simulations.

Can be extended to other alloys and different mechanical conditions.

7. Future Scope

Expand to multi-component alloys (e.g., Fe–Ag–Ni, Fe–Ag–Al)

Integrate temperature and strain-rate dependence

Deploy as a lightweight material property prediction tool

8. Team Members
Name	Roll Number
N. Shivakumar	22CSB0C26
M. Arunkumar	22CSB0C28
9. References

All technical references are documented in the full report (05_Report/mlmi_report.pdf).

Core study based on MD data generated using LAMMPS and ML implementation using Scikit-Learn.

10. Conclusion

This project successfully demonstrates the potential of Machine Learning in accelerating materials research. By integrating ML with atomistic simulations, material property prediction becomes faster, scalable, and more efficient. The developed pipeline can support future material selection and design with reduced dependency on high-cost simulations.
