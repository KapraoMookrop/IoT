# โครงงาน: RS-485 Industrial Extension Module สำหรับเชื่อมต่อเซนเซอร์ XY-MD02 (SHT20) ร่วมกับ THARIT-IoT

**รายวิชา:** การออกแบบระบบสมองกลฝังตัวและ IoT (สัปดาห์ที่ 2: Requirement และ System Block Diagram)  
**ระดับชั้น:** ปริญญาตรี ปีที่ 2  
**สถานะเอกสาร:** Draft v0.1  
**ผู้รับผิดชอบหลัก:** ชัชวาล ตาจา (System Architect / Hardware Interface & Requirement)

---

## 1. ภาพรวมโครงงาน (Project Overview)

โครงงานนี้เป็นการออกแบบ **แผ่นวงจรขยาย (Extension Module)** สำหรับบอร์ดประมวลผลหลัก **THARIT-IoT** เพื่อเพิ่มขีดความสามารถในการสื่อสารข้อมูลระยะไกลผ่านมาตรฐานอุตสาหกรรม **RS-485** โดยมุ่งเน้นการเชื่อมต่อกับเซนเซอร์วัดอุณหภูมิและความชื้นสัมพัทธ์เกรดอุตสาหกรรมรุ่น **XY-MD02** (ซึ่งใช้ชิปเซนเซอร์ความแม่นยำสูง **SHT20** ภายใน และสื่อสารด้วยโปรโตคอล **Modbus RTU**)

### ทำไมต้องใช้ RS-485 คู่กับ XY-MD02 (SHT20)?
1. **แก้ปัญหาข้อจำกัดระยะทางของบอร์ดหลัก:** พอร์ตสื่อสารของ THARIT-IoT เป็นระดับแรงดันตรรกะ (UART $3.3\text{ V}$) ซึ่งลากสายได้เพียงระยะสั้นๆ หากเดินสายยาวในฟาร์มหรือโรงงาน สัญญาณจะดรอปและถูกคลื่นรบกวน (EMI) ทันที
2. **การส่งสัญญาณแบบ Differential Signaling:** RS-485 ส่งข้อมูลด้วยความต่างศักย์ระหว่างสายคู่ตีเกลียว 2 เส้น ($\text{A+}$ และ $\text{B-}$) ทำให้ทนทานต่อสัญญาณรบกวนสูงมาก และลากสายได้ไกลถึง $500 - 1,200\text{ เมตร}$
3. **รองรับการพ่วงหลายจุด (Multi-drop / Daisy Chain):** สายสัญญาณคู่เดิมสามารถพ่วงเซนเซอร์ XY-MD02 หรืออุปกรณ์ Modbus อื่นๆ เพิ่มได้หลายตัวโดยกำหนดหมายเลข Address (Slave ID) แยกกัน

---

## 2. ข้อมูลจำเพาะของเซนเซอร์เป้าหมาย: XY-MD02 (SHT20)

เพื่อให้การออกแบบโมดูล 확장 (Extension Board) ทำงานร่วมกับเซนเซอร์ได้อย่างสมบูรณ์ จึงอ้างอิงพารามิเตอร์ของ **XY-MD02** ดังนี้:

* **เซนเซอร์ตรวจวัดภายใน:** Sensirion SHT20
* **ช่วงการวัดอุณหภูมิ:** $-40^\circ\text{C}$ ถึง $+80^\circ\text{C}$ (ความละเอียด $0.1^\circ\text{C}$)
* **ช่วงการวัดความชื้นสัมพัทธ์:** $0\%$ ถึง $100\%\text{ RH}$ (ความละเอียด $0.1\%\text{ RH}$)
* **แรงดันไฟเลี้ยง ($\text{V+}$):** $\text{DC } 5\text{ V} - 30\text{ V}$ (กินกระแสต่ำ $< 20\text{ mA}$)
* **การเชื่อมต่อสายไฟ (4 เส้น):**
  * **สายสีแดง ($\text{V+}$):** ไฟเลี้ยง $\text{DC } 5\text{ V} - 24\text{ V}$
  * **สายสีดำ ($\text{GND}$):** กราวด์
  * **สายสีเหลือง ($\text{A+}$ หรือ $\text{D+}$):** สัญญาณ RS-485 A+
  * **สายสีขาว/เขียว ($\text{B-}$ หรือ $\text{D-}$):** สัญญาณ RS-485 B-

