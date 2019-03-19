# Tools for automated charge optimization for Molecular Dynamics Simulation

### Goal
SMAMP (synthetic mimics of antimicrobial peptides) can be used for antimicrobial coating in medical applications.
To understand a class of SMAMP, we simulate them via Molecular Dynamics (MD).
An essential component of MD are point-charges.
These are not available for the SMAMP molecules of interest, so we have to determine them ourselves.

### Methods
Multiple methods to determine point charges exists, e.g., Bader Charge Analysis, HORTON-style cost-function fitting and more.
Also, subvariants of these methods are of interest: diverse constraints, different algorithms and convergence parameters.

### Content
This package provides tools to make the charge optimization process easier.
They are used in a [seperate workflow management repo](https://github.com/lukaselflein/charge_optimization_folderstructure).
