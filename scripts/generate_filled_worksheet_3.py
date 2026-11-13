import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(root_dir, 'docs', 'Chatchawan Taja - ใบงานที่ 3.docx')
out_path = os.path.join(root_dir, 'docs', 'Chatchawan Taja - ใบงานที่ 3 (Completed).docx')
img_path = os.path.join(root_dir, 'images', 'system_block_diagram_simple.png')

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

def set_cell_text(cell, text, bold=False, size_pt=12, align=WD_ALIGN_PARAGRAPH.LEFT, color=None, space_after=2):
    cell.text = ''
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(text)
    set_font(run, 'Angsana New', size_pt=size_pt, bold=bold, color=color)

def add_paragraph_to_cell(cell, text, bold=False, size_pt=12, align=WD_ALIGN_PARAGRAPH.LEFT, color=None, space_after=2):
    p = cell.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(text)
    set_font(run, 'Angsana New', size_pt=size_pt, bold=bold, color=color)
    return p

# ---------------------------------------------------------
# Table 0: ข้อมูลสำหรับระบุตัวผู้เรียน
# ---------------------------------------------------------
# R1: ชื่อ–นามสกุล / รหัสนักศึกษา
set_cell_text(doc.tables[0].cell(1, 1), 'นายชัชวาล ตาจา  /  [รหัสนักศึกษา]', bold=True, size_pt=13)

# R2: กลุ่มโครงงาน / ชื่อโมดูล
set_cell_text(doc.tables[0].cell(2, 1), 'กลุ่ม 1 : RS485 / Modbus RTU\nโมดูล: RS-485 Industrial Extension Module สำหรับเซนเซอร์ XY-MD02 (SHT20) ร่วมกับ THARIT-IoT (ESP32-S3)', bold=True, size_pt=12)

# R3: สมาชิกในกลุ่มและบทบาท
doc.tables[0].cell(3, 1).text = ''
m1 = '1. นายชัชวาล ตาจา (หัวหน้ากลุ่ม) — System Architect & Requirements Lead\n   (วิเคราะห์ Interface Matrix, กำหนด Preliminary Pin Mapping บน ESP32-S3, ออกแบบ Power Domain & Safety, จัดทำ Risk Register และ Verification Plan)'
m2 = '2. [ชื่อ-สกุล สมาชิกคนที่ 2] — Hardware Schematic & PCB Design Engineer\n   (รับผิดชอบสัญลักษณ์ Schematic EDA, Footprint 0805/SOIC-8, ตรวจสอบ DRC และเลย์เอาต์ PCB Single-Layer Zero-Crossing)'
m3 = '3. [ชื่อ-สกุล สมาชิกคนที่ 3] — Embedded Firmware & Modbus Protocol Engineer\n   (รับผิดชอบโค้ด ESP32-S3 Hardware Serial, ฟังก์ชันควบคุมทิศทาง DE/RE < 2ms, อัลกอริทึม Modbus RTU CRC-16 Checksum)'
m4 = '4. [ชื่อ-สกุล สมาชิกคนที่ 4] — Hardware Assembly, System QA Testing & Documentation Specialist\n   (รับผิดชอบการประกอบบัดกรีอุปกรณ์, ตรวจสอบ Continuity Test, วางแผนเก็บผล Oscilloscope Waveform และจัดรูปร่างรายงาน)'
set_cell_text(doc.tables[0].cell(3, 1), m1, size_pt=11)
add_paragraph_to_cell(doc.tables[0].cell(3, 1), m2, size_pt=11)
add_paragraph_to_cell(doc.tables[0].cell(3, 1), m3, size_pt=11)
add_paragraph_to_cell(doc.tables[0].cell(3, 1), m4, size_pt=11)

# R4: Revision / วันที่แก้ไข
set_cell_text(doc.tables[0].cell(4, 1), 'Rev. 1.0 (Hardware Interface Design & Pin Mapping) / 12 พฤศจิกายน 2569', bold=True, size_pt=12)

# ---------------------------------------------------------
# Table 1: ขอบเขตโมดูล (กิจกรรม ทบทวนแบบและกำหนดขอบเขตโมดูล)
# ---------------------------------------------------------
# R1: ชื่อและหน้าที่หลักของ Expansion Board
t1_r1 = (
    'RS-485 Industrial Extension Module (SP3485E)\n'
    'ทำหน้าที่แปลงระดับสัญญาณดิจิทัลแบบจุดเดียว (Single-ended UART Logic 3.3V) จาก ESP32-S3 บนบอร์ดหลัก THARIT-IoT '
    'เป็นสัญญาณแรงดันผลต่าง (Differential Signaling บนสายคู่บิดเกลียว A+, B-) ตามมาตรฐาน RS-485 สื่อสารแบบ Half-Duplex '
    'ด้วยโปรโตคอล Modbus RTU เพื่ออ่านค่าอุณหภูมิและความชื้นจากเซนเซอร์เกรดอุตสาหกรรมรุ่น XY-MD02 (SHT20) ในระยะไกล '
    'พร้อมทั้งมีวงจรป้องกันไฟกระชากทางไฟฟ้า (TVS Diode SM712), ฟิวส์ป้องกันกระแสเกิน (PTC Resettable 100mA), '
    'ตัวต้านทาน Termination 120 Ω (R_TERM พร้อม Jumper J_TERM), วงจร Fail-safe Bias (R_PU/R_PD 4.7k) '
    'และระบบจ่ายไฟแบบ Dual-Source (J_PWR)'
)
set_cell_text(doc.tables[1].cell(1, 1), t1_r1, size_pt=12)

# R2: Controller / Mainboard ที่ใช้
t1_r2 = (
    'บอร์ด THARIT-IoT Controller (ใช้ไมโครคอนโทรลเลอร์ Espressif ESP32-S3 Dual-Core Xtensa LX7 ความเร็ว 240 MHz, '
    'Logic IO Voltage 3.3V, พอร์ตสื่อสารภายนอกรองรับ Hardware UART ผ่าน GPIO Matrix)'
)
set_cell_text(doc.tables[1].cell(2, 1), t1_r2, size_pt=12)

