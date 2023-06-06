import pandas as pd
import numpy as np
import data


# -----------------------------------------------------------------------------------
'''
CALCULATION FOR GRIDZONE / DENSITY HEATMAPS
'''
# @Deprecated: this is being handled in data_processing under tools now.
# Description: Function to filter the location data 
#              for both the gridzone and density
#              heatmap
def zones_calculation(data):
    baseball = data.copy()

    # initialize a field for location where ball is hit
    baseball['Location_Side'] = ''
    baseball['Location_Height'] = ''

    # array to hold values for the side 
    location_side = []
    for idx, val in baseball.iterrows():
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
    for idx, val in baseball.iterrows():
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
    baseball['Location_Side'] = location_side
    baseball['Location_Height'] = location_height

    return baseball

# -----------------------------------------------------------------------------------
'''
WOBA CALCULATIONS
'''
def wobaYearWeight(year):
  if year == '2017':
    return (0.721409, 0.75488, 0.933841, 1.39309, 1.84695, 2.18011)

  elif year == '2018':
    return (0.729725, 0.758507, 0.941035, 1.41412, 1.82053, 2.19929)

  elif year == '2019':
    return (0.739806, 0.767695, 0.941771, 1.38062, 1.79559, 2.14158)

  elif year == '2020':
    return (0.756437, 0.781897, 0.955415, 1.39774, 1.81123, 2.1401)

  elif year == '2021':
    return (0.73817, 0.767148, 0.932931, 1.34641, 1.74889, 2.09657)
  # for any year beyond not marked, use 2022 values as default
  else:
    return (0.738822, 0.765579, 0.92845, 1.34266, 1.71558, 2.0296)

def wobaYearWeightList(year):
  if year == "2017":
    return [0.721409, 0.75488, 0.933841, 1.39309, 1.84695, 2.18011]

  elif year == "2018":
    return [0.729725, 0.758507, 0.941035, 1.41412, 1.82053, 2.19929]

  elif year == "2019":
    return [0.739806, 0.767695, 0.941771, 1.38062, 1.79559, 2.14158]

  elif year == "2020":
    return [0.756437, 0.781897, 0.955415, 1.39774, 1.81123, 2.1401]

  elif year == "2021":
    return [0.73817, 0.767148, 0.932931, 1.34641, 1.74889, 2.09657]
  # for any year beyond not marked, use 2022 values as default
  else:
    return [0.738822, 0.765579, 0.92845, 1.34266, 1.71558, 2.0296]

def wOBACalc(bbFile, playerName, year = "2022", ubbFact = .738822, hbpFact = .765579, oneBFact = .92845, twoBFact = 1.34266, 
             threeBFact = 1.71558, hrFact = 2.0296):
    
    # bbFile = file

    player = bbFile.loc[bbFile['Pitcher'] == playerName]

    ubbFact, hbpFact, oneBFact, twoBFact, threeBFact, hrFact = wobaYearWeight(year)

    single = player.loc[player['PlayResult'] == 'Single']
    double = player.loc[player['PlayResult'] == 'Double']
    triple = player.loc[player['PlayResult'] == 'Triple']
    homerun = player.loc[player['PlayResult'] == 'HomeRun']
    hitbypitch = player.loc[player['PitchCall'] == 'HitByPitch']

    intentionalWalk = player.loc[player[ 'PitchCall'] == 'BallIntentional']
    unintentionalWalk = player.loc[player['KorBB'] == 'Walk']

    #Throw out undefined in playresult and add in results from korbb
    kbb = player.loc[player['KorBB'] != 'Undefined']
    play = player.loc[player['PlayResult'] != 'Undefined']

    sacrifice = player.loc[player['PlayResult'] == 'Sacrifice']

    sacrificefly = sacrifice.loc[sacrifice['TaggedHitType'] == 'FlyBall']
    sacrificehit = sacrifice.loc[sacrifice['TaggedHitType'] == 'Bunt']

    oneB = len(single)
    twoB = len(double)
    threeB = len(triple)
    hr = len(homerun)
    hbp = len(hitbypitch)
    ubb = len(unintentionalWalk) - len(intentionalWalk)
    ab = len(play) + len(kbb)
    sf = len(sacrificefly)
    sh = len(sacrificehit)


    if (((ab - sh) + ubb + sf + hbp) == 0):
        return 'UNDEFINED - DIVIDED BY ZERO'
    
    playerWOBA = (ubbFact * ubb + hbpFact * hbp + oneBFact * oneB + twoBFact * twoB + threeBFact * threeB + hrFact * hr) / ((ab - sh) + ubb + sf + hbp)
    
    return playerWOBA

