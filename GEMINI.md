# GEMINI.md: RS-485 Industrial Extension Module for THARIT-IoT (XY-MD02 / SHT20)

## 1. Project Overview & Architecture Decisions
* **Project Name:** RS-485 Industrial Extension Module สำหรับเชื่อมต่อเซนเซอร์ XY-MD02 (SHT20) ร่วมกับ THARIT-IoT
* **Course:** การออกแบบระบบสมองกลฝังตัวและ IoT (สัปดาห์ที่ 2-3: Requirement, Block Diagram และ PCB Hardware Design)
* **Lead / System Architect:** ชัชวาล ตาจา (Chatchawan Taja)
* **Status:** Hardware Revision v2.0 (Single-Layer Non-Crossing Edition) - Design & Specification Completed

### Key Architectural Decisions (From /grill-me Alignment):
1. **Direction Control (Half-Duplex):** ใช้ขา GPIO04 จากบอร์ดหลัก THARIT-IoT ควบคุมขา DE และ /RE ร่วมกัน เพื่อความแม่นยำสูงสุดตามมาตรฐาน Modbus RTU (Switching delay < 2 ms)
2. **Dual-Source Power Architecture (J_PWR):**
   - **โหมดไฟบอร์ด (5V):** เสียบช็อตขา 1-2 ดึงไฟเลี้ยง 5V จากบอร์ดหลัก THARIT-IoT ไปเลี้ยงเซนเซอร์ (สำหรับเทสในแล็บ / สายสั้น < 10m)
   - **โหมดไฟภายนอก (EXT):** เสียบช็อตขา 2-3 รับไฟ DC 12V-24V จากภายนอก สำหรับเดินสายเซนเซอร์ระยะไกลเพื่อป้องกัน Voltage Drop
3. **Transceiver & Protection Circuitry:**
   - **ชิป Transceiver:** 3.3V Low-Power `SP3485E` เข้ากันได้กับระดับตรรกะ 3.3V ของ MCU ESP32 โดยตรง ไม่ต้องใช้วงจรแบ่งแรงดัน
   - **วงจรป้องกัน:** TVS Diode Array `SM712` (ESD ทนแรงดัน ±8 kV), PTC Resettable Fuse (100 mA, 60V) 2 ตัว ป้องกันการช็อตสายผิดขั้ว
   - **Termination Resistor:** ตัวต้านทาน 120 Ω พร้อม Jumper `J_TERM` (เสียบ [ON] คาไว้เสมอเมื่อโมดูลเป็นปลายสายเดี่ยว)
4. **Form Factor (Revision v2.0 Single-Layer Edition):**
   - **ฝั่งต่อ ESP32:** ขั้วต่อ Header 6 ขา เรียงตามแนวพิน IC (5V, 3V3, RX, DE, TX, GND) ทำให้เดินลายทองแดงหน้าเดียวได้โดยไม่มีเส้นตัดกัน (Zero-Crossing)
   - **ฝั่งต่อเซนเซอร์:** ขั้วต่อ Industrial 4-Pin Screw Terminal Block (1: V+, 2: GND, 3: A+, 4: B-) สีเขียว ล็อกแน่นหนา

---

## 2. โครงสร้างโฟลเดอร์ของโปรเจกต์ (Project Directory Structure)
```
d:\Iven\IoT\
├── docs\                     # เอกสารส่งงานและใบงาน Word (.docx)
├── images\                   # คลังภาพผลงานและแบบแปลนทางวิศวกรรมหลัก (.png, .jpg)
│   └── raw\                  # ไฟล์ภาพร่างและภาพอ้างอิงชั่วคราว
├── scripts\                  # สคริปต์ Python สำหรับวาดแปลนและสร้างภาพประกอบ (.py)
├── README.md                 # คู่มือและสารบัญโปรเจกต์ฉบับสมบูรณ์
├── GEMINI.md                 # สรุปสถาปัตยกรรมและกฎข้อบังคับของระบบ
├── PCB_HARDWARE_DESIGN_SPEC.md # สเปกฮาร์ดแวร์ PCB และรายการอุปกรณ์ (BOM)
└── rs_485_extension_module_project_documentation.md # เอกสารทางวิศวกรรมระบบหลัก
```