# R3: ข้อมูลที่ส่งจาก Mainboard ไปยังโมดูล
t1_r3 = (
    '1. สัญญาณข้อมูล UART_TX (Digital Logic 3.3V TTL): ส่งคำสั่ง Master Request Packet ตามโปรโตคอล Modbus RTU '
    '(Function Code 0x04 Read Input Registers) จากพิน GPIO17 ของ ESP32-S3 ไปยังพิน DI ของชิป SP3485E\n'
    '2. สัญญาณควบคุมทิศทาง RS485_DIR (DE/RE Logic 3.3V): สัญญาณดิจิทัลควบคุมโหมดรับ-ส่ง (Active HIGH สำหรับ Transmit / '
    'LOW สำหรับ Receive) จากพิน GPIO04 ของ ESP32-S3 เข้าควบคุมขา DE และ /RE ร่วมกัน'
)
set_cell_text(doc.tables[1].cell(3, 1), t1_r3, size_pt=12)

# R4: ข้อมูลที่ส่งกลับ Mainboard
t1_r4 = (
    'สัญญาณข้อมูล UART_RX (Digital Logic 3.3V TTL): ส่งเฟรมข้อมูลผลการตอบกลับจาก Slave (XY-MD02 Response Packet '
    'ที่บรรจุค่าอุณหภูมิและความชื้นสัมพัทธ์ พร้อมรหัสตรวจสอบ CRC-16) จากพิน RO ของชิป SP3485E กลับเข้าสู่พิน GPIO16 '
    'ของ ESP32-S3 เพื่อให้เฟิร์มแวร์ถอดรหัสและประมวลผล'
)
set_cell_text(doc.tables[1].cell(4, 1), t1_r4, size_pt=12)

# R5: แหล่งจ่ายไฟที่เกี่ยวข้อง
t1_r5 = (
    '1. Logic Power (3.3V DC): รับไฟ 3.3V จาก Power Rail ของ ESP32-S3 เข้ามาเลี้ยงชิป SP3485E, ตัวเก็บประจุ C1 (100nF), '
    'ตัวต้านทาน Pull-up (R_PU 4.7k) และไฟสถานะ LED1 (PWR)\n'
    '2. Sensor Load Power (5V หรือ EXT DC 12V-24V): รองรับผ่าน Jumper J_PWR โดยโหมดบอร์ด (เสียบช็อตขา 1-2) ดึงไฟ 5V '
    'จาก Rail 5V/VBUS ของ ESP32-S3 ไปเลี้ยงเซนเซอร์ (สายสั้น < 10m) หรือโหมดภายนอก (เสียบช็อตขา 2-3) รับไฟ DC 12V-24V '
    'จากแหล่งจ่ายภายนอกสำหรับเดินสายระยะไกล\n'
    '3. Common Ground (GND): บัสกราวด์อ้างอิงร่วมเชื่อมต่อระหว่าง GND ของ ESP32-S3, Ground Plane บนโมดูลขยาย '
    'และขั้วกราวด์ของเซนเซอร์ XY-MD02'
)
set_cell_text(doc.tables[1].cell(5, 1), t1_r5, size_pt=12)

# R6: สิ่งที่อยู่นอกขอบเขตโมดูล
t1_r6 = (
    '1. ฮาร์ดแวร์เซนเซอร์สำเร็จรูป XY-MD02 (แผงวงจรแปลงค่า SHT20 เป็น Modbus RTU ภายในตัวเซนเซอร์)\n'
    '2. แหล่งจ่ายไฟภายนอก (External DC Power Supply 12V-24V กรณีใช้งานโหมด EXT)\n'
    '3. ภาระงานด้านซอฟต์แวร์บนตัวประมวลผล ESP32-S3 (เช่น การคำนวณรหัส CRC-16, การเชื่อมต่อ Wi-Fi/MQTT, หน้าเว็บแดชบอร์ด)'
)
set_cell_text(doc.tables[1].cell(6, 1), t1_r6, size_pt=12)

# ---------------------------------------------------------
# Table 2: แผนภาพ / ลิงก์ผลงานกลุ่ม
# ---------------------------------------------------------
cell_img = doc.tables[2].cell(1, 0)
cell_img.text = ''
p_img = cell_img.paragraphs[0]
p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_img.paragraph_format.space_before = Pt(4)
p_img.paragraph_format.space_after = Pt(4)
r_img = p_img.add_run()
if os.path.exists(img_path):
    r_img.add_picture(img_path, width=Inches(5.8))
p_caption = cell_img.add_paragraph()
p_caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_caption.paragraph_format.space_after = Pt(6)
r_cap = p_caption.add_run('รูปที่ 1 แผนผังบล็อกระบบ (System Block Diagram Revision v2.2) แสดง System Boundary, แหล่งจ่ายไฟแยกโซน และทิศทางสัญญาณครบถ้วน')
set_font(r_cap, 'Angsana New', 12, bold=True)

# R2: คำอธิบายสั้น ๆ
t2_r2 = (
    'คำอธิบายทิศทางสัญญาณและแหล่งจ่ายไฟ:\n'
    '1. ฝั่งซ้าย (THARIT-IoT Controller): จ่ายไฟ 3.3V Logic และ 5V VBUS เข้าโมดูล พร้อมส่งสัญญาณ UART_TX (GPIO17) '
    'และ Direction Control DE/RE (GPIO04) ออกไป และรอรับสัญญาณ UART_RX (GPIO16) กลับเข้ามา\n'
    '2. ตรงกลาง (RS-485 Industrial Extension Module): ชิป SP3485E แปลงสัญญาณดิจิทัลเป็น RS-485 Differential A+, B- '
    'ผ่านวงจรความปลอดภัย (TVS Diode SM712 ดักไฟกระชาก และ PTC Fuse 100mA ดักกระแสเกิน) พร้อมตัวต้านทาน Termination 120 Ω '
    'และ Fail-safe Bias 4.7k โดยมีไฟ LED แสดงสถานะ PWR, TX, RX แยกชัดเจน\n'
    '3. ฝั่งขวา (XY-MD02 Sensor): รับไฟเลี้ยง V+ (5V จากบอร์ดหลัก หรือ 12-24V EXT ผ่าน J_PWR) และเชื่อมต่อสัญญาณข้อมูลต่างศักย์ A+, B- '
    'และ Common GND ผ่าน Screw Terminal Block 4 ช่องแบบ Zero-Crossing Single-Layer ตามมาตรฐาน IPC-2141'
)
set_cell_text(doc.tables[2].cell(2, 0), t2_r2, size_pt=12)

