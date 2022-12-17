function label_delete(task_id){
    $.ajax({
        type: 'delete',
        headers: {
            'X-CSRFToken': csrftoken
        },
        url: `/label-delete-edit/`+label_id,
        success: function(response) {
            var data = window.location.origin
            window.location.href = data;
        },
        error: function(response) {
        }
    })
}
                      

function label_edit(event){

    event.preventDefault();
    var title = $('#label-title').val()
    
    $.ajax({
        type: 'put',
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {'label_title':title},
        url: `/label-delete-edit/`+label_id,
        success: function(response) {
            var data = window.location.origin + '/label-task/' + response.slug
            window.location.href = data;
        },
        error: function(response) {
        }
    })}