import os
import math
from PIL import Image, ImageDraw, ImageFont

font_dir = "C:/Windows/Fonts"
font_title = ImageFont.truetype(os.path.join(font_dir, "tahomabd.ttf"), 16)
font_card_head = ImageFont.truetype(os.path.join(font_dir, "tahomabd.ttf"), 13)
font_card_body = ImageFont.truetype(os.path.join(font_dir, "tahoma.ttf"), 11)
font_card_body_bold = ImageFont.truetype(os.path.join(font_dir, "tahomabd.ttf"), 11)

def draw_callout_card(draw, card_x, card_y, card_w, card_h, header_text, body_lines, header_color=(0, 220, 255), target_pt=None, attach_pt=None):
    # Shadow
    draw.rounded_rectangle([card_x+3, card_y+3, card_x+card_w+3, card_y+card_h+3], radius=8, fill=(0, 0, 0, 180))
    # Box fill
    draw.rounded_rectangle([card_x, card_y, card_x+card_w, card_y+card_h], radius=8, fill=(16, 18, 26, 240), outline=header_color, width=2)
    # Header bar background
    draw.rounded_rectangle([card_x+4, card_y+4, card_x+card_w-4, card_y+26], radius=4, fill=(header_color[0]//5, header_color[1]//5, header_color[2]//5, 230))
    draw.text((card_x+10, card_y+6), header_text, font=font_card_head, fill=header_color)
    
    # Body lines
    curr_y = card_y + 32
    for line in body_lines:
        if isinstance(line, tuple):
            text, is_bold, color = line
            f = font_card_body_bold if is_bold else font_card_body
            draw.text((card_x+10, curr_y), text, font=f, fill=color)
        else:
            draw.text((card_x+10, curr_y), line, font=font_card_body, fill=(235, 235, 245))
        curr_y += 16
        
    # Pointer line & anchor dot
    if target_pt and attach_pt:
        tx, ty = target_pt
        ax, ay = attach_pt
        draw.line([(ax, ay), (tx, ty)], fill=header_color, width=2)
        # Target pinpoint rings
        draw.ellipse([tx-6, ty-6, tx+6, ty+6], fill=(0, 0, 0, 200), outline=header_color, width=2)
        draw.ellipse([tx-2, ty-2, tx+2, ty+2], fill=header_color)
        # Attach point dot
        draw.ellipse([ax-3, ay-3, ax+3, ay+3], fill=header_color)

def draw_banner(draw, w, title_text, sub_text):
    draw.rectangle([0, 0, w, 32], fill=(12, 14, 20, 220))
    draw.line([(0, 32), (w, 32)], fill=(60, 65, 85, 255), width=1)
    draw.text((15, 6), title_text, font=font_title, fill=(255, 255, 255))
    tw = font_title.getbbox(title_text)[2]
    draw.text((tw + 35, 8), sub_text, font=font_card_body, fill=(180, 185, 205))

im2_path = r"d:\Iven\IoT\tharit_iot_rs485_system_simulation.jpg"
im2 = Image.open(im2_path).convert("RGBA")
overlay2 = Image.new("RGBA", im2.size, (0, 0, 0, 0))
draw2 = ImageDraw.Draw(overlay2)

draw_banner(draw2, im2.width, "THARIT-IoT + RS-485 Extension Module + XY-MD02", "ภาพจำลองการต่อวงจรและทดสอบระบบจริงในห้องปฏิบัติการ (Real System Wiring & Testbench)")

# RS-485 Extension Module (Top Shield)
draw_callout_card(
    draw2, 15, 42, 385, 145,
    "🛡️ แผ่นวงจร RS-485 Extension Module (ที่เราออกแบบ)",
    [
        "• ติดตั้งแบบ Stackable Shield เสียบตรงบนบอร์ดหลัก THARIT-IoT",
        "• แปลงสัญญาณ UART 3.3V เป็น RS-485 Differential (A+, B-)",
        "• วิธีเลือกแหล่งจ่ายไฟเลี้ยงเซนเซอร์ (J_PWR):",
        "  - เสียบขา 1-2: ดึงไฟ 5V บอร์ดหลัก จ่ายออกสาย V+ ทันที (เทสในแล็บ)",
        "  - เสียบขา 2-3 หรือต่อขั้ว V+: ต่อไฟภายนอก DC 12V-24V (เดินสายไกล)"
    ],
    header_color=(255, 195, 0),
    target_pt=(460, 310),
    attach_pt=(395, 115)
)

# THARIT-IoT Mainboard
draw_callout_card(
    draw2, 15, 575, 370, 130,
    "🖥️ บอร์ดหลัก THARIT-IoT (ESP32 Node)",
    [
        "• ไมโครคอนโทรลเลอร์ ESP32 ทำหน้าที่เป็น Modbus Master",
        "• ส่งคำสั่ง Function Code 0x04 อ่านค่าอุณหภูมิ/ความชื้น",
        "• สลับสถานะ Transmit/Receive ผ่านขา GPIO ควบคุม DE/RE",
        "• รับไฟเลี้ยง 5V ผ่านพอร์ต USB-C และมี Wi-Fi ส่งข้อมูลขึ้น Cloud"
    ],
    header_color=(0, 210, 255),
    target_pt=(450, 580),
    attach_pt=(385, 630)
)

# Screw Terminal & Cable
draw_callout_card(
    draw2, 450, 42, 370, 135,
    "🔌 ขั้วต่อ Terminal Block & สายสัญญาณเซนเซอร์",
    [
        "• สายไฟ 4 เส้น เชื่อมต่อไปยังเซนเซอร์ XY-MD02:",
        "  [แดง] V+  : ไฟเลี้ยงเซนเซอร์ (เลือกไฟบอร์ด 5V หรือ EXT 12-24V)",
        "  [ดำ] GND : กราวด์ร่วมระบบ",
        "  [เหลือง] A+ : สายสัญญาณ Differential Data+",
        "  [เขียว] B-  : สายสัญญาณ Differential Data-"
    ],
    header_color=(120, 235, 75),
    target_pt=(560, 320),
    attach_pt=(600, 177)
)

# XY-MD02 Sensor
draw_callout_card(
    draw2, 900, 150, 375, 140,
    "🌡️ เซนเซอร์วัดอุณหภูมิ-ความชื้น XY-MD02 (SHT20)",
    [
        "• ภายในติดตั้งชิป Sensirion SHT20 เกรดอุตสาหกรรมแม่นยำสูง",
        "• วัดอุณหภูมิ (-40 ถึง +80 °C) และความชื้น (0 ถึง 100 %RH)",
        "• สื่อสารด้วยโปรโตคอล Modbus RTU ผ่าน RS-485 (Baud 9600 8N1)",
        "• ตัวถังพลาสติกพร้อมช่องระบายอากาศ ป้องกันละอองน้ำหน้างาน"
    ],
    header_color=(255, 110, 190),
    target_pt=(820, 520),
    attach_pt=(940, 290)
)

# Industrial Cable loop
draw_callout_card(
    draw2, 890, 580, 380, 115,
    "🪢 สายเคเบิลอุตสาหกรรม (Industrial Cable)",
    [
        "• สาย 4 คอร์: คู่ตีเกลียว Twisted Pair (A/B) และไฟเลี้ยง (V+/GND)",
        "• ฉนวนทนทานต่อสัญญาณรบกวนคลื่นแม่เหล็กไฟฟ้า (EMI) ในฟาร์ม",
        "• สามารถลากสายเชื่อมต่อกับเซนเซอร์ได้ไกลตั้งแต่ 10 ถึง 1,200 เมตร"
    ],
    header_color=(0, 230, 160),
    target_pt=(710, 620),
    attach_pt=(890, 630)
)

im2_final = Image.alpha_composite(im2, overlay2).convert("RGB")
out2 = r"d:\Iven\IoT\tharit_iot_rs485_system_simulation_annotated.png"
im2_final.save(out2, quality=95)
print("Saved clean annotated lab system to:", out2)
