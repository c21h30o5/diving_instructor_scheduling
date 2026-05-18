from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, time, timedelta
import pytz

class DivingBooking(models.Model):
    _name = 'diving.booking'
    _description = 'Diving Course Booking'

    color = fields.Integer(string='Color Index')
    name = fields.Char(string='Student Name', required=True)

    # --- ส่วนที่ 1: ข้อมูลคอร์สและเวลาเริ่ม ---
    course_type = fields.Selection([
        ('open_water', 'Open Water Diver (3 Slots)'),
        ('advanced', 'Advanced Open Water (3 Slots)'),
        ('rescue', 'Rescue Diver (Standard)'),
        ('fun_dive', 'Fun Dive (Standard)')
    ], string='Course', default='open_water', required=True)

    student_count = fields.Integer(string='Number of Students', default=1, required=True)
    booking_date = fields.Date(string='Booking Date', required=True)

    booking_slot = fields.Selection([
        ('morning', 'Morning (08:00 - 12:00)'),
        ('afternoon', 'Afternoon (13:00 - 17:00)'),
        ('night', 'Night Dive (18:00 - 21:00)')
    ], string='Start Time Slot', required=True, default='morning')

    instructor_id = fields.Many2one('res.users', string='Instructor', required=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Completed'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft')

    # --- ส่วนที่ 2: Logic การจัดการตารางงาน (Slot Management) ---
    
    def _get_required_slots(self):
        self.ensure_one()
        slots = []
        d1 = self.booking_date
        d2 = self.booking_date + timedelta(days=1)

        if self.course_type == 'open_water':
            if self.booking_slot == 'morning':
                slots = [(d1, 'morning'), (d1, 'afternoon'), (d2, 'morning')]
            else:
                slots = [(d1, 'afternoon'), (d2, 'morning'), (d2, 'afternoon')]
        elif self.course_type == 'advanced':
            slots = [(d1, 'afternoon'), (d1, 'night'), (d2, 'morning')]
        else:
            slots = [(d1, self.booking_slot)]
        return slots

    # --- ส่วนที่ 3: ระบบตรวจสอบ (Constraints) ---

    @api.constrains('instructor_id', 'booking_date', 'booking_slot', 'student_count', 'state', 'course_type')
    def _check_instructor_availability(self):
        for record in self:
            if record.state != 'confirmed':
                continue

            required_slots = record._get_required_slots()
            # ตรวจสอบว่ามีฟิลด์ max_students_per_slot ใน res.users หรือไม่ ถ้าไม่มีให้ใช้ 3
            limit = getattr(record.instructor_id, 'max_students_per_slot', 3) or 3

            for slot_date, slot_time in required_slots:
                # เช็กวันลา (ถ้ามีโมดูล instructor.leave)
                try:
                    leave = self.env['instructor.leave'].search([
                        ('instructor_id', '=', record.instructor_id.id),
                        ('leave_date', '=', slot_date),
                        ('leave_slot', 'in', [slot_time, 'full'])
                    ])
                    if leave:
                        raise ValidationError(f"ขออภัย! ครู {record.instructor_id.name} ลาในวันที่ {slot_date} ช่วง {slot_time}")
                except:
                    pass # ข้ามถ้ายังไม่ได้สร้างโมดูลลา

                # เช็กความทับซ้อนและโควตา
                all_confirmed_bookings = self.search([
                    ('id', '!=', record.id),
                    ('instructor_id', '=', record.instructor_id.id),
                    ('state', '=', 'confirmed'),
                    ('booking_date', '>=', record.booking_date - timedelta(days=1)),
                    ('booking_date', '<=', record.booking_date + timedelta(days=1)),
                ])

                total_students_in_this_slot = record.student_count
                for other in all_confirmed_bookings:
                    if (slot_date, slot_time) in other._get_required_slots():
                        total_students_in_this_slot += other.student_count

                if total_students_in_this_slot > limit:
                    raise ValidationError(
                        f"ครู {record.instructor_id.name} คิวเต็มในวันที่ {slot_date} ช่วง {slot_time}!\n"
                        f"เนื่องจากกฎ 1 ครู : {limit} นักเรียน (ขณะนี้รวมได้ {total_students_in_this_slot} คน)"
                    )

    # --- ส่วนที่ 4: ฟังก์ชันจัดการและปฏิทิน ---

    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'

    requested_lang_id = fields.Many2one('res.lang', string="Requested Language")
    student_details = fields.Text(string="Student Names & Details")

    @api.constrains('instructor_id', 'requested_lang_id')
    def _check_instructor_language(self):
        for record in self:
            if record.instructor_id and record.requested_lang_id:
                # ตรวจสอบว่ามีฟิลด์ instructor_lang_ids หรือไม่
                langs = getattr(record.instructor_id, 'instructor_lang_ids', [])
                if record.requested_lang_id not in langs:
                    raise ValidationError(f"ครู {record.instructor_id.name} สอนภาษา {record.requested_lang_id.name} ไม่ได้!")

    # --- จุดที่แก้ไข: คำนวณวันเวลาสำหรับปฏิทิน ---
    start_date = fields.Datetime(string='Calendar Start', compute='_compute_dates', store=True)
    end_date = fields.Datetime(string='Calendar End', compute='_compute_dates', store=True)

    @api.depends('booking_date', 'booking_slot', 'course_type')
    def _compute_dates(self):
        thai_tz = pytz.timezone('Asia/Bangkok')
        slot_times = {'morning': (8, 12), 'afternoon': (13, 17), 'night': (18, 21)}
        
        for record in self:
            if record.booking_date and record.booking_slot:
                slots = record._get_required_slots()
                if not slots:
                    continue
                
                # ดึง Slot แรกและสุดท้ายมาหาเวลาเริ่ม-จบ
                first_date, first_slot = slots[0]
                last_date, last_slot = slots[-1]
                
                start_h = slot_times.get(first_slot, (8, 12))[0]
                end_h = slot_times.get(last_slot, (8, 12))[1]
                
                # สร้าง datetime แบบ Local (ไทย) ก่อน แล้วค่อยแปลงเป็น UTC ส่งให้ Odoo
                start_dt = thai_tz.localize(datetime.combine(first_date, time(start_h, 0)))
                end_dt = thai_tz.localize(datetime.combine(last_date, time(end_h, 0)))
                
                record.start_date = start_dt.astimezone(pytz.utc).replace(tzinfo=None)
                record.end_date = end_dt.astimezone(pytz.utc).replace(tzinfo=None)

    @api.constrains('booking_date', 'student_count')
    def _check_basic_rules(self):
        for record in self:
            if record.booking_date and record.booking_date < fields.Date.today():
                raise ValidationError("ไม่สามารถจองเรียนย้อนหลังได้!")
            if record.student_count < 1:
                raise ValidationError("จำนวนนักเรียนต้องมีอย่างน้อย 1 คน")