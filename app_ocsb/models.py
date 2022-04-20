""" app_ocsb model """
from django.conf import settings
from django.db import models
from django_fsm import FSMIntegerField, transition

from app_base.models import Enterprise, Season, Purchaser

# Create your models here.


class QuotaRequest(models.Model):
    """ ตารางคำร้องขออนุญาตฯ """
    STATUS_DRAFT = 0  # ยื่นขออนุญาต
    STATUS_REVIEW = 1  # แจ้งการตรวจสอบ
    STATUS_SITEVISIT = 2  # ลงพื้นที่ตรวจสอบ
    STATUS_APPROVAL = 3  # พิจารณาอนุญาต
    STATUS_ACCEPT = 4  # อนุญาต
    STATUS_REJECT = 5  # ไม่อนุญาต
    STATUS_CLOSE = 6  # ปิดการใช้งานคำขอ
    STATUS_CHOICES = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_REVIEW, 'Review'),
        (STATUS_SITEVISIT, 'Site Visit'),
        (STATUS_APPROVAL, 'Approval'),
        (STATUS_ACCEPT, 'Accept'),
        (STATUS_REJECT, 'Reject'),
        (STATUS_CLOSE, 'Close'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name=("ผู้บันทึกคำร้อง"), null=True, on_delete=models.SET_NULL)
    enterprise = models.ForeignKey(Enterprise,
        verbose_name=("สถานประกอบการ"), null=True, on_delete=models.SET_NULL)
    no_request = models.CharField(
        verbose_name='เลขคำร้องจากระบบ', max_length=20)
    no_enterprise = models.CharField(
        verbose_name='เลขหนังสือ สปก.', max_length=30, null=True, blank=True)
    no_ocsb = models.CharField(
        verbose_name='เลขอนุญาต สอน.', max_length=30, null=True, blank=True)
    is_season = models.BooleanField(
        verbose_name='ในฤดูการผลิตหรือไม่')
    season = models.ForeignKey(Season,
        verbose_name="ฤดูกาลผลิตที่ขออนุญาตฯ", null=True, on_delete=models.SET_NULL)
    season_round = models.IntegerField(
        verbose_name="รอบที่ขออนุญาตฯ", null=True, blank=True)
    total_syrup = models.DecimalField(
        verbose_name='ปริมาณน้ำเชื่อม Syrub (ตัน)', max_digits=8,
        decimal_places=3, null=True, blank=True, default=0)
    total_bmolasses = models.DecimalField(
        verbose_name='ปริมาณน้ำเชื่อม B-molasses (ตัน)', max_digits=8, decimal_places=3,
        null=True, blank=True, default=0)
    total_cmolasses = models.DecimalField(
        verbose_name='ปริมาณน้ำเชื่อม C-molasses (ตัน)',
        max_digits=8, decimal_places=3, null=True, blank=True, default=0)
    total_amount = models.DecimalField(
        verbose_name='ปริมาณน้ำเชื่อมรวมทั้งหมด (ตัน)',
        max_digits=8, decimal_places=3, default=0)
    total_usage_syrup = models.DecimalField(
        verbose_name='ปริมาณน้ำเชื่อม Syrub (ตัน)[ใช้แล้ว]', max_digits=8,
        decimal_places=3, null=True, blank=True, default=0)
    total_usage_bmolasses = models.DecimalField(
        verbose_name='ปริมาณน้ำเชื่อม B-molasses (ตัน)[ใช้แล้ว]', max_digits=8, decimal_places=3,
        null=True, blank=True, default=0)
    total_usage_cmolasses = models.DecimalField(
        verbose_name='ปริมาณน้ำเชื่อม C-molasses (ตัน)[ใช้แล้ว]',
        max_digits=8, decimal_places=3, null=True, blank=True, default=0)
    date_request = models.DateField(
        verbose_name='วันที่ขออนุญาตฯ', auto_now=False,
        auto_now_add=False, null=True, blank=True)
    date_inspect = models.DateField(
        verbose_name='วันที่บันทึกรับแจ้ง', auto_now=False,
        auto_now_add=False, null=True, blank=True)
    date_visit = models.DateField(
        verbose_name='วันที่บันทึกตรวจสถานที่', auto_now=False,
        auto_now_add=False, null=True, blank=True)
    date_approve = models.DateField(
        verbose_name='วันที่อนุมัติ', auto_now=False,
        auto_now_add=False, null=True, blank=True)
    create_date = models.DateTimeField(
        verbose_name='วันเวลาที่สร้างข้อมูล', auto_now_add=True)
    # Work Flow Control fields
    workflow_state = FSMIntegerField(
        choices=STATUS_CHOICES, default=STATUS_DRAFT, # protected=True,
        help_text='work flow state')
    file_request = models.FileField(
        verbose_name='หนังสือขออนุญาต สถานประกอบการ',
        upload_to='documents/quota/request/', null=True, blank=True)
    file_sitevisit = models.FileField(
        verbose_name='หนังสือประสานคณะทำงานฯ ร่วมลงพื้นที่ตรวจสอบ',
        upload_to='documents/quota/sitevisit/', null=True, blank=True)
    file_survey = models.FileField(
        verbose_name='แบบตรวจสอบกระบวนการส่งถ่ายน้ำเชื่อมฯ',
        upload_to='documents/quota/survey/', null=True, blank=True)
    file_approve = models.FileField(
        verbose_name='หนังสืออนุญาตฯ',
        upload_to='documents/quota/approve/', null=True, blank=True)
    purchasers = models.ManyToManyField(
        Purchaser, verbose_name='โรงงานรับซื้อน้ำเชื่อมฯ', blank=True)
    is_active = models.BooleanField(
        verbose_name='ใช้งานหรือไม่', default=True)

    class Meta:
        """ meta table """
        db_table = ''
        managed = True
        verbose_name = 'QuotaRequest'
        verbose_name_plural = 'QuotaRequests'
        ordering = ['-date_request', 'season', '-no_request']

    def total_usage(self):
        """ Calculate Total_Usage """
        total = self.total_usage_syrup + self.total_usage_bmolasses +\
            self.total_usage_cmolasses
        return total

    def percen_usage_syrup(self):
        """  Calculate Percent Syrup_Usage """
        percen_usage = round((self.total_usage_syrup / self.total_syrup) * 100)
        return percen_usage

    def percen_usage_bmolasses(self):
        """  Calculate Percent B-molasses_Usage """
        percen_usage = round((self.total_usage_bmolasses / self.total_bmolasses) * 100)
        return percen_usage

    def percen_usage_cmolasses(self):
        """  Calculate Percent C-molasses_Usage """
        percen_usage = round((self.total_usage_cmolasses / self.total_cmolasses) * 100)
        return percen_usage

    # def generate_no_request(self, season_code):
    #     """ Generate Request Number depend on Season
    #         format Season+running_no etc. 64/65001
    #     """
    #     filter_kw = season_code
    #     last_rec = QuotaRequest.objects.filter(
    #         no_request__starstwith=filter_kw).last()

    #     if last_rec is None:
    #         last_3digit = '000'
    #         next_3digit = int(last_3digit)+1
    #     else:
    #         last_3digit = str(last_3digit.no_request)[-3:]
    #         next_3digit = int(last_3digit)+1

    #     # Charfield format, 3-digits
    #     new_3digit = "{:03d}".format(int(next_3digit))
    #     new_no_request = '{}{}'.format(filter_kw, str(new_3digit))

    #     return new_no_request

    def __str__(self):
        return f'{self.no_request}'

    @transition(field=workflow_state, source=STATUS_DRAFT, target=STATUS_REVIEW)
    def flow_sent(self):
        """ change state from Draft to Review """

    @transition(field=workflow_state, source=STATUS_REVIEW, target=STATUS_SITEVISIT)
    def flow_reviewed_new(self):
        """ change state from Review to SiteVisit """

    @transition(field=workflow_state, source=STATUS_REVIEW, target=STATUS_APPROVAL)
    def flow_reviewed_old(self):
        """ change state from Review to Approval กรณีเป็นการขอเพิ่ม """

    @transition(field=workflow_state, source=STATUS_SITEVISIT, target=STATUS_APPROVAL)
    def flow_sitevisit(self):
        """ change state from SiteVisit to Approval """

    @transition(field=workflow_state, source=STATUS_APPROVAL, target=STATUS_ACCEPT)
    def flow_accept(self):
        """ change state from Approval to Accept """

    @transition(field=workflow_state, source=STATUS_APPROVAL, target=STATUS_REJECT)
    def flow_reject(self):
        """ change state from Approval to Reject """

    @transition(field=workflow_state, source=STATUS_ACCEPT, target=STATUS_CLOSE)
    def flow_close(self):
        """ change state from Accept to Close """


