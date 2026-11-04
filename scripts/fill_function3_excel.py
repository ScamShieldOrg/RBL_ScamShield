import openpyxl
from openpyxl.cell.cell import MergedCell
from datetime import datetime

file_path = 'C:/Users/USER/Downloads/Report5_UnitTest.xlsx'
wb = openpyxl.load_workbook(file_path)

# 1. Update Cover sheet
s_cover = wb['Cover']
for r in range(11, 25):
    val = s_cover.cell(r, 3).value
    if val and 'Function 3' in str(val):
        break
    if val is None:
        s_cover.cell(r, 1, datetime(2026, 11, 4))
        s_cover.cell(r, 2, 'A')
        s_cover.cell(r, 3, 'Add test results for Function 3 - Moderate and publish reports')
        s_cover.cell(r, 4, 'M')
        s_cover.cell(r, 5, 'Complete 18 unit test cases for Moderator Report Queue & Decision API (F-03)')
        s_cover.cell(r, 6, 'BM01 §6 Feature F-03; SDD §3.7 / §5.2; SCRUM-128')
        break

# 2. Update Functions sheet
s_func = wb['Functions']
s_func.cell(13, 2, 'WF-02 - Community scam report and moderation')
s_func.cell(13, 3, 'ModeratorReportController, ModeratorReportServiceImpl')
s_func.cell(13, 4, 'Moderate and publish reports')
s_func.cell(13, 5, 'Function3')
s_func.cell(13, 6, 'Function3')
s_func.cell(13, 7, 'Thẩm định báo cáo lừa đảo, duyệt/từ chối với lý do >=20 ký tự, taxonomy category, đồng bộ indicator, bảo vệ tài sản whitelist và phân quyền RBAC')
s_func.cell(13, 8, 'Spring Boot test container, Mockito, MockMvc, JPA repositories initialized, authenticated UserPrincipal (MODERATOR/ADMINISTRATOR)')

# 3. Update Function3 sheet
s3 = wb['Function3']

# Unmerge conflicting old template ranges
conflicts = ['B39:D39', 'B40:D40', 'B41:D41', 'B42:D42', 'D19:E19']
for cr in conflicts:
    if cr in [str(r) for r in s3.merged_cells.ranges]:
        s3.unmerge_cells(cr)

# Merge properly like Function4
proper_merges = ['B41:D41', 'B42:D42', 'B43:D43', 'B44:D44']
for pm in proper_merges:
    if pm not in [str(r) for r in s3.merged_cells.ranges]:
        s3.merge_cells(pm)

# Header info
s3.cell(2, 1, 'Function Code')
s3.cell(2, 3, '=Functions!E13')
s3.cell(2, 6, 'Function Name')
s3.cell(2, 12, '=Functions!D13')

s3.cell(3, 1, 'Created By')
s3.cell(3, 3, 'Nguyễn Trung Hiếu')
s3.cell(3, 6, 'Executed By')
s3.cell(3, 12, 'Nguyễn Trung Hiếu')

s3.cell(4, 1, 'Lines  of code')
s3.cell(4, 3, 587.0)
s3.cell(4, 6, 'Lack of test cases')
s3.cell(4, 12, '=IF(Functions!E6<>"N/A",SUM(C4*Functions!E6/1000,-O7),"N/A")')

s3.cell(5, 1, 'Test requirement')
s3.cell(5, 3, 'Verify Moderate and publish reports (F-03): review pending reports queue, approve/reject decision with mandatory audit reason (>= 20 chars), taxonomy category assignment, bulk indicator sync, partner whitelist protection lock, and RBAC authorization.')

s3.cell(6, 1, 'Passed')
s3.cell(6, 3, 'Failed')
s3.cell(6, 6, 'Untested')
s3.cell(6, 12, 'N/A/B')
s3.cell(6, 15, 'Total Test Cases')

