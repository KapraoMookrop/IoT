import os
import math
from PIL import Image, ImageDraw, ImageFont

# Canvas: 1920 x 1080 (Full HD Technical Infographic)
W, H = 1920, 1080
bg_color = (20, 22, 30)  # Premium Dark Graphite

canvas = Image.new("RGB", (W, H), bg_color)
draw = ImageDraw.Draw(canvas)

font_dir = "C:/Windows/Fonts"
font_title = ImageFont.truetype(os.path.join(font_dir, "tahomabd.ttf"), 24)
font_subtitle = ImageFont.truetype(os.path.join(font_dir, "tahoma.ttf"), 14)
font_card_title = ImageFont.truetype(os.path.join(font_dir, "tahomabd.ttf"), 16)
font_text = ImageFont.truetype(os.path.join(font_dir, "tahoma.ttf"), 13)
font_bold = ImageFont.truetype(os.path.join(font_dir, "tahomabd.ttf"), 13)
font_badge = ImageFont.truetype(os.path.join(font_dir, "tahomabd.ttf"), 11)

# Load existing images
im_pcb = Image.open(r"d:\Iven\IoT\tharit_rs485_module_render_3d.jpg")
im_sys = Image.open(r"d:\Iven\IoT\tharit_iot_rs485_system_simulation.jpg")

# 1. Subtle Engineering Grid Pattern
for x in range(0, W, 40):
    draw.line([(x, 80), (x, H - 40)], fill=(28, 32, 44), width=1)
for y in range(80, H - 40, 40):
    draw.line([(0, y), (W, y)], fill=(28, 32, 44), width=1)

# 2. Header Bar
draw.rectangle([0, 0, W, 75], fill=(14, 16, 22))
draw.line([(0, 75), (W, 75)], fill=(0, 200, 255), width=2)

draw.text((30, 14), "แผนผังเส้นทางไฟและสัญญาณเสมือนจริง (Photorealistic Power & Signal Routing Flow)", font=font_title, fill=(255, 255, 255))
draw.text((32, 48), "การเชื่อมต่อระบบ: THARIT-IoT Mainboard  ◄[Header Pins ด้านล่าง]►  RS-485 Extension Module  ◄[Terminal 4 พิน]►  XY-MD02 (SHT20)", font=font_subtitle, fill=(0, 215, 255))

# Top Right Legend
legends = [
    ("สัญญาณ UART & ควบคุม", (0, 210, 255)),
    ("RS-485 Differential", (0, 230, 140)),
    ("ไฟบอร์ด 5V", (255, 75, 75)),
    ("ไฟนอก 12V-24V", (255, 175, 0)),
    ("กราวด์ GND", (150, 155, 175))
]
lx = 1060
for name, col in legends:
    draw.rounded_rectangle([lx, 26, lx+16, 44], radius=3, fill=col)
    draw.text((lx+22, 28), name, font=font_badge, fill=(235, 240, 250))
    lx += 165

# -------------------------------------------------------------
# 3. HARDWARE COMPONENTS PLACEMENT
# -------------------------------------------------------------

# A) External Power Supply Card (Top-Left)
pwr_x, pwr_y, pwr_w, pwr_h = 35, 95, 480, 395
draw.rounded_rectangle([pwr_x, pwr_y, pwr_x + pwr_w, pwr_y + pwr_h], radius=14, fill=(22, 25, 35), outline=(255, 175, 0), width=2)
draw.rounded_rectangle([pwr_x, pwr_y, pwr_x + pwr_w, pwr_y + 38], radius=8, fill=(65, 45, 10))
draw.text((pwr_x + 15, pwr_y + 9), "⚡ แหล่งจ่ายไฟภายนอก (DC 12V - 24V Power Supply)", font=font_card_title, fill=(255, 210, 50))

draw.text((pwr_x + 18, pwr_y + 50), "• ใช้เมื่อเดินสายเคเบิลเซนเซอร์ระยะไกล (> 15 เมตร) เพื่อกันไฟตก", font=font_text, fill=(220, 220, 235))

