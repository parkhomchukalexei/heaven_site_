console.log('hui')
var a = document.getElementsByClassName("day_of_month")
    var tables = document.getElementsByClassName('table table-bordered')
    for (i = 0; i < tables.length; i++) {
        tables[i].setAttribute('id', i)
    }

    function has_perms() {
        const all_perms = perms
        if (all_perms.includes('onlyfans.add_tabledata')) {
            return true;
        }
        else {
            return false;
        }
    }


    function cellForm(method, element, index, daysInMonth) {
        const dayOfMonth = (index + 1) % daysInMonth ? (index + 1) % daysInMonth : daysInMonth;
        const action = method === "post" ? "table_data/" : `${index}`;
        const can_add = has_perms()
        if (can_add) {
            return `<form action="${action}" id="${index}" method="${method}"><input type="hidden" name="csrfmiddlewaretoken" value="${mytoken}"><input name="data" value='${element.innerText}'><input type="hidden" name="date" value='${dayOfMonth}'><input type="hidden" name="data_type" value='${element.parentNode.querySelector(".table_type").textContent}'><input type="hidden" name="table" value='${element.closest("tbody[id]").id}'><input type="submit" style="position: absolute; left: -9999px"/></form>`
        }}

    function putInput(element, index) {
        const can_change = has_perms()
        if (can_change) {
            return `<input value="${element.innerText}" id="${index}"> <input type="hidden" name="csrfmiddlewaretoken" value="${mytoken}">`
        }}

    function sendPut(inputValue, index, inputId, CSRFtoken, dadElement) {

        const dayOfMonth = (index + 1) % 31;

        const table_id = dadElement.parentNode.parentElement.parentElement.id
        const day = dadElement.id


        fetch(`table_data/${inputId}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRFtoken
            },
            body: JSON.stringify({
                'x-csrf-token': CSRFtoken,
                'data': inputValue,
            }),
        }).then( function(response){
                if(!response.ok){
                    console.log(response.statusText)
                    dadElement.style.backgroundColor = '#FF0000';
                    dadElement.innerHTML = `<p id="${inputId}">${inputValue}$</p>`
                    dadElement.innerHTML += `<label for="${inputId}">Вводите только цифры!</label>`
                }}
        ).then(
            dadElement.innerHTML = `<p id="${inputId}">${inputValue}$</p>`,
        ).then(
            write_sum_to_table(+table_id, +day % 31, 31),
        )
    }

    for (let i = 0; i < a.length; i++) {
        a[i].setAttribute('id', i + 1);
        const has_perm = has_perms()
        if (has_perm){
        a[i].addEventListener('dblclick', () => {
            if (!a[i].innerText.trim()) {
                a[i].innerHTML = cellForm("post", a[i], i, 31);
            } else {
                const index = a[i].getElementsByTagName('p')[0].id;
                a[i].innerHTML = putInput(a[i], index);
                const inputElement = a[i].getElementsByTagName("INPUT")[0];
                const parentElement = inputElement.parentElement
                const inputId = inputElement.id;
                const token = a[i].getElementsByTagName('input')[1].value
                inputElement.addEventListener("keypress", (event) => {
                    if (event.code === "Enter") {
                        sendPut(inputElement.value, index, inputId, token, parentElement);
                    }
                })
            }
        });}
    }

    table_list = document.getElementsByClassName('table table-bordered')
    for (let i = 0; i < table_list.length; i++) {
        const operatorname = table_list[i].getElementsByTagName('tbody')[0].attributes[0].value
        table_list[i].parentElement.prepend(operatorname)
        days_list = table_list[i].getElementsByTagName('tfoot')
        for (let a of days_list) {
            const b = a.getElementsByTagName('th')
            for (let c of b){
                if (c.id){
                    write_sum_to_table(+i, +c.id, 31)
                }

            }

        }
    }

    function write_sum_to_table(table_id, day, daysInMonth) {
        const thWithoutId = 1;
        let sum = 0;
        let last_sum = 0;
        const table = document.querySelectorAll("table.table-bordered")[table_id];
        const sumCell = table.getElementsByTagName('tfoot')[0].getElementsByTagName('th')[day + thWithoutId];
        const lastCell = table.getElementsByTagName('tfoot')[0].getElementsByTagName('th')[32]; ///tyt nado menyat cufryposlednego dnya
        const cells = table.getElementsByClassName("day_of_month");
        for (let i of cells) {
            if (i.id % daysInMonth === 0) {
                const cellValue = +i.getElementsByTagName('p')[0]?.innerText.slice(0, -1).replace("$", "").replace(',', '.')
                if (cellValue) {
                    last_sum += cellValue
                    lastCell.innerHTML = `<p id=${i.id}> ${last_sum.toString().replace("$", "").replace(".", ",")}$</p>`
                }
                else{
                    sum += 0
                    lastCell.innerHTML = `<p id=${i.id}>${last_sum.toString().replace("$", "").replace(".", ",")}$</p>`
                }
            }
            if (i.id % daysInMonth === day) {
                const cellValue = +i.getElementsByTagName('p')[0]?.innerText.slice(0, -1).replace("$", "").replace(',', '.')
                if (cellValue) {
                    sum += cellValue
                    sumCell.innerHTML = `<p id=${i.id}>${sum.toString().replace(".", ",")}$</p>`
                } else {
                    sum += 0
                    sumCell.innerHTML = `<p id=${i.id}>${sum.toString().replace(".", ",")}$</p>`
                }
            }
        }}



