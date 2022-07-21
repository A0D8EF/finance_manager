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
            console.log("費目フラグバリデーションエラー")
        }

    }).fail( function(xhr, status, error ){
        console.log(status + ":" + error )
    });
}