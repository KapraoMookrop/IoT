import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

src_path = r'c:\Project\IoT\Chatchawan Taja - ใบงานที่ 2 Requirement และ System Block Diagram.docx'
out_path = r'c:\Project\IoT\Chatchawan Taja - ใบงานที่ 2 Requirement และ System Block Diagram (Completed).docx'
img_path = r'c:\Project\IoT\system_block_diagram.png'

doc = docx.Document(src_path)

def set_font(run, font_name='Angsana New', size_pt=14, bold=False, color=None):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    if color:
        run.font.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="{font_name}" w:hAnsi="{font_name}" w:cs="{font_name}" w:eastAsia="{font_name}"/>')
    rPr.append(rFonts)

def set_cell_text(cell, text, bold=False, size_pt=13, align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.text = ''
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(text)
    set_font(run, 'Angsana New', size_pt=size_pt, bold=bold)

# Table 0: Metadata
set_cell_text(doc.tables[0].cell(1, 0), 'กลุ่ม RS-485 Extension Module', bold=True)
set_cell_text(doc.tables[0].cell(1, 1), 'RS-485 Industrial Extension Module สำหรับเซนเซอร์ XY-MD02 (SHT20) ร่วมกับ THARIT-IoT', bold=True)
set_cell_text(doc.tables[0].cell(1, 2), '29 ตุลาคม 2569')
set_cell_text(doc.tables[0].cell(1, 3), 'Draft v0.1', bold=True)

# Table 1: Members & Roles
set_cell_text(doc.tables[1].cell(1, 0), 'ชัชวาล ตาจา', bold=True)
set_cell_text(doc.tables[1].cell(1, 1), 'System Architect / Hardware Interface & Requirement')
set_cell_text(doc.tables[1].cell(1, 2), 'วิเคราะห์ System Boundary, จัดทำ Engineering Requirements, ผัง Block Diagram, Interface List และ RTM')

# ตอนที่ 1: วิเคราะห์ Use Case และ System Boundary
doc.paragraphs[15].text = 'ผู้ใช้เป้าหมายคือนักพัฒนาอุปกรณ์ IoT วิศวกร และผู้ดูแลระบบสมาร์ทฟาร์มหรือโรงงานอุตสาหกรรมที่ใช้งานบอร์ด THARIT-IoT เพื่อตรวจวัดสภาพแวดล้อม ปัญหาที่พบคือพอร์ตสื่อสารของบอร์ดหลักมีเฉพาะระดับแรงดันตรรกะ UART 3.3V ซึ่งไม่สามารถลากสายสัญญาณระยะไกล และไม่สามารถเชื่อมต่อกับเซนเซอร์วัดอุณหภูมิและความชื้นเกรดอุตสาหกรรมรุ่น XY-MD02 (SHT20) ที่สื่อสารด้วยโปรโตคอล Modbus RTU ผ่านมาตรฐาน RS-485 ได้โดยตรง จึงจำเป็นต้องมีโมดูลขยาย (Extension Module) ทำหน้าที่แปลงสัญญาณ Differential และมีระบบป้องกันสัญญาณรบกวนทางไฟฟ้าเพื่อให้รับส่งข้อมูลระยะไกลได้อย่างแม่นยำและเสถียร'
for r in doc.paragraphs[15].runs:
    set_font(r, 'Angsana New', 14)
doc.paragraphs[16].text = ''

doc.paragraphs[18].text = '• Input: บอร์ดหลัก THARIT-IoT ส่งเฟรมคำสั่ง Modbus RTU Master (Function Code 0x04 Read Input Registers) ระดับตรรกะ 3.3V ออกทางขา UART TX พร้อมสัญญาณควบคุมทิศทาง (DE/RE)\n• Processing: ชิป Transceiver (SP3485/MAX3485) บนโมดูลขยายแปลงสัญญาณดิจิทัล UART 3.3V เป็นสัญญาณแรงดันผลต่าง (Differential Signaling A+ / B-) ส่งผ่านวงจรป้องกันไฟกระชาก (TVS Diode Array) และฟิวส์ PTC\n• Output/Outcome: สัญญาณถูกส่งผ่านสายเคเบิล Twisted Pair ไปยังเซนเซอร์ XY-MD02 (SHT20) และรับเฟรมข้อมูลอุณหภูมิและความชื้นที่ตอบกลับ แปลงคืนเป็นสัญญาณ UART RX ส่งกลับเข้าสู่บอร์ด THARIT-IoT เพื่อนำค่าไปประมวลผล แสดงผล หรือส่งขึ้น Cloud ได้อย่างถูกต้อง'
for r in doc.paragraphs[18].runs:
    set_font(r, 'Angsana New', 14)
doc.paragraphs[19].text = ''

doc.paragraphs[21].text = '• สิ่งที่อยู่ในขอบเขตการทำงาน (In-Scope / กลุ่มออกแบบสร้างเอง):\n  1. แผงวงจร Expansion Module พร้อมชิปแปลงสัญญาณ UART <-> RS-485 (Transceiver 3.3V เช่น SP3485 หรือ MAX3485)\n  2. วงจรควบคุมทิศทางการรับ-ส่งข้อมูล (Half-Duplex Control ผ่านขา DE/RE หรือวงจร Auto-Direction)\n  3. วงจรป้องกันทางไฟฟ้าบนบัส RS-485: TVS Diode ป้องกันไฟกระชาก/ESD และฟิวส์ PTC Resettable Fuse ป้องกันกระแสเกิน\n  4. ตัวต้านทาน Termination 120 โอห์ม คร่อมสาย A/B พร้อม Jumper เลือกเปิด/ปิด และตัวต้านทาน Fail-safe Bias\n  5. ขั้วต่อ Industrial Screw Terminal Block 4 ช่อง (V+, GND, A+, B-) สำหรับต่อสายสัญญาณและไฟเลี้ยงไปยังเซนเซอร์'
for r in doc.paragraphs[21].runs:
    set_font(r, 'Angsana New', 14)

doc.paragraphs[22].text = '• สิ่งที่อยู่นอกขอบเขต (Out-of-Scope):\n  1. ตัวฮาร์ดแวร์เซนเซอร์สำเร็จรูป XY-MD02 (ภายในประกอบด้วยโมดูล MCU และชิป Sensirion SHT20)\n  2. แหล่งจ่ายไฟภายนอก DC 9V-24V (กรณีลากสายระยะไกลมากและต้องจ่ายไฟแยกที่ปลายทาง)\n  3. สายเคเบิลภายนอกอาคารและตู้ควบคุมภายนอก'
for r in doc.paragraphs[22].runs:
    set_font(r, 'Angsana New', 14)

doc.paragraphs[23].text = '• งานที่ต้องพึ่งบอร์ดหลัก (THARIT-IoT Dependency):\n  1. แหล่งจ่ายไฟเลี้ยงวงจรตรรกะ 3.3V, 5V และ GND\n  2. พอร์ตสื่อสารฮาร์ดแวร์ UART (TX, RX) และ GPIO ขาควบคุมทิศทาง\n  3. ซอฟต์แวร์เฟิร์มแวร์ Modbus RTU Master (สร้าง Request Packet, คำนวณรหัสตรวจสอบ CRC-16 และแปลงค่าไบต์กลับเป็นอุณหภูมิ/ความชื้นทศนิยม)'
for r in doc.paragraphs[23].runs:
    set_font(r, 'Angsana New', 14)

# Table 3: Engineering Requirements
reqs = [
    ('REQ-RS485-01\n(Functional)', 'ระบบต้องสามารถแปลงสัญญาณ UART 3.3V จากบอร์ด THARIT-IoT เป็นสัญญาณ RS-485 Differential (A+, B-) เพื่อสื่อสารกับเซนเซอร์ XY-MD02 (SHT20) ที่ความเร็ว Baud rate มาตรฐาน 9,600 bps (8N1) และรองรับสูงสุดถึง 115,200 bps ได้', 'เซนเซอร์ XY-MD02 ใช้ค่าเริ่มต้นจากโรงงานคือ Baud rate 9,600 bps, 8N1\nสถานะ: ยืนยันแล้ว (ตาม Datasheet XY-MD02)'),
    ('REQ-RS485-02\n(Functional)', 'ระบบต้องสามารถสลับสถานะการส่งคำสั่ง (Transmit) และการรอรับข้อมูลตอบกลับ (Receive) แบบ Half-Duplex ได้ภายในเวลาไม่เกิน 2 ms ก่อนที่เซนเซอร์ XY-MD02 จะส่งเฟรมข้อมูลตอบกลับ', 'ป้องกันการสูญหายของไบต์แรกจากเซนเซอร์ XY-MD02 ขณะสลับทิศทางบัส RS-485\nสถานะ: ยืนยันแล้ว'),
    ('REQ-RS485-03\n(Interface)', 'โมดูลต้องเชื่อมต่อกับบอร์ดหลัก THARIT-IoT ผ่านขั้วต่อ Header Pin โดยใช้สัญญาณ UART (TX, RX), ขาควบคุมทิศทาง (DE/RE), แรงดันไฟเลี้ยง VCC (3.3V หรือ 5V) และ GND ร่วมกัน', 'เพื่อให้เสียบใช้งานเข้ากับพอร์ตขยายของบอร์ด THARIT-IoT ได้โดยตรงโดยไม่ต้องดัดแปลงบอร์ดหลัก\nสถานะ: TBR (ตรวจสอบผัง Pinout ของ THARIT-IoT)'),
    ('REQ-RS485-04\n(Interface)', 'ฝั่งเชื่อมต่ออุปกรณ์ภายนอกต้องมีขั้วต่อ Screw Terminal Block อย่างน้อย 4 ช่อง สำหรับสายสัญญาณ A+, B- และขั้วจ่ายไฟเลี้ยงเซนเซอร์ XY-MD02 (V+, GND รองรับแรงดัน DC 5V - 24V)', 'เซนเซอร์ XY-MD02 มีสายเชื่อมต่อ 4 เส้น ได้แก่ V+, GND, A+ และ B-\nสถานะ: ยืนยันแล้ว'),
    ('REQ-RS485-05\n(Safety / Fault)', 'สายสัญญาณบัส RS-485 (A+ และ B-) ต้องมีวงจรป้องกันแรงดันไฟกระชากชั่วขณะ (TVS Diode) ที่ทนแรงดัน ESD ได้ไม่น้อยกว่า ±8 kV และมีฟิวส์รีเซ็ตตัวเองได้ (PTC Resettable Fuse) ป้องกันกระแสเกิน', 'ป้องกันความเสียหายต่อชิป Transceiver และบอร์ด THARIT-IoT เมื่อเดินสายไปยังเซนเซอร์ XY-MD02 ในสภาพแวดล้อมจริง\nสถานะ: ยืนยันแล้ว'),
    ('REQ-RS485-06\n(Safety / Fault)', 'ระบบต้องมีตัวต้านทาน Termination 120 Ω คร่อมระหว่างสาย A+ และ B- พร้อม Jumper สำหรับเลือกเปิด/ปิดการใช้งาน และมีตัวต้านทาน Fail-safe Bias (Pull-up ที่ A+ / Pull-down ที่ B-)', 'รักษาระดับแรงดันบัสให้อยู่ในสถานะปลอดภัย (Idle state) เมื่อไม่มีการส่งข้อมูล หรือเมื่อสายเซนเซอร์หลุดขาด\nสถานะ: ยืนยันแล้ว')
]

for idx, req in enumerate(reqs, start=1):
    set_cell_text(doc.tables[3].cell(idx, 0), req[0], bold=True, size_pt=12)
    set_cell_text(doc.tables[3].cell(idx, 1), req[1], size_pt=12)
    set_cell_text(doc.tables[3].cell(idx, 2), req[2], size_pt=12)

# ตอนที่ 3: Insert System Block Diagram image & text
p_diagram_anchor = doc.paragraphs[32]
p_img = p_diagram_anchor.insert_paragraph_before()
p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_img.paragraph_format.space_before = Pt(8)
p_img.paragraph_format.space_after = Pt(4)
r_img = p_img.add_run()
r_img.add_picture(img_path, width=Inches(6.2))

p_caption = p_diagram_anchor.insert_paragraph_before()
p_caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_caption.paragraph_format.space_after = Pt(12)
r_cap = p_caption.add_run('รูปที่ 1 แผนผังบล็อกของระบบ (System Block Diagram) แสดง System Boundary, แหล่งจ่ายไฟ, บัสข้อมูล และจุดทดสอบ TP1-TP4')
set_font(r_cap, 'Angsana New', 13, bold=True)

# Table 4: Self-check checkboxes
for r in range(1, 5):
    set_cell_text(doc.tables[4].cell(r, 1), '☑ ครบ   ☐ ต้องแก้', bold=True, size_pt=13, align=WD_ALIGN_PARAGRAPH.CENTER)

# Table 5: Interface List
ifs = [
    ('IF-01', 'THARIT-IoT Mainboard → Expansion Module', 'UART TX / Digital Signal (ทางเดียว)', 'Logic Level 3.3V TTL, Baud rate 9,600 bps (มาตรฐาน XY-MD02)\nหลักฐาน: ผังวงจร Schematic ของ THARIT-IoT'),
    ('IF-02', 'Expansion Module → THARIT-IoT Mainboard', 'UART RX / Digital Signal (ทางเดียว)', 'Logic Level ต้องไม่เกิน 3.3V (ห้ามจ่าย 5V เข้าขา MCU โดยตรง; ใช้ชิป 3.3V เช่น SP3485 หรือ MAX3485)\nหลักฐาน: Datasheet ชิป Transceiver'),
    ('IF-03', 'THARIT-IoT Mainboard → Expansion Module', 'Power Supply (VCC 3.3V/5V, GND) (ทางเดียว)', 'กระแสใช้งานของโมดูลและเซนเซอร์รวมกันต้องไม่เกินพิกัด LDO ของบอร์ดหลัก (XY-MD02 กินกระแสต่ำ < 20 mA)\nTBR: ตรวจพิกัดกระแสพอร์ต 5V/3.3V บนบอร์ดหลัก'),
    ('IF-04', 'Expansion Module ↔ XY-MD02 (SHT20)', 'RS-485 Bus (A+, B-) / Differential (สองทาง Half-Duplex)', 'แรงดันผลต่าง |V_OD| ≥ 1.5V, โปรโตคอล Modbus RTU (Slave ID เริ่มต้น = 0x01, Function 0x04 อ่าน Register 0x0001 และ 0x0002)\nหลักฐาน: คู่มือเซนเซอร์ XY-MD02'),
    ('IF-05', 'Expansion Module / Ext. Power → XY-MD02', 'Sensor Power (V+, GND) (ทางเดียว)', 'แรงดันไฟเลี้ยง DC 5V – 24V สำหรับเลี้ยงวงจรภายในหัววัด XY-MD02\nTBR: ตรวจสอบว่าจะดึงไฟ 5V จากบอร์ดหลักผ่าน Terminal หรือต่อไฟเลี้ยง 12V/24V แยกจากภายนอก')
]

for idx, if_item in enumerate(ifs, start=1):
    set_cell_text(doc.tables[5].cell(idx, 0), if_item[0], bold=True, size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(doc.tables[5].cell(idx, 1), if_item[1], size_pt=12)
    set_cell_text(doc.tables[5].cell(idx, 2), if_item[2], size_pt=12)
    set_cell_text(doc.tables[5].cell(idx, 3), if_item[3], size_pt=12)

# Table 6: RTM
rtm_rows = [
    ('REQ-RS485-01', 'Demonstration & Test: ส่งคำสั่ง Modbus RTU (01 04 00 01 00 02 20 0B) ที่ Baud rate 9,600 bps ไปยัง XY-MD02 และวัดสัญญาณด้วย Oscilloscope', 'TC-MOD-01', 'ภาพหน้าจอ Serial Monitor แสดงค่าอุณหภูมิ/ความชื้นจาก SHT20 ถูกต้อง และภาพสัญญาณ Differential A/B บน Oscilloscope', 'Not Tested'),
    ('REQ-RS485-02', 'Test: วัดเวลาหน่วงการสลับสถานะขา DE//RE หรือวงจร Auto-Direction เทียบกับจังหวะที่ XY-MD02 ตอบกลับด้วย Logic Analyzer', 'TC-MOD-02', 'ไฟล์บันทึก Timing Diagram จาก Logic Analyzer แสดงช่วงเปลี่ยนผ่านจาก TX เป็น RX ก่อนไบต์แรกของเซนเซอร์มาถึง', 'Not Tested'),
    ('REQ-RS485-03', 'Inspection & Measurement: ตรวจสอบตำแหน่งขา Header และวัดระดับแรงดันที่ขา RX/TX ด้วย Digital Multimeter', 'TC-IF-01', 'ตารางบันทึกผลการวัดแรงดันไฟฟ้า (ต้องไม่เกิน 3.3V ที่ขาเข้า MCU) และภาพถ่ายการเชื่อมต่อกับบอร์ด THARIT-IoT', 'Not Tested'),
    ('REQ-RS485-05', 'Inspection: ตรวจสอบเบอร์อุปกรณ์ TVS Diode, พิกัด Breakdown Voltage และการจัดวางใกล้ขั้ว Screw Terminal บนแผ่นวงจร', 'TC-SAFE-01', 'เอกสาร Datasheet ของ TVS Diode และภาพ Layout / Schematic ที่แสดงตำแหน่งวงจรป้องกันชัดเจน', 'Not Tested')
]

for idx, rtm in enumerate(rtm_rows, start=1):
    set_cell_text(doc.tables[6].cell(idx, 0), rtm[0], bold=True, size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(doc.tables[6].cell(idx, 1), rtm[1], size_pt=12)
    set_cell_text(doc.tables[6].cell(idx, 2), rtm[2], bold=True, size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(doc.tables[6].cell(idx, 3), rtm[3], size_pt=12)
    set_cell_text(doc.tables[6].cell(idx, 4), rtm[4], size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER)

# Table 7: Risks & TBR
risks = [
    ('1. แรงดันไฟเลี้ยงของเซนเซอร์ XY-MD02 (SHT20)\n(TBR: 5V จากบอร์ดหลัก vs 12V-24V ภายนอก)', 'คู่มือ XY-MD02 ระบุรับไฟ DC 5V - 30V แต่หากลากสายยาวเกิน 10 - 20 เมตร แรงดัน 5V จะตกลงในสาย (Voltage Drop) ทำให้เซนเซอร์ SHT20 รีเซ็ตตัวเองหรืออ่านค่าเพี้ยน', 'ออกแบบ Screw Terminal ให้มี Jumper เลือกแหล่งจ่ายไฟ V+ ได้ระหว่างไฟ 5V จากบอร์ดหลัก (สายสั้น) หรือต่อไฟ DC 12V/24V จากภายนอก (สายยาว)\nผู้รับผิดชอบ: ชัชวาล ตาจา'),
    ('2. ระดับแรงดัน Logic Level ไม่ตรงกัน (5V vs 3.3V)', 'หากใช้ชิป MAX485 รุ่นดั้งเดิมที่ใช้ไฟ 5V สัญญาณขา RO ที่ต่อเข้าขา RX ของบอร์ด THARIT-IoT จะมีแรงดัน 5V ซึ่งอาจทำให้พอร์ต GPIO ของไมโครคอนโทรลเลอร์ ESP32 พังเสียหาย', 'เลือกใช้ชิป Transceiver ที่ทำงานด้วยไฟเลี้ยง 3.3V โดยตรง เช่น SP3485 หรือ MAX3485 เพื่อให้ระดับสัญญาณเข้ากันได้ 100%\nผู้รับผิดชอบ: ชัชวาล ตาจา'),
    ('3. การต่อสลับสาย A+ และ B- หรือสายหลุดระหว่างใช้งาน', 'ระบบสื่อสารไม่ได้ หรือเกิดแรงดันลอยตัว (Floating) ทำให้บอร์ดหลักรับข้อมูลขยะ (Framing Error) ต่อเนื่อง', 'พิมพ์ Silk Screen กำกับขั้ว A+, B-, V+, GND บน PCB ให้ชัดเจน และใส่วงจร Fail-safe Bias Resistor บังคับสถานะบัส Idle เมื่อสายหลุด\nผู้รับผิดชอบ: ชัชวาล ตาจา')
]

for idx, rk in enumerate(risks, start=1):
    set_cell_text(doc.tables[7].cell(idx, 0), rk[0], bold=True, size_pt=12)
    set_cell_text(doc.tables[7].cell(idx, 1), rk[1], size_pt=12)
    set_cell_text(doc.tables[7].cell(idx, 2), rk[2], size_pt=12)

# Individual Reflection
for i, p in enumerate(doc.paragraphs):
    if 'ก. Requirement ข้อใดสำคัญที่สุด' in p.text:
        doc.paragraphs[i+1].text = 'คำตอบ: ข้อ REQ-RS485-05 (วงจรป้องกันแรงดันไฟกระชากและกระแสเกิน) และ REQ-RS485-01 (การแปลงสัญญาณที่ Baud rate 9,600 bps สำหรับ XY-MD02) สำคัญที่สุด เพราะการต่อสายออกไปหาเซนเซอร์ XY-MD02 ภายนอกมีความเสี่ยงต่อไฟกระชากและการต่อสายผิดพลาด หากไม่มีวงจรป้องกันที่ดีพอร์ตของบอร์ดหลัก THARIT-IoT จะเสียหายทันที และหากระดับสัญญาณไม่ตรงตามโปรโตคอล Modbus RTU ของ SHT20 ระบบก็จะไม่สามารถอ่านค่าได้เลย'
        for r in doc.paragraphs[i+1].runs:
            set_font(r, 'Angsana New', 14)
        doc.paragraphs[i+2].text = ''
    elif 'ข. ข้อมูลทางวิศวกรรมเรื่องใดต้องตรวจ' in p.text:
        doc.paragraphs[i+1].text = 'คำตอบ:\n1. ผังวงจรและ Pinout ของบอร์ด THARIT-IoT เพื่อยืนยันขาสัญญาณ UART และพิกัดกระแสของแหล่งจ่ายไฟ 3.3V และ 5V บน Expansion Header\n2. Datasheet ของชิป SP3485 / MAX3485 (3.3V Transceiver) และคู่มือเซนเซอร์ XY-MD02 (SHT20) เรื่องช่วงแรงดันไฟเลี้ยงขั้นต่ำและรูปแบบการต่อตัวต้านทาน Fail-safe / Termination 120 โอห์ม'
        for r in doc.paragraphs[i+1].runs:
            set_font(r, 'Angsana New', 14)
        doc.paragraphs[i+2].text = ''
    elif 'ค. บทบาทของตนเองในกลุ่ม' in p.text:
        doc.paragraphs[i+1].text = 'คำตอบ: รับผิดชอบการวิเคราะห์ความต้องการของระบบ (System Requirements) และการออกแบบ Interface เชื่อมต่อระหว่าง THARIT-IoT กับเซนเซอร์ XY-MD02 (SHT20) ผ่านบัส RS-485 สิ่งที่จะทำให้ดีขึ้นในครั้งหน้าคือ การตรวจสอบขนาด Footprint ของขั้วต่อ Screw Terminal และเบอร์อุปกรณ์ SMD ที่มีจำหน่ายจริงก่อนเริ่มวาดวงจร Schematic ในสัปดาห์ที่ 3'
        for r in doc.paragraphs[i+1].runs:
            set_font(r, 'Angsana New', 14)
        doc.paragraphs[i+2].text = ''

doc.save(out_path)
print('Successfully generated filled docx at:', out_path)