### รูปแบบโปรโตคอล Modbus RTU ของ XY-MD02
* **Baud Rate มาตรฐาน:** $9,600\text{ bps}$ (ตั้งค่าได้: $9600, 14400, 19200$)
* **Frame Format:** $8\text{ Data bits, No Parity, } 1\text{ Stop bit (8N1)}$
* **Default Slave ID:** `0x01` ($1$)
* **Function Code สำหรับอ่านค่า:** `0x04` (Read Input Registers)
* **ตำแหน่ง Register:**
  * `0x0001`: ค่าอุณหภูมิ (หารด้วย $10$ เพื่อแปลงเป็นทศนิยม เช่น อ่านได้ `285` $= 28.5^\circ\text{C}$)
  * `0x0002`: ค่าความชื้นสัมพัทธ์ (หารด้วย $10$ เช่น อ่านได้ `652` $= 65.2\%\text{ RH}$)

**ตัวอย่างเฟรมคำสั่งที่ THARIT-IoT ต้องส่งออกไปอ่านค่าทั้งอุณหภูมิและความชื้นพร้อมกัน:**
```text
Request (Master -> XY-MD02):  [01] [04] [00 01] [00 02] [20 0B]
Response (XY-MD02 -> Master): [01] [04] [04] [01 1D] [02 8C] [6A 4F]
                                              |       |
                                    Temp: 0x011D     Humid: 0x028C
                                    (285 -> 28.5°C)  (652 -> 65.2%RH)
```

---

## 3. วิเคราะห์ Use Case และ System Boundary

### 3.1 ผู้ใช้เป้าหมายและปัญหาที่พบ (Target Users & Pain Points)
ผู้ใช้เป้าหมายคือ นักพัฒนาอุปกรณ์ IoT และผู้ดูแลระบบสมาร์ทฟาร์มหรือโรงงานที่ใช้งานบอร์ด **THARIT-IoT** เพื่อตรวจวัดสภาพแวดล้อม ปัญหาที่พบคือพอร์ตสื่อสารของบอร์ดหลักเป็นระดับแรงดันตรรกะ UART $3.3\text{ V}$ ซึ่งไม่สามารถลากสายสัญญาณระยะไกลและไม่สามารถเชื่อมต่อกับเซนเซอร์วัดอุณหภูมิ-ความชื้นเกรดอุตสาหกรรม **XY-MD02 (SHT20)** ที่สื่อสารผ่านมาตรฐาน RS-485 Modbus RTU ได้โดยตรง จึงจำเป็นต้องมีโมดูลขยาย (Extension Module) ทำหน้าที่แปลงสัญญาณและป้องกันสัญญาณรบกวนทางไฟฟ้าเพื่อให้รับส่งข้อมูลระยะไกลได้อย่างเสถียร

### 3.2 สถานการณ์ใช้งานจริง (Input $\rightarrow$ Processing $\rightarrow$ Output/Outcome)
* **Input:** บอร์ดหลัก THARIT-IoT ส่งเฟรมคำสั่ง Modbus RTU (เช่น Function Code `0x04` เพื่อขออ่านค่า Input Register ของ SHT20) ออกทางขา UART ($\text{TX}$) พร้อมสัญญาณควบคุมทิศทางและไฟเลี้ยง
* **Processing:** โมดูลเสริมรับสัญญาณ UART $3.3\text{ V}$ เข้าสู่ชิป RS-485 Transceiver เพื่อแปลงเป็นสัญญาณแรงดันผลต่าง (Differential Signaling บนสายคู่ $\text{A+}$ และ $\text{B-}$) พร้อมผ่านวงจรป้องกันไฟกระชาก (TVS Protection)
* **Output/Outcome:** ส่งสัญญาณผ่านสายคู่ตีเกลียวไปยังเซนเซอร์ XY-MD02 (SHT20) และรับข้อมูลอุณหภูมิและความชื้นสัมพัทธ์ที่เซนเซอร์ตอบกลับ แปลงคืนเป็นสัญญาณ UART ($\text{RX}$) ส่งเข้าสู่บอร์ด THARIT-IoT เพื่อนำไปแสดงผลหรือส่งขึ้นระบบ Cloud ได้อย่างแม่นยำ

