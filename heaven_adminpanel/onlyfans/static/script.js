$(".day_of_month").css("color", "red");
$("p").css("color", "red");


$.ajax({
    url: 'get_table_data/2/',         /* Куда отправить запрос */
    method: 'get',             /* Метод запроса (post или get) */
    dataType: 'json',          /* Тип данных в ответе (xml, json, script, html). */     /* Данные передаваемые в массиве */
    success: function(data){   /* функция которая будет выполнена после успешного запроса.  */
	     alert(data); /* В переменной data содержится ответ от index.php. */
    }
});


$(".day_of_month")