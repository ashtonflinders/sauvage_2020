#!/usr/bin/python3

import os
import numpy as np

from pyproj import Proj
from pyproj import transform
from scipy.interpolate import griddata

from radiolysis_model import *
from BST_categories import *
from sediment_parameters import *
from netcdf_api import *


""" Parameters """
# Input grid locations
input = './input'

# Set the depth resolution (binning) of the radiolytic H2 production calculation (meters)
zstep = 10 

# Output locations
output_dir = './output'
# Write output GMT netcdf4 grids
write_grd = True
# Write output numpy arrays
write_numpy = False


""" Load the preprocessed datasets """
# Load the bathymetry grid (GEBCO 2014);
depth = load_grid(os.path.join(input, 'depth.grd'))

# Load the porosity grid, and divide by 100 (Martin et al., 2015);
porosity = load_grid(os.path.join(input, 'porosity.grd')) / 100

# Load the sediment thickness composite grid (Whittaker et al., 2013; Laske and Masters 1997);
sedthickness = load_grid(os.path.join(input, 'sediment_thickness.grd'))

# Load the seafloor bottom sediment type (BST) grid (NAVO 2003) and create a simplify;
lithology_file = os.path.join(input, 'sediment_type.grd')
lith, lat, lon = BST_array(lithology_file)

""" Create the input parameter grids for the radiolytic production calculation """
U, Th, K, RHO, H2_ALPHA, H2_BETA, H2_GAMMA = sediment_parameters(lith)


""" Calculate depth integrated radiolytic H2 production at each location """
# Initialize H2_PRODUCTION grid
H2_PRODUCTION = np.copy(U)
H2_PRODUCTION[:] = np.nan


# Loop over each location coordinate
for x in range(0, U.shape[0]):
	print( str(x) + '/' + str(U.shape[0]))
	for y in range(0, U.shape[1]):
		
		# NaN check - if any of the input values are NaN (e.g. land), don't do the calculation
		nan_check = [U[x,y], sedthickness[x,y], depth[x,y], porosity[x,y]]
		if np.isnan(nan_check).any():
			continue

        # Calculate H2 production in zstep-sized sediment depth column bins
		H2_PRODUCTION_at_xy = 0
		for z in np.arange(zstep, int(sedthickness[x,y]), zstep):
		    # Calculate the sediment-column depth and ocean dependent dependent porosity 
			Phi = calculate_Phi_at_z(porosity[x,y], z, depth[x,y])
			# If the porosity is < 0.1% halt the depth integration
			if Phi < .001:
				break

            # Output of calculate_production is in (mol H2 / yr / cm3)
			H2_PRODUCTION_over_zstep = calculate_production(U[x,y], Th[x,y], K[x,y], \
			    H2_ALPHA[x,y], H2_GAMMA[x,y], H2_BETA[x,y], RHO[x,y], Phi)
			    
			# Convert to mol H2 / yr / m3; (100 cm / 1 m)**3
			H2_PRODUCTION_over_zstep = H2_PRODUCTION_over_zstep * (100**3)
			                
            # Integrate over zstep/depth-bin size; * zstep
			H2_PRODUCTION_over_zstep = H2_PRODUCTION_over_zstep * zstep    
			   
			# Add to the running location specific depth integration
			H2_PRODUCTION_at_xy = H2_PRODUCTION_at_xy + H2_PRODUCTION_over_zstep

        # Insert into global array (units of mol H2 / yr / m2)
		H2_PRODUCTION[x,y] = H2_PRODUCTION_at_xy


""" Integrate the global calculation """
# We will reproject the data to the 5 arc-minute data onto a cartesian grid
sourceProj = Proj("+proj=latlong +ellps=WGS84 +datum=WGS84")
# We will use a Lambert Azimuthal Equal Area projection
targetProj = Proj("+proj=laea +lat_0=0 +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +units=km +no_defs")

# Grid data so we have coordinate pairs
LON_grid, LAT_grid = np.meshgrid(lon, lat)
# Project locations of the original 5 arc-minute grid in LAEA projection coordinates
LAEAx, LAEAy = transform(sourceProj, targetProj, LON_grid, LAT_grid)

# Replace infinites with NaNs
LAEAx[LAEAx == np.inf] = np.nan
LAEAy[LAEAy == np.inf] = np.nan

