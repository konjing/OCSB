$(document).ready(function () {
  // init  
  
  //Date picker, date_request
  $("#id_date_request").datetimepicker({
    format: "YYYY-MM-DD",
  });
  // คำนวณ ปริมาณน้ำเชื่อมรวมทั้งหมด (ตัน)
  $("#id_total_syrup, #id_total_bmolasses, #id_total_cmolasses").change(function () {
    var total_syrup = $("#id_total_syrup").val();
    var total_bmolasses = $("#id_total_bmolasses").val();
    var total_cmolasses = $("#id_total_cmolasses").val();
    var total_amount = parseFloat(total_syrup) + parseFloat(total_bmolasses) + parseFloat(total_cmolasses);

    $("#id_total_amount").val(parseFloat(total_amount).toFixed(2));
    return true;
  });
});