# enable using custom values, note the year is being handled in callback/layout, and requires entering "None" or "none" in the ids.INPUT_WOBA_YEAR
def wOBACalcCustom(bbFile, playerName, ubbFact = .738822, hbpFact = .765579, oneBFact = .92845, twoBFact = 1.34266, 
             threeBFact = 1.71558, hrFact = 2.0296):
    
    # bbFile = file

    player = bbFile.loc[bbFile['Pitcher'] == playerName]

    single = player.loc[player['PlayResult'] == 'Single']
    double = player.loc[player['PlayResult'] == 'Double']
    triple = player.loc[player['PlayResult'] == 'Triple']
    homerun = player.loc[player['PlayResult'] == 'HomeRun']
    hitbypitch = player.loc[player['PitchCall'] == 'HitByPitch']

    intentionalWalk = player.loc[player[ 'PitchCall'] == 'BallIntentional']
    unintentionalWalk = player.loc[player['KorBB'] == 'Walk']

    #Throw out undefined in playresult and add in results from korbb
    kbb = player.loc[player['KorBB'] != 'Undefined']
    play = player.loc[player['PlayResult'] != 'Undefined']

    sacrifice = player.loc[player['PlayResult'] == 'Sacrifice']

    sacrificefly = sacrifice.loc[sacrifice['TaggedHitType'] == 'FlyBall']
    sacrificehit = sacrifice.loc[sacrifice['TaggedHitType'] == 'Bunt']

    oneB = len(single)
    twoB = len(double)
    threeB = len(triple)
    hr = len(homerun)
    hbp = len(hitbypitch)
    ubb = len(unintentionalWalk) - len(intentionalWalk)
    ab = len(play) + len(kbb)
    sf = len(sacrificefly)
    sh = len(sacrificehit)


    if (((ab - sh) + ubb + sf + hbp) == 0):
        return 'UNDEFINED - DIVIDED BY ZERO'
    
    playerWOBA = (ubbFact * ubb + hbpFact * hbp + oneBFact * oneB + twoBFact * twoB + threeBFact * threeB + hrFact * hr) / ((ab - sh) + ubb + sf + hbp)
    
    return playerWOBA

# FASTER!!!
# first defines a dictionary that maps event types to their corresponding factors, and then uses groupby and agg to count the occurrences of each event type. 
# Then calculates the various components of wOBA using the aggregated event counts, and returns the final wOBA value.
def wOBACalcCustom_v3(bbFile, playerName, ubbFact=0.738822, hbpFact=0.765579, oneBFact=0.92845, twoBFact=1.34266, 
                      threeBFact=1.71558, hrFact=2.0296):
    
    player = bbFile.loc[bbFile['Pitcher'] == playerName]
    
    single = (player['PlayResult'] == 'Single').sum()
    double = (player['PlayResult'] == 'Double').sum()
    triple = (player['PlayResult'] == 'Triple').sum()
    homerun = (player['PlayResult'] == 'HomeRun').sum()
    hitbypitch = (player['PitchCall'] == 'HitByPitch').sum()

    intentionalWalk = (player['PitchCall'] == 'BallIntentional').sum()
    unintentionalWalk = (player['KorBB'] == 'Walk').sum()

    kbb = (player['KorBB'] != 'Undefined').sum()
    play = (player['PlayResult'] != 'Undefined').sum()

    sacrifice = player.loc[player['PlayResult'] == 'Sacrifice']

    sacrificefly = (sacrifice['TaggedHitType'] == 'FlyBall').sum()
    sacrificehit = (sacrifice['TaggedHitType'] == 'Bunt').sum()

    oneB = single
    twoB = double
    threeB = triple
    hr = homerun
    hbp = hitbypitch
    ubb = unintentionalWalk - intentionalWalk
    ab = play + kbb
    sf = sacrificefly
    sh = sacrificehit

    if (ab - sh + ubb + sf + hbp) == 0:
        return 'UNDEFINED - DIVIDED BY ZERO'
    
    playerWOBA = (ubbFact * ubb + hbpFact * hbp + oneBFact * oneB + twoBFact * twoB + threeBFact * threeB + hrFact * hr) / (ab - sh + ubb + sf + hbp)
    
    return playerWOBA


