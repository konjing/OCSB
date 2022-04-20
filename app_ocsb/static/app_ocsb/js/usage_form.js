$(document).ready(function () {
  // init

  //Date picker, date_request

  $("#id_syrup_weight, #id_syrup_brix, #id_syrup_pol, #id_rawsugar_moisture, #id_rawsugar_pol," +
      "#id_mollasses_brix, #id_mollasses_pol, #id_theoretical," + 
      "#id_undetermine_loss, #id_daily_cane_input, #id_pol_in_can," +
      "#id_pol_extraction, #id_loss_filter_cake").change(function () {
      //"#id_raw_sugar_tons_ent, #id_ton_mollasses_ent"
    var syrup_weight = $("#id_syrup_weight").val();
    var syrup_brix = $("#id_syrup_brix").val();
    var syrup_pol = $("#id_syrup_pol").val();
    var rawsugar_pol = $("#id_rawsugar_pol").val();
    var rawsugar_moisture = $("#id_rawsugar_moisture").val();
    var mollasses_pol = $("#id_mollasses_pol").val();
    var mollasses_brix = $("#id_mollasses_brix").val();
    var theoretical = $("#id_theoretical").val();
    var undetermine_loss = $("#id_undetermine_loss").val();
    var daily_cane_input = $("#id_daily_cane_input").val();
    var pol_in_can = $("#id_pol_in_can").val();
    var pol_extraction = $("#id_pol_extraction").val();
    var loss_filter_cake = $("#id_loss_filter_cake").val();
    // var raw_sugar_tons_ent = $("#id_raw_sugar_tons_ent").val();
    // var ton_mollasses_ent = $("#id_ton_mollasses_ent").val();


    // คำนวณ syrup_purity (ความบริสุทธิ์ของน้ำเชื่อม)
    var syrup_purity = (parseFloat(syrup_pol) / parseFloat(syrup_brix)) * 100;
    $("#id_syrup_purity").val(parseFloat(syrup_purity).toFixed(2));
    // คำนวณ Raw Sugar purity (ความบริสุทธิ์ของน้ำตาลดิบ)
    var rawsugar_purity = (parseFloat(rawsugar_pol) / (100 - parseFloat(rawsugar_moisture))) * 100;
    $("#id_rawsugar_purity").val(parseFloat(rawsugar_purity).toFixed(2));
    // คำนวณ Mollasses purity (ความบริสุทธิ์ของกากน้ำตาล)
    var mollasses_purity = (parseFloat(mollasses_pol) / parseFloat(mollasses_brix)) * 100;
    $("#id_mollasses_purity").val(parseFloat(mollasses_purity).toFixed(2));

    //น้ำตาลที่ควรจะผลิตได้ในรูป S-J-M
    var sjm = (100 * (rawsugar_purity * (syrup_purity - mollasses_purity))) / (syrup_purity * (rawsugar_purity - mollasses_purity));
    $("#id_sjm").val(parseFloat(sjm).toFixed(2));

    //Actual Sugar Recovery
    var actual_sugar = (theoretical / 100) * sjm;
    $("#id_actual_sugar_recovery").val(parseFloat(actual_sugar).toFixed(2));

    //Raw Sugar (Tons Pol)
    var raw_sugar_tons_pol = syrup_pol / 100 * actual_sugar / 100 * syrup_weight;
    $("#id_raw_sugar_tons_pol").val(parseFloat(raw_sugar_tons_pol).toFixed(2));
    
    //Raw Sugar (Tons)
    var raw_sugar_tons = raw_sugar_tons_pol / (rawsugar_pol / 100);
    $("#id_raw_sugar_tons").val(parseFloat(raw_sugar_tons).toFixed(2));

    //Ton Pol Syrup
    // var ton_pol_syrup = syrup_weight * syrup_pol /100;
    // $("#id_ton_pol_syrup").val(parseFloat(ton_pol_syrup).toFixed(2));

    //Ton Pol Raw Sugar
    // var ton_pol_rawsuger = raw_sugar_tons_pol;
    // $("#id_ton_pol_rawsuger").val(parseFloat(ton_pol_rawsuger).toFixed(2));

    //Ton Undetermine Loss
    // var ton_under_loss = undetermine_loss / 100 * ton_pol_syrup;
    // $("#id_ton_under_loss").val(parseFloat(ton_under_loss).toFixed(2));

    //Ton Pol Mollasses
    // var ton_pol_mollasses = (ton_pol_syrup - ton_pol_rawsuger - ton_under_loss);
    // $("#id_ton_pol_mollasses").val(parseFloat(ton_pol_mollasses).toFixed(2));

    //Ton Mollasses (Tons)
    var ton_mollasses = ton_pol_mollasses / (mollasses_pol/100);
    $("#id_ton_mollasses").val(parseFloat(ton_mollasses).toFixed(2));

    //////
    //Ton Pol Daily Cane Input
    // var ton_pol_daily = daily_cane_input * pol_in_can / 100;
    // $("#id_ton_pol_daily").val(parseFloat(ton_pol_daily).toFixed(2));

    //Ton Pol Mixed Juice
    // var ton_pol_mixed = ton_pol_daily * pol_extraction / 100;
    // $("#id_ton_pol_mixed").val(parseFloat(ton_pol_mixed).toFixed(2));

    //Ton Pol Filter Cake
    // var ton_pol_filter = ton_pol_daily * loss_filter_cake / 100;
    // $("#id_ton_pol_filter").val(parseFloat(ton_pol_filter).toFixed(2));

    //Ton Pol Clearified Juice
    // var ton_pol_clearified = ton_pol_mixed - ton_pol_filter;
    // $("#id_ton_pol_clearified").val(parseFloat(ton_pol_clearified).toFixed(2));

    //Ton Raw Syrup
    // var ton_raw_syrup = ton_pol_clearified / (syrup_pol / 100);
    // $("#id_ton_raw_syrup").val(parseFloat(ton_raw_syrup).toFixed(2));

    //Ratio of Raw Syup per Cane
    // var ratio_raw_cane = ton_raw_syrup / daily_cane_input;
    // $("#id_ratio_raw_cane").val(parseFloat(ratio_raw_cane).toFixed(4));

    //Estimated Ton Cane Using as Raw
    // var estimate_ton_can = syrup_weight / ratio_raw_cane;
    // $("#id_estimate_ton_can").val(parseFloat(estimate_ton_can).toFixed(2));

    //ประสิทธิภาพการผลิตน้ำตาล กก/ตันอ้อย
    // var efficiency_raw = (raw_sugar_tons * 1000) / estimate_ton_can;
    // $("#id_efficiency_raw").val(parseFloat(efficiency_raw).toFixed(2));

    //ประสิทธิภาพการผลิตกากน้ำตาล กก/ตันอ้อย
    // var efficiency_mollasses = (ton_mollasses * 1000) / estimate_ton_can;
    // $("#id_efficiency_mollasses").val(parseFloat(efficiency_mollasses).toFixed(2));

    //ส่วนต่าง Raw Sugar (Tons) (สอน.-บริษัท)
    // var diff_raw_sugar = raw_sugar_tons - raw_sugar_tons_ent;
    // $("#id_diff_raw_sugar").val(parseFloat(diff_raw_sugar).toFixed(2));

    //ส่วนต่าง Ton Mollasses (Tons) (สอน.-บริษัท)
    // var diff_ton_mollasses = ton_mollasses - ton_mollasses_ent;
    // $("#id_diff_ton_mollasses").val(parseFloat(diff_ton_mollasses).toFixed(3));
    
    $("#syrup_weight_show").val(syrup_weight);

    return true;
  });
});
