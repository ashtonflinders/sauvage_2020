import numpy as np
from netCDF4 import Dataset

def load_grid(filename, keep_mask = False):
	grid = Dataset(filename, mode = 'r')
	values = grid.variables['z'][:]
	grid.close()
	if keep_mask:
		return values
	else:
		return values.data


def write_netcdf(x, y, data, filename, units = ''):
	nc_file = Dataset(filename, 'w', format = 'NETCDF4')
	nc_file.node_offset = 0
	nc_file.institution = 'Ashton Flinders, USGS, HVO, aflinders@usgs.gov'
	nc_file.units = units
	
	# dimensions
	nc_file.createDimension('x', len(x))
	nc_file.createDimension('y', len(y))

	# variables
	longitudes = nc_file.createVariable('x', 'd', ('x',), zlib=True)
	longitudes.long_name = "x"
	latitudes = nc_file.createVariable('y', 'd', ('y',), zlib=True)
	latitudes.long_name = "y"

	output = nc_file.createVariable('z', 'd', ('y', 'x',), fill_value = 'NaN', zlib=True)

	latitudes[:] = y
	longitudes[:] = x
	output[:,:] = data
	output.actual_range = np.array((np.nanmin(data), np.nanmax(data)))
	nc_file.close()