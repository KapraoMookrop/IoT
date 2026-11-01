# RS-485 Industrial Extension Module สำหรับ THARIT-IoT (XY-MD02 / SHT20)

**ผู้ออกแบบ / System Architect:** ชัชวาล ตาจา (Chatchawan Taja)  
**เวอร์ชันบอร์ด:** Hardware Revision v2.2 (Single-Layer Zero-Crossing & Complete Component Edition)  
**สถานะ:** ดีไซน์สมบูรณ์ - แก้ปัญหาเส้นทับกัน 100% (True Zero-Crossing) • ลายทองแดงหน้าเดียว (Single-Layer) • แสดงตัวต้านทานครบทุกตัว

---

## 📌 สรุปภาพรวมสถาปัตยกรรม (Architectural Summary)
โมดูลขยายสัญญาณอุตสาหกรรม RS-485 สำหรับบอร์ดหลัก **THARIT-IoT** เพื่อเชื่อมต่อกับเซนเซอร์วัดอุณหภูมิและความชื้นสัมพัทธ์ **XY-MD02 (SHT20)** ด้วยโปรโตคอล **Modbus RTU** ระยะไกลสูงสุด $1,200\text{ เมตร}$

### จุดเด่นของการออกแบบ Revision v2.2:
1. **Zero-Crossing Single-Layer:** จัดวางพินขั้วต่อใหม่ทำให้สามารถเดินลายทองแดงหน้าเดียวได้ 100% โดยไม่มีเส้นตัดข้ามสายแม้แต่เส้นเดียว
2. **ขั้วต่อ Terminal Block เรียงตาม Differential Pair:** จัดเรียงช่องเป็น `[1:V+, 2:A+, 3:B-, 4:GND]` ทำให้คู่สาย A+/B- ขนานตรงกลางตามมาตรฐาน IPC-2141 และเส้น GND ด้านล่างวิ่งเข้าช่อง 4 ตรงๆ
3. **วงจรไฟสถานะ LED 3 สี พร้อมตัวต้านทานคุมกระแส:** หลอดไฟ LED ทุกดวง (PWR, TX, RX) มีตัวต้านทาน $1\text{ k}\Omega$ แยกตัวถังชัดเจน (R1, R2, R3) และต่อแบบ **"แท็ปแยกสาขาลง GND"** ไม่คั่นกลางสายสัญญาณ ทำให้รูปคลื่นสัญญาณ UART ไม่ดรอป
4. **เกราะป้องกันทางไฟฟ้าอุตสาหกรรมครบชุด:** TVS Diode Array `SM712` ป้องกันเสิร์จ $\pm 8\text{ kV}$, ฟิวส์ตัดตอนอัตโนมัติ `PTC 100mA` 2 ตัว, วงจร Termination 120Ω (`J_TERM` + `R_TERM`), และตัวต้านทาน Fail-Safe Bias (`R_PU` 4.7k, `R_PD` 4.7k)

---

## 🔌 การเชื่อมต่อพินและอุปกรณ์ (Pinout & Wiring)

### ขั้วต่อ ESP32 Interface Header (1x6 Pin Male Header 2.54mm):
* `Pin 1: 5V`  ➔ ไฟ 5V จากบอร์ดหลัก วิ่งเข้า J_PWR พิน 1 เพื่อจ่ายไฟให้เซนเซอร์
* `Pin 2: 3V3` ➔ ไฟ 3.3V เลี้ยงชิป SP3485 (VCC), C1, และ R1 LED PWR
* `Pin 3: RX`  ➔ สัญญาณรับ Modbus Response เข้า GPIO16 ของ ESP32
* `Pin 4: DE`  ➔ สัญญาณสลับทิศทาง Half-Duplex ควบคุมจาก GPIO04 ของ ESP32 พร้อม R_DE Pulldown 10k
* `Pin 5: TX`  ➔ สัญญาณส่ง Modbus Request จาก GPIO17 ของ ESP32
* `Pin 6: GND` ➔ กราวด์ร่วมระบบ วิ่งลง Bottom Ground Bus

### ขั้วต่อเซนเซอร์ Screw Terminal Block (4 ช่อง Pitch 3.81mm):
* `ช่อง 1: V+`  ➔ **สายสีแดง (V+)**: ไฟเลี้ยงเซนเซอร์ DC 5V-24V
* `ช่อง 2: A+`  ➔ **สายสีเหลือง (A+)**: RS-485 Data+ ผ่านฟิวส์ F1 และ TVS
* `ช่อง 3: B-`  ➔ **สายสีเขียว หรือ ขาว (B-)**: RS-485 Data- ผ่านฟิวส์ F2 และ TVS
* `ช่อง 4: GND` ➔ **สายสีดำ (GND)**: กราวด์ร่วมระบบเซนเซอร์

---

## 📁 สารบัญเอกสารและไฟล์ในระบบ (Project Deliverables)
* [Chatchawan Taja - ใบงานที่ 2 Requirement และ System Block Diagram (Revision v2.2).docx](file:///c:/Project/IoT/docs/Chatchawan%20Taja%20-%20ใบงานที่%202%20Requirement%20และ%20System%20Block%20Diagram%20(Revision%20v2.2).docx) — ไฟล์ใบงานฉบับสมบูรณ์ที่กรอกข้อมูล Rev v2.2 ครบถ้วน
* [GEMINI.md](file:///c:/Project/IoT/GEMINI.md) — สรุปสถาปัตยกรรมและกฎข้อบังคับของระบบ (Single Source of Truth)
* [PCB_HARDWARE_DESIGN_SPEC.md](file:///c:/Project/IoT/PCB_HARDWARE_DESIGN_SPEC.md) — ข้อกำหนดการออกแบบทางวิศวกรรม PCB และรายการอุปกรณ์ (BOM)
* [rs_485_extension_module_project_documentation.md](file:///c:/Project/IoT/rs_485_extension_module_project_documentation.md) — เอกสารทางวิศวกรรมระบบหลักและผลการวิเคราะห์

### ภาพแบบแปลนและไดอะแกรมสำคัญ:
1. [pcb_complete_component_blueprint.png](file:///c:/Project/IoT/images/pcb_complete_component_blueprint.png) — แบบแปลนวงจรแยกอุปกรณ์ครบถ้วน (Rev 2.2 Complete Component Blueprint)
2. [pcb_zero_crossing_blueprint.png](file:///c:/Project/IoT/images/pcb_zero_crossing_blueprint.png) — แบบแปลนลายวงจรไร้เส้นทับกัน 100% (Zero-Crossing Edition)
3. [pcb_rev2_compact_design_render.png](file:///c:/Project/IoT/images/pcb_rev2_compact_design_render.png) — ภาพเรนเดอร์บอร์ด PCB 3D พร้อมผังระบุพิน
4. [photorealistic_wiring_power_signal_flow.png](file:///c:/Project/IoT/images/photorealistic_wiring_power_signal_flow.png) — ผังเส้นทางไฟและสัญญาณเสมือนจริงของทั้งระบบ
5. [system_block_diagram_simple.png](file:///c:/Project/IoT/images/system_block_diagram_simple.png) — แผนผังบล็อกระบบฉบับเข้าใจง่าย

