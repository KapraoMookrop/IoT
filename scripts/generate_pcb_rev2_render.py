import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# 2x Supersampling for ultra-sharp rendering
SCALE = 2
W, H = 1920 * SCALE, 1080 * SCALE

BG_COLOR = (18, 20, 26)
canvas = Image.new("RGBA", (W, H), BG_COLOR)
draw = ImageDraw.Draw(canvas)

font_dir = "C:/Windows/Fonts"
font_title = ImageFont.truetype(os.path.join(font_dir, "tahomabd.ttf"), 26 * SCALE)
font_subtitle = ImageFont.truetype(os.path.join(font_dir, "tahoma.ttf"), 15 * SCALE)
font_section = ImageFont.truetype(os.path.join(font_dir, "tahomabd.ttf"), 16 * SCALE)
font_bold = ImageFont.truetype(os.path.join(font_dir, "tahomabd.ttf"), 13 * SCALE)
font_text = ImageFont.truetype(os.path.join(font_dir, "tahoma.ttf"), 12 * SCALE)
font_pin_label = ImageFont.truetype(os.path.join(font_dir, "tahomabd.ttf"), 14 * SCALE)
font_ic_text = ImageFont.truetype(os.path.join(font_dir, "tahomabd.ttf"), 11 * SCALE)
font_badge = ImageFont.truetype(os.path.join(font_dir, "tahomabd.ttf"), 11 * SCALE)

# 1. Subtle Engineering Grid
grid_step = 40 * SCALE
for x in range(0, W, grid_step):
    draw.line([(x, 80 * SCALE), (x, H - 40 * SCALE)], fill=(26, 29, 38), width=1 * SCALE)
for y in range(80 * SCALE, H - 40 * SCALE, grid_step):
    draw.line([(0, y), (W, y)], fill=(26, 29, 38), width=1 * SCALE)

# 2. Header Bar
draw.rectangle([0, 0, W, 75 * SCALE], fill=(12, 14, 18))
draw.line([(0, 75 * SCALE), (W, 75 * SCALE)], fill=(0, 200, 255), width=2 * SCALE)

draw.text((35 * SCALE, 14 * SCALE), "RS-485 COMPACT EXTENSION MODULE — HARDWARE REVISION v2.0", font=font_title, fill=(255, 255, 255))
draw.text((38 * SCALE, 48 * SCALE), "ออกแบบใหม่: ตัดขาหลอกทิ้งทั้งหมด • สกรีนชื่อขา ESP32 เด่นชัด 6 พิน • ระบุขั้วไฟ 5V/EXT ชัดเจน 100%", font=font_subtitle, fill=(0, 215, 255))

# Top Right Status Badge
draw.rounded_rectangle([W - 320 * SCALE, 18 * SCALE, W - 40 * SCALE, 56 * SCALE], radius=8 * SCALE, fill=(0, 40, 60), outline=(0, 200, 255), width=1 * SCALE)
draw.text((W - 305 * SCALE, 27 * SCALE), "STATUS: PRODUCTION READY v2.0", font=font_bold, fill=(0, 240, 255))

# 3. PCB BOARD RENDERING
pcb_w = 980 * SCALE
pcb_h = 650 * SCALE
pcb_cx = W // 2 - 20 * SCALE
pcb_cy = H // 2 + 10 * SCALE
pcb_x1 = pcb_cx - pcb_w // 2
pcb_y1 = pcb_cy - pcb_h // 2
pcb_x2 = pcb_x1 + pcb_w
pcb_y2 = pcb_y1 + pcb_h

# Outer drop shadow for PCB
shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sdraw = ImageDraw.Draw(shadow_layer)
sdraw.rounded_rectangle([pcb_x1 + 10 * SCALE, pcb_y1 + 15 * SCALE, pcb_x2 + 15 * SCALE, pcb_y2 + 25 * SCALE], radius=28 * SCALE, fill=(0, 0, 0, 180))
shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(14 * SCALE))
canvas.paste(shadow_layer, (0, 0), shadow_layer)

# PCB Substrate (FR-4 Matte Black)
draw.rounded_rectangle([pcb_x1, pcb_y1, pcb_x2, pcb_y2], radius=26 * SCALE, fill=(24, 25, 28), outline=(60, 64, 75), width=3 * SCALE)