# Power Mockup
draw.rounded_rectangle([pwr_x + 20, pwr_y + 78, pwr_x + 230, pwr_y + 165], radius=8, fill=(30, 34, 46), outline=(255, 175, 0), width=1)
draw.text((pwr_x + 35, pwr_y + 88), "อะแดปเตอร์ DC 12V-24V", font=font_bold, fill=(255, 255, 255))
draw.rounded_rectangle([pwr_x + 35, pwr_y + 118, pwr_x + 115, pwr_y + 152], radius=5, fill=(220, 50, 50))
draw.text((pwr_x + 44, pwr_y + 126), "+12V/+24V", font=font_badge, fill=(255, 255, 255))
draw.rounded_rectangle([pwr_x + 125, pwr_y + 118, pwr_x + 205, pwr_y + 152], radius=5, fill=(60, 65, 80))
draw.text((pwr_x + 144, pwr_y + 126), "GND (-)", font=font_badge, fill=(255, 255, 255))

# Instruction guide box
draw.rounded_rectangle([pwr_x + 15, pwr_y + 180, pwr_x + pwr_w - 15, pwr_y + 380], radius=8, fill=(26, 23, 18), outline=(255, 175, 0), width=1)
draw.text((pwr_x + 25, pwr_y + 190), "📌 กฎการเลือกแหล่งจ่ายไฟ (Jumper J2 บน PCB):", font=font_bold, fill=(255, 210, 50))
draw.text((pwr_x + 25, pwr_y + 218), "• แบบที่ 1 (ใช้ไฟบอร์ด 5V): เสียบ J2 ช็อตขา 1-2", font=font_bold, fill=(255, 100, 100))
draw.text((pwr_x + 25, pwr_y + 238), "  ดึงไฟ 5V บอร์ดหลัก จ่ายออกสาย V+ ทันที (เทสในแล็บ)", font=font_text, fill=(230, 230, 240))
draw.text((pwr_x + 25, pwr_y + 265), "• แบบที่ 2 (ใช้ไฟนอก EXT): เสียบ J2 ช็อตขา 2-3", font=font_bold, fill=(255, 195, 0))
draw.text((pwr_x + 25, pwr_y + 285), "  ต่อสายบวก 12-24V เข้าพิน 3 ของ J2 จ่ายออกสาย V+", font=font_text, fill=(230, 230, 240))
draw.text((pwr_x + 25, pwr_y + 312), "• แบบที่ 3 (ต่อตรงหน้างาน): ต่อไฟ 12-24V เข้าหัวสายแดง", font=font_bold, fill=(120, 220, 255))
draw.text((pwr_x + 25, pwr_y + 332), "  ของ XY-MD02 โดยตรง แล้วถอด Jumper J2 ออกได้เลย", font=font_text, fill=(230, 230, 240))
draw.text((pwr_x + 25, pwr_y + 355), "  *หมายเหตุ: สายลบ (GND) ต้องต่อร่วมเข้าช่อง GND บอร์ดเสมอ", font=font_badge, fill=(170, 180, 200))


# B) THARIT-IoT Mainboard (Bottom-Left)
esp_crop = im_sys.crop((280, 500, 830, 740))
esp_w = 480
esp_h = int(esp_crop.height * (esp_w / esp_crop.width))
esp_resized = esp_crop.resize((esp_w, esp_h), Image.Resampling.LANCZOS)
esp_x, esp_y = 35, 520

draw.rounded_rectangle([esp_x, esp_y, esp_x + esp_w, esp_y + esp_h + 38], radius=14, fill=(22, 25, 35), outline=(100, 140, 255), width=2)
draw.rounded_rectangle([esp_x, esp_y, esp_x + esp_w, esp_y + 36], radius=8, fill=(30, 45, 80))
draw.text((esp_x + 15, esp_y + 8), "🖥️ บอร์ดหลัก THARIT-IoT (ESP32-S3 Master Node)", font=font_card_title, fill=(255, 255, 255))
canvas.paste(esp_resized, (esp_x, esp_y + 36))


# C) RS-485 Extension Module (Center)
pcb_w = 660
pcb_h = int(im_pcb.height * (pcb_w / im_pcb.width))
im_pcb_resized = im_pcb.resize((pcb_w, pcb_h), Image.Resampling.LANCZOS)
pcb_x, pcb_y = 545, 185

draw.rounded_rectangle([pcb_x - 12, pcb_y - 12, pcb_x + pcb_w + 12, pcb_y + pcb_h + 12], radius=14, fill=(22, 25, 35), outline=(0, 200, 255), width=2)
canvas.paste(im_pcb_resized, (pcb_x, pcb_y))