### 3.3 ขอบเขตของระบบ (System Boundary)
* **ในขอบเขต (In-Scope / สิ่งที่กลุ่มออกแบบสร้างเอง):**
  * แผงวงจร Expansion Module พร้อมชิปแปลงสัญญาณ UART $\leftrightarrow$ RS-485 ($3.3\text{ V}$ Transceiver เช่น `SP3485` หรือ `MAX3485`)
  * วงจรควบคุมทิศทางรับ-ส่ง (Auto-Direction หรือควบคุมผ่านขา $\text{DE}/\overline{\text{RE}}$)
  * วงจรป้องกันไฟกระชากและกระแสเกิน (TVS Diode, PTC Resettable Fuse)
  * ตัวต้านทานจบสาย $120\,\Omega$ (Termination Resistor) พร้อม Jumper และตัวต้านทาน Fail-safe Bias
  * ขั้วต่อ Screw Terminal 4 ช่อง ($\text{V+}, \text{GND}, \text{A+}, \text{B-}$) สำหรับต่อสายไปยังเซนเซอร์ XY-MD02
* **นอกขอบเขต (Out-of-Scope):**
  * ตัวฮาร์ดแวร์เซนเซอร์สำเร็จรูป XY-MD02 (SHT20)
  * แหล่งจ่ายไฟภายนอกระดับ $\text{DC } 9\text{ V} - 24\text{ V}$ (ในกรณีจ่ายไฟแยกให้เซนเซอร์ที่จุดปลายทางระยะไกล)
  * สายเคเบิลเดินภายนอกอาคาร
* **งานที่ต้องพึ่งบอร์ดหลัก (THARIT-IoT Dependency):**
  * แหล่งจ่ายไฟเลี้ยงวงจรตรรกะ $3.3\text{ V} / 5\text{ V}$ และ $\text{GND}$
  * พอร์ตสื่อสารฮาร์ดแวร์ UART ($\text{TX}, \text{RX}$)
  * ซอฟต์แวร์จัดการโปรโตคอล Modbus RTU Master (การสร้าง Packet, คำนวณ $\text{CRC16}$ และการแปลงค่า Register เป็นทศนิยม)

---

## 4. ข้อกำหนดทางวิศวกรรม (Engineering Requirements)