def addWOBA(inFile):
    # FIXME: Temporary fix
    import warnings
    warnings.filterwarnings("ignore")

    # creating copy of original dataframe to be returned
    # inFile = df.copy() # don't do this, copying is slow and memory intensive!
    # limit values to only include baylor players

    # each unique attribute
    playerName = inFile["Pitcher"].unique() # use dynamically generated list!!! Do NOT hard code here!
    
    graphWoba = pd.DataFrame(columns = ['Name', 'RelSpeed',
                                        'VertRelAngle','HorzRelAngle','SpinRate',
                                        'SpinAxis', 'RelHeight','RelSide','Extension',
                                        'HorzBreak', 'PlateLocHeight', 'PlateLocSide',
                                        'ZoneSpeed','VertApprAngle','HorzApprAngle',
                                        'ZoneTime','EffectiveVelo','SpeedDrop', 
                                        'BatterSide', 'TaggedPitchType', 'Datetime', 
                                        'wOBA', 'atBats', 'hitByPitch'])
    # iteration through the players
    for i in playerName:
        # woba calculation of each player
        woba = wOBACalc(inFile, i, '2022') # FIXME: why is this 2022 hard coded? shouldn't this be whatever the current year is?
        player = inFile.loc[inFile['Pitcher'] == i]
        
        # mean calculation of attributes
        relSpeed = player["RelSpeed"].mean()
        vertAngle = player["VertRelAngle"].mean()
        horzAngle = player["HorzRelAngle"].mean()
        spinRate = player["SpinRate"].mean()
        spinAxis = player["SpinAxis"].mean()
        relHeight = player["RelHeight"].mean()
        relSide = player["RelSide"].mean()
        ext = player["Extension"].mean()
        horzBreak = player["HorzBreak"].mean()
        plateHeight = player["PlateLocHeight"].mean()
        plateSide = player["PlateLocSide"].mean()
        zoneSpeed = player["ZoneSpeed"].mean()
        vertAngle = player["VertApprAngle"].mean()
        horzAngle = player["HorzApprAngle"].mean()
        zoneTime = player["ZoneTime"].mean()
        effectVelo = player["EffectiveVelo"].mean()
        speedDrop = player["SpeedDrop"].mean()
        
        new_row = {'Name':i, 'RelSpeed':relSpeed, 
                    'VertRelAngle':vertAngle,'HorzRelAngle':horzAngle,
                    'SpinRate':spinRate,'SpinAxis':spinAxis, 'RelHeight':relHeight,
                    'RelSide':relSide,'Extension':ext, 'HorzBreak':horzBreak, 
                    'PlateLocHeight':plateHeight, 'PlateLocSide':plateSide ,
                    'ZoneSpeed':zoneSpeed, 'VertApprAngle':vertAngle, 
                    'HorzApprAngle':horzAngle, 'ZoneTime':zoneTime,
                    'EffectiveVelo':effectVelo, 'SpeedDrop':speedDrop, 
                    'wOBA':woba}

        graphWoba = graphWoba.append(new_row, ignore_index=True)
    return graphWoba

