# GEMINI.md: RS-485 Industrial Extension Module for THARIT-IoT (XY-MD02 / SHT20)

## 1. Project Overview & Architecture Decisions
* **Project Name:** RS-485 Industrial Extension Module สำหรับเชื่อมต่อเซนเซอร์ XY-MD02 (SHT20) ร่วมกับ THARIT-IoT
* **Course:** การออกแบบระบบสมองกลฝังตัวและ IoT (สัปดาห์ที่ 2-3: Requirement, Block Diagram และ PCB Hardware Design)
* **Lead / System Architect:** ชัชวาล ตาจา (Chatchawan Taja)
* **Status:** Hardware Revision v2.2 (Single-Layer Zero-Crossing & Complete Component Edition) - Specification & Design Completed

### Key Architectural Decisions (From /grill-me Alignment):
1. **Target PCB Fabrication Strategy:**
   - **Primary Target:** ออกแบบเป็น **Single-Layer 100% (บอร์ดหน้าเดียว ลายทองแดงไม่ทับกัน)** กัดแผ่นปริ้นท์ง่าย เหมาะสำหรับทำในห้องแล็บ
   - **Fallback Alternative:** หากการเดินลายวงจรในโปรแกรม CAD มีข้อจำกัดเรื่องพื้นที่ สามารถสลับเป็น **Double-Layer (บอร์ด 2 หน้า)** โดยกำหนดให้เลเยอร์ล่าง (Bottom Layer) เป็น Solid Ground Plane และเจาะ Via กราวด์ลงแผ่นล่างทั้งหมด
2. **Direction Control (Half-Duplex):** ใช้ขา GPIO04 จากบอร์ดหลัก THARIT-IoT ควบคุมขา DE และ /RE ร่วมกัน เพื่อความแม่นยำสูงสุดตามมาตรฐาน Modbus RTU (Switching delay < 2 ms) พร้อมตัวต้านทาน Pulldown `R_DE` (10 kΩ) ดึงลง GND ให้เริ่มที่โหมดรับเสมอ
3. **Dual-Source Power Architecture (J_PWR):**
   - **โหมดไฟบอร์ด (5V):** เสียบช็อตขา 1-2 ดึงไฟเลี้ยง 5V จากบอร์ดหลัก THARIT-IoT ไปเลี้ยงเซนเซอร์ (สำหรับเทสในแล็บ / สายสั้น < 10m)
   - **โหมดไฟภายนอก (EXT):** เสียบช็อตขา 2-3 รับไฟ DC 12V-24V จากภายนอก สำหรับเดินสายเซนเซอร์ระยะไกลเพื่อป้องกัน Voltage Drop
4. **Transceiver & Protection Circuitry:**
   - **ชิป Transceiver:** 3.3V Low-Power `SP3485E` เข้ากันได้กับระดับตรรกะ 3.3V ของ MCU ESP32 โดยตรง
   - **วงจรป้องกัน:** TVS Diode Array `SM712` (ESD ทนแรงดัน ±8 kV), PTC Resettable Fuse `F1, F2` (100 mA, 60V) 2 ตัว ป้องกันการช็อตสายผิดขั้ว
   - **Termination & Fail-Safe Bias:** ตัวต้านทาน `R_TERM` (120 Ω) อนุกรมกับ Jumper `J_TERM` วางคร่อมระหว่างสาย A+ และ B- โดยตรง, พร้อม `R_PU` (4.7 kΩ) ดึง A+ ขึ้น 3.3V และ `R_PD` (4.7 kΩ) ดึง B- ลง GND