| REQ-ID | ชนิด | ข้อกำหนด “ระบบต้อง…” | เหตุผล / แหล่งที่มา / สถานะ |
| :--- | :--- | :--- | :--- |
| **REQ-RS485-01** | Functional | ระบบต้องสามารถแปลงสัญญาณ UART $3.3\text{ V}$ จากบอร์ด THARIT-IoT เป็นสัญญาณ RS-485 Differential ($\text{A+}, \text{B-}$) เพื่อสื่อสารกับเซนเซอร์ XY-MD02 (SHT20) ที่ความเร็ว Baud rate มาตรฐาน $9,600\text{ bps}$ (8N1) และรองรับสูงสุดถึง $115,200\text{ bps}$ ได้ | เซนเซอร์ XY-MD02 ใช้ค่าเริ่มต้นจากโรงงานคือ Baud rate $9,600\text{ bps}$, 8N1<br>**สถานะ:** ยืนยันแล้ว (ตาม Datasheet XY-MD02) |
| **REQ-RS485-02** | Functional | ระบบต้องสามารถสลับสถานะการส่งคำสั่ง (Transmit) และการรอรับข้อมูลตอบกลับ (Receive) แบบ Half-Duplex ได้ภายในเวลาไม่เกิน $2\text{ ms}$ ก่อนที่เซนเซอร์ XY-MD02 จะส่งเฟรมข้อมูลตอบกลับ | ป้องกันการสูญหายของไบต์แรกจากเซนเซอร์ XY-MD02 ขณะสลับทิศทางบัส RS-485<br>**สถานะ:** ยืนยันแล้ว |
| **REQ-RS485-03** | Interface | โมดูลต้องเชื่อมต่อกับบอร์ดหลัก THARIT-IoT ผ่านขั้วต่อ Header Pin โดยใช้สัญญาณ UART ($\text{TX}, \text{RX}$), ขาควบคุมทิศทาง (ถ้ามี), แรงดันไฟเลี้ยง $\text{VCC}$ ($3.3\text{ V}$ หรือ $5\text{ V}$) และ $\text{GND}$ ร่วมกัน | เพื่อให้เสียบใช้งานเข้ากับพอร์ตขยายของบอร์ด THARIT-IoT ได้โดยตรงโดยไม่ต้องดัดแปลงบอร์ดหลัก<br>**สถานะ:** TBR (ตรวจสอบผัง Pinout ของ THARIT-IoT) |
| **REQ-RS485-04** | Interface | ฝั่งเชื่อมต่ออุปกรณ์ภายนอกต้องมีขั้วต่อ Screw Terminal Block อย่างน้อย 4 ช่อง สำหรับสายสัญญาณ $\text{A+}, \text{B-}$ และขั้วจ่ายไฟเลี้ยงเซนเซอร์ XY-MD02 ($\text{V+}, \text{GND}$ รองรับแรงดัน $\text{DC } 5\text{ V} - 24\text{ V}$) | เซนเซอร์ XY-MD02 มีสายเชื่อมต่อ 4 เส้น ได้แก่ $\text{V+}, \text{GND}, \text{A+}$ และ $\text{B-}$<br>**สถานะ:** ยืนยันแล้ว |
| **REQ-RS485-05** | Safety / Fault | สายสัญญาณบัส RS-485 ($\text{A+}$ และ $\text{B-}$) ต้องมีวงจรป้องกันแรงดันไฟกระชากชั่วขณะ (TVS Diode) ที่ทนแรงดัน ESD ได้ไม่น้อยกว่า $\pm 8\text{ kV}$ และมีฟิวส์รีเซ็ตตัวเองได้ (PTC Resettable Fuse) ป้องกันกระแสเกิน | ป้องกันความเสียหายต่อชิป Transceiver และบอร์ด THARIT-IoT เมื่อเดินสายไปยังเซนเซอร์ XY-MD02 ในสภาพแวดล้อมจริง<br>**สถานะ:** ยืนยันแล้ว |
| **REQ-RS485-06** | Safety / Fault | ระบบต้องมีตัวต้านทาน Termination $120\,\Omega$ คร่อมระหว่างสาย $\text{A+}$ และ $\text{B-}$ พร้อม Jumper สำหรับเลือกเปิด/ปิดการใช้งาน และมีตัวต้านทาน Fail-safe Bias (Pull-up ที่ $\text{A+}$ / Pull-down ที่ $\text{B-}$) | รักษาระดับแรงดันบัสให้อยู่ในสถานะปลอดภัย (Idle state) เมื่อไม่มีการส่งข้อมูล หรือเมื่อสายเซนเซอร์หลุดขาด<br>**สถานะ:** ยืนยันแล้ว |

---

## 5. แผนผังบล็อกของระบบ (System Block Diagram)

