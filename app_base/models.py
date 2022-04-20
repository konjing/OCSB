""" app_base Model"""
from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.


class Region(models.Model):
    """ ตารางภูมิภาค """
    name = models.CharField(verbose_name='ชื่อภูมิภาค', max_length=100)

    def __str__(self):
        return f'{self.name}'


class Province(models.Model):
    """ ตารางจังหวัด """
    region = models.ForeignKey(Region, null=True, on_delete=models.SET_NULL)
    code = models.CharField(verbose_name='รหัสจังหวัด', max_length=20)
    name = models.CharField(verbose_name='ชื่อจังหวัด', max_length=100)

    def __str__(self):
        return f'{self.name}'


class Amphur(models.Model):
    """ ตารางอำเภอ """
    province = models.ForeignKey(
        Province, null=True, on_delete=models.SET_NULL)
    code = models.CharField(verbose_name='รหัสอำเภอ', max_length=20)
    name = models.CharField(verbose_name='ชื่ออำเภอ', max_length=100)
    postcode = models.CharField(verbose_name='รหัสไปรษณีย์', max_length=20)

    def __str__(self):
        return f'{self.name}'


class Tumbol(models.Model):
    """ ตารางตำบล """
    amphur = models.ForeignKey(Amphur, null=True, on_delete=models.SET_NULL)
    code = models.CharField(verbose_name='รหัสตำบล', max_length=20)
    name = models.CharField(verbose_name='ชื่อตำบล', max_length=100)

    def __str__(self):
        return f'{self.name}'


class Enterprise(models.Model):
    """ ตารางโรงงานผลิตน้ำตาล (จำหน่ายน้ำตาล) """
    name = models.CharField(verbose_name='ชื่อสถานประกอบการ', max_length=200)
    address_no = models.CharField(
        verbose_name='เลขที่', max_length=100, null=True, blank=True)
    mu = models.CharField(verbose_name='หมู่',
                          max_length=100, null=True, blank=True)
    soi = models.CharField(
        verbose_name='ซอย', max_length=100, null=True, blank=True)
    street = models.CharField(
        verbose_name='ถนน', max_length=100, null=True, blank=True)
    province = models.ForeignKey(
        Province, null=True, on_delete=models.SET_NULL)
    amphur = models.ForeignKey(Amphur, null=True, on_delete=models.SET_NULL)
    tumbol = models.ForeignKey(Tumbol, null=True, on_delete=models.SET_NULL)
    postcode = models.CharField(
        verbose_name='รหัสไปรษณีย์', max_length=200, null=True, blank=True)
    tel = models.CharField(verbose_name='เบอร์ติดต่อ',
                           max_length=200, null=True, blank=True)
    fax = models.CharField(verbose_name='แฟกซ์ติดต่อ',
                           max_length=200, null=True, blank=True)
    email = models.EmailField(
        verbose_name='อีเมลติดต่อ', null=True, blank=True)
    website = models.CharField(
        verbose_name='เว็บไซต์ติดต่อ', max_length=200, null=True, blank=True)

    class Meta:
        """ Docstring """
        verbose_name = "Enterprise"
        verbose_name_plural = "Enterprises"

    def __str__(self):
        """ Docstring """
        return f'{self.name}'

    def get_absolute_url(self):
        """ Docstring """
        return reverse("Enterprise_detail", kwargs={"pk": self.pk})


class Season(models.Model):
    """ ตารางฤดูกาลผลิต """
    name = models.CharField(verbose_name='ชื่อฤดูกาล', max_length=20)
    code = models.CharField(verbose_name='รหัสย่อ', max_length=6, null=True)
    is_active = models.BooleanField(verbose_name='สถานะ', default=True)

    class Meta:
        """ Docstring """
        verbose_name = "Season"
        verbose_name_plural = "Seasons"

    def __str__(self):
        """ Docstring """
        return f'{self.name}'

    def get_absolute_url(self):
        """ Docstring """
        return reverse("Season_detail", kwargs={"pk": self.pk})


class Profile(models.Model):
    """ ตารางรายละเอียดผู้ใช้งาน 1 on 1 กับตาราง User """
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
        verbose_name=("อ้างอิงโมเดล User"), related_name="user_profile", on_delete=models.CASCADE)
    address_no = models.CharField(
        verbose_name='เลขที่', max_length=100, null=True, blank=True)
    mu = models.CharField(
        verbose_name='หมู่', max_length=100, null=True, blank=True)
    soi = models.CharField(
        verbose_name='ซอย', max_length=100, null=True, blank=True)
    street = models.CharField(
        verbose_name='ถนน', max_length=100, null=True, blank=True)
    province = models.ForeignKey(
        Province, null=True, on_delete=models.SET_NULL)
    amphur = models.ForeignKey(Amphur, null=True, on_delete=models.SET_NULL)
    tumbol = models.ForeignKey(Tumbol, null=True, on_delete=models.SET_NULL)
    postcode = models.CharField(
        verbose_name='รหัสไปรษณีย์', max_length=200, null=True, blank=True)
    tel = models.CharField(
        verbose_name='เบอร์ติดต่อ', max_length=200, null=True, blank=True)
    enterprises = models.ManyToManyField(Enterprise,
        verbose_name=("โรงงานที่รับผิดชอบ"), blank=True)

    class Meta:
        """ Docstring """
        verbose_name = ("Profile")
        verbose_name_plural = ("Profiles")

    def __str__(self):
        return f'{self.user}'

    def get_absolute_url(self):
        """ Docstring """
        return reverse("Profile_detail", kwargs={"pk": self.pk})


class Purchaser(models.Model):
    """ ตารางโรงงานรับซื้อน้ำเชื่อมฯ (ผลิตเอทานอล) """
    name = models.CharField(verbose_name='ชื่อโรงงาน', max_length=200)
    factory_code = models.CharField(verbose_name='รหัสโรงงานรับซื้อ', max_length=20,
                                    null=True, blank=True)

    class Meta:
        """ Docstring """
        verbose_name = "Purchaser"
        verbose_name_plural = "Purchasers"

    def __str__(self):
        """ Docstring """
        return f'{self.name}'


class Brix(models.Model):
    """ ตารางความหนาแน่นของน้ำเชื่อม"""
    brix_value = models.DecimalField(
        verbose_name='ค่าบริกซ์',
        max_digits=4, decimal_places=1, unique=True)
    spcific_gravity = models.DecimalField(
        verbose_name="spcific gravity at 20 C/20 C",
        max_digits=6, decimal_places=5)

    def __str__(self):
        return f'{self.brix_value}'

    class Meta:
        """ Docstring """
        db_table = ''
        managed = True
        verbose_name = 'Brix'
        verbose_name_plural = 'Brixs'