class SyrupUsage(models.Model):
    """ บันทึกข้อมูลการใช้น้ำเชื่อมเป็นวัตถุดิบฯ """
    TYPE_CHOICES = (
        (1, 'Syrup'),
        (2, 'B-molasses'),
        (3, 'C-molasses')
    )

    STATUS_DRAFT = 0  # ร่างข้อมูลการใช้น้ำเชื่อมฯ
    STATUS_REVIEW_1 = 1  # รอยืนยัน/รับทราบโดย เจ้าหน้าที่บริษัท
    STATUS_REVIEW_2 = 2  # รอยืนยัน/รับทราบโดย เจ้าหน้าที่ สอน. ประจำโรงงาน
    STATUS_REVIEW_3 = 3  # รอยืนยัน/รับทราบโดย เจ้าหน้าที่ เขต
    STATUS_REVIEW_4 = 4  # รอยืนยัน/รับทราบโดย เจ้าหน้าที่ สบน.
    STATUS_REVIEW_5 = 5  # รอยืนยัน/รับทราบโดย เจ้าหน้าที่ กสช.
    STATUS_CONFIRM = 6  # ผ่านการยืนยัน/รับทราบ
    STATUS_REJECT = 7  # ไม่ผ่านการยืนยัน/รับทราบ
    STATUS_CHOICES = (
        (STATUS_DRAFT, 'รอส่งข้อมูล'),
        (STATUS_REVIEW_1, 'รอยืนยัน จนท.บริษัท'),
        (STATUS_REVIEW_2, 'รอยืนยัน สอน. ประจำโรงงาน'),
        (STATUS_REVIEW_3, 'รอยืนยัน จนท. เขต'),
        (STATUS_REVIEW_4, 'รอยืนยัน จนท. สบน.'),
        (STATUS_REVIEW_5, 'รอยืนยัน จนท. กสช.'),
        (STATUS_CONFIRM, 'ผ่านการยืนยัน'),
        (STATUS_REJECT, 'ไม่ผ่าน'),
    )
    # ---------------------- ข้อมูลจากพารามีเตอร์ (Hidden)
    quota_request = models.ForeignKey(
        QuotaRequest, verbose_name='คำร้องขออนุญาตฯ', on_delete=models.CASCADE,
        null=True)
    enterprise = models.ForeignKey(
        Enterprise, verbose_name='โรงงานที่ได้รับอนุญาต', on_delete=models.CASCADE)
    # ---------------------- ข้อมูลที่ต้องกรอก
    purchaser = models.ForeignKey(
        Purchaser, verbose_name='โรงงานรับซื้อ', on_delete=models.CASCADE)
    date_report = models.DateField(
        verbose_name='วันที่รายงาน', auto_now=False, auto_now_add=False)
    syrup_weight = models.DecimalField(
        verbose_name='น้ำหนัก/ปริมาณน้ำเชื่อม (ตัน)', max_digits=8,
        decimal_places=3)
    syrup_valume = models.DecimalField(
        verbose_name='ปริมาตรน้ำเชื่อม (ลบ.ม.)', max_digits=9,
        decimal_places=3, default=0)
    syrup_type = models.SmallIntegerField(
        verbose_name='ชนิดของน้ำเชื่อม', choices=TYPE_CHOICES)
    theoretical = models.DecimalField(
        verbose_name='Actual to Theoretical Recovery', max_digits=5, decimal_places=2)
    undetermine_loss = models.DecimalField(
        verbose_name='ร้อยละของการสูญเสียโดยไม่ทราบสาเหตุ', max_digits=5, decimal_places=2)
    daily_cane_input = models.DecimalField(
        verbose_name='ปริมาณอ้อยทั้งหมดที่เข้าหีบประจำวัน (ตัน)', max_digits=9, decimal_places=2)
    pol_in_can = models.DecimalField(
        verbose_name='ร้อยละของค่าโพลในอ้อย', max_digits=5, decimal_places=2)
    pol_extraction = models.DecimalField(
        verbose_name='ร้อยละของ Pol Extraction', max_digits=5, decimal_places=2)
    loss_filter_cake = models.DecimalField(
        verbose_name='ร้อยละของการสูญเสียน้ำตาลในกากตะกอนกรอง', max_digits=5, decimal_places=2)
    raw_sugar_tons_ent = models.DecimalField(
        verbose_name='บริษัทคำนวณ Raw Sugar (Tons)',
        max_digits=9, decimal_places=2, default=0)
    ton_mollasses_ent = models.DecimalField(
        verbose_name='บริษัทคำนวณ Ton Mollasses (Tons)', decimal_places=3,
        max_digits=9, null=True, blank=True)
    # ---------------------- ข้อมูลน้ำเชื่อม (syrup)
    syrup_brix = models.DecimalField(
        verbose_name='ค่าบริกซ์น้ำเชื่อม', max_digits=4, decimal_places=2)
    syrup_pol = models.DecimalField(
        verbose_name='ค่าโพลน้ำเชื่อม', max_digits=4, decimal_places=2)
    syrup_purity = models.DecimalField(
        verbose_name='ความบริสุทธิ์ของน้ำเชื่อม', max_digits=5, decimal_places=2)
    # ---------------------- ข้อมูลน้ำตาลทรายดิบ (Raw Sugar)
    rawsugar_pol = models.DecimalField(
        verbose_name='ค่าโพลน้ำตาลทรายดิบ', max_digits=4, decimal_places=2)
    rawsugar_moisture = models.DecimalField(
        verbose_name='ค่าความชื้นน้ำตาลทรายดิบ',
        max_digits=4, decimal_places=2)
    rawsugar_purity = models.DecimalField(
        verbose_name='ความบริสุทธิ์น้ำตาลทรายดิบ',
        max_digits=5, decimal_places=2)
    # ---------------------- ข้อมูลกากน้ำตาล (Mollasses)
    mollasses_brix = models.DecimalField(
        verbose_name='ค่าบริกซ์กากน้ำตาล', max_digits=4, decimal_places=2)
    mollasses_pol = models.DecimalField(
        verbose_name='ค่าโพลกากน้ำตาล', max_digits=4, decimal_places=2)
    mollasses_purity = models.DecimalField(
        verbose_name='ความบริสุทธิ์ของกากน้ำตาล', max_digits=5, decimal_places=2)
    # ---------------------- ข้อมูลจากการคำนวณอื่นๆ
    density_indice = models.DecimalField(
        verbose_name='ดัชนีความหนาแน่น', max_digits=7, decimal_places=5, default=0)
    sjm = models.DecimalField(
        verbose_name='น้ำตาลที่ควรจะผลิตได้ในรูป S-J-M', max_digits=5, decimal_places=2)
    actual_sugar_recovery = models.DecimalField(
        verbose_name='Actual Sugar Recovery', max_digits=5, decimal_places=2)
    raw_sugar_tons_pol = models.DecimalField(
        verbose_name='Raw Sugar (Tons Pol)', max_digits=6, decimal_places=2)
    raw_sugar_tons = models.DecimalField(
        verbose_name='ปริมาณน้ำตาลทรายดิบที่ผลิตได้/Raw Sugar (Tons)',
        max_digits=9, decimal_places=2, default=0)
    ton_pol_syrup = models.DecimalField(
        verbose_name='Ton Pol Syrup', decimal_places=2,
        max_digits=9, null=True, blank=True)
    ton_pol_rawsuger = models.DecimalField(
        verbose_name='Ton Pol Raw Sugar', decimal_places=2,
        max_digits=9, null=True, blank=True)
    ton_under_loss = models.DecimalField(
        verbose_name='Ton Undetermine Loss', decimal_places=2,
        max_digits=9, null=True, blank=True)
    ton_pol_mollasses = models.DecimalField(
        verbose_name='Ton Pol  Mollasses', decimal_places=2,
        max_digits=9, null=True, blank=True)
    ton_mollasses = models.DecimalField(
        verbose_name='Ton Mollasses (Tons)', decimal_places=3,
        max_digits=9, null=True, blank=True)
    ton_pol_daily = models.DecimalField(
        verbose_name='Ton Pol Daily Cane Input', decimal_places=2,
        max_digits=9, null=True, blank=True)
    ton_pol_mixed = models.DecimalField(
        verbose_name='Ton Pol Mixed Juice', decimal_places=2,
        max_digits=9, null=True, blank=True)
    ton_pol_filter = models.DecimalField(
        verbose_name='Ton Pol Filter Cake', decimal_places=2,
        max_digits=9, null=True, blank=True)
    ton_pol_clearified = models.DecimalField(
        verbose_name='Ton Pol Clearified Juice', decimal_places=2,
        max_digits=9, null=True, blank=True)
    ton_raw_syrup = models.DecimalField(
        verbose_name='Ton Raw Syrup', decimal_places=2,
        max_digits=9, null=True, blank=True)
    ratio_raw_cane = models.DecimalField(
        verbose_name='Ratio of Raw Syup per Cane', decimal_places=4,
        max_digits=6, null=True, blank=True)

    estimate_ton_can = models.DecimalField(
        verbose_name='Estimated Ton Cane Using as Raw ', decimal_places=2,
        max_digits=9, null=True, blank=True)
    efficiency_raw = models.DecimalField(
        verbose_name='ประสิทธิภาพการผลิตน้ำตาล กก/ตันอ้อย', decimal_places=2,
        max_digits=9, null=True, blank=True)
    efficiency_mollasses = models.DecimalField(
        verbose_name='ประสิทธิภาพการผลิตกากน้ำตาล กก/ตันอ้อย', decimal_places=2,
        max_digits=9, null=True, blank=True)
    diff_raw_sugar = models.DecimalField(
        verbose_name='ส่วนต่าง Raw Sugar (Tons) (สอน.-บริษัท)', decimal_places=2,
        max_digits=9, null=True, blank=True)
    diff_ton_mollasses = models.DecimalField(
        verbose_name='ส่วนต่าง Ton Mollasses (Tons) (สอน.-บริษัท)', decimal_places=3,
        max_digits=9, null=True, blank=True)


    workflow_state = FSMIntegerField(choices=STATUS_CHOICES,
                                     default=STATUS_DRAFT,
                                     # protected=True,
                                     help_text='work flow state')
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name=("ผู้บันทึก"), null=True, on_delete=models.SET_NULL)
    create_date = models.DateField(
        verbose_name='วันที่บันทึก', auto_now=False, auto_now_add=True)
    is_active = models.BooleanField(verbose_name='ใช้งานหรือไม่', default=True)

    def __str__(self):
        return f'{self.date_report} {self.enterprise}'

    @transition(field=workflow_state, source=STATUS_DRAFT, target=STATUS_REVIEW_1)
    def flow_draft(self):
        """ change state from Draft to Review_1 """

    @transition(field=workflow_state, source=STATUS_REVIEW_1, target=STATUS_REVIEW_2)
    def flow_reviewed_1(self):
        """ change state from Review_1 to Review_2 """

    @transition(field=workflow_state, source=STATUS_REVIEW_2, target=STATUS_REVIEW_3)
    def flow_reviewed_2(self):
        """ change state from Review_2 to Review_3 """

    @transition(field=workflow_state, source=STATUS_REVIEW_3, target=STATUS_REVIEW_4)
    def flow_reviewed_3(self):
        """ change state from Review_3 to Review_4 """

    @transition(field=workflow_state, source=STATUS_REVIEW_4, target=STATUS_REVIEW_5)
    def flow_reviewed_4(self):
        """ change state from Review_4 to Review_5 """

    @transition(field=workflow_state, source=STATUS_REVIEW_5, target=STATUS_CONFIRM)
    def flow_reviewed_5(self):
        """ change state from Review_5 to Confirm """

    @transition(field=workflow_state, source=[STATUS_REVIEW_1, STATUS_REVIEW_2,
        STATUS_REVIEW_3, STATUS_REVIEW_4, STATUS_REVIEW_5], target=STATUS_REJECT)
    def flow_reject(self):
        """ change state from Review to Reject """

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'SyrupUsage'
        verbose_name_plural = 'SyrupUsages'