```text
 ┌─────────────────────────────────────────────────────────────────────────────────┐
 │                                SYSTEM BOUNDARY                                  │
 │                                                                                 │
 │  ┌───────────────────────────────────────────────────────────────────────────┐  │
 │  │ THARIT-IoT Mainboard (Master Controller)                                  │  │
 │  │  • MCU (ESP32 / Processor)  • Modbus RTU Master Firmware                  │  │
 │  └──┬───────────────────▲───────────────────────┬─────────────────────────┬──┘  │
 │     │ Power (3.3V / 5V) │ UART RX (3.3V)        │ UART TX (3.3V)          │     │
 │     │ & GND             │ [TP1]                 │ [TP2]                   │     │
 │     │                   │                       │        Direction (DE/RE)│     │
 │  ┌──▼───────────────────┴───────────────────────▼─────────────────────────▼──┐  │
 │  │ RS-485 EXPANSION MODULE (ขอบเขตส่วนที่กลุ่มออกแบบและสร้าง)                     │  │
 │  │                                                                           │  │
 │  │  ┌────────────────────┐      ┌─────────────────────────────────────────┐  │  │
 │  │  │ Power Filtering &  │      │ 3.3V RS-485 Transceiver (SP3485/MAX3485)│  │  │
 │  │  │ V+ Source Selector │      │  + Auto-Direction / DE-RE Control       │  │  │
 │  │  │ Jumper (5V / Ext.) │      └────────────────────▲────────────────────┘  │  │
 │  │  └─────────┬──────────┘                           │ Differential A+ / B-  │  │
 │  │            │                         ┌────────────▼────────────┐          │  │
 │  │            │                         │ Bus Protection & Term.  │          │  │
 │  │            │                         │ • 120Ω Jumper           │          │  │
 │  │            │                         │ • Fail-safe Bias R      │          │  │
 │  │            │                         │ • PTC Fuse & TVS Diode  │          │  │
 │  │            │                         └────────────▲────────────┘          │  │
 │  │            │ V+, GND                              │ A+, B- [TP3, TP4]     │  │
 │  │  ┌─────────▼──────────────────────────────────────▼────────────────────┐  │  │
 │  │  │              4-Pin Screw Terminal Block (V+, GND, A+, B-)           │  │  │
 │  └──┴───────────────────────────────────┬─────────────────────────────────┴──┘  │
 └─────────────────────────────────────────┼───────────────────────────────────────┘
                                           │
                          สายเคเบิล 4 เส้น   │ (V+, GND, RS-485 A+, RS-485 B-)
                          (Twisted Pair)   │
  ┌────────────────────────────────────────▼───────────────────────────────────────┐
  │ EXTERNAL DEVICE (นอกขอบเขตการสร้างของโมดูล)                                      │
  │                                                                                │
  │  ┌──────────────────────────────────────────────────────────┐                  │
  │  │ เซนเซอร์วัดอุณหภูมิและความชื้น XY-MD02 (ชิป SHT20 ภายใน)     │                  │
  │  │ • Protocol: Modbus RTU Slave (ID = 0x01, Baud = 9600)    │                  │
  │  │ • Power Input: DC 5V–24V                                 │                  │
  │  └──────────────────────────────────────────────────────────┘                  │
  └────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. รายการเชื่อมต่อระหว่างโมดูล (Interface List)

| ID | From $\rightarrow$ To | ชนิด / ทิศทาง | Constraint / TBR / หลักฐาน |
| :--- | :--- | :--- | :--- |
| **IF-01** | THARIT-IoT Mainboard $\rightarrow$ Expansion Module | `UART TX` / Digital Signal (ทางเดียว) | Logic Level $3.3\text{ V}$ TTL, Baud rate $9,600\text{ bps}$ (มาตรฐาน XY-MD02), เอกสารตรวจ: Schematic ของ THARIT-IoT |
| **IF-02** | Expansion Module $\rightarrow$ THARIT-IoT Mainboard | `UART RX` / Digital Signal (ทางเดียว) | Logic Level ต้องไม่เกิน $3.3\text{ V}$ (ห้ามจ่าย $5\text{ V}$ เข้าขา MCU โดยตรง; ใช้ชิป $3.3\text{ V}$ เช่น `SP3485` หรือ `MAX3485`), เอกสารตรวจ: Datasheet ชิป Transceiver |
| **IF-03** | THARIT-IoT Mainboard $\rightarrow$ Expansion Module | `Power Supply` ($\text{VCC } 3.3\text{V}/5\text{V}, \text{GND}$) (ทางเดียว) | กระแสใช้งานของโมดูลและเซนเซอร์รวมกันต้องไม่เกินพิกัด LDO ของบอร์ดหลัก (XY-MD02 กินกระแสต่ำ $< 20\text{ mA}$), **TBR:** ตรวจพิกัดกระแสพอร์ต $5\text{ V}/3.3\text{ V}$ บนบอร์ดหลัก |
| **IF-04** | Expansion Module $\leftrightarrow$ XY-MD02 (SHT20 Sensor) | `RS-485 Bus` ($\text{A+}, \text{B-}$) / Differential (สองทาง Half-Duplex) | แรงดันผลต่าง $|V_{OD}| \ge 1.5\text{ V}$, โปรโตคอล Modbus RTU (Slave ID เริ่มต้น $= \text{0x01}$, Function $\text{0x04}$ อ่าน Address $\text{0x0001}$ และ $\text{0x0002}$), เอกสารตรวจ: คู่มือ XY-MD02 |
| **IF-05** | Expansion Module / Ext. Power $\rightarrow$ XY-MD02 (SHT20) | `Sensor Power` ($\text{V+}, \text{GND}$) (ทางเดียว) | แรงดันไฟเลี้ยง $\text{DC } 5\text{ V} - 24\text{ V}$ สำหรับเลี้ยงวงจรภายในหัววัด XY-MD02 (**TBR:** ตรวจสอบว่าจะดึงไฟ $5\text{ V}$ จากบอร์ดหลักผ่าน Terminal หรือต่อไฟเลี้ยง $12\text{ V}/24\text{ V}$ แยกจากภายนอก) |

---

## 7. ตารางตรวจสอบย้อนกลับข้อกำหนด (Requirements Traceability Matrix: RTM)

| REQ-ID | วิธี Verify | TC-ID | หลักฐานที่จะจัดเก็บ | สถานะ |
| :--- | :--- | :--- | :--- | :--- |
| **REQ-RS485-01** | **Demonstration & Test:** ส่งคำสั่ง Modbus RTU (`01 04 00 01 00 02 20 0B`) ที่ Baud rate $9,600\text{ bps}$ ไปยัง XY-MD02 และวัดสัญญาณด้วย Oscilloscope | `TC-MOD-01` | ภาพหน้าจอ Serial Monitor ที่แสดงค่าอุณหภูมิ/ความชื้นจาก SHT20 ถูกต้อง และภาพสัญญาณ Differential A/B บน Oscilloscope | `Not Tested` |
| **REQ-RS485-02** | **Test:** วัดเวลาหน่วงการสลับสถานะขา $\text{DE}/\overline{\text{RE}}$ หรือวงจร Auto-Direction เทียบกับจังหวะที่ XY-MD02 ตอบกลับด้วย Logic Analyzer | `TC-MOD-02` | ไฟล์บันทึก Timing Diagram จาก Logic Analyzer แสดงช่วงเปลี่ยนผ่านจาก TX เป็น RX ก่อนไบต์แรกของเซนเซอร์มาถึง | `Not Tested` |
| **REQ-RS485-03** | **Inspection & Measurement:** ตรวจสอบตำแหน่งขา Header และวัดระดับแรงดันที่ขา RX/TX ด้วย Digital Multimeter | `TC-IF-01` | ตารางบันทึกผลการวัดแรงดันไฟฟ้า (ต้องไม่เกิน $3.3\text{ V}$ ที่ขาเข้า MCU) และภาพถ่ายการเชื่อมต่อกับบอร์ด THARIT-IoT | `Not Tested` |
| **REQ-RS485-05** | **Inspection:** ตรวจสอบเบอร์อุปกรณ์ TVS Diode, พิกัด Breakdown Voltage และการจัดวางใกล้ขั้ว Screw Terminal บนแผ่นวงจร | `TC-SAFE-01` | เอกสาร Datasheet ของ TVS Diode และภาพ Layout / Schematic ที่แสดงตำแหน่งวงจรป้องกันชัดเจน | `Not Tested` |

---

## 8. การวิเคราะห์ความเสี่ยงและประเด็นที่ต้องตรวจสอบเพิ่ม (Risk & TBR Analysis)

| ความเสี่ยง / จุด TBR | ผลกระทบที่เป็นไปได้ | แนวทางลดความเสี่ยง / ผู้รับผิดชอบ |
| :--- | :--- | :--- |
| **1. แรงดันไฟเลี้ยงของเซนเซอร์ XY-MD02 (SHT20)**<br>*(TBR: $5\text{ V}$ จากบอร์ดหลัก vs $12\text{ V}-24\text{ V}$ ภายนอก)* | คู่มือ XY-MD02 ระบุรับไฟ $\text{DC } 5\text{ V} - 30\text{ V}$ แต่หากลากสายยาวเกิน $10 - 20\text{ เมตร}$ แรงดัน $5\text{ V}$ จะตกลงในสาย (Voltage Drop) ทำให้เซนเซอร์ SHT20 รีเซ็ตตัวเองหรืออ่านค่าเพี้ยน | ออกแบบ Screw Terminal ให้มี Jumper เลือกแหล่งจ่ายไฟ $\text{V+}$ ได้ระหว่างไฟ $5\text{ V}$ จากบอร์ดหลัก (สำหรับสายสั้น) หรือต่อไฟ $\text{DC } 12\text{ V}/24\text{ V}$ จากภายนอก (สำหรับสายยาว)<br>**ผู้รับผิดชอบ:** ชัชวาล |
| **2. ระดับแรงดัน Logic Level ไม่ตรงกัน ($5\text{ V}$ vs $3.3\text{ V}$)** | หากใช้ชิป `MAX485` รุ่นดั้งเดิมที่ใช้ไฟ $5\text{ V}$ สัญญาณขา $\text{RO}$ ที่ต่อเข้าขา $\text{RX}$ ของบอร์ด THARIT-IoT จะมีแรงดัน $5\text{ V}$ ซึ่งอาจทำให้พอร์ต GPIO ของไมโครคอนโทรลเลอร์พังเสียหาย | เลือกใช้ชิป Transceiver ที่ทำงานด้วยไฟเลี้ยง $3.3\text{ V}$ โดยตรง เช่น `SP3485` หรือ `MAX3485` เพื่อให้ระดับสัญญาณเข้ากันได้ $100\%$<br>**ผู้รับผิดชอบ:** ชัชวาล |
| **3. การต่อสลับสาย $\text{A+}$ และ $\text{B-}$ หรือสายหลุดระหว่างใช้งาน** | ระบบสื่อสารไม่ได้ หรือเกิดแรงดันลอยตัว (Floating) ทำให้บอร์ดหลักรับข้อมูลขยะ (Framing Error) ต่อเนื่อง | พิมพ์ Silk Screen กำกับขั้ว $\text{A+}, \text{B-}, \text{V+}, \text{GND}$ บน PCB ให้ชัดเจน และใส่วงจร Fail-safe Bias Resistor บังคับสถานะ Idle เมื่อสายหลุด<br>**ผู้รับผิดชอบ:** ทีมออกแบบ PCB |

---

## 9. ตัวอย่างโค้ดทดสอบสำหรับ THARIT-IoT (ESP32 Arduino C++)

โค้ดตัวอย่างสำหรับนำไปรันบนบอร์ดหลักเพื่อทดสอบตาม Test Case `TC-MOD-01` (อ่านค่าอุณหภูมิและความชื้นจาก XY-MD02):

```cpp
#include <Arduino.h>

