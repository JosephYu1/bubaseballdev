# -----------------------------------------------------------------------------------
'''
CALCULATION FOR GRIDZONE / DENSITY HEATMAPS
'''

# Description: Function to filter the location data 
#              for both the gridzone and density
#              heatmap
def zones_calculation(df):

    # array to hold values for the side 
    location_side = []
    for idx, val in df.iterrows():
        # middle range
        if (val['PlateLocSide'] >= -0.5 and val['PlateLocSide'] <= 0.5):
            location_side.append('Middle')
        # left range
        elif (val['PlateLocSide'] < -0.5 and val['PlateLocSide'] >= -1.0):
            location_side.append('Left')
        # right range
        elif (val['PlateLocSide'] > 0.5 and val['PlateLocSide'] <= 1.0):
            location_side.append('Right')
        # outside box ranges
        elif (val['PlateLocSide'] < 1.0):
            location_side.append('Outside left')
        elif (val['PlateLocSide'] > 1.0):
            location_side.append('Outside right')
        else:
            location_side.append('')

    # array to hold values for the height
    location_height = []
    for idx, val in df.iterrows():
        # middle range
        if (val['PlateLocHeight'] >= 1.4 and val['PlateLocHeight'] <= 2.7):
            location_height.append('Middle')
        # upper range
        elif (val['PlateLocHeight'] > 2.7 and val['PlateLocHeight'] <= 4.0):
            location_height.append('Upper')
        # lower range
        elif (val['PlateLocHeight'] < 1.4 and val['PlateLocHeight'] >= 0.0):
            location_height.append('Lower')
        # outside box ranges
        elif (val['PlateLocHeight'] > 4.0):
            location_height.append('Outside upper')
        elif (val['PlateLocHeight'] < 0.0):
            location_height.append('Outside lower')
        else:
            location_height.append('')

    # annex each of the locations to the dataset
    df['Location_Side'] = location_side
    df['Location_Height'] = location_height

    return df