# newer woba calc that can actually use custom values
def addWOBACustom(inFile, ubb_num, hbp_num, oneB_num, twoB_num, threeB_num, hr_num):
    # FIXME: Temporary fix
    import warnings
    warnings.filterwarnings("ignore")

    # creating copy of original dataframe to be returned
    # inFile = df.copy() # don't do this, copying is slow and memory intensive!
    # limit values to only include baylor players

    # each unique attribute
    playerName = inFile["Pitcher"].unique() # use dynamically generated list!!! Do NOT hard code here!
    
    graphWoba = pd.DataFrame(columns = ['Name', 'RelSpeed',
                                        'VertRelAngle','HorzRelAngle','SpinRate',
                                        'SpinAxis', 'RelHeight','RelSide','Extension',
                                        'HorzBreak', 'PlateLocHeight', 'PlateLocSide',
                                        'ZoneSpeed','VertApprAngle','HorzApprAngle',
                                        'ZoneTime','EffectiveVelo','SpeedDrop', 
                                        'BatterSide', 'TaggedPitchType', 'Datetime', 
                                        'wOBA', 'atBats', 'hitByPitch'])
    # iteration through the players
    for i in playerName:
        # woba calculation of each player
        woba = wOBACalcCustom(inFile, i, ubb_num, hbp_num, oneB_num, twoB_num, threeB_num, hr_num) # year is being handled in callback from defaults
        player = inFile.loc[inFile['Pitcher'] == i]
        
        # mean calculation of attributes
        relSpeed = player["RelSpeed"].mean()
        vertAngle = player["VertRelAngle"].mean()
        horzAngle = player["HorzRelAngle"].mean()
        spinRate = player["SpinRate"].mean()
        spinAxis = player["SpinAxis"].mean()
        relHeight = player["RelHeight"].mean()
        relSide = player["RelSide"].mean()
        ext = player["Extension"].mean()
        horzBreak = player["HorzBreak"].mean()
        plateHeight = player["PlateLocHeight"].mean()
        plateSide = player["PlateLocSide"].mean()
        zoneSpeed = player["ZoneSpeed"].mean()
        vertAngle = player["VertApprAngle"].mean()
        horzAngle = player["HorzApprAngle"].mean()
        zoneTime = player["ZoneTime"].mean()
        effectVelo = player["EffectiveVelo"].mean()
        speedDrop = player["SpeedDrop"].mean()
        
        new_row = {'Name':i, 'RelSpeed':relSpeed, 
                    'VertRelAngle':vertAngle,'HorzRelAngle':horzAngle,
                    'SpinRate':spinRate,'SpinAxis':spinAxis, 'RelHeight':relHeight,
                    'RelSide':relSide,'Extension':ext, 'HorzBreak':horzBreak, 
                    'PlateLocHeight':plateHeight, 'PlateLocSide':plateSide ,
                    'ZoneSpeed':zoneSpeed, 'VertApprAngle':vertAngle, 
                    'HorzApprAngle':horzAngle, 'ZoneTime':zoneTime,
                    'EffectiveVelo':effectVelo, 'SpeedDrop':speedDrop, 
                    'wOBA':woba}

        graphWoba = graphWoba.append(new_row, ignore_index=True)
    return graphWoba

def addWOBACustomFast(inFile, ubb_num, hbp_num, oneB_num, twoB_num, threeB_num, hr_num):
    # FIXME: Temporary fix
    import warnings
    warnings.filterwarnings("ignore")

    # creating copy of original dataframe to be returned
    # inFile = df.copy() # don't do this, copying is slow and memory intensive!
    # limit values to only include baylor players

    # each unique attribute
    playerName = inFile["Pitcher"].unique() # use dynamically generated list!!! Do NOT hard code here!
    
    graphWoba = pd.DataFrame(columns = ['Name', 'RelSpeed',
                                        'VertRelAngle','HorzRelAngle','SpinRate',
                                        'SpinAxis', 'RelHeight','RelSide','Extension',
                                        'HorzBreak', 'PlateLocHeight', 'PlateLocSide',
                                        'ZoneSpeed','VertApprAngle','HorzApprAngle',
                                        'ZoneTime','EffectiveVelo','SpeedDrop', 
                                        'BatterSide', 'TaggedPitchType', 'Datetime', 
                                        'wOBA', 'atBats', 'hitByPitch'])
    # iteration through the players
    for i in playerName:
        # woba calculation of each player
        woba = wOBACalcCustom_v3(inFile, i, ubb_num, hbp_num, oneB_num, twoB_num, threeB_num, hr_num) # year is being handled in callback from defaults
        player = inFile.loc[inFile['Pitcher'] == i]
        
        # mean calculation of attributes
        relSpeed = player["RelSpeed"].mean()
        vertAngle = player["VertRelAngle"].mean()
        horzAngle = player["HorzRelAngle"].mean()
        spinRate = player["SpinRate"].mean()
        spinAxis = player["SpinAxis"].mean()
        relHeight = player["RelHeight"].mean()
        relSide = player["RelSide"].mean()
        ext = player["Extension"].mean()
        horzBreak = player["HorzBreak"].mean()
        plateHeight = player["PlateLocHeight"].mean()
        plateSide = player["PlateLocSide"].mean()
        zoneSpeed = player["ZoneSpeed"].mean()
        vertAngle = player["VertApprAngle"].mean()
        horzAngle = player["HorzApprAngle"].mean()
        zoneTime = player["ZoneTime"].mean()
        effectVelo = player["EffectiveVelo"].mean()
        speedDrop = player["SpeedDrop"].mean()
        
        new_row = {'Name':i, 'RelSpeed':relSpeed, 
                    'VertRelAngle':vertAngle,'HorzRelAngle':horzAngle,
                    'SpinRate':spinRate,'SpinAxis':spinAxis, 'RelHeight':relHeight,
                    'RelSide':relSide,'Extension':ext, 'HorzBreak':horzBreak, 
                    'PlateLocHeight':plateHeight, 'PlateLocSide':plateSide ,
                    'ZoneSpeed':zoneSpeed, 'VertApprAngle':vertAngle, 
                    'HorzApprAngle':horzAngle, 'ZoneTime':zoneTime,
                    'EffectiveVelo':effectVelo, 'SpeedDrop':speedDrop, 
                    'wOBA':woba}

        graphWoba = graphWoba.append(new_row, ignore_index=True)
    return graphWoba

