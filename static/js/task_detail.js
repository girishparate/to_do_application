console.log(task_archive)
if (task_archive == 'True')
{
    $( "#edit-archive").prop('checked', true);
}
else
{
    $( "#edit-archive").prop('checked', false);
}

if (task_complete == 'True')
{
    $( "#edit-complete").prop('checked', true);
}
else
{
    $( "#edit-complete").prop('checked', false);
}

if (task_reminder == 'True')
{
    $( "#edit-reminder").prop('checked', true);
}
else
{
    $( "#edit-reminder").prop('checked', false);
}

function task_delete(task_id){
    $.ajax({
        type: 'delete',
        headers: {
            'X-CSRFToken': csrftoken
        },
        url: `/task-delete-edit/`+task_id,
        success: function(response) {
            var data = window.location.origin
            window.location.href = data;
        },
        error: function(response) {
        }
    })
}

function task_edit(event){

    event.preventDefault();
    var title = $('#edit-title').val()
    var note = $('#edit-description').val()
    var reminds_on = $('#edit-reminds-on').val()
    var label = $("#edit-label-select").val();
    var image = $('#edit-image').val()

    if ($('#edit-reminder').is(":checked") == true)
    {
        completed = 'on'
    }else{
        completed = 'off'
    }

    if ($('#edit-complete').is(":checked") == true)
    {
        completed = 'on'
    }else{
        completed = 'off'
    }

    if ($('#edit-archive').is(":checked") == true)
    {
        archive = 'on'
    }else{
        archive = 'off'
    }
    data = {
        'title':title,
        'note':note,
        'reminds_on':reminds_on,
        'archive':archive,
        'completed':completed,
        'label':label,
        'reminds_on':reminds_on,
        'image':image
     }
    
    $.ajax({
        type: 'put',
        headers: {
            'X-CSRFToken': csrftoken
        },
        enctype: "multipart/form-data",
        data: data,
        url: `/task-delete-edit/`+task_id,
        success: function(response) {

            var data = window.location.origin + '/task-details/' + response.slug
            window.location.href = data;
        },
        error: function(response) {
        }
    })
}