# ---------------------------------------------------------
# Table 3: ศึกษา Datasheet / Schematic ก่อนกำหนดขา
# ---------------------------------------------------------
# R1: Controller / Development Board
set_cell_text(doc.tables[3].cell(1, 0), 'Controller: ESP32-S3\n(บอร์ด THARIT-IoT / DevKit)', bold=True, size_pt=12)
set_cell_text(doc.tables[3].cell(1, 1), (
    '• พิกัดแรงดัน IO Logic Level: 3.3V (V_IL max 0.8V, V_IH min 2.0V, V_OH min 2.64V, V_OL max 0.33V)\n'
    '• ขาที่ใช้ได้: ตรวจสอบ GPIO Matrix สามารถแมป Hardware UART ไปยังขา GPIO ทั่วไปได้อย่างอิสระ\n'
    '• ขาพิเศษที่ต้องเลี่ยง: Strapping Pins (GPIO0, GPIO3, GPIO45, GPIO46), Octal Flash/PSRAM (GPIO33-37), USB Native (GPIO19, 20)\n'
    '• ขาที่เลือกใช้: GPIO17 (TX), GPIO16 (RX), GPIO04 (DE) เป็น General IO ปลอดภัย 100%'
), size_pt=11)
set_cell_text(doc.tables[3].cell(1, 2), 'Espressif ESP32-S3 Series Datasheet v1.6 & Technical Reference Manual\nสถานะ: ยืนยันแล้ว', size_pt=11)

# R2: IC / Module หลักของกลุ่ม
set_cell_text(doc.tables[3].cell(2, 0), 'IC Transceiver:\nSP3485EN-L/TR (MaxLinear)', bold=True, size_pt=12)
set_cell_text(doc.tables[3].cell(2, 1), (
    '• แรงดันไฟเลี้ยง VCC: 3.0V ถึง 3.6V (ใช้ 3.3V จากบอร์ดหลัก)\n'
    '• ระดับตรรกะอินพุต: V_IH min 2.0V, V_IL max 0.8V (รับตรงจาก ESP32-S3 ได้)\n'
    '• กระแสใช้งาน: Typical 600 µA (Idle/Receive), Max 10 mA (Transmit)\n'
    '• ลำดับขา (SOIC-8): 1:RO, 2:/RE, 3:DE, 4:DI, 5:GND, 6:A, 7:B, 8:VCC'
), size_pt=11)
set_cell_text(doc.tables[3].cell(2, 2), 'MaxLinear SP3485 3.3V Low Power Half-Duplex RS-485 Transceiver Datasheet\nสถานะ: ยืนยันแล้ว', size_pt=11)

# R3: Load / Sensor / External Device
set_cell_text(doc.tables[3].cell(3, 0), 'Industrial Sensor:\nXY-MD02 (Sensirion SHT20)', bold=True, size_pt=12)
set_cell_text(doc.tables[3].cell(3, 1), (
    '• แรงดันไฟเลี้ยงใช้งาน: DC 5V ถึง 30V (โหมดบอร์ด 5V หรือโหมด EXT 12V-24V)\n'
    '• กำลังไฟฟ้าและการกินกระแส: < 0.2W (~15–20 mA ขณะวัดผล)\n'
    '• โปรโตคอล: Modbus RTU ผ่าน RS-485 (ค่าเริ่มต้น 9600 bps, 8 Data bits, No Parity, 1 Stop bit, Slave ID 0x01)\n'
    '• ขั้วต่อสาย: V+ (แดง), A+ (เหลือง), B- (เขียว/ขาว), GND (ดำ)'
), size_pt=11)
set_cell_text(doc.tables[3].cell(3, 2), 'XY-MD02 Temperature and Humidity Transmitter User Manual & Sensirion SHT20 Datasheet\nสถานะ: ยืนยันแล้ว', size_pt=11)

# R4: Connector / Protection
set_cell_text(doc.tables[3].cell(4, 0), 'วงจรป้องกันและจุดเชื่อมต่อ:\nSM712 TVS + PTC 100mA + Screw Terminal 4-Pin', bold=True, size_pt=12)
set_cell_text(doc.tables[3].cell(4, 1), (
    '• TVS Diode SM712: แรงดัน Stand-off ไม่สมมาตร -7V ถึง +12V สำหรับบัส RS-485, ทน ESD ±8kV Contact / ±15kV Air\n'
    '• PTC Resettable Fuse (F1, F2): พิกัด Holding Current 100mA, Voltage Rating 60Vdc, Max Fault Current 10A\n'
    '• ขั้วต่อ Terminal Block: Pitch 3.81mm 4 ช่อง [1:V+, 2:A+, 3:B-, 4:GND] เรียงสาย A+/B- ชิดตรงกลางแบบ Differential Pair\n'
    '• ขั้วต่อ Header ฝั่ง ESP32: 1x6 Pin 2.54mm [1:5V, 2:3V3, 3:RX, 4:DE, 5:TX, 6:GND]'
), size_pt=11)
set_cell_text(doc.tables[3].cell(4, 2), 'Semtech SM712 Datasheet, Littlefuse 1812L010PR PTC Datasheet & IPC-2141 Standard\nสถานะ: ยืนยันแล้ว', size_pt=11)