# doesn't work!
def addWOBACustomFast_v2(inFile, ubb_num, hbp_num, oneB_num, twoB_num, threeB_num, hr_num):
    # FIXME: Temporary fix
    import warnings
    warnings.filterwarnings("ignore")

    # creating copy of original dataframe to be returned
    # inFile = df.copy() # don't do this, copying is slow and memory intensive!
    # limit values to only include baylor players

    # define custom function to calculate mean values and woba
    def calculate_stats(group):
        woba = wOBACalcCustom_v3(group, group.index[0], ubb_num, hbp_num, oneB_num, twoB_num, threeB_num, hr_num)
        stats = group[['RelSpeed', 'VertRelAngle', 'HorzRelAngle', 'SpinRate', 'SpinAxis', 'RelHeight', 'RelSide', 'Extension', 'HorzBreak', 'PlateLocHeight', 'PlateLocSide', 'ZoneSpeed', 'VertApprAngle', 'HorzApprAngle', 'ZoneTime', 'EffectiveVelo', 'SpeedDrop']].mean()
        stats['wOBA'] = woba
        stats['Name'] = group.index[0]
        return stats
    
    # group data by pitcher's name and apply custom function
    graphWoba = inFile.groupby('Pitcher').apply(calculate_stats).reset_index(drop=True)
    graphWoba = graphWoba[['Name', 'RelSpeed', 'VertRelAngle', 'HorzRelAngle', 'SpinRate', 'SpinAxis', 'RelHeight', 'RelSide', 'Extension', 'HorzBreak', 'PlateLocHeight', 'PlateLocSide', 'ZoneSpeed', 'VertApprAngle', 'HorzApprAngle', 'ZoneTime', 'EffectiveVelo', 'SpeedDrop', 'wOBA']]
    
    return graphWoba

def addWOBACustomFast_v3(inFile, ubb_num, hbp_num, oneB_num, twoB_num, threeB_num, hr_num):
    # FIXME: Temporary fix
    import warnings
    warnings.filterwarnings("ignore")

    # creating copy of original dataframe to be returned
    # inFile = df.copy() # don't do this, copying is slow and memory intensive!
    # limit values to only include baylor players

    # use dynamically generated list!!! Do NOT hard code here!
    playerName = inFile["Pitcher"].unique()

    # group the data by pitcher and apply a lambda function to calculate the wOBA and the average values
    graphWoba = inFile.groupby("Pitcher").apply(lambda group: pd.Series({
        "wOBA": wOBACalcCustom_v3(group, group.name, ubb_num, hbp_num, oneB_num, twoB_num, threeB_num, hr_num),
        "RelSpeed": group["RelSpeed"].mean(),
        "VertRelAngle": group["VertRelAngle"].mean(),
        "HorzRelAngle": group["HorzRelAngle"].mean(),
        "SpinRate": group["SpinRate"].mean(),
        "SpinAxis": group["SpinAxis"].mean(),
        "RelHeight": group["RelHeight"].mean(),
        "RelSide": group["RelSide"].mean(),
        "Extension": group["Extension"].mean(),
        "HorzBreak": group["HorzBreak"].mean(),
        "PlateLocHeight": group["PlateLocHeight"].mean(),
        "PlateLocSide": group["PlateLocSide"].mean(),
        "ZoneSpeed": group["ZoneSpeed"].mean(),
        "VertApprAngle": group["VertApprAngle"].mean(),
        "HorzApprAngle": group["HorzApprAngle"].mean(),
        "ZoneTime": group["ZoneTime"].mean(),
        "EffectiveVelo": group["EffectiveVelo"].mean(),
        "SpeedDrop": group["SpeedDrop"].mean()
    }))

    # reset the index to get the "Pitcher" column back
    graphWoba = graphWoba.reset_index()

    # remove rows with missing or undefined wOBA values
    graphWoba = graphWoba.dropna(subset=["wOBA"])
    graphWoba = graphWoba[graphWoba["wOBA"] != "UNDEFINED - DIVIDED BY ZERO"]
    graphWoba = graphWoba.rename(columns={"Pitcher" : "Name"})

    return graphWoba






