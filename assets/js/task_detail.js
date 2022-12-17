function task_delete(task_id){
    $.ajax({
        type: 'delete',
        headers: {
            'X-CSRFToken': csrftoken
        },
        url: `/task-delete-edit/`+task_id,
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
    var title = $('#edit-title').val()
    var note = $('#edit-description').val()
    var reminds_on = $('#edit-reminds-on').val()
    var archive = $('#edit-archive').val()
    var completed = $('#edit-complete').val()
    var label = $('#edit-label-select').find(":selected").val();
    console.log(title, note, reminds_on, archive, completed)
    
    // $.ajax({
    //     type: 'put',
    //     headers: {
    //         'X-CSRFToken': csrftoken
    //     },
    //     data: ,
    //     url: `/task-delete-edit/`+task_id,
    //     success: function(response) {
    //         console.log(response)
    //         location.reload()
    //     },
    //     error: function(response) {
    //     }
    // })
}