# ---------------------------------------------------------
# Table 4: กิจกรรม จัดทำ Interface List (อย่างน้อย 5 อินเทอร์เฟซ)
# ---------------------------------------------------------
ifs_data = [
    ('IF-01', 'ESP32-S3 (GPIO17) → SP3485E (DI)', 'UART_TX / Digital 3.3V', 'Out', 'ระดับแรงดัน 3.3V TTL, Baud rate 9,600 bps (Modbus Frame) ต่อเข้าขา 4 (DI) ของ SP3485E โดยตรง'),
    ('IF-02', 'SP3485E (RO) → ESP32-S3 (GPIO16)', 'UART_RX / Digital 3.3V', 'In', 'ระดับแรงดัน 3.3V TTL ออกจากขา 1 (RO) ของ SP3485E เข้าขา GPIO16 ของ ESP32-S3 ปลอดภัย ไม่ต้องใช้ Level Shifter'),
    ('IF-03', 'ESP32-S3 (GPIO04) → SP3485E (DE & /RE)', 'Direction Control (Half-Duplex)', 'Out', 'ระดับแรงดัน 3.3V ควบคุมขา DE และ /RE ร่วมกัน (HIGH=ส่ง, LOW=รับ) มี Pulldown R_DE 10k ดึงลงกราวด์ เริ่มต้นเป็นโหมดรับเสมอ'),
    ('IF-04', 'SP3485E (A, B) ↔ XY-MD02 (A+, B-)', 'RS-485 Differential Pair (Modbus RTU)', 'Bidirectional', 'แรงดันผลต่าง |V_OD| ≥ 1.5V สื่อสารสองทางแบบสลับเวลา มี TVS SM712, PTC 100mA, R_TERM 120Ω และ Fail-safe Bias 4.7k'),
    ('IF-05', 'THARIT-IoT / EXT Supply → SP3485E & XY-MD02', 'Power Distribution (3.3V, 5V/EXT, GND)', 'In', '3.3V เลี้ยงวงจรตรรกะและ Transceiver; ไฟเซนเซอร์เลือกผ่าน J_PWR (5V จากบอร์ดหลัก หรือ EXT 12V-24V); บัส Common GND ร่วมกัน'),
    ('IF-06', 'SP3485E & Signals → Discrete Status LEDs', 'Status Indicators (PWR, TX, RX)', 'Out', 'ไฟ LED 3 สี ต่อแบบแท็ปแยกสาขาลง GND ผ่าน R1, R2, R3 (1k) ไม่ต่อคั่นกลางสายสัญญาณ ไม่กระทบรูปคลื่นข้อมูล')
]

