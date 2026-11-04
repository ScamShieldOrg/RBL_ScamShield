import openpyxl
from openpyxl.cell.cell import MergedCell
from datetime import datetime

file_path = 'C:/Users/USER/Downloads/Report5_UnitTest.xlsx'
wb = openpyxl.load_workbook(file_path)
s3 = wb['Function3']

# Clear rows 37 to 44 columns A to Z completely first
for r in range(37, 46):
    for c in range(1, 35):
        cell = s3.cell(r, c)
        if not isinstance(cell, MergedCell):
            cell.value = None

# Row 36: Exception header
s3.cell(36, 2, 'Exception')

# Rows 37 - 40: Exceptions list (Column D)
s3.cell(37, 4, 'BadRequestException (400 Bad Request)')
s3.cell(38, 4, 'ResourceNotFoundException (404 Not Found)')
s3.cell(39, 4, 'AccessDeniedException (403 Forbidden)')
s3.cell(40, 4, 'AuthenticationException (401 Unauthorized)')

# Row 41: Result Type
s3.cell(41, 1, 'Result')
s3.cell(41, 2, 'Type(N : Normal, A : Abnormal, B : Boundary)')

# Row 42: Passed/Failed
s3.cell(42, 2, 'Passed/Failed')

# Row 43: Executed Date
s3.cell(43, 2, 'Executed Date')

# Row 44: Defect ID
s3.cell(44, 2, 'Defect ID')

# 18 Test Cases mapping (Cols F=6 to W=23)
test_cases = [
    # UTCID01: Approve report with valid reason & category
    {'id': 'UTCID01', 'type': 'N', 'pre': [11, 12], 'in': [15], 'ret': [32], 'ex': []},
    # UTCID02: Reject report with valid reason
    {'id': 'UTCID02', 'type': 'N', 'pre': [11, 12], 'in': [16], 'ret': [33], 'ex': []},
    # UTCID03: Approve report with reason exact 20 chars
    {'id': 'UTCID03', 'type': 'B', 'pre': [11, 12], 'in': [17], 'ret': [32], 'ex': []},
    # UTCID04: Decision with reason too short (< 20 chars)
    {'id': 'UTCID04', 'type': 'B', 'pre': [11, 12], 'in': [18], 'ret': [], 'ex': [37]},
    # UTCID05: Decision with reason null / blank
    {'id': 'UTCID05', 'type': 'A', 'pre': [11, 12], 'in': [19], 'ret': [], 'ex': [37]},
    # UTCID06: Decision with decision enum null
    {'id': 'UTCID06', 'type': 'A', 'pre': [11, 12], 'in': [20], 'ret': [], 'ex': [37]},
    # UTCID07: Decision on report already processed
    {'id': 'UTCID07', 'type': 'A', 'pre': [11], 'in': [22], 'ret': [], 'ex': [37]},
    # UTCID08: Decision on report not found
    {'id': 'UTCID08', 'type': 'A', 'pre': [11], 'in': [23], 'ret': [], 'ex': [38]},
    # UTCID09: Decision on locked / partner whitelist report
    {'id': 'UTCID09', 'type': 'A', 'pre': [11, 13], 'in': [15], 'ret': [], 'ex': [37]},
    # UTCID10: Decision by regular user (403)
    {'id': 'UTCID10', 'type': 'A', 'pre': [], 'in': [26], 'ret': [], 'ex': [39]},
    # UTCID11: Decision by unauthenticated caller (401)
    {'id': 'UTCID11', 'type': 'A', 'pre': [], 'in': [27], 'ret': [], 'ex': [40]},
    # UTCID12: Bulk approve sibling reports of same indicator
    {'id': 'UTCID12', 'type': 'N', 'pre': [11, 12], 'in': [15, 24], 'ret': [32], 'ex': []},
    # UTCID13: Bulk reject sibling reports of same indicator
    {'id': 'UTCID13', 'type': 'N', 'pre': [11, 12], 'in': [16, 24], 'ret': [33], 'ex': []},
    # UTCID14: Get report detail by ID (Moderator)
    {'id': 'UTCID14', 'type': 'N', 'pre': [11, 12], 'in': [28], 'ret': [34], 'ex': []},
    # UTCID15: Get report queue with priority sort
    {'id': 'UTCID15', 'type': 'N', 'pre': [11], 'in': [29], 'ret': [35], 'ex': []},
    # UTCID16: Get queue status counts
    {'id': 'UTCID16', 'type': 'N', 'pre': [11], 'in': [29], 'ret': [35], 'ex': []},
    # UTCID17: Get queue with invalid sort property
    {'id': 'UTCID17', 'type': 'A', 'pre': [11], 'in': [30], 'ret': [], 'ex': [37]},
    # UTCID18: Get queue with page < 0 or size < 1
    {'id': 'UTCID18', 'type': 'B', 'pre': [11], 'in': [30], 'ret': [], 'ex': [37]},
]

for idx, tc in enumerate(test_cases):
    col = 6 + idx # Col F is 6
    s3.cell(9, col, tc['id'])
    
    # Preconditions & Inputs
    for row in tc['pre']:
        s3.cell(row, col, 'O')
    for row in tc['in']:
        s3.cell(row, col, 'O')
    for row in tc['ret']:
        s3.cell(row, col, 'O')
    for row in tc['ex']:
        s3.cell(row, col, 'O')
        
    # Results
    s3.cell(41, col, tc['type'])
    s3.cell(42, col, 'P')
    s3.cell(43, col, datetime(2026, 11, 4))
    s3.cell(44, col, None)

# Ensure row 7 formulas are exact
s3.cell(7, 1, '=COUNTIF(F42:W42,"P")')
s3.cell(7, 3, '=COUNTIF(F42:W42,"F")')
s3.cell(7, 6, '=SUM(O7,-A7,-C7)')
s3.cell(7, 12, '=COUNTIF(F41:W41,"N")')
s3.cell(7, 13, '=COUNTIF(F41:W41,"A")')
s3.cell(7, 14, '=COUNTIF(F41:W41,"B")')
s3.cell(7, 15, '=COUNTA(F9:W9)')

target_clean = 'C:/Users/USER/Downloads/Report5_UnitTest_Cleaned.xlsx'
wb.save(target_clean)
print("SAVED CLEANED VERSION TO:", target_clean)

# Also try saving to original if unlocked
try:
    wb.save(file_path)
    print("SAVED ORIGINAL AS WELL!")
except Exception as e:
    print("Original still locked by Excel application:", e)