5. **Discrete Status LEDs Circuitry (R1, R2, R3 + LED1, LED2, LED3):**
   - ไฟสถานะแต่ละดวงต้องมีตัวต้านทานจำกัดกระแสแยกตัวถังชัดเจน (R = 1 kΩ SMD 0805)
   - ต่อแบบ **"แท็ปแยกสาขาลง GND (Branch Tap to GND)"** ไม่ต่อคั่นกลางสายสัญญาณหลัก เพื่อรักษารูปคลื่นสัญญาณ UART Modbus ให้คมชัด 100%
   - `LED1 (PWR เขียว)` + `R1 (1k)`: ต่อกับไฟ 3.3V
   - `LED2 (TX น้ำเงิน)` + `R2 (1k)`: ต่อกับสัญญาณ TX (GPIO17)
   - `LED3 (RX ส้ม/เหลือง)` + `R3 (1k)`: ต่อกับสัญญาณ RX (GPIO16 / RO)
6. **Form Factor & True Zero-Crossing Layout (Revision v2.2):**
   - **ฝั่งต่อ ESP32 (CN1: 1x6 Pin Header 2.54mm):** เรียงลำดับ `[1:5V, 2:3V3, 3:RX, 4:DE, 5:TX, 6:GND]` สอดรับกับแนวขา IC โดยตรง
   - **ฝั่งต่อเซนเซอร์ (TB1: 4-Pin Screw Terminal Block 3.81mm):** จัดเรียงลำดับใหม่เป็น `[1:V+, 2:A+, 3:B-, 4:GND]` เพื่อให้คู่สายต่างศักย์ (A+/B-) อยู่ติดกันตรงกลางเป็น Differential Pair ตาม IPC-2141 และเส้น GND Bus ด้านล่างวิ่งเข้าช่อง 4 ตรงๆ โดยไม่ตัดผ่ากลางสายสัญญาณใดๆ

---

## 2. โครงสร้างโฟลเดอร์ของโปรเจกต์ (Project Directory Structure)
```
c:\Project\IoT\
├── docs\                     # เอกสารส่งงานและใบงาน Word (.docx)
├── images\                   # คลังภาพผลงานและแบบแปลนทางวิศวกรรมหลัก (.png, .jpg)
│   └── raw\                  # ไฟล์ภาพร่างและภาพอ้างอิงชั่วคราว
├── scripts\                  # สคริปต์ Python สำหรับวาดแปลนและสร้างภาพประกอบ (.py)
├── README.md                 # คู่มือและสารบัญโปรเจกต์ฉบับสมบูรณ์
├── GEMINI.md                 # สรุปสถาปัตยกรรมและกฎข้อบังคับของระบบ (Single Source of Truth)
├── PCB_HARDWARE_DESIGN_SPEC.md # สเปกฮาร์ดแวร์ PCB และรายการอุปกรณ์ (BOM Revision v2.2)
└── rs_485_extension_module_project_documentation.md # เอกสารทางวิศวกรรมระบบหลัก
```

---