# Inner Copper Ground Ring (ENIG Gold border trace)
draw.rounded_rectangle([pcb_x1 + 10 * SCALE, pcb_y1 + 10 * SCALE, pcb_x2 - 10 * SCALE, pcb_y2 - 10 * SCALE], radius=20 * SCALE, outline=(180, 150, 70), width=2 * SCALE)

# 4 Corner Mounting Holes (M3 with gold rings)
holes = [
    (pcb_x1 + 32 * SCALE, pcb_y1 + 32 * SCALE),
    (pcb_x2 - 32 * SCALE, pcb_y1 + 32 * SCALE),
    (pcb_x1 + 32 * SCALE, pcb_y2 - 32 * SCALE),
    (pcb_x2 - 32 * SCALE, pcb_y2 - 32 * SCALE)
]
for hx, hy in holes:
    draw.ellipse([hx - 18 * SCALE, hy - 18 * SCALE, hx + 18 * SCALE, hy + 18 * SCALE], fill=(210, 175, 80), outline=(240, 210, 120), width=1 * SCALE)
    draw.ellipse([hx - 11 * SCALE, hy - 11 * SCALE, hx + 11 * SCALE, hy + 11 * SCALE], fill=(12, 13, 16), outline=(80, 70, 40), width=1 * SCALE)

# Silkscreen Branding on PCB
draw.text((pcb_x1 + 75 * SCALE, pcb_y1 + 30 * SCALE), "THARIT RS-485 COMPACT EXTENSION v2.0", font=font_section, fill=(255, 255, 255))
draw.text((pcb_x1 + 75 * SCALE, pcb_y1 + 55 * SCALE), "Designed by Chatchawan Taja • For THARIT-IoT & ESP32", font=font_subtitle, fill=(180, 185, 200))


# COMPONENT 1: LEFT 6-PIN HEADER (ESP32 INTERFACE)
hdr_x = pcb_x1 + 65 * SCALE
hdr_start_y = pcb_y1 + 140 * SCALE
pin_spacing = 75 * SCALE

pin_data = [
    ("3V3", "Pin 1", "ไฟตรรกะ 3.3V (จาก ESP32 3V3)", (0, 215, 255)),
    ("5V",  "Pin 2", "ไฟบอร์ด 5V (จาก ESP32 VIN/VBUS)", (255, 85, 85)),
    ("GND", "Pin 3", "กราวด์ร่วมระบบ (จาก ESP32 GND)", (170, 175, 195)),
    ("TX",  "Pin 4", "สายส่งคำสั่ง (ต่อ ESP32 GPIO17)", (255, 215, 0)),
    ("RX",  "Pin 5", "สายรับข้อมูล (ต่อ ESP32 GPIO16)", (0, 230, 140)),
    ("DE",  "Pin 6", "สลับทิศทาง (ต่อ ESP32 GPIO04)", (255, 130, 230))
]

draw.rounded_rectangle([hdr_x - 32 * SCALE, hdr_start_y - 25 * SCALE, hdr_x + 140 * SCALE, hdr_start_y + 5 * pin_spacing + 35 * SCALE], radius=12 * SCALE, fill=(30, 32, 40), outline=(0, 200, 255), width=2 * SCALE)
draw.text((hdr_x - 20 * SCALE, hdr_start_y - 18 * SCALE), "MCU INTERFACE (6-PIN)", font=font_badge, fill=(0, 220, 255))

for i, (pname, pnum, pdesc, pcol) in enumerate(pin_data):
    py = hdr_start_y + i * pin_spacing + 25 * SCALE
    if i == 0:
        draw.rectangle([hdr_x - 14 * SCALE, py - 14 * SCALE, hdr_x + 14 * SCALE, py + 14 * SCALE], fill=(215, 180, 85), outline=(245, 220, 120), width=1 * SCALE)
    else:
        draw.ellipse([hdr_x - 14 * SCALE, py - 14 * SCALE, hdr_x + 14 * SCALE, py + 14 * SCALE], fill=(215, 180, 85), outline=(245, 220, 120), width=1 * SCALE)
    draw.ellipse([hdr_x - 7 * SCALE, py - 7 * SCALE, hdr_x + 7 * SCALE, py + 7 * SCALE], fill=(20, 22, 28))
    draw.text((hdr_x + 28 * SCALE, py - 11 * SCALE), pname, font=font_pin_label, fill=(255, 255, 255))
    draw.line([(hdr_x + 95 * SCALE, py), (hdr_x + 130 * SCALE, py)], fill=(180, 150, 70), width=2 * SCALE)