# Top Badge on PCB
draw.rounded_rectangle([pcb_x + 10, pcb_y + 10, pcb_x + 360, pcb_y + 38], radius=6, fill=(10, 12, 18, 230), outline=(0, 200, 255), width=1)
draw.text((pcb_x + 20, pcb_y + 14), "RS-485 EXTENSION MODULE (แผ่น PCB ของเรา)", font=font_bold, fill=(0, 220, 255))


# D) XY-MD02 Sensor (Top-Right)
sensor_crop = im_sys.crop((970, 480, 1230, 730))
sens_w = 460
sens_h = int(sensor_crop.height * (sens_w / sensor_crop.width))
sens_resized = sensor_crop.resize((sens_w, sens_h), Image.Resampling.LANCZOS)
sens_x, sens_y = 1420, 95

draw.rounded_rectangle([sens_x, sens_y, sens_x + sens_w, sens_y + sens_h + 38], radius=14, fill=(22, 25, 35), outline=(0, 230, 140), width=2)
draw.rounded_rectangle([sens_x, sens_y, sens_x + sens_w, sens_y + 36], radius=8, fill=(15, 55, 40))
draw.text((sens_x + 15, sens_y + 8), "🌡️ เซนเซอร์วัดอุณหภูมิ-ความชื้น XY-MD02 (SHT20)", font=font_card_title, fill=(0, 240, 150))
canvas.paste(sens_resized, (sens_x, sens_y + 36))


# E) Sensor Cable Pinout Card (Bottom-Right)
sw_x, sw_y, sw_w, sw_h = sens_x, sens_y + sens_h + 55, sens_w, 360
draw.rounded_rectangle([sw_x, sw_y, sw_x + sw_w, sw_y + sw_h], radius=14, fill=(22, 25, 35), outline=(0, 220, 255), width=2)
draw.rounded_rectangle([sw_x, sw_y, sw_x + sw_w, sw_y + 36], radius=8, fill=(15, 45, 65))
draw.text((sw_x + 15, sw_y + 8), "🔌 ขั้วต่อสายเคเบิล 4 เส้นจากตัวเซนเซอร์ XY-MD02", font=font_card_title, fill=(0, 230, 255))

cable_defs = [
    ("สายสีแดง (V+)", "ไฟเลี้ยงเซนเซอร์ (DC 5V - 30V)", (255, 75, 75), "ขันเข้าช่อง 1: V+"),
    ("สายสีดำ (GND)", "กราวด์ระบบไฟเลี้ยงและสัญญาณ", (160, 165, 185), "ขันเข้าช่อง 2: GND"),
    ("สายสีเหลือง (A+)", "RS-485 Data+ (Non-inverting)", (255, 215, 0), "ขันเข้าช่อง 3: A+"),
    ("สายสีเขียว (B-)", "RS-485 Data- (Inverting)", (0, 230, 120), "ขันเข้าช่อง 4: B-")
]
cy = sw_y + 52
for cname, cdesc, ccolor, cpin in cable_defs:
    draw.rounded_rectangle([sw_x + 15, cy, sw_x + 160, cy + 30], radius=5, fill=ccolor)
    text_color = (0, 0, 0) if ccolor in [(255, 215, 0), (0, 230, 120)] else (255, 255, 255)
    draw.text((sw_x + 22, cy + 6), cname, font=font_bold, fill=text_color)
    draw.text((sw_x + 175, cy + 1), cdesc, font=font_text, fill=(240, 240, 250))
    draw.text((sw_x + 175, cy + 17), "➔ " + cpin, font=font_badge, fill=(0, 210, 255))
    cy += 46

draw.rounded_rectangle([sw_x + 15, cy + 8, sw_x + sw_w - 15, sw_y + sw_h - 15], radius=6, fill=(28, 33, 46))
draw.text((sw_x + 25, cy + 18), "• โปรโตคอลสื่อสาร: Modbus RTU Master/Slave (9,600 bps)", font=font_text, fill=(225, 230, 245))
draw.text((sw_x + 25, cy + 40), "• ส่งด้วย Differential Voltage (A+ เทียบกับ B-) ทนทานคลื่นกวน EMI", font=font_text, fill=(225, 230, 245))
draw.text((sw_x + 25, cy + 62), "• เดินสายคู่ตีเกลียว (Twisted Pair) ได้ไกลสูงสุด 1,200 เมตร", font=font_bold, fill=(0, 230, 150))


# -------------------------------------------------------------
# 4. PRECISE SIGNAL & POWER FLOW DRAWING
# -------------------------------------------------------------

