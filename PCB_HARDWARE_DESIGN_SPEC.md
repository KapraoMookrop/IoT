# ข้อกำหนดการออกแบบแผ่นวงจรพิมพ์ (PCB Hardware Design Specification)
## RS-485 Industrial Extension Module สำหรับ THARIT-IoT (XY-MD02 / SHT20)

**ผู้ออกแบบ / System Architect:** ชัชวาล ตาจา (Chatchawan Taja)  
**เวอร์ชันบอร์ด:** Hardware Revision v1.0 (Production-Ready Prototype)  
**วันที่:** 29 ตุลาคม 2569  

---

### 1. ข้อมูลทางกลและโครงสร้างแผ่นวงจร (Mechanical & Physical Specifications)

| พารามิเตอร์ | ค่ากำหนดทางวิศวกรรม | หมายเหตุประกอบการผลิต |
| :--- | :--- | :--- |
| **ขนาดบอร์ด (Dimensions)** | $50.8\text{ mm} \times 28.0\text{ mm}$ ($2.0" \times 1.1"$) | กะทัดรัด เสียบซ้อนเป็น Shield หรือต่อสายแยกได้ |
| **ชนิดและวัสดุ PCB** | FR-4 Standard (Double-sided 2 Layers) | ทนอุณหภูมิ $T_g \ge 140^\circ\text{C}$ |
| **ความหนาแผ่นวงจร** | $1.6\text{ mm}$ ($\pm 10\%$) | แข็งแรง ทนแรงขันสกรู Terminal Block |
| **ความหนาทองแดง** | $1\text{ oz}$ ($35\,\mu\text{m}$) ทั้งสองหน้า | รองรับกระแสไฟเลี้ยงและกราวด์ระบายความร้อน |
| **ผิวเคลือบตัวนำ (Surface Finish)**| ENIG (Electroless Nickel Immersion Gold) | ป้องกันสนิม หน้าสัมผัสแบนเรียบ บัดกรีง่าย |
| **สีหน้ากากประสาน (Solder Mask)** | สีดำด้าน (Matte Black) หรือ สีเขียวอุตสาหกรรม | คอนทราสต์สูง มองเห็นเส้นลายวงจรชัดเจน |
| **สีสกรีนตัวอักษร (Silkscreen)** | สีขาว (High-Density White) | พิมพ์กำกับขั้ว พิน และจุดวัดสัญญาณชัดเจน |
| **รูยึดบอร์ด (Mounting Holes)** | 2 รู ขนาด $\varnothing 3.2\text{ mm}$ (สำหรับน็อต M3) | ห่างจากขอบ $3.5\text{ mm}$ พร้อมวงแหวนกราวด์ |

---

### 2. ผังวงจรและการทำงานของแต่ละส่วน (Circuit Subsystems Architecture)

```
                            ┌──────────────────────────────────────────────┐
                            │      RS-485 EXTENSION MODULE (REV 1.0)       │
                            │                                              │
 ┌──────────────────────┐   │  ┌───────────────┐     ┌──────────────────┐  │   ┌────────────────────┐
 │ THARIT-IoT Mainboard │   │  │ Power Circuit │     │ RS-485 Line Prot.│  │   │ Sensor: XY-MD02    │
 │ (ESP32 Node)         │   │  │ • 3.3V Filter │     │ • TVS (SM712)    │  │   │ (SHT20 inside)     │
 │                      │   │  │ • J_PWR Select│     │ • PTC Fuse (x2)  │  │   │                    │
 │  [3.3V Logic] ───────┼───┼─►│   (5V / EXT)  │     │ • 120Ω Term (J1) │  │   │                    │
 │  [GND] ──────────────┼───┼─►│               │     │ • Fail-safe Bias │  │   │                    │
 │                      │   │  └───────┬───────┘     └────────▲─────────┘  │   │                    │
 │                      │   │          │                      │            │   │                    │
 │  [GPIO17 (TXD)] ─────┼───┼──────────┼───────────────┐      │ (A+, B-)   │   │                    │
 │                      │   │          ▼               ▼      │            │   │                    │
 │  [GPIO16 (RXD)] ◄────┼───┼── [ SP3485E Transceiver IC ] ───┘            │   │                    │
 │                      │   │      (3.3V Half-Duplex)                      │   │                    │
 │  [GPIO04 (DE/RE)] ───┼───┼──────────▲                                   │   │                    │
 └──────────────────────┘   │          │ (V+, GND, A+, B-)                 │   │                    │
                            │  ┌───────┴────────────────────────────────┐  │   │                    │
                            │  │ 4-Pin Industrial Screw Terminal Block  │══╪═══╡ 4-Wire Cable       │
                            │  │    [ 1:V+ | 2:GND | 3:A+ | 4:B- ]      │  │   │ (V+, GND, A+, B-)  │
                            │  └────────────────────────────────────────┘  │   └────────────────────┘
                            └──────────────────────────────────────────────┘
```