# COMPONENT 2: RIGHT 4-PIN SCREW TERMINAL BLOCK
term_w = 110 * SCALE
term_h = 360 * SCALE
term_x = pcb_x2 - 160 * SCALE
term_y = pcb_cy - term_h // 2 + 30 * SCALE

draw.rounded_rectangle([term_x, term_y, term_x + term_w, term_y + term_h], radius=10 * SCALE, fill=(35, 135, 65), outline=(25, 95, 45), width=3 * SCALE)

term_pins = [
    ("1: V+", "แดง (V+)", (255, 80, 80)),
    ("2: GND", "ดำ (GND)", (180, 185, 200)),
    ("3: A+", "เหลือง (A+)", (255, 215, 0)),
    ("4: B-", "เขียว (B-)", (0, 240, 140))
]
term_step = term_h // 4
for i, (tname, tcolor_label, tcolor) in enumerate(term_pins):
    ty = term_y + i * term_step + term_step // 2
    draw.ellipse([term_x + 35 * SCALE, ty - 22 * SCALE, term_x + 75 * SCALE, ty + 22 * SCALE], fill=(180, 185, 195), outline=(100, 105, 115), width=2 * SCALE)
    draw.line([(term_x + 43 * SCALE, ty - 12 * SCALE), (term_x + 67 * SCALE, ty + 12 * SCALE)], fill=(50, 55, 65), width=4 * SCALE)
    draw.rectangle([term_x + term_w - 12 * SCALE, ty - 18 * SCALE, term_x + term_w + 5 * SCALE, ty + 18 * SCALE], fill=(20, 25, 30), outline=(15, 60, 30), width=1 * SCALE)
    
    draw.text((term_x - 110 * SCALE, ty - 11 * SCALE), tname, font=font_pin_label, fill=(255, 255, 255))
    draw.line([(term_x - 30 * SCALE, ty), (term_x - 8 * SCALE, ty)], fill=(180, 150, 70), width=2 * SCALE)

draw.text((term_x - 125 * SCALE, term_y - 28 * SCALE), "SENSOR INTERFACE (XY-MD02)", font=font_badge, fill=(0, 230, 140))


# COMPONENT 3: POWER SELECT JUMPER (J_PWR)
jpwr_x = pcb_cx - 130 * SCALE
jpwr_y = pcb_y1 + 160 * SCALE

draw.rounded_rectangle([jpwr_x - 50 * SCALE, jpwr_y - 35 * SCALE, jpwr_x + 170 * SCALE, jpwr_y + 80 * SCALE], radius=10 * SCALE, fill=(28, 30, 38), outline=(255, 180, 0), width=2 * SCALE)
draw.text((jpwr_x - 35 * SCALE, jpwr_y - 26 * SCALE), "J_PWR: เลือกแหล่งจ่ายไฟเซนเซอร์", font=font_badge, fill=(255, 205, 50))
draw.text((jpwr_x - 40 * SCALE, jpwr_y + 12 * SCALE), "5V", font=font_bold, fill=(255, 90, 90))
draw.text((jpwr_x + 130 * SCALE, jpwr_y + 12 * SCALE), "EXT", font=font_bold, fill=(255, 195, 0))

p1 = (jpwr_x + 5 * SCALE, jpwr_y + 22 * SCALE)
p2 = (jpwr_x + 45 * SCALE, jpwr_y + 22 * SCALE)
p3 = (jpwr_x + 85 * SCALE, jpwr_y + 22 * SCALE)

for px, py in [p1, p2, p3]:
    draw.ellipse([px - 10 * SCALE, py - 10 * SCALE, px + 10 * SCALE, py + 10 * SCALE], fill=(215, 180, 85), outline=(245, 220, 120), width=1 * SCALE)
    draw.ellipse([px - 5 * SCALE, py - 5 * SCALE, px + 5 * SCALE, py + 5 * SCALE], fill=(20, 22, 28))

