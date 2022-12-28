
function set_operator(){
    const new_operator_id = document.getElementsByName('valuable_operators')[0].value
    const client_id =  document.getElementsByName('client_id')[0].innerText
    fetch(`../client_api/${client_id}/set_operator/`, {
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