for idx, item in enumerate(ifs_data, start=1):
    set_cell_text(doc.tables[4].cell(idx, 0), item[0], bold=True, size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(doc.tables[4].cell(idx, 1), item[1], size_pt=11)
    set_cell_text(doc.tables[4].cell(idx, 2), item[2], size_pt=11)
    set_cell_text(doc.tables[4].cell(idx, 3), item[3], size_pt=11, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(doc.tables[4].cell(idx, 4), item[4], size_pt=11)

# ---------------------------------------------------------
# Table 5: Preliminary Pin Mapping
# ---------------------------------------------------------
pins_data = [
    ('UART_TX (Modbus Request)', 'GPIO17', 'Pin 4 (DI) ของ SP3485E (ผ่านพิน 5 ของ CN1)', 'ESP32-S3 Datasheet Table 2-1 (GPIO Matrix) / ยืนยันแล้ว'),
    ('UART_RX (Sensor Response)', 'GPIO16', 'Pin 1 (RO) ของ SP3485E (ผ่านพิน 3 ของ CN1)', 'ESP32-S3 Datasheet Table 2-1 (GPIO Matrix) / ยืนยันแล้ว'),
    ('RS485_DIR (Direction DE/RE)', 'GPIO04', 'Pin 2 (/RE) & Pin 3 (DE) ของ SP3485E (ผ่านพิน 4 ของ CN1)', 'ESP32-S3 Datasheet Table 2-1 (General IO) / ยืนยันแล้ว'),
    ('VCC_3V3 (Logic Power)', '3V3 Rail', 'Pin 8 (VCC) ของ SP3485E (ผ่านพิน 2 ของ CN1)', 'THARIT-IoT Schematic (3.3V LDO Output) / ยืนยันแล้ว'),
    ('VCC_5V (Sensor Power Base)', '5V / VBUS Rail', 'Pin 1 ของ Header J_PWR (ผ่านพิน 1 ของ CN1)', 'THARIT-IoT Schematic (5V USB Power Rail) / ยืนยันแล้ว'),
    ('GND (System Ground)', 'GND Rail', 'Pin 5 (GND) SP3485E, SM712 Pin 3, TB1 Pin 4 (ผ่านพิน 6 CN1)', 'THARIT-IoT Ground Plane / ยืนยันแล้ว')
]

for idx, item in enumerate(pins_data, start=1):
    set_cell_text(doc.tables[5].cell(idx, 0), item[0], bold=True, size_pt=12)
    set_cell_text(doc.tables[5].cell(idx, 1), item[1], bold=True, size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(doc.tables[5].cell(idx, 2), item[2], size_pt=11)
    set_cell_text(doc.tables[5].cell(idx, 3), item[3], size_pt=11)

# ---------------------------------------------------------
# Table 6: วิเคราะห์ Power Domain และความเข้ากันได้
# ---------------------------------------------------------
pwr_data = [
    ('ไฟเลี้ยง ESP32-S3 / Logic IO', (
        '• ไมโครคอนโทรลเลอร์ ESP32-S3 ใช้ไฟเลี้ยงระบบ 3.3V DC ผ่านวงจร On-board Voltage Regulator (LDO) ของบอร์ด THARIT-IoT '
        'ซึ่งแปลงจากไฟ 5V USB (VBUS) โดยวงจรจ่ายกระแสได้อย่างน้อย 500–800 mA เพียงพอต่อการทำงานของ MCU ขณะส่งคลื่นวิทยุ\n'
        '• ระดับแรงดัน Logic IO คือ 3.3V CMOS: V_OH ต่ำสุด 2.64V, V_OL สูงสุด 0.33V พิกัดกระแสขับต่อขา GPIO สูงสุด 40 mA '
        '(แนะนำไม่เกิน 12–20 mA ต่อขา)\n'
        '• อ้างอิง: Espressif ESP32-S3 Datasheet หมวด DC Electrical Characteristics หน้า 45–48'
    )),
    ('ไฟเลี้ยง IC / Module บน Expansion Board', (
        '• ชิป Transceiver SP3485E ทำงานที่แรงดันไฟเลี้ยง 3.3V DC (ช่วงใช้งานปกติ 3.0V ถึง 3.6V) '
        'จึงดึงไฟเลี้ยงโดยตรงจากราง 3V3 ของ ESP32-S3 ผ่านพิน 2 ของ Header CN1\n'
        '• อัตราการกินกระแสต่ำมาก: สภาวะรอรับข้อมูล (Quiescent/Receive mode) ใช้กระแสเพียง 600 µA ถึง 1 mA, '
        'สภาวะขับสัญญาณส่ง (Driver Loaded) ใช้กระแสสูงสุดไม่เกิน 10–15 mA (ไม่ส่งผลกระทบต่อ LDO 3.3V ของบอร์ดหลัก)\n'
        '• มีตัวเก็บประจุ Decoupling C1 (100nF Ceramic SMD 0805) วางชิดขา 8 (VCC) และขา 5 (GND) เพื่อกรองสัญญาณรบกวนความถี่สูง'
    )),
    ('ไฟเลี้ยง Load / External Device', (
        '• เซนเซอร์วัดอุณหภูมิและความชื้น XY-MD02 ต้องการไฟเลี้ยง DC 5V ถึง 30V กินกระแสเฉลี่ย 15–20 mA (< 0.2W)\n'
        '• ออกแบบสถาปัตยกรรม Dual-Source ผ่าน Jumper J_PWR:\n'
        '  - โหมดบอร์ด (เสียบช็อตขา 1-2): รับไฟ 5V DC จากพอร์ต USB ของบอร์ด THARIT-IoT เหมาะสำหรับการทดสอบในห้องแล็บหรือสายสั้น (< 10 เมตร)\n'
        '  - โหมดไฟภายนอก (เสียบช็อตขา 2-3): รับไฟ DC 12V–24V จากภายนอก เหมาะสำหรับการเดินสายระยะไกล (10–100 เมตร) '
        'เพื่อป้องกันปัญหา Voltage Drop และตัดการรบกวนกระแสกระชาก (Inrush current) ไม่ให้ย้อนเข้าบอร์ดหลัก\n'
        '• สายกราวด์ของเซนเซอร์ต่อกลับเข้าสู่ Common Ground Bus ผ่านขั้วต่อ Terminal Block ช่อง 4 เพื่อรักษาศักย์อ้างอิงให้เท่ากัน'
    )),
    ('การป้องกันที่ต้องพิจารณา', (
        '• Overvoltage & ESD Protection: ติดตั้ง TVS Diode SM712 คร่อมระหว่างสาย A+, B- ลงกราวด์ ทนแรงดันไม่สมมาตรตามมาตรฐาน RS-485 '
        '(-7V ถึง +12V) สามารถดูดซับแรงดันไฟฟ้าสถิต ESD ได้สูงถึง ±8 kV (Contact) และ ±15 kV (Air) ตามมาตรฐาน IEC 61000-4-2\n'
        '• Overcurrent & Short-Circuit Protection: ติดตั้ง PTC Resettable Fuse (F1, F2 ขนาด 100mA, 60Vdc) อนุกรมที่สาย A+ และ B- '
        'เพื่อตัดวงจรเมื่อเกิดการต่อสายไฟ 24V ลัดวงจรเข้าสายข้อมูลโดยพลการ และคืนสภาพปกติได้เองเมื่อขจัดจุดลัดวงจร\n'
        '• Bus Idle Stability: ติดตั้งตัวต้านทาน Fail-Safe Bias (R_PU 4.7k ดึงสาย A+ ขึ้น 3.3V และ R_PD 4.7k ดึงสาย B- ลง GND) '
        'ร่วมกับตัวต้านทาน Termination 120 Ω (R_TERM มี Jumper J_TERM เลือกเปิด/ปิด) เพื่อป้องกันสายลอย (Floating Bus) ในสภาวะ Idle'
    )),
    ('ความเข้ากันได้ของ Logic Level', (
        '• ผลการวิเคราะห์: "Compatible สมบูรณ์ 100% โดยตรง ไม่ต้องใช้วงจรแปลงระดับแรงดัน (No Level Shifter Required)"\n'
        '• หลักฐานทางวิศวกรรม:\n'
        '  1. ชิป SP3485E เป็น Transceiver ชนิด 3.3V แท้ มีระดับอินพุต V_IH ขั้นต่ำ 2.0V ซึ่งขา GPIO17 และ GPIO04 ของ ESP32-S3 '
        'ส่งแรงดันระดับสูง (V_OH) ออกมาได้ที่ 2.64V–3.3V จึงตรวจจับสถานะ Logic HIGH ได้อย่างสมบูรณ์\n'
        '  2. สัญญาณตอบกลับจากขา RO ของ SP3485E ส่งแรงดัน V_OH สูงสุดที่ 3.3V ซึ่งอยู่ในพิกัดปลอดภัยของขา GPIO16 ของ ESP32-S3 '
        '(ไม่เกิน Max Rating 3.6V) แตกต่างจากชิปรุ่นเก่าอย่าง MAX485 ที่ใช้ไฟ 5V ซึ่งต้องใช้ Level Shifter แปลงลดแรงดัน'
    ))
]

for idx, item in enumerate(pwr_data, start=1):
    set_cell_text(doc.tables[6].cell(idx, 0), item[0], bold=True, size_pt=12)
    set_cell_text(doc.tables[6].cell(idx, 1), item[1], size_pt=11)

# ---------------------------------------------------------
# Table 8: ตารางประเมินความเสี่ยง (Risk Register)
# ---------------------------------------------------------
risks_data = [
    ('R-01', (
        'การชนกันของข้อมูลบนบัส (Bus Contention) หรือข้อมูลตกหล่น\n'
        'สาเหตุ: เฟิร์มแวร์ ESP32-S3 สลับสถานะขา DE/RE จาก Transmit เป็น Receive เร็วหรือช้าเกินไป '
        'โดยไม่รอให้ข้อมูลในฮาร์ดแวร์ UART Buffer ส่งออกครบ (ขาดคำสั่ง flush)'
    ), (
        'เฟรมคำสั่ง Modbus ขาดหาย ไบต์สุดท้ายถูกตัด หรือไบต์แรกที่ Slave ตอบกลับมาชนกับสถานะขับบัส '
        'ส่งผลให้เกิด CRC Error และไม่สามารถอ่านค่าเซนเซอร์ได้'
    ), (
        'วิธีป้องกัน: ในเฟิร์มแวร์ต้องเรียกคำสั่ง Serial2.flush() ทันทีหลังสิ้นสุดการเขียนข้อมูล '
        'เพื่อให้มั่นใจว่าส่งข้อมูลครบทุกบิตแล้วจึงดึงขา DE ลง LOW (หน่วงเวลา < 1 ms) '
        'พร้อมมีตัวต้านทาน Pulldown R_DE 10 kΩ ทางฮาร์ดแวร์ให้บอร์ดอยู่ในสถานะรับข้อมูลเป็นค่าเริ่มต้นเสมอ'
    )),
    ('R-02', (
        'แรงดันไฟกระชากชั่วขณะและสัญญาณรบกวนเหนี่ยวนำ (Surge / ESD Impulse)\n'
        'สาเหตุ: สายสัญญาณ RS-485 เดินคู่ไปกับท่อร้อยสายไฟ AC หรือติดตั้งภายนอกอาคารที่เสี่ยงต่อฟ้าผ่าใกล้เคียง'
    ), (
        'ชิป Transceiver SP3485E ถูกทำลายถาวร และแรงดันเกินอาจรั่วทะลุผ่านขา DI/RO เข้าสู่พอร์ต GPIO ของ ESP32-S3 ทำให้บอร์ดหลักเสียหาย'
    ), (
        'วิธีป้องกัน: ติดตั้ง TVS Diode SM712 ดักจับแรงดันเกินที่หน้าจุดต่อ Terminal Block โดยตรง '
        'ร่วมกับฟิวส์ PTC 100mA 60V เพื่อจำกัดกระแสเหนี่ยวนำ และจัดวางคู่สาย A+, B- เป็น Differential Pair ตาม IPC-2141'
    )),
    ('R-03', (
        'ปัญหาความต่างศักย์ของกราวด์ (Ground Potential Difference / Ground Loop)\n'
        'สาเหตุ: เซนเซอร์ XY-MD02 ปลายทางใช้ไฟจากแหล่งจ่ายภายนอกโดยไม่มีสายกราวด์อ้างอิงเชื่อมต่อกลับมายังบอร์ดหลัก'
    ), (
        'แรงดัน Common-Mode ข้ามขีดจำกัดสูงสุดของชิป SP3485E (-7V ถึง +12V) ทำให้สัญญาณรับส่งเพี้ยน หรือชิปไหม้เสียหาย'
    ), (
        'วิธีป้องกัน: ต่อสาย Common GND จากพิน 4 ของ Terminal Block ไปยังกราวด์ของเซนเซอร์เสมอ และรักษาบัสกราวด์ให้มีศักย์อ้างอิงเดียวกัน '
        'หากจำเป็นต้องติดตั้งในโรงงานที่มีการรบกวนรุนแรง ในเฟสถัดไปจะพิจารณาใช้โมดูลแบบ Isolated RS-485'
    )),
    ('R-04', (
        'ปัญหาแรงดันตกคร่อมสายไฟ (Voltage Drop บนสาย V+)\n'
        'สาเหตุ: เดินสายเคเบิลไปยังเซนเซอร์ระยะทางยาวเกิน 15–20 เมตร โดยใช้ไฟเลี้ยง 5V จากบอร์ดหลัก'
    ), (
        'แรงดันไฟที่ปลายทางตกต่ำกว่า 4.5V ส่งผลให้วงจรไมโครคอนโทรลเลอร์ภายใน XY-MD02 รีเซ็ตตัวเอง หรือหยุดส่งข้อมูล'
    ), (
        'วิธีป้องกัน: ปรับ Jumper J_PWR สลับไปใช้งานโหมดไฟภายนอก (EXT Mode 12V-24V) ซึ่งเซนเซอร์รองรับไฟได้กว้างถึง 30V '
        'ทำให้แรงดันตกคร่อมในสายไม่มีผลกระทบต่อการทำงาน'
    ))
]

# Table 8 has 4 rows originally (R0: header, R1-R3). We can add a 5th row for R-04!
# Check row count
while len(doc.tables[8].rows) < 5:
    doc.tables[8].add_row()

for idx, item in enumerate(risks_data, start=1):
    set_cell_text(doc.tables[8].cell(idx, 0), item[0], bold=True, size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(doc.tables[8].cell(idx, 1), item[1], size_pt=11)
    set_cell_text(doc.tables[8].cell(idx, 2), item[2], size_pt=11)
    set_cell_text(doc.tables[8].cell(idx, 3), item[3], size_pt=11)

# ---------------------------------------------------------
# Table 9: แผนทดสอบและหลักฐานที่ต้องเก็บในอนาคต (Verification Plan)
# ---------------------------------------------------------
tests_data = [
    ('TC-01 / REQ-RS485-01', (
        'ทดสอบส่งเฟรม Modbus RTU Read Input Registers (01 04 00 01 00 02 20 0B) ที่ความเร็ว 9,600 bps จาก ESP32-S3 '
        'และตรวจจับเฟรมข้อมูลตอบกลับผ่าน Serial Monitor และ Logic Analyzer'
    ), (
        'เฟรมตอบกลับมีความถูกต้องตามมาตรฐาน Modbus RTU, ค่า Checksum CRC-16 ถูกต้อง, '
        'ค่าอุณหภูมิและความชื้นที่แปลงได้สมเหตุสมผล (เช่น Temp 25-35 °C, Humidity 40-70 %RH)'
    ), (
        'Not Tested\n'
        'หลักฐานที่วางแผนเก็บ: ภาพหน้าจอ Serial Monitor แสดงค่า Raw Hex Data (Request & Response) '
        'และตารางบันทึกค่าอุณหภูมิ/ความชื้นเทียบกับเครื่องวัดอ้างอิง'
    )),
    ('TC-02 / REQ-RS485-02', (
        'วัดเวลาหน่วงการสลับทิศทาง Half-Duplex (Direction Switching Latency) ของขา DE/RE เทียบกับรูปคลื่นข้อมูล TX และ RX '
        'โดยใช้ Digital Storage Oscilloscope (DSO 2 ช่องสัญญาณ)'
    ), (
        'เวลาสลับสถานะจาก TX เป็น RX (DE เปลี่ยนจาก HIGH เป็น LOW) ต้องเกิดขึ้นภายในเวลาไม่เกิน 2.0 ms '
        'และขา DE ต้องลง LOW ก่อนที่บิตแรกของ Slave Response จะมาถึง'
    ), (
        'Not Tested\n'
        'หลักฐานที่วางแผนเก็บ: รูปถ่ายรูปคลื่นสัญญาณ Oscilloscope แสดงจังหวะตกของสัญญาณ DE เทียบกับจุดเริ่มต้นของเฟรมตอบกลับ (Delta t < 2ms)'
    )),
    ('TC-03 / REQ-RS485-03', (
        'วัดระดับแรงดันไฟฟ้ากระแสตรง (DC Voltage Level) ที่จุดเชื่อมต่อ Header 1x6 (3.3V, 5V, TX, RX, DE) '
        'และวัดแรงดันผลต่าง |V_OD| บนสายบัส A+ และ B- ด้วย Digital Multimeter'
    ), (
        '• ขาตรรกะดิจิทัลทุกขาต้องมีแรงดันอยู่ในช่วง 3.0V ถึง 3.3V (ไม่เกิน 3.6V)\n'
        '• สภาวะ Idle: สาย A+ ต้องมีศักย์สูงกว่า B- อย่างน้อย 200 mV ด้วยอิทธิพลของวงจร Fail-safe Bias'
    ), (
        'Not Tested\n'
        'หลักฐานที่วางแผนเก็บ: ตารางบันทึกค่าแรงดันไฟฟ้าที่วัดได้จริงทุกพิน พร้อมภาพถ่ายการวัดด้วยเครื่อง Digital Multimeter ในแล็บ'
    )),
    ('TC-04 / REQ-RS485-05', (
        'ตรวจสอบความต่อเนื่องทางไฟฟ้า (Continuity Check) และความปลอดภัยของวงจรป้องกัน TVS SM712 และฟิวส์ PTC 100mA '
        'บนแผ่น PCB ก่อนต่อไฟเข้าสู่ระบบ'
    ), (
        '• ฟิวส์ F1, F2 มีค่าความต้านทานต่ำ < 2.0 Ω ในสภาวะปกติ\n'
        '• ขา TVS Diode SM712 ไม่ช็อตลงกราวด์ในสภาวะแรงดันปกติ (ความต้านทานระดับ Mega-ohm)\n'
        '• ไม่มีการลัดวงจรระหว่างสาย V+, A+, B- และ GND'
    ), (
        'Not Tested\n'
        'หลักฐานที่วางแผนเก็บ: ตารางผลการทดสอบการไม่ช็อตข้ามขั้ว (Point-to-Point Continuity Matrix) และภาพถ่ายการตรวจสอบบอร์ด PCB'
    ))
]

while len(doc.tables[9].rows) < 5:
    doc.tables[9].add_row()

for idx, item in enumerate(tests_data, start=1):
    set_cell_text(doc.tables[9].cell(idx, 0), item[0], bold=True, size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(doc.tables[9].cell(idx, 1), item[1], size_pt=11)
    set_cell_text(doc.tables[9].cell(idx, 2), item[2], size_pt=11)
    set_cell_text(doc.tables[9].cell(idx, 3), item[3], size_pt=11)

# ---------------------------------------------------------
# Table 10: คำถามสะท้อนคิด ก.
# ---------------------------------------------------------
t10_answer = (
    'จากโครงสร้างทั้งระบบ จุดเชื่อมต่อที่มีความเสี่ยงสูงที่สุดคือ "ขั้วต่อ Industrial Screw Terminal Block 4 ช่อง '
    '[1:V+, 2:A+, 3:B-, 4:GND]" ฝั่งที่เชื่อมต่อออกไปยังสายเคเบิลของเซนเซอร์ภายนอกอาคาร\n'
    'เหตุผลทางวิศวกรรม:\n'
    '1. เป็นจุดรอยต่อ (System Boundary) ที่ต้องเผชิญกับสภาพแวดล้อมทางกายภาพจริงภายนอกบอร์ด ซึ่งมีความเสี่ยงสูงต่อการถูกเหนี่ยวนำ '
    'จากสัญญาณรบกวนคลื่นแม่เหล็กไฟฟ้า (EMI), ไฟกระชากจากแรงดันไฟฟ้าสถิต (ESD), และปรากฏการณ์ Ground Potential Difference '
    'จากการที่เซนเซอร์อยู่ห่างไกล\n'
    '2. มีความเสี่ยงต่อความผิดพลาดของผู้ใช้งาน (Human Error) ในการขันสายไฟ เช่น การต่อสลับขั้ว หรือการนำสายไฟเลี้ยง 24V ลัดวงจรเข้าสายข้อมูล A+ หรือ B-\n'
    'แนวทางลดความเสี่ยงที่ออกแบบไว้:\n'
    '• ติดตั้งวงจรป้องกันหลายระดับ (Multi-stage Protection) ประกอบด้วย TVS Diode SM712 ทนแรงดันไม่สมมาตร (-7V ถึง +12V) ดักจับ Transient Voltage '
    'และฟิวส์ PTC Resettable 100mA 60V ตัดกระแสเกินเมื่อเกิดการช็อตสาย\n'
    '• จัดลำดับพินขั้วต่อแบบ [1:V+, 2:A+, 3:B-, 4:GND] เพื่อให้คู่สายข้อมูล A+/B- อยู่ตรงกลางชิดกันเป็น Differential Pair ตามมาตรฐาน IPC-2141 '
    'และสกรีน Silkscreen ระบุขั้ว สีสายของเซนเซอร์ (แดง, เหลือง, ขาว, ดำ) อย่างชัดเจนบนหน้าบอร์ด'
)
set_cell_text(doc.tables[10].cell(1, 0), t10_answer, size_pt=12)

# ---------------------------------------------------------
# Table 11: คำถามสะท้อนคิด ข.
# ---------------------------------------------------------
t11_answer = (
    'ก่อนลงมือเริ่มออกแบบผังวงจร Schematic มีข้อมูลทางเทคนิคที่ต้องตรวจสอบยืนยันเพิ่มเติม 3 ประเด็นหลัก โดยอ้างอิงเอกสารดังนี้:\n'
    '1. การตรวจสอบขา Pinout & Internal Multiplexing บนบอร์ด ESP32-S3 จริง: ต้องยืนยันว่าขา GPIO17, GPIO16 และ GPIO04 '
    'ที่กลุ่มเลือกใช้ ไม่ได้ถูกดึงไปเชื่อมต่อกับอุปกรณ์ออนบอร์ดอื่นๆ บนบอร์ด THARIT-IoT (เช่น ชิปจอแสดงผล, โมดูลสื่อสารอื่น, หรือ LED บนบอร์ด) '
    'และไม่ได้ชนกับระบบ Octal PSRAM ของ ESP32-S3 ในโมดูลรุ่นเฉพาะ โดยตรวจยืนยันจาก "THARIT-IoT Mainboard Schematic Diagram" '
    'และ "ESP32-S3 Hardware Design Guidelines (Espressif Systems)"\n'
    '2. การตรวจสอบขนาด Footprint และพิกัดกระแสจริงของอุปกรณ์ SMD ในแล็บ: ต้องตรวจสอบสเปกของ Screw Terminal Block 3.81mm, '
    'TVS Diode SM712 (ตัวถัง SOT-23), ชิป SP3485E (ตัวถัง SOIC-8) และตัวต้านทาน SMD 0805 ให้มีขนาดแพ็กเกจตรงกับอุปกรณ์ที่มีอยู่จริงในสต็อกห้องปฏิบัติการ '
    'โดยตรวจยืนยันจาก "Manufacturer Datasheet & Package Dimensions" ของอุปกรณ์แต่ละเบอร์\n'
    '3. คุณสมบัติการทนกระแสและแรงดันของฟิวส์ PTC 100mA: ต้องตรวจเช็กค่า Trip Current และเวลาในการตัดวงจร (Time-to-Trip) '
    'เทียบกับกระแสสูงสุดที่ไดโอด SM712 สามารถทนได้ เพื่อให้แน่ใจว่าฟิวส์จะตัดวงจรก่อนที่ไดโอดหรือชิป SP3485E จะเกิดความร้อนสะสมจนเสียหาย '
    'โดยตรวจยืนยันจาก "Bourns/Littlefuse PPTC Resettable Fuse Datasheet"'
)
set_cell_text(doc.tables[11].cell(1, 0), t11_answer, size_pt=12)

# ---------------------------------------------------------
# Table 12: คำถามสะท้อนคิด ค.
# ---------------------------------------------------------
t12_answer = (
    'บทบาทหน้าที่และความรับผิดชอบในวันนี้:\n'
    'ในกิจกรรมวันนี้ ข้าพเจ้า (นายชัชวาล ตาจา) ปฏิบัติหน้าที่ในฐานะ "System Architect & Requirements Lead" รับผิดชอบการวิเคราะห์ภาพรวมของระบบ '
    'สืบเนื่องจากใบงานที่ 2 โดยเป็นผู้ออกแบบการเชื่อมต่อ Hardware Interface Design และ Preliminary Pin Mapping ระหว่างโมดูลขยาย RS-485 '
    'กับบอร์ดหลัก ESP32-S3 (THARIT-IoT) วิเคราะห์การจัดการ Power Domain และความเข้ากันได้ของระดับแรงดันตรรกะ 3.3V '
    'จัดทำตารางประเมินความเสี่ยงเชิงวิศวกรรม (Risk Register) และกำหนด Verification Plan & Test Cases เพื่อรองรับการทดสอบในอนาคตอย่างเป็นระบบ\n'
    'สิ่งที่ตั้งใจปรับปรุงในการทำงานคาบถัดไป:\n'
    '1. การประสานงานเชิงลึกกับสมาชิกฝ่าย Hardware Schematic: จะจัดทำเอกสารสรุป Pinout Netlist และรายละเอียด Footprint ส่งต่อให้เพื่อนร่วมกลุ่ม '
    'ที่รับผิดชอบการวาด Schematic ในโปรแกรม EDA ได้อย่างแม่นยำ ไร้ข้อผิดพลาด เพื่อให้การขึ้นผังวงจรเป็นไปอย่างราบรื่น\n'
    '2. การเตรียมการด้าน Timing ใน Firmware: วางแผนร่วมกับฝ่าย Firmware Engineer เพื่อเตรียมฟังก์ชันการสลับขา DE/RE ของ ESP32-S3 '
    'ให้มีประสิทธิภาพสูงสุด รองรับ Baud rate ได้ตั้งแต่ 9,600 bps จนถึง 115,200 bps ตาม Requirement ที่กำหนดไว้'
)
set_cell_text(doc.tables[12].cell(1, 0), t12_answer, size_pt=12)

# Save document
doc.save(out_path)
print(f'Saved completed worksheet to: {out_path}')

