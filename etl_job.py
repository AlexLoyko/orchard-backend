import pandas as pd
from db import DBsession, Restaurant, Inspection
from utils import str_to_date, int_or_none, grade_or_none

# read csv file and retrieve all entries
dataframe = pd.read_csv('./DOHMH_New_York_City_Restaurant_Inspection_Results.csv')
entries = dataframe.iloc[:,:].values

session = DBsession()
rest_ids = set()

# for each row in csv
for i in range(0, entries.shape[0]):
    current_rest = []
    current_insp = []
    is_new_rest = False

    # for each column of a csv row
    for j in range(0, entries.shape[1]):
        field = entries[i][j]

        # if current field is CAMIS ID
        if j == 0:
            if not field in rest_ids:
                rest_ids.add(field)
                is_new_rest = True
            current_insp.append(field)

        if j <= 7 and is_new_rest:
            current_rest.append(field)
        elif j > 7:
            current_insp.append(field)

    if len(current_rest) > 0:
        session.add(                                 \
            Restaurant(                              \
                id=int(current_rest[0]),             \
                name=current_rest[1],                \
                boro=current_rest[2],                \
                building=current_rest[3],            \
                street=current_rest[4],              \
                zip=int_or_none(current_rest[5]),    \
                phone=current_rest[6],               \
                cuisine=current_rest[7],             \
            )                                        \
        )

    session.add(                                                \
        Inspection(                                             \
            rest_id=int(current_insp[0]),                       \
            inspection_date=str_to_date(current_insp[1]),       \
            action=current_insp[2],                             \
            violation_code=current_insp[3],                     \
            violation_desc=current_insp[4],                     \
            is_critical=current_insp[5] == 'Critical',          \
            score=int_or_none(current_insp[6]),                 \
            grade=grade_or_none(current_insp[7]),               \
            grade_date=str_to_date(current_insp[8]),            \
            record_date=str_to_date(current_insp[9]),           \
            inspection_type=current_insp[10],                   \
        )                                                       \
    )

# commit changes to the database
session.commit()
session.close()
