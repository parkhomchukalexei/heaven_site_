var a = document.getElementsByClassName("day_of_month")


for ( let i = 0; i <  a.length; i++){
    a[i].addEventListener('dblclick', (event) => {
        a[i].innerHTML='<form action="api/add_tabledata" method="POST">' + {% csrf_token %} + '<input name="data"><input type="hidden" name="date" value="1"><input type="hidden" name="data_type" value="{{info.data_type}}"><input type="hidden" name="table" value="{{info.table}}"><input type="submit" style="position: absolute; left: -9999px"/></form>';
});
}