# Formulas for row 7
s3.cell(7, 1, '=COUNTIF(F42:W42,"P")')
s3.cell(7, 3, '=COUNTIF(F42:W42,"F")')
s3.cell(7, 6, '=SUM(O7,-A7,-C7)')
s3.cell(7, 12, '=COUNTIF(F41:W41,"N")')
s3.cell(7, 13, '=COUNTIF(F41:W41,"A")')
s3.cell(7, 14, '=COUNTIF(F41:W41,"B")')
s3.cell(7, 15, '=COUNTA(F9:W9)')

# Row headers in column A, B, D
s3.cell(10, 1, 'Condition')
s3.cell(10, 2, 'Precondition')

s3.cell(11, 4, 'Moderator is authenticated (ROLE_MODERATOR)')
s3.cell(12, 4, 'Report exists and status is PENDING / IN_REVIEW')
s3.cell(13, 4, 'Indicator is locked / on partner whitelist')

s3.cell(14, 2, 'Input: Decision & Reason')
s3.cell(15, 4, 'Decision: APPROVE, reason >= 20 chars, categoryId valid')
s3.cell(16, 4, 'Decision: REJECT, reason >= 20 chars')
s3.cell(17, 4, 'Reason boundary: exact 20 chars')
s3.cell(18, 4, 'Reason invalid: < 20 chars (e.g. 19 chars or "Quá ngắn")')
s3.cell(19, 4, 'Reason invalid: null / blank')
s3.cell(20, 4, 'Decision invalid: null / missing')

s3.cell(21, 2, 'Input: Report State & Duplicates')
s3.cell(22, 4, 'Report already processed (APPROVED / REJECTED)')
s3.cell(23, 4, 'Report not found (invalid / non-existent ID)')
s3.cell(24, 4, 'Sibling pending reports with same indicator exist')

s3.cell(25, 2, 'Input: Auth Role & Query Filters')
s3.cell(26, 4, 'Caller role: REGISTERED_USER (regular user)')
s3.cell(27, 4, 'Caller role: Unauthenticated (no JWT)')
s3.cell(28, 4, 'Get detail: valid report ID by Moderator')
s3.cell(29, 4, 'Get queue / counts: valid pagination & filter')
s3.cell(30, 4, 'Pagination / sort invalid: page < 0, size < 1, bad sort')

s3.cell(31, 1, 'Confirm')
s3.cell(31, 2, 'Return')
s3.cell(32, 4, 'Decision response (Approved, indicator confirmed public)')
s3.cell(33, 4, 'Decision response (Rejected, indicator unpublished)')
s3.cell(34, 4, 'Report detail response (DTO, evidence list, audit code)')
s3.cell(35, 4, 'Queue list / Queue counts response (200 OK)')

s3.cell(36, 2, 'Exception')
s3.cell(37, 4, 'BadRequestException (400 Bad Request)')
s3.cell(38, 4, 'ResourceNotFoundException (404 Not Found)')
s3.cell(39, 4, 'AccessDeniedException (403 Forbidden)')
s3.cell(40, 4, 'AuthenticationException (401 Unauthorized)')

s3.cell(41, 1, 'Result')
s3.cell(41, 2, 'Type(N : Normal, A : Abnormal, B : Boundary)')
s3.cell(42, 2, 'Passed/Failed')
s3.cell(43, 2, 'Executed Date')
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
    
    # Clear any old marks in this col
    for r in range(11, 41):
        s3.cell(r, col, None)
        
    for row in tc['pre']:
        s3.cell(row, col, 'O')
        
    for row in tc['in']:
        s3.cell(row, col, 'O')
        
    for row in tc['ret']:
        s3.cell(row, col, 'O')
        
    for row in tc['ex']:
        s3.cell(row, col, 'O')
        
    s3.cell(41, col, tc['type'])
    s3.cell(42, col, 'P')
    s3.cell(43, col, datetime(2026, 11, 4))
    s3.cell(44, col, None)

wb.save(file_path)
print("SUCCESS: Function 3 filled and saved to", file_path)
