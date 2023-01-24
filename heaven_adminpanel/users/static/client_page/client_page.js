

document.getElementsByName('valuable_operators')[0].setAttribute('class', 'form-select')
document.getElementsByName('valuable_promo')[0].setAttribute('class', 'form-select')
document.getElementsByName('valuable_project_manager')[0].setAttribute('class', 'form-select')


function set_operator(){
    const new_operator_id = document.getElementsByName('valuable_operators')[0].value
    const client_id =  document.getElementsByName('client_id')[0].innerText
    fetch(`../client_api/${client_id}/set_manager/`,  {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': mytoken
            },
            body: JSON.stringify({
                'x-csrf-token': mytoken ,
                'data': new_operator_id,
            }),
        }).then(
            console.log('vse zaebis')
    )
}

function set_promo(){
    const new_promo_id = document.getElementsByName('valuable_promo')[0].value
    const client_id =  document.getElementsByName('client_id')[0].innerText
    fetch(`../client_api/${client_id}/set_manager/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': mytoken
            },
            body: JSON.stringify({
                'x-csrf-token': mytoken ,
                'data': new_promo_id,
            }),
        }).then(
            console.log('vse zaebis')
    )
}


function set_project_manager(){
    const new_project_id = document.getElementsByName('valuable_project_manager')[0].value
    const client_id =  document.getElementsByName('client_id')[0].innerText
    fetch(`../client_api/${client_id}/set_manager/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': mytoken
            },
            body: JSON.stringify({
                'x-csrf-token': mytoken ,
                'data': new_project_id,
            }),
        }).then(
            console.log('vse zaebis')
    )
}