// กำหนดขาเชื่อมต่อระหว่าง THARIT-IoT กับโมดูล RS-485 (ปรับตาม Schematic จริงของบอร์ด)
#define RS485_RX_PIN  16
#define RS485_TX_PIN  17
#define RS485_DE_PIN  4   // ขาควบคุมทิศทาง (DE และ /RE รวบเข้าด้วยกัน)

// เฟรมคำสั่ง Modbus RTU: Slave ID=1, Func=0x04, Start Addr=0x0001, Qty=2 registers, CRC=0x0B20
const uint8_t modbusRequest[] = {0x01, 0x04, 0x00, 0x01, 0x00, 0x02, 0x20, 0x0B};
uint8_t modbusResponse[9];

void setup() {
  Serial.begin(115200);
  // XY-MD02 ใช้ค่าเริ่มต้น 9600 bps, 8N1
  Serial2.begin(9600, SERIAL_8N1, RS485_RX_PIN, RS485_TX_PIN);
  
  pinMode(RS485_DE_PIN, OUTPUT);
  digitalWrite(RS485_DE_PIN, LOW); // เริ่มต้นในโหมดรอรับข้อมูล (Receive Mode)
  
  Serial.println("THARIT-IoT RS-485 XY-MD02 (SHT20) Reader Initialized.");
}

