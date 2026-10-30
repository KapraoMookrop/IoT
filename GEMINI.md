# GEMINI.md: RS-485 Industrial Extension Module for THARIT-IoT (XY-MD02 / SHT20)

## 1. Project Overview & Architecture Decisions
* **Project Name:** RS-485 Industrial Extension Module สำหรับเชื่อมต่อเซนเซอร์ XY-MD02 (SHT20) ร่วมกับ THARIT-IoT
* **Course:** การออกแบบระบบสมองกลฝังตัวและ IoT (สัปดาห์ที่ 2: Requirement และ System Block Diagram)
* **Lead / System Architect:** ชัชวาล ตาจา (Chatchawan Taja)
* **Status:** Requirement & System Architecture Completed (Draft v0.1)

### Key Architectural Decisions (From /grill-me Alignment):
1. **Direction Control (Half-Duplex):** ใช้ขา GPIO จากบอร์ดหลัก THARIT-IoT ควบคุมขา DE และ /RE ร่วมกัน เพื่อความแม่นยำสูงสุดตามมาตรฐาน Modbus RTU (Switching delay < 2 ms)
2. **Power Architecture:** Dual-Source Jumper (J_PWR):
   - รองรับไฟเลี้ยง 5V จากบอร์ดหลัก THARIT-IoT สำหรับการใช้งานระยะสั้น
   - รองรับแหล่งจ่ายไฟภายนอก DC 12V-24V สำหรับการเดินสายเซนเซอร์ระยะไกลเพื่อป้องกัน Voltage Drop
3. **Transceiver & Protection Circuitry:**
   - ชิป Transceiver: 3.3V Low-Power (SP3485 / MAX3485) เข้ากันได้กับระดับตรรกะ 3.3V ของ MCU ESP32 โดยตรง
   - วงจรป้องกัน: TVS Diode Array (ESD ทนแรงดัน ±8 kV), PTC Resettable Fuse (100 mA), Fail-safe Bias Resistors (Pull-up A+ / Pull-down B-) และตัวต้านทาน 120 Ω Termination Resistor พร้อม Jumper (J_TERM)
4. **Form Factor:** Stackable Extension Shield เสียบตรงเข้ากับ Expansion Header ของบอร์ด THARIT-IoT พร้อมขั้วต่อ Industrial 4-Pin Screw Terminal Block (V+, GND, A+, B-) ด้านข้าง

---

## 2. Deliverables & Artifacts Generated
* **Worksheet Document (Completed):** `c:\Project\IoT\Chatchawan Taja - ใบงานที่ 2 Requirement และ System Block Diagram (Completed).docx`
* **System Block Diagram Graphic:** `c:\Project\IoT\system_block_diagram.png`
* **Project Specification & Engineering Requirements:** `c:\Project\IoT\rs_485_extension_module_project_documentation.md`
* **Automation Helper Script:** `c:\Project\IoT\fill_worksheet.py`
* **PCB Hardware Design Specification (Completed):** `c:\Project\IoT\PCB_HARDWARE_DESIGN_SPEC.md`
* **3D Photorealistic Module Render:** `c:\Project\IoT\tharit_rs485_module_render_3d.jpg`
* **Full System Realistic Simulation Photo:** `c:\Project\IoT\tharit_iot_rs485_system_simulation.jpg`

---

## 3. Engineering Requirements Summary (Traceability Baseline)
* **REQ-RS485-01 (Functional):** แปลงสัญญาณ UART 3.3V เป็น RS-485 Differential (A+, B-) สื่อสารกับ XY-MD02 ที่ Baud rate 9,600 bps (8N1) และรองรับสูงสุด 115,200 bps
* **REQ-RS485-02 (Functional):** สลับสถานะ Transmit / Receive แบบ Half-Duplex ภายใน < 2 ms
* **REQ-RS485-03 (Interface):** เชื่อมต่อกับบอร์ดหลัก THARIT-IoT ผ่าน Header Pin (UART TX, RX, GPIO DE/RE, VCC 3.3V/5V, GND)
* **REQ-RS485-04 (Interface):** ขั้วต่อ Screw Terminal Block 4 ช่อง สำหรับสาย A+, B-, V+, GND (DC 5V-24V)
* **REQ-RS485-05 (Safety/Fault):** วงจรป้องกันไฟกระชาก TVS Diode (ESD ±8 kV) และ PTC Resettable Fuse ป้องกันกระแสเกิน
* **REQ-RS485-06 (Safety/Fault):** ตัวต้านทาน Termination 120 Ω พร้อม Jumper และตัวต้านทาน Fail-safe Bias

---

## 4. Hardware Design Progress (Week 3 Completed)
1. **PCB Form Factor & Layout Blueprint:** บอร์ด 2 เลเยอร์ ขนาด $50.8 \times 28.0\text{ mm}$ พร้อมรูยึด M3, ขั้วต่อ Screw Terminal 4 พิน ($3.81\text{ mm}$), Header 6 พินเสียบตรงกับบอร์ด THARIT-IoT
2. **Bill of Materials (BOM) & Components:** ระบุเบอร์ชิ้นส่วน SMD พร้อมตัวอย่าง MPN จริง (SP3485E, SM712, 100mA PTC, 120Ω Term, Fail-safe 4.7k, 3-Color Status LEDs)
3. **Photorealistic 3D Renders:** สร้างภาพเรนเดอร์ 3 มิติเสมือนจริงของตัวบอร์ดและภาพจำลองการต่อร่วมกับบอร์ดหลัก THARIT-IoT และเซนเซอร์ XY-MD02 (SHT20) สำเร็จครบถ้วน
