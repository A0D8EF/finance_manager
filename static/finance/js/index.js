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

    flatpickr("#date", config_date);

    $("#income_chk").on("change", function(){ change_expense_item( $(this).prop("checked") ); });
    change_expense_item($("#income_chk").prop("checked"));

    $("#add_income").on("click", function() { add_income(); });

});

function change_expense_item(income){
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
            $("[name='expense_item']").html(data.content);
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

    console.log("for v of data");
    for (let v of data){ console.log(v); }
    console.log("for v of data.entries()");
    for (let v of data.entries()){ console.log(v); }

    $.ajax({
        url: url,
        type: method,
        data: data,
        processData: false, // dataに指定しtあ内容をURLにエンコードして送信するかの指定
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

