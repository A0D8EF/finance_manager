window.addEventListener("load", function (){

    let today   = new Date();
    let year    = String(today.getFullYear());
    let month   = ("0" + String(today.getMonth() + 1)).slice(-2);
    let day     = ("0" + String(today.getDate())).slice(-2);

    let date    = year + "-" + month + "-" + day;
    let config_date = {
        locale: "ja",
        dateFormat: "Y-m-d",
        defaultDate: date
    }

    $(".modal_label").on("click", function(){ flatpickr(".date", config_date); });

    const tab_radios = $(".tab_radio");
    $(".tab_radio").on("change", (event) => {
        for(let t of tab_radios) {
            if( t.checked ){
                document.cookie = "tab=" + decodeURIComponent(t.id);
                document.cookie = "Path=/single";
                document.cookie = "SameSite=strict";
                // console.log(document.cookie);
            }
        }
    });

    set_tab();

    $(".income_chk").on("change", function(){ change_expense_item( $(this).prop("checked"), $(this).val() ); });
    change_expense_item($("#income_chk").prop("checked"), $("#income_chk").val() );

    $("#add_income").on("click", function() { add_income(); });
    $("#modal_sw").on("click", function() { list_income(); });
    $(".modal_bg").on("click", function() {
        $("#modal_sw").prop("checked", false);
    })

    // balanceの新規登録
    $(".modal_label[for='modal_chk']").on("click", function() {
        $("#balance_form").prop("action", "");
    });

    // balanceの編集
    $(".edit_modal_chk").prop("checked", false);
    $(".submit_edit").on("click", function() { edit( $(this).val() ); });

    // balanceの削除
    $(".trash").on("click", function() { trash( $(this).val() ); });

    $(".create_day_balance").on("click", function() { create_day_balance( $(this).data("day") ); });

    draw_bar_graph();
    draw_income_pie_graph();
    draw_spending_pie_graph();
});

function set_tab() {

    let tab_id = "tab_radio_1";
    const tab_radios = $(".tab_radio");
    
    let cookies         = document.cookie;
    let cookiesArray    = cookies.split(';');
    for(let c of cookiesArray) {
        let cArray = c.split('=');
        if( cArray[0].trim() === "tab"){
            tab_id  = cArray[1];
            break;
        }
    }
    for(let t of tab_radios) {
        if( t.id == tab_id ){
            t.checked = true;
        }
    }
}

function change_expense_item(income, id){
    url = "income/?income=" + String(income);

    $.ajax({
        url: url,
        type: "GET",
        dataType: 'json'
    }).done( function(data, status, xhr ){
        if(!data.error){
            $("#expense_item_" + id).html(data.content);
        }else{
            console.log("費目フラグバリデーションエラー");
        }
    }).fail( function(xhr, status, error ){
        console.log(status + ":" + error );
    });
}

function add_income(){

    let form_elem = "#add_income_form";

    let data    = new FormData( $(form_elem).get(0) );
    let url     = $(form_elem).prop("action");
    let method  = $(form_elem).prop("method");

    $.ajax({
        url: url,
        type: method,
        data: data,
        processData: false, // dataに指定した内容をURLにエンコードして送信するかの指定
        contentType: false, // デフォルトではURLエンコードされた形式で送信されてしまう
        dataType: 'json'
    }).done( function(data, status, xhr ){
        
        if(data.error){
            console.log("ERROR");
        }else{
            change_expense_item($("#income_chk").prop("checked"));
        }

    }).fail( function(xhr, status, error) {
        console.log(status + ":" + error );
    });
    
}

function list_income(){

    let url = "income_list";

    $.ajax({
        url: url,
        type: "GET",
        dataType: 'json'
    }).done( function(data, status, xhr ){
        console.log("done");

        if(!data.error){
            $("#income_list").html(data.content);
        }else{
            console.log("費目リストバリデーションエラー");
        }

    }).fail( function(xhr, status, error ){
        console.log(status + ":" + error );
    });
}

function trash(id){

    if(!confirm("本当に削除しますか？")){
        return false;
    }

    let url = DELETE_URL.replace("1", id);
    console.log(url);

    $.ajax({
        url: url,
        type: "DELETE",
        dataType: 'json'
    }).done( function(data, status, xhr){
        if(!data.error){
            location.reload();
        }else{
            console.log("DELETE ERROR");
        }
    }).fail( function(xhr, status, error){
        console.log(status + ":" + error );
    });
}

function edit(id){

    let form_elem   = "#edit_form_" + id;
    let data        = new FormData( $(form_elem).get(0) );
    let url         = $(form_elem).prop("action");

    $.ajax({
        url: url,
        type: "PUT",
        data: data,
        processData: false,
        contentType: false,
        dataType: 'json'
    }).done( function(data, status, xhr){
        if(!data.error){
            let date_id = "#date_" + id;
            let date    = $(date_id).val();
            let config_date = {
                locale: "ja",
                dateFormat: "Y-m-d",
                defaultDate: date
            }
            flatpickr(date_id, config_date);
            location.reload();
        }else{
            console.log("EDIT ERROR");
        }
    }).fail( function(xhr, status, error){
        console.log(status + ":" + error );
    });
}

