Diving Center Instructor Scheduling Module (v1.0)
Odoo ERP Customization for Dive Centers
โมดูล Odoo ที่ออกแบบมาเพื่อแก้ไขปัญหาความซับซ้อนในการจัดตารางเรียนดำน้ำ (Course Scheduling) โดยเน้นระบบการตรวจสอบเงื่อนไขทางธุรกิจ (Business Logic) และการจัดการทรัพยากรบุคคล (Instructor Management) ให้มีประสิทธิภาพสูงสุด

🌟 Key Features
Intelligent Course Scheduling: รองรับคอร์สเรียนแบบหลายช่วงเวลา (Multi-slot) เช่น Open Water และ Advanced ที่กินเวลาครูฝึกมากกว่า 1 ช่วง โดยระบบจะทำการจอง Slot ที่เกี่ยวข้องให้อัตโนมัติ (Morning/Afternoon/Night)

Instructor Language Matching: ระบบ Domain Filtering กรองเฉพาะครูฝึกที่พูดภาษาตรงตามที่ลูกค้าต้องการ (Requested Language)

Instructor Workload Validation: ระบบตรวจสอบโควตานักเรียนต่อครูฝึก (Ratio 1:3 หรือตามที่กำหนด) โดยคำนวณจากทุกใบจองที่ทับซ้อนกันใน Slot นั้นๆ

Data Integrity & Constraints:

ป้องกันการจองเรียนย้อนหลัง (Anti-Past Booking)

ตรวจสอบจำนวนนักเรียนขั้นต่ำ (Minimum Student Validation)

ป้องกันการแก้ไขข้อมูลสำคัญหลังยืนยันการจอง (State-based Readonly fields)

Visual Management: ระบบ Calendar View ที่แสดงแถบเวลาตามการใช้ทรัพยากรจริงของคอร์สเรียน และ Reporting (Graph/Pivot) สำหรับวิเคราะห์สถิติ

🛠 Tech Stack
Framework: Odoo 17.0+ (MVC Architecture)

Language: Python 3.10+

Frontend: XML, XPath (Inheritance), QWeb

Database: PostgreSQL

Environment: Dockerized Odoo environment

📁 Project Structure
Plaintext
diving_instructor_scheduling/
├── models/
│   ├── diving_booking.py    # Core Logic, Constraints, Slot Calculation
│   └── res_users.py         # Extended User model for Instructor settings
├── views/
│   ├── diving_booking_views.xml  # UI Definitions (Form, Tree, Calendar, Graph)
│   └── res_users_views.xml       # UI Extension for Instructor profiles
├── security/
│   └── ir.model.access.csv  # Access Rights Control
└── data/
    └── instructor_data.xml  # Initial Master Data


🚀 Business Logic Highlights
ในโมดูลนี้ ผมได้ใช้แนวคิด Relational Database Management และ Backend Validation มาประยุกต์ใช้:

Slot Logic: คอร์ส Open Water จะถูกจอง 3 slots ต่อเนื่อง (เช่น เช้าวันที่ 1, บ่ายวันที่ 1 และเช้าวันที่ 2) โดยใช้ timedelta ในการคำนวณวันเวลาจริงเพื่อแสดงผลบนปฏิทิน

Concurrency Control: การใช้ @api.constrains เพื่อดึงข้อมูลใบจองอื่น (Search) มาเปรียบเทียบในขณะบันทึกข้อมูล เพื่อป้องกันการรับนักเรียนเกินโควตาของครูฝึกใน Slot นั้นๆ

📸 Screenshots & Demo
(แนะนำ: ให้แคปรูปภาพจากหน้าจอจริงของคุณมาใส่ในส่วนนี้)

Form View พร้อม Validation Error (ตามรูปที่คุณส่งมา)

Calendar View ที่แสดงคอร์สซ้อนกัน

Pivot Table สรุปจำนวนนักเรียนต่อครู

👨‍💻 Developer Information
Current Version: 1.0.0

Developer: [Rathanont Ama]

Experience: Full-stack Background (MERN Stack) with a focus on ERP Customization.