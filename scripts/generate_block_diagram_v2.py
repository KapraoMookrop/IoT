import os
import math
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions (2x supersampling for ultra crispness)
SCALE = 2
WIDTH, HEIGHT = 920 * SCALE, 560 * SCALE

# Colors (matching the user's reference image exactly)
COLOR_BG = (34, 34, 38)            # Dark Graphite/Slate Background
COLOR_BOX_FILL = (44, 25, 72)       # Deep Purple Box
COLOR_BOX_BORDER = (88, 52, 140)    # Purple Box Border
COLOR_PILL_FILL = (22, 13, 37)      # Dark Purple Pill
COLOR_PILL_BORDER = (75, 42, 115)   # Pill Border
COLOR_LINE = (140, 140, 150)        # Grey Line
COLOR_TEXT_MAIN = (255, 255, 255)   # Crisp White
COLOR_TEXT_SUB = (210, 200, 230)    # Lavender Subtext
COLOR_TEXT_ACCENT = (0, 215, 255)   # Cyan Accent

# Load fonts
font_dir = "C:/Windows/Fonts"
font_box_title = ImageFont.truetype(os.path.join(font_dir, "tahomabd.ttf"), 17 * SCALE)
font_box_sub = ImageFont.truetype(os.path.join(font_dir, "tahoma.ttf"), 12 * SCALE)
font_pill = ImageFont.truetype(os.path.join(font_dir, "tahomabd.ttf"), 11 * SCALE)

im = Image.new("RGB", (WIDTH, HEIGHT), COLOR_BG)
draw = ImageDraw.Draw(im)

def draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=1):
    x1, y1, x2, y2 = bbox
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)

def get_pill_bounds(cx, cy, text, font):
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad_x = 16 * SCALE
    pad_y = 6 * SCALE
    w = tw + pad_x * 2
    h = th + pad_y * 2
    x1 = cx - w // 2
    y1 = cy - h // 2
    x2 = x1 + w
    y2 = y1 + h
    return (x1, y1, x2, y2, tw, th, bbox)

def draw_pill(draw, cx, cy, text, font, fill=COLOR_PILL_FILL, outline=COLOR_PILL_BORDER):
    x1, y1, x2, y2, tw, th, bbox = get_pill_bounds(cx, cy, text, font)
    radius = (y2 - y1) // 2
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=1 * SCALE)
    tx = cx - tw // 2 - bbox[0]
    ty = cy - th // 2 - bbox[1]
    draw.text((tx, ty), text, font=font, fill=COLOR_TEXT_MAIN)
    return (x1, y1, x2, y2)

