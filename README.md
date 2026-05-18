# 🤿 Diving Center Instructor Scheduling Module (v1.0)
### *Odoo ERP Customization for Dive Centers*

โมดูล Odoo ที่ออกแบบมาเพื่อแก้ไขปัญหาความซับซ้อนในการจัดตารางเรียนดำน้ำ (Course Scheduling) โดยเน้นระบบการตรวจสอบเงื่อนไขทางธุรกิจ (Business Logic) และการจัดการทรัพยากรบุคคล (Instructor Management) ให้มีประสิทธิภาพสูงสุด

---

## 🌟 Key Features

* **📅 Intelligent Course Scheduling**: รองรับคอร์สเรียนแบบหลายช่วงเวลา (**Multi-slot**) เช่น Open Water และ Advanced ที่กินเวลาครูฝึกมากกว่า 1 ช่วง โดยระบบจะทำการจอง Slot ที่เกี่ยวข้องให้อัตโนมัติ (Morning/Afternoon/Night)
* **🗣️ Instructor Language Matching**: ระบบ **Domain Filtering** กรองเฉพาะครูฝึกที่พูดภาษาตรงตามที่ลูกค้าต้องการ (Requested Language)
* **⚖️ Instructor Workload Validation**: ระบบตรวจสอบโควตานักเรียนต่อครูฝึก (**Ratio 1:3** หรือตามที่กำหนด) โดยคำนวณจากทุกใบจองที่ทับซ้อนกันใน Slot นั้นๆ
* **🛡️ Data Integrity & Constraints**:
    * ป้องกันการจองเรียนย้อนหลัง (Anti-Past Booking)
    * ตรวจสอบจำนวนนักเรียนขั้นต่ำ (Minimum Student Validation)
    * ป้องกันการแก้ไขข้อมูลสำคัญหลังยืนยันการจอง (State-based Readonly fields)
* **📊 Visual Management**: ระบบ **Calendar View** ที่แสดงแถบเวลาตามการใช้ทรัพยากรจริงของคอร์สเรียน และระบบ **Reporting (Graph/Pivot)** สำหรับวิเคราะห์สถิติ

---

## 🛠 Tech Stack

* **Framework**: Odoo 19 (MVC Architecture)
* **Language**: Python 3.10+
* **Frontend**: XML, XPath (Inheritance), QWeb
* **Database**: PostgreSQL
* **Environment**: Dockerized Odoo environment

---

## 📁 Project Structure

```text
diving_instructor_scheduling/
├── data/
│   └── instructor_data.xml         # ข้อมูลเริ่มต้น (Master Data)
├── models/
│   ├── __init__.py
│   ├── diving_booking.py          # หัวใจหลัก: Logic, Constraints, Slot Calc
│   ├── instructor_leave.py        # ระบบจัดการการลาของครู
│   └── res_users.py               # ขยายฟิลด์เพิ่มให้ Model User (Instructor)
├── security/
│   └── ir.model.access.csv         # การกำหนดสิทธิ์การเข้าถึงข้อมูล
├── static/
│   └── description/
│       └── icon.png               # ไอคอนของโมดูล
└── views/
    ├── diving_booking_views.xml   # หน้าจอหลัก (Form, Tree, Calendar, Graph)
    ├── instructor_leave_views.xml # หน้าจอจัดการการลา
    └── res_users_views.xml        # หน้าจอตั้งค่าครูฝึก
```

## 🚀 Business Logic Highlights
ในโมดูลนี้ ผมได้นำแนวคิด Relational Database Management และ Backend Validation มาประยุกต์ใช้เพื่อแก้ปัญหาจริง:

Slot Logic: คอร์ส Open Water จะถูกจอง 3 slots ต่อเนื่อง (เช่น เช้าวันที่ 1, บ่ายวันที่ 1 และเช้าวันที่ 2) โดยใช้ timedelta ในการคำนวณช่วงเวลาจริงเพื่อแสดงผลบนปฏิทินอย่างแม่นยำ

Concurrency Control: การใช้ @api.constrains เพื่อดึงข้อมูลใบจองอื่น (search) มาเปรียบเทียบในขณะบันทึกข้อมูล เพื่อป้องกันการรับนักเรียนเกินโควตาของครูฝึกในแต่ละ Slot

## 📸 Screenshots & Demo
**📝 Form View & Validation**
ระบบแจ้งเตือนทันทีเมื่อข้อมูลไม่เป็นไปตามเงื่อนไข (Business Rules)

**📅 Calendar Management**
การจัดตารางเรียนแบบเห็นภาพรวมตาม Slot เวลาจริง

## 👨‍💻 Developer Information
* **Current Version**: 1.0.0

* **Developer**: [Rathanont Ama]

* **Experience**: Full-stack Background (MERN Stack) with a focus on ERP Customization & Business Logic.