void loop() {
  // 1. สลับเป็นโหมดส่งข้อมูล (Transmit Mode)
  digitalWrite(RS485_DE_PIN, HIGH);
  delayMicroseconds(100);
  
  Serial2.write(modbusRequest, sizeof(modbusRequest));
  Serial2.flush(); // รอให้ส่งข้อมูลครบทุกบิตออกจากบัฟเฟอร์ฮาร์ดแวร์
  
  // 2. สลับกลับเป็นโหมดรับข้อมูลทันที (Receive Mode) ตาม REQ-RS485-02
  delayMicroseconds(100);
  digitalWrite(RS485_DE_PIN, LOW);

  // 3. รอรับข้อมูลตอบกลับ 9 ไบต์จาก XY-MD02
  uint32_t startTime = millis();
  int index = 0;
  while ((millis() - startTime) < 500 && index < 9) {
    if (Serial2.available()) {
      modbusResponse[index++] = Serial2.read();
    }
  }

  // 4. แปลงค่าและแสดงผล
  if (index == 9 && modbusResponse[0] == 0x01 && modbusResponse[1] == 0x04) {
    int16_t rawTemp = (modbusResponse[3] << 8) | modbusResponse[4];
    uint16_t rawHum = (modbusResponse[5] << 8) | modbusResponse[6];
    
    float temperature = rawTemp / 10.0;
    float humidity = rawHum / 10.0;
    
    Serial.printf("Temperature: %.1f °C | Humidity: %.1f %%RH\n", temperature, humidity);
  } else {
    Serial.println("Error: Timeout or Invalid Modbus Response from XY-MD02");
  }

  delay(2000); // อ่านค่าทุก 2 วินาที
}
```

---

## 10. บันทึกคำถามสะท้อนคิด (Individual Reflection)

* **ก. Requirement ข้อใดสำคัญที่สุดและเพราะเหตุใด?**
  * **คำตอบ:** ข้อ `REQ-RS485-05` (วงจรป้องกันแรงดันไฟกระชากและกระแสเกิน) และ `REQ-RS485-01` (การแปลงสัญญาณที่ Baud rate $9,600\text{ bps}$ สำหรับ XY-MD02) สำคัญที่สุด เพราะการต่อสายออกไปหาเซนเซอร์ XY-MD02 ภายนอกมีความเสี่ยงต่อไฟกระชากและการต่อสายผิดพลาด หากไม่มีวงจรป้องกันที่ดีพอร์ตของบอร์ดหลัก THARIT-IoT จะเสียหายทันที และหากระดับสัญญาณไม่ตรงตามโปรโตคอล Modbus RTU ของ SHT20 ระบบก็จะไม่สามารถอ่านค่าได้เลย
* **ข. ข้อมูลทางวิศวกรรมเรื่องใดต้องตรวจ Datasheet / Schematic ก่อนสัปดาห์ที่ 3?**
  * **คำตอบ:**
    1. ผังวงจรและ Pinout ของบอร์ด THARIT-IoT เพื่อยืนยันขาสัญญาณ UART และพิกัดกระแสของแหล่งจ่ายไฟ $3.3\text{ V}$ และ $5\text{ V}$ บน Expansion Header
    2. Datasheet ของชิป `SP3485` / `MAX3485` ($3.3\text{ V}$ Transceiver) และคู่มือเซนเซอร์ XY-MD02 (SHT20) เรื่องช่วงแรงดันไฟเลี้ยงขั้นต่ำและรูปแบบการต่อตัวต้านทาน Fail-safe / Termination $120\,\Omega$
* **ค. บทบาทของตนเองในกลุ่มและสิ่งที่จะทำให้ดีขึ้นครั้งหน้า:**
  * **คำตอบ:** รับผิดชอบการวิเคราะห์ความต้องการของระบบ (System Requirements) และการออกแบบ Interface เชื่อมต่อระหว่าง THARIT-IoT กับเซนเซอร์ XY-MD02 (SHT20) ผ่านบัส RS-485 สิ่งที่จะทำให้ดีขึ้นในครั้งหน้าคือ การตรวจสอบขนาด Footprint ของขั้วต่อ Screw Terminal และเบอร์อุปกรณ์ SMD ที่มีจำหน่ายจริงก่อนเริ่มวาดวงจร Schematic ในสัปดาห์ที่ 3