function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    // 正規表現.test()は引数に正規表現が含まれるかどうかをチェックする。含まれていればtrueを返す
}
// POST,PUT,PATCH,DELETE: CSRFトークンが必要

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        // xhrはXMLHttpRequest Object。これを使うことでAjaxの送信結果・設定・内容を取得することができる
        // settingsには$.ajax()実行時のオブジェクト型の引数の値が充てられる
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});