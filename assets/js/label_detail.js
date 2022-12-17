function task_delete(task_id){
    $.ajax({
        type: 'delete',
        headers: {
            'X-CSRFToken': csrftoken
        },
        url: `/label-delete-edit/`+label_id,
        success: function(response) {
            
        },
        error: function(response) {
        }
    })
}
const form = document.getElementById('task-edit-form');

form.addEventListener('submit', task_edit);
                      

function task_edit(event){

    event.preventDefault();
    var title = 
    
    $.ajax({
        type: 'put',
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: ,
        url: `/label-delete-edit/`+label_id,
        success: function(response) {
            console.log(response)
            location.reload()
        },
        error: function(response) {
        }
    })}