#### 2.1 วงจรแปลงสัญญาณสื่อสาร (RS-485 Transceiver Section)
* **ชิปไอซีหลัก (U1):** `SP3485EN-L/TR` หรือ `MAX3485ESA+` ในตัวถัง SOIC-8
  * ทำงานด้วยไฟเลี้ยง $+3.3\text{V DC}$ เข้ากันได้กับระดับตรรกะของชิป ESP32 บนบอร์ด THARIT-IoT โดยตรงโดยไม่ต้องใช้วงจรแบ่งแรงดัน (Level Shifter)
  * ขา 1 ($\text{RO}$): ต่อเข้าขา $\text{RXD}$ ของบอร์ดหลัก พร้อมต่อเข้าวงจรไฟแสดงสถานะ LED สีเหลือง
  * ขา 2 ($\overline{\text{RE}}$) และ ขา 3 ($\text{DE}$): รวบเข้าด้วยกันและต่อเข้าขาควบคุมทิศทาง $\text{DE/RE}$ ของบอร์ดหลัก พร้อมตัวต้านทาน Pull-down $10\text{ k}\Omega$ (R_DE) ดึงลงกราวด์เพื่อให้เข้าสู่โหมดรับข้อมูล (Receive Mode) โดยอัตโนมัติตอนเริ่มทำงาน
  * ขา 4 ($\text{DI}$): ต่อเข้าขา $\text{TXD}$ ของบอร์ดหลัก พร้อมต่อเข้าวงจรไฟแสดงสถานะ LED สีน้ำเงิน
  * ขา 6 ($\text{A}$) และ ขา 7 ($\text{B}$): ขาสัญญาณ Differential ส่งต่อไปยังวงจรป้องกันทางไฟฟ้า
  * คาปาซิเตอร์ดีคัปปลิง: $\text{C1} = 0.1\,\mu\text{F}$ (X7R Ceramic 0603) วางชิดขา 8 ($\text{VCC}$) และขา 5 ($\text{GND}$) ระยะห่างไม่เกิน $2\text{ mm}$

#### 2.2 วงจรป้องกันความเสียหายทางไฟฟ้า (Fault & Surge Protection Network)
* **ฟิวส์รีเซ็ตตัวเอง (F1, F2 - PTC Resettable Fuses):**
  * พิกัดกระแส $100\text{ mA}$, ทนแรงดัน $60\text{ V}$ ขนาดแพ็กเกจ 1206
  * ต่ออนุกรมคั่นระหว่างขาของชิป Transceiver และขั้วต่อ Screw Terminal ทั้งฝั่ง $\text{A+}$ และ $\text{B-}$ เพื่อป้องกันกรณีช่างต่อสายสลับไปแตะกับสายไฟเลี้ยงเซนเซอร์ ($\text{DC } 12\text{V}-24\text{V}$)