def draw_flow_arrow(points, color, width=3, is_dashed=False):
    if is_dashed:
        for i in range(len(points)-1):
            p1, p2 = points[i], points[i+1]
            dx, dy = p2[0]-p1[0], p2[1]-p1[1]
            dist = math.hypot(dx, dy)
            if dist == 0: continue
            ux, uy = dx/dist, dy/dist
            curr = 0
            while curr < dist:
                end = min(curr + 7, dist)
                draw.line([(p1[0]+ux*curr, p1[1]+uy*curr), (p1[0]+ux*end, p1[1]+uy*end)], fill=color, width=width)
                curr += 13
    else:
        for i in range(len(points)-1):
            draw.line([points[i], points[i+1]], fill=color, width=width)
            
    p_last = points[-1]
    p_prev = points[-2]
    ang = math.atan2(p_last[1]-p_prev[1], p_last[0]-p_prev[0])
    l = 10
    tip = p_last
    left = (tip[0] - l*math.cos(ang - 0.4), tip[1] - l*math.sin(ang - 0.4))
    right = (tip[0] - l*math.cos(ang + 0.4), tip[1] - l*math.sin(ang + 0.4))
    draw.polygon([tip, left, right], fill=color)

# Physical Pins on Resized PCB:
j2_x = pcb_x + 138
j2_y = pcb_y + 155

hdr_x = pcb_x + 410
hdr_y = pcb_y + 325

term_x = pcb_x + 515
term_y = pcb_y + 130


# CALLOUT 1: J2 (PWR SEL) at top center (y = 95 .. 165)
draw.rounded_rectangle([pcb_x + 20, 95, pcb_x + 480, 168], radius=8, fill=(16, 20, 30, 245), outline=(255, 175, 0), width=2)
draw.text((pcb_x + 35, 102), "⚡ จัมเปอร์ J2 (PWR SEL): เลือกแหล่งจ่ายไฟให้เซนเซอร์", font=font_bold, fill=(255, 195, 0))
draw.text((pcb_x + 35, 124), "• ขา 1-2: ไฟ 5V จากบอร์ดหลัก THARIT-IoT (วิ่งขึ้นมาจาก Header ด้านล่าง)", font=font_badge, fill=(255, 100, 100))
draw.text((pcb_x + 35, 144), "• ขา 2-3: ไฟภายนอก DC 12V-24V (สำหรับลากสายเซนเซอร์ระยะไกล)", font=font_badge, fill=(255, 195, 0))

# Line from J2 Callout down to J2 pin
draw.line([(pcb_x + 140, 168), (j2_x, j2_y)], fill=(255, 175, 0), width=2)
draw.ellipse([j2_x-4, j2_y-4, j2_x+4, j2_y+4], fill=(255, 175, 0))

# External DC arrow to J2
draw_flow_arrow([(pwr_x + pwr_w - 15, pwr_y + 135), (j2_x, pwr_y + 135), (j2_x, j2_y - 15)], (255, 175, 0), width=3, is_dashed=True)


# CALLOUT 2: Terminal Block 4-pin (Right of PCB)
# Screws positions on terminal block:
# Channel 1: V+ (Red)
# Channel 2: GND (Black)
# Channel 3: A+ (Yellow)
# Channel 4: B- (Green)
screw_v = (term_x + 10, pcb_y + 80)
screw_g = (term_x + 25, pcb_y + 115)
screw_a = (term_x + 40, pcb_y + 148)
screw_b = (term_x + 55, pcb_y + 180)

# Wire 1: V+ (Red) -> Card
draw_flow_arrow([screw_v, (1370, pcb_y + 80), (1370, sw_y + 66), (sw_x + 15, sw_y + 66)], (255, 75, 75), width=3)
# Wire 2: GND (Black/Grey) -> Card
draw_flow_arrow([screw_g, (1350, pcb_y + 115), (1350, sw_y + 112), (sw_x + 15, sw_y + 112)], (160, 165, 185), width=3)
# Wire 3: A+ (Yellow) -> Card
draw_flow_arrow([screw_a, (1330, pcb_y + 148), (1330, sw_y + 158), (sw_x + 15, sw_y + 158)], (255, 215, 0), width=3)
# Wire 4: B- (Green) -> Card
draw_flow_arrow([screw_b, (1310, pcb_y + 180), (1310, sw_y + 204), (sw_x + 15, sw_y + 204)], (0, 230, 120), width=3)