---

## 3. Deliverables & Artifacts Generated
* **Hardware Specification (Rev 2.0):** [PCB_HARDWARE_DESIGN_SPEC.md](file:///d:/Iven/IoT/PCB_HARDWARE_DESIGN_SPEC.md)
* **Project Specification & Engineering Requirements:** [rs_485_extension_module_project_documentation.md](file:///d:/Iven/IoT/rs_485_extension_module_project_documentation.md)
* **Word Worksheet (Completed):** [Chatchawan Taja - ใบงานที่ 2 Requirement และ System Block Diagram (Completed).docx](file:///d:/Iven/IoT/docs/Chatchawan%20Taja%20-%20ใบงานที่%202%20Requirement%20และ%20System%20Block%20Diagram%20(Completed).docx)

### Visual Artifacts & Renders:
1. **แบบแปลนลายวงจร PCB (EDA CAD Blueprint):** [pcb_eda_cad_layout_blueprint.png](file:///d:/Iven/IoT/images/pcb_eda_cad_layout_blueprint.png)
2. **บอร์ด PCB ดีไซน์ใหม่ (Rev 2.0):** [pcb_rev2_compact_design_render.png](file:///d:/Iven/IoT/images/pcb_rev2_compact_design_render.png)
3. **ผังเส้นทางไฟและสัญญาณเสมือนจริง:** [photorealistic_wiring_power_signal_flow.png](file:///d:/Iven/IoT/images/photorealistic_wiring_power_signal_flow.png)
4. **Block Diagram ฉบับเข้าใจง่าย:** [system_block_diagram_simple.png](file:///d:/Iven/IoT/images/system_block_diagram_simple.png)
5. **ภาพชี้ตำแหน่งอุปกรณ์ 3D:** [tharit_rs485_module_render_3d_annotated.png](file:///d:/Iven/IoT/images/tharit_rs485_module_render_3d_annotated.png)
6. **ภาพจำลองระบบจริงในห้องแล็บ:** [tharit_iot_rs485_system_simulation_annotated.png](file:///d:/Iven/IoT/images/tharit_iot_rs485_system_simulation_annotated.png)

---

## 4. Pinout & Wiring Rules (Quick Reference)

### ฝั่ง ESP32 (เชื่อมต่อ 6 ขาตามลำดับ Zero-Crossing Single-Layer):
* `1: 5V`  ➔ ช่องขา 5V / VIN ของ ESP32 (ไฟส่งไปเลี้ยงเซนเซอร์)
* `2: 3V3` ➔ ช่องขา 3V3 ของ ESP32 (ไฟเลี้ยงชิป SP3485)
* `3: RX`  ➔ ช่องขา GPIO16 ของ ESP32 (รับค่าตอบกลับ Response)
* `4: DE`  ➔ ช่องขา GPIO04 ของ ESP32 (สลับโหมด Half-Duplex รับ/ส่ง)
* `5: TX`  ➔ ช่องขา GPIO17 ของ ESP32 (ส่งคำสั่ง Master Request)
* `6: GND` ➔ ช่องขา GND ของ ESP32 (กราวด์ร่วมระบบ)

### ฝั่งเซนเซอร์ XY-MD02 (Screw Terminal 4 ช่อง):
* `1: V+`  ➔ สายสีแดง (ไฟเลี้ยงเซนเซอร์ DC 5V-24V)
* `2: GND` ➔ สายสีดำ (กราวด์)
* `3: A+`  ➔ สายสีเหลือง (RS-485 Differential Data+)
* `4: B-`  ➔ สายสีเขียว (RS-485 Differential Data-)