* **วงจรป้องกันแรงดันไฟกระชาก (D1 - TVS Diode Array):**
  * เลือกใช้ไอซี `SM712` (หรือ CDSOT23-SM712) ซึ่งออกแบบมาสำหรับมาตรฐาน RS-485 โดยเฉพาะ
  * มีระดับการแคลมป์แรงดันไม่สมมาตร (Asymmetric Clamping): $-7\text{ V}$ สำหรับฝั่งลบ และ $+12\text{ V}$ สำหรับฝั่งบวก ตรงตามมาตรฐานพิกัด Common-mode voltage ของ RS-485
  * รองรับแรงดันไฟฟ้าสถิต (ESD Protection) ได้ถึง $\pm 15\text{ kV}$ (Air Discharge) และ $\pm 8\text{ kV}$ (Contact Discharge)
* **ตัวต้านทานจบสาย (R_TERM - Termination Resistor):**
  * ค่า $120\,\Omega$ ($\pm 1\%$, 0805) ต่ออนุกรมกับ 2-Pin Jumper Header (`J_TERM`)
  * ปิด Jumper เมื่อโมดูลอยู่ที่ปลายสายบัสเพื่อป้องกันคลื่นสะท้อน (Signal Reflection) และเปิดออกเมื่อเป็นโหนดกลาง
* **ตัวต้านทานรักษาสถานะบัส (Fail-Safe Bias Network):**
  * $\text{R\_PU} = 4.7\text{ k}\Omega$ (0603) ดึงสาย $\text{A+}$ ขึ้นไฟเลี้ยง $+3.3\text{V}$
  * $\text{R\_PD} = 4.7\text{ k}\Omega$ (0603) ดึงสาย $\text{B-}$ ลงกราวด์ $\text{GND}$
  * บังคับให้ความต่างศักย์ $V_A - V_B > +200\text{ mV}$ (สถานะ Logic 1 หรือ Mark) เสมอ เมื่อไม่มีอุปกรณ์ส่งสัญญาณ หรือเมื่อสายเซนเซอร์หลุด ป้องกันไม่ให้ไมโครคอนโทรลเลอร์ได้รับสัญญาณขยะ (Noise Glitch)

#### 2.3 วงจรเลือกแหล่งจ่ายไฟเซนเซอร์ (Power Selection Header: J_PWR)
* จัมเปอร์ 3 พิน (Header $2.54\text{ mm}$) สำหรับเลือกแหล่งจ่ายไฟเลี้ยง $\text{V+}$ ไปยังเซนเซอร์ XY-MD02:
  * **พิน 1:** รับไฟเลี้ยง $+5\text{V}$ จากบอร์ด THARIT-IoT
  * **พิน 2:** ต่อไปยังช่อง $\text{V+}$ ของขั้วต่อ Screw Terminal
  * **พิน 3:** จุดรับไฟเลี้ยงภายนอก $\text{DC } 12\text{V} - 24\text{V}$ ($\text{EXT\_DC}$)
  * เสียบช็อตขั้ว 1-2 เมื่อเดินสายเซนเซอร์ระยะสั้น ($< 10\text{ เมตร}$)
  * เสียบช็อตขั้ว 2-3 (หรือต่อไฟแยก) เมื่อเดินสายเซนเซอร์ระยะไกลเพื่อป้องกันปัญหาแรงดันตกคร่อมสาย (Voltage Drop)
* คาปาซิเตอร์กรองสัญญาณรบกวนภาคจ่ายไฟ: $\text{C2} = 10\,\mu\text{F}$ (35V, 1206) คร่อมระหว่าง $\text{V+}$ และ $\text{GND}$

---

### 3. รายการอุปกรณ์และการคัดเลือกพาร์ท (Bill of Materials: BOM)