# Highlight ring around Terminal Block
draw.rounded_rectangle([term_x - 15, pcb_y + 55, term_x + 65, pcb_y + 205], radius=6, outline=(0, 255, 140), width=2)
draw.text((term_x - 135, pcb_y + 70), "ขั้วต่อ Screw\nTerminal 4 พิน\n(สีเขียว)", font=font_bold, fill=(0, 255, 140))


# CALLOUT 3: Expansion Header Pins (Bottom of PCB)
# Arrow coming up from THARIT-IoT to Header pins
draw_flow_arrow([(esp_x + esp_w - 40, esp_y + 60), (hdr_x, esp_y + 60), (hdr_x, hdr_y + 20)], (0, 210, 255), width=4)

# Callout Card for Header Pins (placed at bottom center)
hp_card_x, hp_card_y, hp_card_w, hp_card_h = 545, 570, 660, 200
draw.rounded_rectangle([hp_card_x, hp_card_y, hp_card_x + hp_card_w, hp_card_y + hp_card_h], radius=10, fill=(16, 20, 30, 245), outline=(0, 210, 255), width=2)
draw.text((hp_card_x + 20, hp_card_y + 12), "🔗 ขาสัญญาณและไฟเลี้ยงที่ส่งไปบอร์ดหลัก (Expansion Header Pins แถวทองด้านล่าง)", font=font_bold, fill=(0, 220, 255))
draw.text((hp_card_x + 20, hp_card_y + 36), "โมดูลเสียบประกบ (Stack Shield) ตรงเข้ากับ THARIT-IoT โดยขาสัญญาณและไฟจะเชื่อมต่อกันโดยตรง:", font=font_text, fill=(230, 235, 245))

hp_items = [
    ("• ขา TXD (ส่ง):", "รับคำสั่งจาก GPIO17 ของ ESP32 เข้าขา DI ของ SP3485 เพื่อแปลงส่งออก RS-485", (255, 215, 0)),
    ("• ขา RXD (รับ):", "ส่งข้อมูลที่ SP3485 แปลงได้ (RO) กลับเข้า GPIO16 ของ ESP32 ไร้ตัวแบ่งแรงดัน", (0, 230, 150)),
    ("• ขา DE/RE (คุมทิศทาง):", "ต่อกับ GPIO04 ของ ESP32 ควบคุมสลับโหมดส่ง (High) หรือ รับ (Low) ภายใน < 2 ms", (255, 130, 220)),
    ("• ไฟ 3.3V & GND:", "รับไฟตรรกะ 3.3V จากบอร์ดหลักมาเลี้ยงชิป SP3485 พร้อมกราวด์ร่วมระบบ", (120, 220, 255)),
    ("• ไฟ 5V (จากบอร์ด):", "รับไฟ 5V บอร์ดหลัก วิ่งขึ้นมาเข้าจัมเปอร์ J2 (พิน 1) เพื่อจ่ายออกเซนเซอร์ต่อไป", (255, 90, 90))
]
h_item_y = hp_card_y + 62
for title_t, desc_t, col_t in hp_items:
    draw.text((hp_card_x + 20, h_item_y), title_t, font=font_bold, fill=col_t)
    draw.text((hp_card_x + 180, h_item_y), desc_t, font=font_text, fill=(225, 230, 240))
    h_item_y += 24

# Pointer line from Header Card up to Header pins
draw.line([(hp_card_x + 330, hp_card_y), (hdr_x, hdr_y)], fill=(0, 210, 255), width=2)
draw.ellipse([hdr_x-4, hdr_y-4, hdr_x+4, hdr_y+4], fill=(0, 210, 255))


# Footer Bar
draw.rectangle([0, H - 35, W, H], fill=(14, 16, 22))
draw.text((30, H - 25), "ผู้ออกแบบ / สถาปัตยกรรมฮาร์ดแวร์: ชัชวาล ตาจา (Chatchawan Taja) | โครงการ RS-485 Industrial Extension Module", font=font_badge, fill=(150, 155, 175))
draw.text((W - 460, H - 25), "มาตรฐานอุตสาหกรรม Half-Duplex RS-485 / Modbus RTU", font=font_badge, fill=(0, 210, 255))

out_path = r"d:\Iven\IoT\photorealistic_wiring_power_signal_flow.png"
canvas.save(out_path, quality=95)
print("Saved cleanly refined photorealistic wiring flow to:", out_path)
