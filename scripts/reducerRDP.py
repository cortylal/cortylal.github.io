# import necessary modules
import pandas as pd
from shapely.geometry import LineString

df = pd.read_csv('geocoded_openpaths_data.csv')
coordinates = df.as_matrix(columns=['lat', 'lon'])

# create a shapely line from the point data
line = LineString(coordinates)

# all points in the simplified object will be within the tolerance distance of the original geometry
tolerance = 0.015

# if preserve topology is set to False the much quicker Douglas-Peucker algorithm is used
# we don't need to preserve topology bc we just need a set of points, not the relationship between them
simplified_line = line.simplify(tolerance, preserve_topology=False)

# save the simplified set of coordinates as a new dataframe
lon = pd.Series(pd.Series(simplified_line.coords.xy)[1])
lat = pd.Series(pd.Series(simplified_line.coords.xy)[0])
si = pd.DataFrame({'lon':lon, 'lat':lat})

# df_index will contain the index of the matching row from the original full data set
si['df_index'] = None

# for each coordinate pair in the simplified set
for si_i, si_row in si.iterrows():
    
    si_coords = (si_row['lat'], si_row['lon'])
    # for each coordinate pair in the original full data set
    for df_i, df_row in df.iterrows():
        
        # compare tuples of coordinates, if the points match, save this row's index as the matching one
        if si_coords == (df_row['lat'], df_row['lon']):
            si.loc[si_i, 'df_index'] = df_i
            break

# select the rows from the original full data set whose indices appear in the df_index
# column of the simplified data set
rs = df.ix[si['df_index'].dropna()]

rs.to_csv('reduced_geocoded_openpaths_data.csv', index=False)