# Blue Shunt Jumper Cap on 1-2
draw.rounded_rectangle([p1[0] - 8 * SCALE, p1[1] - 16 * SCALE, p2[0] + 8 * SCALE, p2[1] + 16 * SCALE], radius=4 * SCALE, fill=(20, 90, 220), outline=(40, 140, 255), width=2 * SCALE)
draw.text((jpwr_x - 35 * SCALE, jpwr_y + 52 * SCALE), "[เสียบ 1-2: ไฟบอร์ด 5V]   [เสียบ 2-3: ไฟนอก 12-24V]", font=font_text, fill=(220, 225, 235))


# COMPONENT 4: RS-485 TRANSCEIVER IC (SP3485E SOIC-8)
ic_w = 110 * SCALE
ic_h = 150 * SCALE
ic_x = pcb_cx - 100 * SCALE
ic_y = pcb_cy - 10 * SCALE

draw.rounded_rectangle([ic_x, ic_y, ic_x + ic_w, ic_y + ic_h], radius=6 * SCALE, fill=(35, 36, 40), outline=(65, 68, 78), width=2 * SCALE)
draw.ellipse([ic_x + 12 * SCALE, ic_y + 14 * SCALE, ic_x + 22 * SCALE, ic_y + 24 * SCALE], fill=(20, 20, 22))

for i in range(4):
    l_py = ic_y + 24 * SCALE + i * 34 * SCALE
    draw.rectangle([ic_x - 14 * SCALE, l_py - 5 * SCALE, ic_x, l_py + 5 * SCALE], fill=(210, 215, 225))
    draw.rectangle([ic_x + ic_w, l_py - 5 * SCALE, ic_x + ic_w + 14 * SCALE, l_py + 5 * SCALE], fill=(210, 215, 225))

draw.text((ic_x + 18 * SCALE, ic_y + 55 * SCALE), "SP3485E", font=font_bold, fill=(200, 205, 215))
draw.text((ic_x + 25 * SCALE, ic_y + 80 * SCALE), "3.3V RS-485", font=font_ic_text, fill=(160, 165, 175))


# COMPONENT 5: TERMINATION JUMPER (J_TERM 120Ω) - Adjusted position to prevent overlap
jterm_x = pcb_cx + 40 * SCALE
jterm_y = pcb_cy + 175 * SCALE

draw.rounded_rectangle([jterm_x - 20 * SCALE, jterm_y - 28 * SCALE, jterm_x + 140 * SCALE, jterm_y + 55 * SCALE], radius=8 * SCALE, fill=(28, 30, 38), outline=(255, 90, 160), width=1 * SCALE)
draw.text((jterm_x - 10 * SCALE, jterm_y - 20 * SCALE), "TERM 120Ω (J1)", font=font_badge, fill=(255, 110, 180))

tp1 = (jterm_x + 20 * SCALE, jterm_y + 18 * SCALE)
tp2 = (jterm_x + 55 * SCALE, jterm_y + 18 * SCALE)
for px, py in [tp1, tp2]:
    draw.ellipse([px - 10 * SCALE, py - 10 * SCALE, px + 10 * SCALE, py + 10 * SCALE], fill=(215, 180, 85), outline=(245, 220, 120), width=1 * SCALE)
    draw.ellipse([px - 5 * SCALE, py - 5 * SCALE, px + 5 * SCALE, py + 5 * SCALE], fill=(20, 22, 28))

draw.rounded_rectangle([tp1[0] - 8 * SCALE, tp1[1] - 15 * SCALE, tp2[0] + 8 * SCALE, tp2[1] + 15 * SCALE], radius=4 * SCALE, fill=(220, 40, 60), outline=(255, 90, 110), width=2 * SCALE)
draw.text((jterm_x + 80 * SCALE, jterm_y + 8 * SCALE), "[ON]", font=font_bold, fill=(255, 255, 255))


# COMPONENT 6: PROTECTION CIRCUIT
prot_x = pcb_cx + 70 * SCALE
prot_y = pcb_cy - 10 * SCALE

draw.rounded_rectangle([prot_x, prot_y, prot_x + 55 * SCALE, prot_y + 40 * SCALE], radius=4 * SCALE, fill=(35, 36, 40), outline=(65, 68, 78), width=1 * SCALE)
draw.text((prot_x + 7 * SCALE, prot_y + 12 * SCALE), "SM712", font=font_ic_text, fill=(200, 205, 215))

draw.rectangle([prot_x + 5 * SCALE, prot_y + 60 * SCALE, prot_x + 45 * SCALE, prot_y + 85 * SCALE], fill=(195, 180, 40), outline=(230, 215, 70), width=1 * SCALE)
draw.text((prot_x + 8 * SCALE, prot_y + 66 * SCALE), "PTC 1", font=font_badge, fill=(30, 30, 30))

