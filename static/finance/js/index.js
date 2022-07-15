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

});

function change_expense_item(income){
    // TODO:selectタグの選択肢をレンダリング（Ajax）
    console.log(income);
}