| ลำดับ | รหัส (Designator) | รายการอุปกรณ์ / ค่าความจุ-ความต้านทาน | ขนาดตัวถัง (Footprint) | พิกัดทางเทคนิค (Rating / Specs) | ตัวอย่างเบอร์ชิ้นส่วน (MPN) | จำนวน |
| :---: | :--- | :--- | :---: | :--- | :--- | :---: |
| 1 | **U1** | RS-485 Transceiver IC | SOIC-8 | 3.3V, Half-Duplex, 10Mbps, ±15kV ESD | SP3485EN-L/TR หรือ MAX3485ESA+ | 1 |
| 2 | **D1** | Asymmetric TVS Diode Array | SOT-23 | Stand-off: -7V/+12V, Peak Power: 400W | SM712 / CDSOT23-SM712 | 1 |
| 3 | **F1, F2** | PTC Resettable Fuse | 1206 | Hold: 100mA, Trip: 200mA, Max 60V | PolySwitch nanoSMDC010F หรือ 1206L010YR | 2 |
| 4 | **R_TERM** | Termination Resistor | 0805 | $120\,\Omega$, $\pm 1\%$, 1/8W | Thick Film Chip Resistor | 1 |
| 5 | **R_PU, R_PD** | Fail-Safe Bias Resistors | 0603 | $4.7\text{ k}\Omega$, $\pm 1\%$, 1/10W | RC0603FR-074K7L | 2 |
| 6 | **R_DE** | Pulldown Resistor (DE/RE) | 0603 | $10\text{ k}\Omega$, $\pm 5\%$, 1/10W | RC0603JR-0710KL | 1 |
| 7 | **R1, R2, R3** | Current Limiting Resistors (LED) | 0603 | $1.0\text{ k}\Omega$, $\pm 5\%$, 1/10W | RC0603JR-071KL | 3 |
| 8 | **C1** | IC Bypass Capacitor | 0603 | $0.1\,\mu\text{F}$ ($100\text{ nF}$), 16V, X7R | CC0603KRX7R7BB104 | 1 |
| 9 | **C2** | Bulk Power Filter Capacitor | 1206 | $10\,\mu\text{F}$, 35V, X5R/X7R Ceramic | CL31A106KAHNNNE | 1 |
| 10 | **LED1 (PWR)** | Power Indicator LED | 0603 | สีเขียว (Green), Super Bright | 19-217/GHC-YR1S2/3T | 1 |
| 11 | **LED2 (TX)** | RS-485 Transmit Indicator | 0603 | สีน้ำเงิน (Blue), High Efficiency | 19-217/BHC-AP1Q2/3T | 1 |
| 12 | **LED3 (RX)** | RS-485 Receive Indicator | 0603 | สีส้ม/เหลือง (Amber/Yellow) | 19-217/Y2C-CP2Q2B/3T | 1 |
| 13 | **J_TERM** | 2-Pin Shunt Header | 1x2 2.54mm | Gold Plated Header + Red Shunt Cap | Pin Header Male 2.54mm | 1 |
| 14 | **J_PWR** | 3-Pin Power Selector Header | 1x3 2.54mm | Gold Plated Header + Blue Shunt Cap | Pin Header Male 2.54mm | 1 |
| 15 | **TB1** | Industrial Pluggable Screw Terminal | 4-Pin 3.81mm | Pitch $3.81\text{ mm}$ (หรือ $5.08\text{ mm}$), 300V/8A | KF2EDGK-3.81-4P / Degson 15EDGK | 1 |
| 16 | **HDR_THARIT**| Extension Header Pin to Mainboard | 1x6 2.54mm | Right-Angle หรือ Straight Male Header | 2.54mm Single Row Male Header 6P | 1 |

---

### 4. ผังการเชื่อมต่อขาพิน (Connector & Header Pinout)