draw.rectangle([prot_x + 5 * SCALE, prot_y + 100 * SCALE, prot_x + 45 * SCALE, prot_y + 125 * SCALE], fill=(195, 180, 40), outline=(230, 215, 70), width=1 * SCALE)
draw.text((prot_x + 8 * SCALE, prot_y + 106 * SCALE), "PTC 2", font=font_badge, fill=(30, 30, 30))


# COMPONENT 7: STATUS LEDS
led_start_x = pcb_cx - 100 * SCALE
led_y = pcb_y2 - 75 * SCALE
leds = [
    ("PWR", (50, 230, 90), "เขียว"),
    ("TX",  (40, 150, 255), "น้ำเงิน"),
    ("RX",  (255, 180, 30), "ส้ม")
]

for i, (lname, lcol, lth) in enumerate(leds):
    lx = led_start_x + i * 80 * SCALE
    draw.rectangle([lx - 12 * SCALE, led_y - 8 * SCALE, lx + 12 * SCALE, led_y + 8 * SCALE], fill=(220, 220, 225), outline=(120, 120, 130), width=1 * SCALE)
    draw.ellipse([lx - 6 * SCALE, led_y - 6 * SCALE, lx + 6 * SCALE, led_y + 6 * SCALE], fill=lcol)
    draw.text((lx - 14 * SCALE, led_y + 14 * SCALE), lname, font=font_bold, fill=(255, 255, 255))


# 4. EXTERNAL CALLOUT CARDS
# Left Card: ESP32 Wiring Guide
call_l_x = 35 * SCALE
call_l_y = pcb_y1 + 40 * SCALE
call_l_w = 380 * SCALE
call_l_h = 560 * SCALE

draw.rounded_rectangle([call_l_x, call_l_y, call_l_x + call_l_w, call_l_y + call_l_h], radius=14 * SCALE, fill=(22, 25, 35), outline=(0, 215, 255), width=2 * SCALE)
draw.rounded_rectangle([call_l_x, call_l_y, call_l_x + call_l_w, call_l_y + 40 * SCALE], radius=8 * SCALE, fill=(15, 45, 65))
draw.text((call_l_x + 18 * SCALE, call_l_y + 10 * SCALE), "🔗 ต่อเข้า ESP32 แค่ 6 ขานี้เท่านั้น!", font=font_section, fill=(0, 225, 255))
draw.text((call_l_x + 20 * SCALE, call_l_y + 55 * SCALE), "ไม่ต้องต่อขาอื่น ขาที่เหลือบน ESP32 ปล่อยว่างได้เลย:", font=font_subtitle, fill=(220, 225, 240))

c_y = call_l_y + 90 * SCALE
for pname, pnum, pdesc, pcol in pin_data:
    draw.rounded_rectangle([call_l_x + 20 * SCALE, c_y, call_l_x + 95 * SCALE, c_y + 30 * SCALE], radius=6 * SCALE, fill=pcol)
    text_color = (0, 0, 0) if pname in ["TX", "RX", "3V3"] else (255, 255, 255)
    draw.text((call_l_x + 32 * SCALE, c_y + 5 * SCALE), pname, font=font_bold, fill=text_color)
    draw.text((call_l_x + 108 * SCALE, c_y + 5 * SCALE), pdesc, font=font_text, fill=(240, 240, 250))
    c_y += 48 * SCALE

draw.rounded_rectangle([call_l_x + 20 * SCALE, c_y + 10 * SCALE, call_l_x + call_l_w - 20 * SCALE, call_l_y + call_l_h - 20 * SCALE], radius=8 * SCALE, fill=(28, 33, 46))
draw.text((call_l_x + 30 * SCALE, c_y + 22 * SCALE), "💡 เคล็ดลับการประกอบ:", font=font_bold, fill=(255, 215, 50))
draw.text((call_l_x + 30 * SCALE, c_y + 46 * SCALE), "• ใช้สายแพจั๊มเปอร์ตัวเมีย-ตัวเมีย 6 เส้น เสียบตรงๆ", font=font_text, fill=(220, 225, 235))
draw.text((call_l_x + 30 * SCALE, c_y + 70 * SCALE), "• หรือบัดกรีลงบนแผ่นไข่ปลาประกบหัว ESP32 ได้ทันที", font=font_text, fill=(220, 225, 235))
draw.text((call_l_x + 30 * SCALE, c_y + 94 * SCALE), "• ไม่มีขาหลอกให้สับสน ใช้งานได้แม่นยำ 100%", font=font_bold, fill=(0, 230, 140))