def draw_box(draw, cx, cy, w, h, title, sub=""):
    w = w * SCALE
    h = h * SCALE
    x1 = cx - w // 2
    y1 = cy - h // 2
    x2 = x1 + w
    y2 = y1 + h
    radius = 16 * SCALE
    draw_rounded_rect(draw, [x1, y1, x2, y2], radius=radius, fill=COLOR_BOX_FILL, outline=COLOR_BOX_BORDER, width=2 * SCALE)
    
    if sub:
        t_box = font_box_title.getbbox(title)
        tw = t_box[2] - t_box[0]
        th = t_box[3] - t_box[1]
        s_box = font_box_sub.getbbox(sub)
        sw = s_box[2] - s_box[0]
        sh = s_box[3] - s_box[1]
        spacing = 5 * SCALE
        total_h = th + spacing + sh
        
        top_y = cy - total_h // 2
        draw.text((cx - tw // 2 - t_box[0], top_y - t_box[1]), title, font=font_box_title, fill=COLOR_TEXT_MAIN)
        draw.text((cx - sw // 2 - s_box[0], top_y + th + spacing - s_box[1]), sub, font=font_box_sub, fill=COLOR_TEXT_SUB)
    else:
        t_box = font_box_title.getbbox(title)
        tw = t_box[2] - t_box[0]
        th = t_box[3] - t_box[1]
        draw.text((cx - tw // 2 - t_box[0], cy - th // 2 - t_box[1]), title, font=font_box_title, fill=COLOR_TEXT_MAIN)
        
    return (x1, y1, x2, y2)

def draw_arrow_head(draw, pt, angle_rad, length=10*SCALE, color=COLOR_LINE):
    x, y = pt
    tip = (x, y)
    spread = 0.42
    left = (x - length * math.cos(angle_rad - spread), y - length * math.sin(angle_rad - spread))
    right = (x - length * math.cos(angle_rad + spread), y - length * math.sin(angle_rad + spread))
    draw.polygon([tip, left, right], fill=color)

def draw_dashed_line(draw, points, dash_len=7*SCALE, gap_len=5*SCALE, color=COLOR_LINE, width=2*SCALE):
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        dx = x2 - x1
        dy = y2 - y1
        dist = math.hypot(dx, dy)
        if dist == 0:
            continue
        ux = dx / dist
        uy = dy / dist
        curr = 0
        while curr < dist:
            end = min(curr + dash_len, dist)
            draw.line([(x1 + ux * curr, y1 + uy * curr), (x1 + ux * end, y1 + uy * end)], fill=color, width=width)
            curr += dash_len + gap_len


# Coordinates layout
col_center_x = 360 * SCALE
col_right_x = 730 * SCALE

# Y Positions
y_top = 70 * SCALE          # XY-MD02
y_mid = 230 * SCALE         # RS-485 Extension Module
y_bot = 450 * SCALE         # THARIT-IoT
y_pwr = 230 * SCALE         # Power Supply

# Box dimensions
w_top, h_top = 220, 72
w_mid, h_mid = 260, 76
w_bot, h_bot = 260, 76
w_pwr, h_pwr = 190, 72

# Left Bus (Power to sensor)
left_bus_x = 105 * SCALE

# Pills Y Positions
pill_v1_y = (y_top + y_mid) // 2
pill_v2_y = (y_mid + y_bot) // 2
pill_left_y = (y_top + y_mid) // 2

# Power drop positions & pills
pwr1_drop_x = 650 * SCALE
pill_pwr1_x = 595 * SCALE
pill_pwr1_y = 315 * SCALE

pwr2_drop_x = 790 * SCALE
pill_pwr2_x = 720 * SCALE
pill_pwr2_y = 415 * SCALE

# Precalculate pill bounds for breaking lines cleanly
text_rs485 = "สายสัญญาณ RS-485 [2:A+, 3:B-]"
text_uart = "UART (TX:GPIO17 / RX:GPIO16) & DE:GPIO04"
text_sens_pwr = "ไฟเลี้ยงเซนเซอร์ [1:V+, 4:GND] (DC 5V-24V)"
text_pwr1 = "จ่ายไฟเลี้ยงภายนอก EXT (DC 12V-24V)"
text_pwr2 = "จ่ายไฟเลี้ยงบอร์ดหลัก (USB / DC 5V)"

bbox_p_v1 = get_pill_bounds(col_center_x, pill_v1_y, text_rs485, font_pill)
bbox_p_v2 = get_pill_bounds(col_center_x, pill_v2_y, text_uart, font_pill)

# 1. Left Power Loop (From RS-485 Module up into XY-MD02)
pts_left_power = [
    (col_center_x - w_mid * SCALE // 2, y_mid),
    (left_bus_x, y_mid),
    (left_bus_x, y_top),
    (col_center_x - w_top * SCALE // 2, y_top)
]
for i in range(len(pts_left_power) - 1):
    draw.line([pts_left_power[i], pts_left_power[i+1]], fill=COLOR_LINE, width=2 * SCALE)
draw_arrow_head(draw, (col_center_x - w_top * SCALE // 2, y_top), 0)

# 2. Vertical line 1: XY-MD02 to RS-485 Module (split by pill)
draw.line([(col_center_x, y_top + h_top * SCALE // 2), (col_center_x, bbox_p_v1[1])], fill=COLOR_LINE, width=2 * SCALE)
draw.line([(col_center_x, bbox_p_v1[3]), (col_center_x, y_mid - h_mid * SCALE // 2)], fill=COLOR_LINE, width=2 * SCALE)
draw_arrow_head(draw, (col_center_x, y_mid - h_mid * SCALE // 2), math.pi / 2)
# Bidirectional arrow head pointing back up to XY-MD02
draw_arrow_head(draw, (col_center_x, y_top + h_top * SCALE // 2), -math.pi / 2)

# 3. Vertical line 2: RS-485 Module to THARIT-IoT (split by pill)
draw.line([(col_center_x, y_mid + h_mid * SCALE // 2), (col_center_x, bbox_p_v2[1])], fill=COLOR_LINE, width=2 * SCALE)
draw.line([(col_center_x, bbox_p_v2[3]), (col_center_x, y_bot - h_bot * SCALE // 2)], fill=COLOR_LINE, width=2 * SCALE)
draw_arrow_head(draw, (col_center_x, y_bot - h_bot * SCALE // 2), math.pi / 2)
# Bidirectional arrow head pointing back up to RS-485 Module
draw_arrow_head(draw, (col_center_x, y_mid + h_mid * SCALE // 2), -math.pi / 2)

# 4. Power supply line 1 (to RS-485 Module): exits bottom of Power Supply, turns left into RS-485 Module
pts_pwr1 = [
    (col_right_x - 40 * SCALE, y_pwr + h_pwr * SCALE // 2),
    (col_right_x - 40 * SCALE, pill_pwr1_y),
    (col_center_x + w_mid * SCALE // 2, pill_pwr1_y)
]
draw_dashed_line(draw, pts_pwr1)
draw_arrow_head(draw, (col_center_x + w_mid * SCALE // 2, pill_pwr1_y), math.pi)

# 5. Power supply line 2 (to THARIT-IoT): exits bottom-right of Power Supply, drops, turns left into THARIT-IoT
pts_pwr2 = [
    (col_right_x + 35 * SCALE, y_pwr + h_pwr * SCALE // 2),
    (pwr2_drop_x, y_pwr + h_pwr * SCALE // 2),
    (pwr2_drop_x, y_bot + 12 * SCALE),
    (col_center_x + w_bot * SCALE // 2, y_bot + 12 * SCALE)
]
draw_dashed_line(draw, pts_pwr2)
draw_arrow_head(draw, (col_center_x + w_bot * SCALE // 2, y_bot + 12 * SCALE), math.pi)

# 6. Draw Boxes
box_top = draw_box(draw, col_center_x, y_top, w_top, h_top, "XY-MD02", "เซนเซอร์วัดอุณหภูมิ-ความชื้น (SHT20)")
box_mid = draw_box(draw, col_center_x, y_mid, w_mid, h_mid, "RS-485 Extension Module", "PCB แปลงสัญญาณ (SP3485E Rev v2.2)")
box_bot = draw_box(draw, col_center_x, y_bot, w_bot, h_bot, "THARIT-IoT", "ESP32 Controller (Master Node)")
box_pwr = draw_box(draw, col_right_x, y_pwr, w_pwr, h_pwr, "Power Supply", "แหล่งจ่ายไฟ (5V / DC 12V-24V)")

# 7. Draw Pill Badges
# Left Power badge
draw_pill(draw, left_bus_x, pill_left_y, text_sens_pwr, font_pill)

# Top vertical badge (RS-485)
draw_pill(draw, col_center_x, pill_v1_y, text_rs485, font_pill)

# Bottom vertical badge (UART)
draw_pill(draw, col_center_x, pill_v2_y, text_uart, font_pill)

# Power supply 1 pill
draw_pill(draw, pill_pwr1_x, pill_pwr1_y, text_pwr1, font_pill)

# Power supply 2 pill
draw_pill(draw, pill_pwr2_x, pill_pwr2_y, text_pwr2, font_pill)

# Resize down with Lanczos supersampling
final_im = im.resize((WIDTH // SCALE, HEIGHT // SCALE), Image.Resampling.LANCZOS)

out_file1 = r"c:\Project\IoT\images\system_block_diagram_simple.png"
out_file2 = r"c:\Project\IoT\images\system_block_diagram.png"
final_im.save(out_file1, quality=95)
final_im.save(out_file2, quality=95)
print("Saved system block diagram successfully to:", out_file1)

