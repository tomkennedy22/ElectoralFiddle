
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

Headers = []
LineCount = 0
for line in f:
    LineDict = {}
    LineVals = line.split(',')
    SkipLine = False
    if LineCount == 0:
        Headers = LineVals

    else:

        CellCount = 0
        for Cell in LineVals:
            HeaderField = Headers[CellCount]

            if HeaderField in AllUsedFields and not SkipLine:
                if HeaderField in PercentageFields:
                    LineDict[HeaderField+'_total'] = int(float(Cell) / 100.0 * LineDict['TotalPop'])
                elif HeaderField in TotalsFields:
                    LineDict[HeaderField] = int(Cell)
                    if Cell == '0' or len(Cell) == 0:
                        SkipLine = True
                else:
                    LineDict[Headers[CellCount]] = Cell

            CellCount +=1


        if not SkipLine:
            Tract = LineDict['CensusTract']
            TractDict[Tract] = LineDict


    LineCount +=1

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