# Right Card: XY-MD02 Wiring Guide
call_r_x = W - 415 * SCALE
call_r_y = pcb_y1 + 40 * SCALE
call_r_w = 380 * SCALE
call_r_h = 560 * SCALE

draw.rounded_rectangle([call_r_x, call_r_y, call_r_x + call_r_w, call_r_y + call_r_h], radius=14 * SCALE, fill=(22, 25, 35), outline=(0, 230, 140), width=2 * SCALE)
draw.rounded_rectangle([call_r_x, call_r_y, call_r_x + call_r_w, call_r_y + 40 * SCALE], radius=8 * SCALE, fill=(15, 55, 40))
draw.text((call_r_x + 18 * SCALE, call_r_y + 10 * SCALE), "🌡️ ขันสายเข้าเซนเซอร์ XY-MD02", font=font_section, fill=(0, 240, 150))
draw.text((call_r_x + 20 * SCALE, call_r_y + 55 * SCALE), "สายเคเบิล 4 เส้น ขันล็อกแน่นหนาที่ Terminal Block:", font=font_subtitle, fill=(220, 225, 240))

r_y = call_r_y + 90 * SCALE
for tname, tcolor_label, tcolor in term_pins:
    draw.rounded_rectangle([call_r_x + 20 * SCALE, r_y, call_r_x + 115 * SCALE, r_y + 30 * SCALE], radius=6 * SCALE, fill=tcolor)
    text_color = (0, 0, 0) if "เหลือง" in tcolor_label or "เขียว" in tcolor_label else (255, 255, 255)
    draw.text((call_r_x + 28 * SCALE, r_y + 5 * SCALE), tname, font=font_bold, fill=text_color)
    draw.text((call_r_x + 130 * SCALE, r_y + 5 * SCALE), "➔ สาย" + tcolor_label, font=font_bold, fill=(240, 240, 250))
    r_y += 48 * SCALE

draw.rounded_rectangle([call_r_x + 20 * SCALE, r_y + 10 * SCALE, call_r_x + call_r_w - 20 * SCALE, call_r_y + call_r_h - 20 * SCALE], radius=8 * SCALE, fill=(28, 33, 46))
draw.text((call_r_x + 30 * SCALE, r_y + 22 * SCALE), "⚙️ ข้อมูลทางเทคนิค RS-485:", font=font_bold, fill=(0, 220, 255))
draw.text((call_r_x + 30 * SCALE, r_y + 46 * SCALE), "• Baud Rate: 9,600 bps (มาตรฐาน XY-MD02)", font=font_text, fill=(220, 225, 235))
draw.text((call_r_x + 30 * SCALE, r_y + 70 * SCALE), "• โปรโตคอล: Modbus RTU (Slave ID: 0x01)", font=font_text, fill=(220, 225, 235))
draw.text((call_r_x + 30 * SCALE, r_y + 94 * SCALE), "• ระยะสายสูงสุด: 1,200 เมตร ด้วยสายคู่ตีเกลียว", font=font_bold, fill=(0, 230, 140))


# Footer Bar
draw.rectangle([0, H - 35 * SCALE, W, H], fill=(12, 14, 18))
draw.text((35 * SCALE, H - 25 * SCALE), "ผู้ออกแบบ / สถาปัตยกรรมฮาร์ดแวร์: ชัชวาล ตาจา (Chatchawan Taja) | ใบงานที่ 2-3 การออกแบบระบบสมองกลฝังตัวและ IoT", font=font_badge, fill=(150, 155, 175))
draw.text((W - 480 * SCALE, H - 25 * SCALE), "Hardware Revision v2.0 • Ultra-Clean Compact Edition", font=font_badge, fill=(0, 210, 255))

final_img = canvas.resize((1920, 1080), Image.Resampling.LANCZOS)
out_file = r"d:\Iven\IoT\pcb_rev2_compact_design_render.png"
final_img.save(out_file, quality=95)
print("Saved cleanly refined PCB Revision 2.0 Render to:", out_file)