# Reshape our grid back into a 1 x N array
LAEAx_reshaped = np.reshape(LAEAx, (LAEAx.shape[0] * LAEAx.shape[1]))
LAEAy_reshaped = np.reshape(LAEAy, (LAEAy.shape[0] * LAEAy.shape[1]))
H2_PRODUCTION_reshaped = np.reshape(H2_PRODUCTION,(LAEAy.shape[0] * LAEAy.shape[1]))

# Find values in the reshaped input data array and remove them
H2_PRODUCTION_notnan_i = ~np.isnan(H2_PRODUCTION_reshaped)
H2_PRODUCTION_reshaped = H2_PRODUCTION_reshaped[H2_PRODUCTION_notnan_i]
LAEAx_reshaped = LAEAx_reshaped[H2_PRODUCTION_notnan_i] 
LAEAy_reshaped = LAEAy_reshaped[H2_PRODUCTION_notnan_i]

# Find values in the reshaped and transformed input coordinate array and remove them
# *should just be two points at the poles...
coord_notnan_i = ~np.isnan(LAEAx_reshaped)
H2_PRODUCTION_reshaped = H2_PRODUCTION_reshaped[coord_notnan_i]
LAEAx_reshaped = LAEAx_reshaped[coord_notnan_i] 
LAEAy_reshaped = LAEAy_reshaped[coord_notnan_i]

# Supersample - the NAVO lithology grid extends from 70 N to 50 S. The maximum resolution 
# in the 5 arc-minute database is ~3.2 km (length of 5 arc-minutes at 70 N).
# We supersample the reprojected grid to this grid spacing to avoid possible aliasing.
xi = np.arange(int(np.nanmin(LAEAx_reshaped)), int(np.nanmax(LAEAx_reshaped)), 3.2)
yi = np.arange(int(np.nanmin(LAEAy_reshaped)), int(np.nanmax(LAEAy_reshaped)), 3.2)
xi, yi = np.meshgrid(xi, yi)

# Create a list of the new coordinate points
points=np.column_stack((LAEAx_reshaped, LAEAy_reshaped))
# Regrid the data onto the new LAEA projection using a 2D cubic spline
resampled_values = griddata(points, H2_PRODUCTION_reshaped, (xi, yi), method = 'cubic')

# Calculate the cell size in meters
cell_size=(xi[0][1]-xi[0][0])*(yi[1][0]-yi[0][0]) * (1000**2)

# Calculate the total integrated global radiolytic H2 production (mol H2 / yr)
integrated_global_H2 = np.nansum(resampled_values) * cell_size

# Calculate it in electron equivalents (mol e-eq / yr)
integrated_global_H2_electron_eq = integrated_global_H2 * 2
print('Global production rate of radiolytic H2 and radiolytic oxidant (marine sediment):', \
    integrated_global_H2_electron_eq, 'mol electron equivalents per year (mol e-eq / yr)')


if write_grd:
    write_netcdf(lon, lat, U, output_dir + '/U.grd', 'ppm')
    write_netcdf(lon, lat, Th, output_dir + '/Th.grd', 'ppm')
    write_netcdf(lon, lat, K, output_dir + '/K.grd', 'ppm')
    write_netcdf(lon, lat, H2_ALPHA, output_dir + '/H2_alpha.grd', 'Molecules H2 MeV**(-1)')
    write_netcdf(lon, lat, H2_GAMMA, output_dir + '/H2_gamma.grd', 'Molecules H2 MeV**(-1)')
    write_netcdf(lon, lat, H2_BETA, output_dir + '/H2_beta.grd', 'Molecules H2 MeV**(-1)')
    write_netcdf(lon, lat, RHO, output_dir + '/density.grd', 'Molecules H2 MeV**(-1)')
    write_netcdf(lon, lat, lith, output_dir + '/lithology.grd', 'Molecules H2 MeV**(-1)')
    write_netcdf(lon, lat, H2_PRODUCTION, output_dir + '/H2_production.grd', 'mol H2/yr/m2')
    
if write_numpy:
    np.save(output_dir + '/U', U)
    np.save(output_dir + '/Th', Th)
    np.save(output_dir + '/K', K)
    np.save(output_dir + '/H2_alpha',H2_ALPHA)
    np.save(output_dir + '/H2_gamma', H2_GAMMA)
    np.save(output_dir + '/H2_beta', H2_BETA)
    np.save(output_dir + '/Grain_RHO', RHO)
    np.save(output_dir + '/lithology', lith)
    np.save(output_dir + '/lats', lat)
    np.save(output_dir + '/lons', lon)
    np.save(output_dir + '/H2_production', np.asarray(H2_PRODUCTION))