## 3. Deliverables & Artifacts Generated
* **Hardware Specification (Rev 2.2):** [PCB_HARDWARE_DESIGN_SPEC.md](file:///c:/Project/IoT/PCB_HARDWARE_DESIGN_SPEC.md)
* **Project Specification & Engineering Requirements:** [rs_485_extension_module_project_documentation.md](file:///c:/Project/IoT/rs_485_extension_module_project_documentation.md)
* **Word Worksheet (Revision v2.2 Completed):** [Chatchawan Taja - ใบงานที่ 2 Requirement และ System Block Diagram (Revision v2.2).docx](file:///c:/Project/IoT/docs/Chatchawan%20Taja%20-%20ใบงานที่%202%20Requirement%20และ%20System%20Block%20Diagram%20(Revision%20v2.2).docx)
* **Word Worksheet (Original Template):** [Chatchawan Taja - ใบงานที่ 2 Requirement และ System Block Diagram.docx](file:///c:/Project/IoT/docs/Chatchawan%20Taja%20-%20ใบงานที่%202%20Requirement%20และ%20System%20Block%20Diagram.docx)

### Visual Artifacts & Renders:
1. **แบบแปลนวงจรแยกอุปกรณ์ครบถ้วน (Rev 2.2 Blueprint):** [pcb_complete_component_blueprint.png](file:///c:/Project/IoT/images/pcb_complete_component_blueprint.png)
2. **แบบแปลนลายวงจรไร้เส้นทับกัน (Zero-Crossing Edition):** [pcb_zero_crossing_blueprint.png](file:///c:/Project/IoT/images/pcb_zero_crossing_blueprint.png)
3. **แบบแปลนลายวงจร PCB EDA CAD ดั้งเดิม:** [pcb_eda_cad_layout_blueprint.png](file:///c:/Project/IoT/images/pcb_eda_cad_layout_blueprint.png)
4. **บอร์ด PCB ดีไซน์ใหม่ 3D Render:** [pcb_rev2_compact_design_render.png](file:///c:/Project/IoT/images/pcb_rev2_compact_design_render.png)
5. **ผังเส้นทางไฟและสัญญาณเสมือนจริง:** [photorealistic_wiring_power_signal_flow.png](file:///c:/Project/IoT/images/photorealistic_wiring_power_signal_flow.png)
6. **Block Diagram ฉบับเข้าใจง่าย:** [system_block_diagram_simple.png](file:///c:/Project/IoT/images/system_block_diagram_simple.png)
7. **ภาพชี้ตำแหน่งอุปกรณ์ 3D:** [tharit_rs485_module_render_3d_annotated.png](file:///c:/Project/IoT/images/tharit_rs485_module_render_3d_annotated.png)
8. **ภาพจำลองระบบจริงในห้องแล็บ:** [tharit_iot_rs485_system_simulation_annotated.png](file:///c:/Project/IoT/images/tharit_iot_rs485_system_simulation_annotated.png)

---

## 4. Pinout & Wiring Rules (Quick Reference Revision v2.2)

### ฝั่ง ESP32 (Header 1x6 เชื่อมต่อ 6 ขาตามลำดับ Zero-Crossing Single-Layer):
* `1: 5V`  ➔ ช่องขา 5V / VIN ของ ESP32 (ไฟส่งไปเลี้ยงเซนเซอร์ผ่าน J_PWR)
* `2: 3V3` ➔ ช่องขา 3V3 ของ ESP32 (ไฟเลี้ยงชิป SP3485, C1, R_PU, และ R1 LED PWR)
* `3: RX`  ➔ ช่องขา GPIO16 ของ ESP32 (รับค่าตอบกลับ Modbus Response พร้อมแท็ปเข้า R3 LED RX)
* `4: DE`  ➔ ช่องขา GPIO04 ของ ESP32 (สลับโหมด Half-Duplex รับ/ส่ง พร้อม R_DE Pulldown)
* `5: TX`  ➔ ช่องขา GPIO17 ของ ESP32 (ส่งคำสั่ง Master Request พร้อมแท็ปเข้า R2 LED TX)
* `6: GND` ➔ ช่องขา GND ของ ESP32 (กราวด์ร่วมระบบ วิ่งลง Bottom Ground Bus)

### ฝั่งเซนเซอร์ XY-MD02 (Screw Terminal Block 4 ช่อง Revision v2.2):
* `1: V+`  ➔ **สายสีแดง (V+)**: ไฟเลี้ยงเซนเซอร์ DC 5V-24V รับจากพินกลาง J_PWR
* `2: A+`  ➔ **สายสีเหลือง (A+)**: สัญญาณ RS-485 Data+ ผ่านฟิวส์ F1 และ TVS SM712
* `3: B-`  ➔ **สายสีเขียว หรือ ขาว (B-)**: สัญญาณ RS-485 Data- ผ่านฟิวส์ F2 และ TVS SM712
* `4: GND` ➔ **สายสีดำ (GND)**: กราวด์อ้างอิงเซนเซอร์ ต่อตรงเข้า Bottom Ground Bus
