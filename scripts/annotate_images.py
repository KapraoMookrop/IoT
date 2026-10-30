import os
import math
from PIL import Image, ImageDraw, ImageFont

# Script to create:
# 1. tharit_rs485_module_render_3d_annotated.png (Zoomed PCB with full callouts)
# 2. tharit_iot_rs485_system_simulation_annotated.png (Real lab setup wiring callouts)

font_dir = "C:/Windows/Fonts"
font_title = ImageFont.truetype(os.path.join(font_dir, "tahomabd.ttf"), 18)
font_card_head = ImageFont.truetype(os.path.join(font_dir, "tahomabd.ttf"), 14)
font_card_body = ImageFont.truetype(os.path.join(font_dir, "tahoma.ttf"), 12)
font_card_body_bold = ImageFont.truetype(os.path.join(font_dir, "tahomabd.ttf"), 12)
font_badge = ImageFont.truetype(os.path.join(font_dir, "tahomabd.ttf"), 11)

def draw_callout_card(draw, card_x, card_y, card_w, card_h, header_text, body_lines, header_color=(0, 220, 255), target_pt=None, attach_pt=None):
    # Draw shadow
    draw.rounded_rectangle([card_x+3, card_y+3, card_x+card_w+3, card_y+card_h+3], radius=8, fill=(0, 0, 0, 160))
    # Draw background box (Dark high-contrast translucent)
    draw.rounded_rectangle([card_x, card_y, card_x+card_w, card_y+card_h], radius=8, fill=(18, 20, 28, 235), outline=header_color, width=2)
    
    # Header bar accent
    draw.rounded_rectangle([card_x+6, card_y+6, card_x+card_w-6, card_y+28], radius=4, fill=(header_color[0]//5, header_color[1]//5, header_color[2]//5, 200))
    draw.text((card_x+12, card_y+8), header_text, font=font_card_head, fill=header_color)
    
    # Body text
    curr_y = card_y + 34
    for line in body_lines:
        if isinstance(line, tuple):
            text, is_bold, color = line
            f = font_card_body_bold if is_bold else font_card_body
            draw.text((card_x+12, curr_y), text, font=f, fill=color)
        else:
            draw.text((card_x+12, curr_y), line, font=font_card_body, fill=(230, 230, 240))
        curr_y += 18
        
    # Draw pointer line & anchor dot if provided
    if target_pt and attach_pt:
        tx, ty = target_pt
        ax, ay = attach_pt
        # Line with accent color
        draw.line([(ax, ay), (tx, ty)], fill=header_color, width=2)
        # Target pinpoint rings
        draw.ellipse([tx-6, ty-6, tx+6, ty+6], fill=(0, 0, 0, 200), outline=header_color, width=2)
        draw.ellipse([tx-2, ty-2, tx+2, ty+2], fill=header_color)
        # Attach point dot
        draw.ellipse([ax-3, ay-3, ax+3, ay+3], fill=header_color)

print("Helper functions ready.")