#### 4.1 ขั้วต่อเทอร์มินัลภายนอกสำหรับเซนเซอร์ (4-Pin Screw Terminal Block: TB1)
| ขาที่ | ชื่อสัญญาณ (Silkscreen) | สีสายไฟเซนเซอร์ XY-MD02 | คำอธิบายการต่อใช้งาน |
| :---: | :--- | :--- | :--- |
| **1** | **V+ (PWR)** | **สายสีแดง** | จ่ายไฟเลี้ยง $+5\text{V}$ หรือ $+12\text{V}-24\text{V}$ ให้กับเซนเซอร์ XY-MD02 |
| **2** | **GND** | **สายสีดำ** | กราวด์ร่วมของระบบไฟฟ้าและสัญญาณ |
| **3** | **A+ (D+)** | **สายสีเหลือง** | สายสัญญาณคู่ผลต่าง Differential ขั้วบวก (Non-inverting) |
| **4** | **B- (D-)** | **สายสีขาว หรือ เขียว** | สายสัญญาณคู่ผลต่าง Differential ขั้วลบ (Inverting) |

#### 4.2 ขั้วต่อเชื่อมกับบอร์ดประมวลผลหลัก (THARIT-IoT Expansion Header: 6-Pin 2.54mm)
| ขาที่ | ชื่อสัญญาณ | ต่อเข้ากับขา ESP32 บนบอร์ด THARIT-IoT | หน้าที่การทำงาน |
| :---: | :--- | :--- | :--- |
| **1** | **VCC 3.3V** | `3V3 Power Rail` | ไฟเลี้ยงวงจรตรรกะและชิป SP3485 |
| **2** | **5V_IN** | `5V / VBUS Power Rail` | ไฟเลี้ยงบอร์ด $5\text{V}$ ส่งต่อไปยัง Jumper `J_PWR` |
| **3** | **GND** | `System Common GND` | กราวด์อ้างอิงของระบบ |
| **4** | **UART_TX** | `GPIO17` (Hardware Serial2 TX) | สัญญาณส่งข้อมูล Modbus Request จากบอร์ดหลัก |
| **5** | **UART_RX** | `GPIO16` (Hardware Serial2 RX) | สัญญาณรับข้อมูลตอบกลับ Modbus Response จากเซนเซอร์ |
| **6** | **DE_RE** | `GPIO04` (Digital Output) | ควบคุมทิศทาง (High = Transmit, Low = Receive) |

---

### 5. กฎและแนวทางการเดินลายวงจร (PCB Layout & Routing Guidelines)

1. **Differential Pair Routing:**
   - เส้นสัญญาณบัส $\text{A+}$ และ $\text{B-}$ ต้องเดินคู่ขนานกันแบบ Differential Pair ด้วยความกว้างเส้นทองแดง (Trace Width) และระยะห่าง (Spacing) ที่รักษาค่า Differential Impedance ประมาณ $120\,\Omega$
   - ความยาวของเส้น $\text{A+}$ และ $\text{B-}$ ต้องมีความยาวใกล้เคียงกันที่สุด (Length Matching ภายใน $\pm 0.5\text{ mm}$) เพื่อป้องกัน Phase Skew
2. **Ground Plane & Noise Isolation:**
   - เลเยอร์ล่าง (Bottom Layer) กำหนดให้เป็น Solid Ground Plane อย่างน้อย $85\%$ ของพื้นที่บอร์ดเพื่อเป็นเส้นทางย้อนกลับของสัญญาณความถี่สูง (Return Path) และป้องกันสัญญาณกวน
3. **ESD & TVS Placement:**
   - อุปกรณ์ป้องกัน TVS Diode (`D1`) และฟิวส์ PTC (`F1`, `F2`) ต้องวางชิดกับขั้วต่อ Screw Terminal มากที่สุด เพื่อดักจับและสลายพลังงานเสิร์จ (Surge/ESD) ลงกราวด์ทันที ก่อนที่คลื่นแรงดันสูงจะหลุดเข้าไปยังชิปไอซี
4. **Thermal Relief & High Current:**
   - ขาของ Screw Terminal และจุดต่อไฟเลี้ยง $\text{V+}$, $\text{GND}$ ต้องเดินลายเส้นทองแดงกว้างอย่างน้อย $30 - 40\text{ mil}$ ($0.76 - 1.0\text{ mm}$) และใช้ Thermal Relief Pad แบบ 4 ก้านเพื่อง่ายต่อการบัดกรีด้วยมือ

