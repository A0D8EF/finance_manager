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

    $(".create_day_balance").on("click", function() { create_day_balance($(this).text()) });
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
            console.log(tab_id);
            break;
        }
    }
    for(let t of tab_radios) {
        if( t.id == tab_id ){
            console.log("t.id: " + t.id + ", tab_id: " + tab_id);
            t.checked = true;
        }
    }
}

function change_expense_item(income, id){
    console.log(income);

    url = "income/?income=" + String(income);

    console.log(url);

    $.ajax({
        url: url,
        type: "GET",
        dataType: 'json'
    }).done( function(data, status, xhr ){
        console.log("done");

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