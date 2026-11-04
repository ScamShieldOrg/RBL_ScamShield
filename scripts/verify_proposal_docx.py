# -*- coding: utf-8 -*-
import sys
import docx

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def verify():
    filename = "ScamShield_Information Technology.docx"
    doc = docx.Document(filename)
    print(f"=== VERIFYING {filename} ===")
    
    # 1. Section check
    s = doc.sections[0]
    print(f"Page size: {round(s.page_width.inches, 2)} x {round(s.page_height.inches, 2)} inches (Expected ~8.27 x 11.69 A4)")
    print(f"Margins: top={round(s.top_margin.inches, 2)}, bottom={round(s.bottom_margin.inches, 2)}, left={round(s.left_margin.inches, 2)}, right={round(s.right_margin.inches, 2)}")
    
    # 2. Table 0 check
    t0 = doc.tables[0]
    print(f"\nTable 0 rows: {len(t0.rows)}, cols: {len(t0.columns)}")
    title_cell = t0.rows[0].cells[1].text.strip()
    sub_cell = t0.rows[1].cells[1].text.strip()
    grp_cell = t0.rows[2].cells[1].text.strip()
    auth_cell = t0.rows[3].cells[1].text.strip()
    men_cell = t0.rows[4].cells[1].text.strip()
    print(f"Title: {title_cell}")
    print(f"Sub-committee: {sub_cell}")
    print(f"Group name: '{grp_cell}'")
    assert grp_cell == "ScamShield", f"Expected 'ScamShield', got '{grp_cell}'"
    print(f"Authors:\n{auth_cell}")
    assert "Nguyen Minh Quang (Team Leader)" in auth_cell
    assert "SE190820" in auth_cell
    assert "Nguyen Trung Hieu" in auth_cell
    assert "SE190843" in auth_cell
    assert "Hoang Hai Phuc" in auth_cell
    assert "SE190740" in auth_cell
    assert "Nguyen Quoc Huy" in auth_cell
    assert "SE190794" in auth_cell
    print(f"Mentor: {men_cell}")
    assert "Le Thi Quynh Chi" in men_cell
    
    # 3. Abstract word count
    # Let's find abstract paragraph
    abstract_paras = []
    found_abstract = False
    for p in doc.paragraphs:
        if p.text.strip() == "Abstract":
            found_abstract = True
            continue
        if found_abstract:
            if p.text.startswith("Key words:"):
                break
            if p.text.strip():
                abstract_paras.append(p.text.strip())
    full_abstract = " ".join(abstract_paras)
    word_count = len(full_abstract.split())
    print(f"\nAbstract word count: {word_count} words (Limit: <= 250 words)")
    assert word_count <= 250, f"Abstract exceeds 250 words: {word_count}"
    
    # 4. Table 1 check (Research plan)
    t1 = doc.tables[1]
    print(f"\nTable 1 rows: {len(t1.rows)}, cols: {len(t1.columns)}")
    for r_idx in range(1, len(t1.rows)):
        task = t1.rows[r_idx].cells[2].text.strip()[:60]
        pic = t1.rows[r_idx].cells[4].text.strip().replace('\n', ' ')
        print(f"  Row {r_idx}: {task}... -> PIC: {pic}")
    
    # Check that Quang is Leader, Huy has SLR & report writing, Hieu has models, Phuc has data/stats
    all_t1_text = " ".join([c.text for r in t1.rows for c in r.cells])
    assert "Nguyen Minh Quang" in all_t1_text
    assert "Nguyen Quoc Huy" in all_t1_text
    assert "Nguyen Trung Hieu" in all_t1_text
    assert "Hoang Hai Phuc" in all_t1_text
    
    # 5. Table 2 check (Signatures)
    t2 = doc.tables[2]
    print(f"\nTable 2 rows: {len(t2.rows)}, cols: {len(t2.columns)}")
    assert len(t2.columns) == 4, f"Expected 4 columns, got {len(t2.columns)}"
    names_row = [c.text.strip().replace('\n', ' ') for c in t2.rows[1].cells]
    print(f"Table 2 signatories: {names_row}")
    assert any("Nguyen Minh Quang" in n for n in names_row)
    assert any("Nguyen Trung Hieu" in n for n in names_row)
    assert any("Hoang Hai Phuc" in n for n in names_row)
    assert any("Nguyen Quoc Huy" in n for n in names_row)
    
    # 6. Check font throughout document
    non_tnr_runs = 0
    total_runs = 0
    for p in doc.paragraphs:
        for r in p.runs:
            total_runs += 1
            if r.font.name and r.font.name != "Times New Roman":
                non_tnr_runs += 1
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for r in p.runs:
                        total_runs += 1
                        if r.font.name and r.font.name != "Times New Roman":
                            non_tnr_runs += 1
    print(f"\nFont check: {total_runs - non_tnr_runs}/{total_runs} runs verified as Times New Roman.")
    assert non_tnr_runs == 0, f"Found {non_tnr_runs} runs not in Times New Roman"

    print("\nALL VERIFICATION CHECKS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    verify()