function create_day_balance(calender_day){
    let year    = $("[name='year'] option:selected").val();
    let month   = $("[name='month'] option:selected").val();

    month       = ("0" + String(month)).slice(-2);
    let day     = ("0" + String(calender_day)).slice(-2);
    
    let date    = year + "-" + month + "-" + day;

    let config_date = {
        locale: "ja",
        dateFormat: "Y-m-d",
        defaultDate: date
    }

    flatpickr(".date", config_date);
    $("#modal_chk").prop("checked", true);

}

function draw_bar_graph(){

    let label_elems = $(".monthly_balance_label");
    let data_elems  = $(".monthly_balance_data");

    let labels      = [];
    let datas       = [];

    for (let label_elem of label_elems){
        labels.push(label_elem.innerText.replace("年", "/").replace("月", ""));
    }
    for (let data_elem of data_elems){
        let raw_data    = data_elem.innerText;
        datas.push(Number(raw_data.replace(/,/g, "").replace("円", "")));
    }

    let colors      = [];
    for (let data of datas){
        if (data >= 0){
            colors.push('rgba(20,60,220,0.8)');
        }else{
            colors.push('rgba(220,20,60,0.8)');
        }
    }

    const ctx       = document.getElementById("monthly_balance_graph").getContext("2d");
    const myChart   = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "収支",
                data: datas,
                backgroundColor: colors,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false,
                }
            }
        }
    });
}

function draw_income_pie_graph(){
    let label_elems = $(".monthly_income_label");
    let data_elems  = $(".monthly_income_data");

    let labels      = [];
    let datas       = [];

    for (let label_elem of label_elems){
        labels.push(label_elem.innerText);
    }
    let total       = 0;
    for (let data_elem of data_elems){
        let raw_data    = data_elem.innerText;
        datas.push(Number(raw_data.replace(/,/g, "").replace("\xA5", "")));
        total += Number(raw_data.replace(/,/g, "").replace("\xA5", ""))
    }
    
    let colors      = [];
    let base_r      = 20;
    let base_g      = 60;
    let base_b      = 220;
    for (let data of datas){
        colors.push("rgba(" + String(base_r) + "," + String(base_g) + "," + String(base_b) + ",0.8)");
        base_b      = base_b / 1.4;
        base_g  = base_g * 1.1;
    }

    const ctx       = document.getElementById("income_graph").getContext("2d");
    const myChart   = new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                label: "収入",
                data: datas,
                backgroundColor: colors,
                borderWidth: 1
            }]
        },
        options: {
            // CHIPS:https://blog.imind.jp/entry/2019/07/19/210646
            plugins: {
                // tooltip: {
                //     enabled: false
                // },
                datalabels: {
                    font: {
                        weight: "bold",
                        size: 16
                    },
                    formatter: function( value, ctx ) {
                        let label = ctx.chart.data.labels[ctx.dataIndex];
                        if (value/total < 0.1) {
                            return "";
                        }
                        return label + '\n' + "\xA5" + value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
                    },
                    color: "#ffffff"
                },
                legend: {
                        display: false,
                },
            }
        },
        plugins: [
            ChartDataLabels,
        ],
    });
}

function draw_spending_pie_graph(){
    let label_elems = $(".monthly_spending_label");
    let data_elems  = $(".monthly_spending_data");

    let labels      = [];
    let datas       = [];

    for (let label_elem of label_elems){
        labels.push(label_elem.innerText);
    }
    let total       = 0;
    for (let data_elem of data_elems){
        let raw_data    = data_elem.innerText;
        datas.push(Number(raw_data.replace(/,/g, "").replace("\xA5", "")));
        total += Number(raw_data.replace(/,/g, "").replace("\xA5", ""))
    }
    
    let colors      = [];
    let base_r      = 220;
    let base_g      = 20;
    let base_b      = 60;
    for (let data of datas){
        colors.push("rgba(" + String(base_r) + "," + String(base_g) + "," + String(base_b) + ",0.8)");
        base_r      = base_r / 1.2;
        if (base_r < 60){
            base_g  = base_g / 1.1;
            base_b  = base_b / 1.2;
        }
    }

    const ctx       = document.getElementById("spending_graph").getContext("2d");
    const myChart   = new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                label: "支出",
                data: datas,
                backgroundColor: colors,
                borderWidth: 1
            }]
        },
        options: {
            // CHIPS:https://blog.imind.jp/entry/2019/07/19/210646
            plugins: {
                // tooltip: {
                //     enabled: false
                // },
                datalabels: {
                    font: {
                        weight: "bold",
                        size: 16
                    },
                    formatter: function( value, ctx ) {
                        let label = ctx.chart.data.labels[ctx.dataIndex];
                        if (value/total < 0.1) {
                            return "";
                        }
                        return label + '\n' + "\xA5" + value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
                    },
                    color: "#ffffff"
                },
                legend: {
                        display: false,
                },
            }
        },
        plugins: [
            ChartDataLabels,
        ],
    });
}
