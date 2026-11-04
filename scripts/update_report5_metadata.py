import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from datetime import datetime

wb = openpyxl.load_workbook('C:/Users/USER/Downloads/Report5_UnitTest.xlsx')

# Update Cover sheet Record of change
s_cover = wb['Cover']
if s_cover.cell(12, 1).value is None:
    s_cover.cell(12, 1, datetime(2026, 11, 4))
    s_cover.cell(12, 2, 'A')
    s_cover.cell(12, 3, 'Add test results for Function 3 - Moderate and publish reports')
    s_cover.cell(12, 4, 'M')
    s_cover.cell(12, 5, 'Complete 18 unit test cases for Moderator Report Queue & Decision API (F-03)')
    s_cover.cell(12, 6, 'BM01 §6 Feature F-03; SDD §3.7 / §5.2; SCRUM-128')

# Update Functions sheet
s_func = wb['Functions']
s_func.cell(13, 2, 'WF-02 - Community scam report and moderation')
s_func.cell(13, 3, 'ModeratorReportController, ModeratorReportServiceImpl')
s_func.cell(13, 4, 'Moderate and publish reports')
s_func.cell(13, 5, 'Function3')
s_func.cell(13, 6, 'Function3')
s_func.cell(13, 7, 'Thẩm định báo cáo lừa đảo, duyệt/từ chối với lý do >=20 ký tự, taxonomy category, đồng bộ indicator, bảo vệ tài sản whitelist và phân quyền RBAC')
s_func.cell(13, 8, 'Spring Boot test container, Mockito, MockMvc, JPA repositories initialized, authenticated UserPrincipal (MODERATOR/ADMINISTRATOR)')

# Now configure Function3
s3 = wb['Function3']

# Header metadata
s3.cell(2, 1, 'Function Code')
s3.cell(2, 3, '=Functions!E13')
s3.cell(2, 6, 'Function Name')
s3.cell(2, 12, '=Functions!D13')

s3.cell(3, 1, 'Created By')
s3.cell(3, 3, 'Nguyễn Trung Hiếu')
s3.cell(3, 6, 'Executed By')
s3.cell(3, 12, 'Nguyễn Trung Hiếu')

s3.cell(4, 1, 'Lines  of code')
s3.cell(4, 3, 587.0) # Line count of ModeratorReportServiceImpl
s3.cell(4, 6, 'Lack of test cases')
s3.cell(4, 12, '=IF(Functions!E6<>"N/A",SUM(C4*Functions!E6/1000,-O7),"N/A")')

s3.cell(5, 1, 'Test requirement')
s3.cell(5, 3, 'Verify Moderate and publish reports (F-03): review pending reports queue, approve/reject decision with mandatory audit reason (>= 20 chars), taxonomy category assignment, bulk indicator sync, partner whitelist protection lock, and RBAC authorization.')

wb.save('C:/Users/USER/Downloads/Report5_UnitTest_preview.xlsx')
print("Metadata updated successfully.")
