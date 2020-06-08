
DimensionFields = [
    'CensusTract', 'State', 'County'
]

TotalsFields = [
    'TotalPop', 'Men', 'Women', 'Citizen'
]

PercentageFields = [
    'Hispanic', 'White', 'Black', 'Native', 'Asian', 'Pacific'
]


StateDictStruct = {
    'Hispanic':0, 'White':0, 'Black':0, 'Native':0, 'Asian':0, 'Pacific':0, 'Men':0, 'Women':0, 'TotalPop': 0, 'Citizen':0
}

OutputFields = [
    'State', 'Hispanic', 'White', 'Black', 'Native', 'Asian', 'Pacific', 'Men', 'Women', 'TotalPop', 'Citizen'
]


StateDict = {}

TractDict = {}


AllUsedFields = DimensionFields + TotalsFields + PercentageFields

f = open('acs2015_census_tract_data.csv', 'r')

headers = []
line_count = 0
for line in f:
    line_dict = {}
    line_vals = line.split(',')
    SkipLine = False
    if line_count == 0:
        headers = line_vals

    else:

        cell_count = 0
        for cell in line_vals:
            header_field = headers[cell_count]

            if header_field in AllUsedFields and not SkipLine:
                if header_field in PercentageFields:
                    line_dict[header_field+'_total'] = int(float(cell) / 100.0 * line_dict['TotalPop'])
                elif header_field in TotalsFields:
                    line_dict[header_field] = int(cell)
                    if cell == '0' or len(cell) == 0:
                        SkipLine = True
                else:
                    line_dict[headers[cell_count]] = cell

            cell_count +=1


        if not SkipLine:
            Tract = line_dict['CensusTract']
            TractDict[Tract] = line_dict


    line_count +=1

for Tract in TractDict:
    TractData = TractDict[Tract]
    State = TractData['State']

    if State not in StateDict:
        StateDict[State] = StateDictStruct.copy()

    StateDict[State]['State'] = State

    for TotalField in TotalsFields:
        StateDict[State][TotalField] += TractData[TotalField]

    for PercentageField in PercentageFields:
        StateDict[State][PercentageField] += TractData[PercentageField+'_total']


o = open('StateCensusData.csv', 'w')
HeaderLines = ','.join([Field for Field in OutputFields])
o.write(HeaderLines)
o.write('\n')
for State in StateDict:
    StateData = StateDict[State]
    OutputValues = [str(StateData[Field]) for Field in OutputFields]
    OutputData = ','.join(OutputValues)
    o.write(OutputData)
    o.write('\n')

o.close()
