/**
 * Created by adamsimon on 11/22/16.
 * This loads an editor into the center of the window.
 */

var centralEditor;

window.onbeforeunload = function () {
    if (centralEditor) {
        preventDefault();
        console.log('unload called and centralEditor found');
        alert('Please save or discard your edits');
    }
};

// editor
function centralCKEditStart(central_section2edit) {
    console.log('start called; central_section2edit: ' + central_section2edit);

    var edit_bucket = document.getElementById('edit_bucket'),
        central_editor_container = document.getElementById('central_editor_container'),
        central_title = document.getElementById('central_editor_title');

    var central_orig_elmnt = document.getElementById('original_content_' + central_section2edit);
    var orig_text = $(central_orig_elmnt).text();

    console.log('central_orig_elmnt: ' + central_orig_elmnt.id);
    console.log('central_editor_container: ' + central_editor_container);


    if (centralEditor) {
        console.log('return on exist');
        return;
    }

    centralEditor = CKEDITOR.appendTo(
        central_editor_container, ck_config_small, orig_text);

    $(central_title).text('Editing ' + central_section2edit);
    $(edit_bucket).show();

}

function centralCKEditSave(sw_template, upload_url) {

    if (!centralEditor) {
        return;
    }
    var central_title = document.getElementById('central_editor_title'),
        central_sect2save = $(central_title).text().split(' ')[1];
    
    console.log('save called; central_sect2save: ' + central_sect2save);
    console.log('url: ' + upload_url);
    console.log('sw_template: ' + sw_template);

    // Retrieve the editor contents, then ajax to server.
    var html_content = centralEditor.getData();
    var central_new_content = $(html_content).text();

    $.ajax({
        type: "POST",
        url: upload_url,
        data: {
            'central_new_content': central_new_content,
            'template_section': central_sect2save,
            'sw_template': sw_template
        },

        success: function (serverResponse_data) {
            console.log(serverResponse_data + ', successfully posted:  ' + central_new_content + ', template_section: ' + central_sect2save);

            centralCKDestroy();
            location.reload();
        }
    });
}

function centralCKDestroy() {

    var edit_bucket = document.getElementById('edit_bucket'),
        central_title = document.getElementById('central_editor_title'),
        central_sect2destroy = $(central_title).text().split(' ')[1];

    console.log('destroy called; central_sect2destroy: ' + central_sect2destroy);

    if (!centralEditor) {
        return;
    }

    $(edit_bucket).hide();

    centralEditor.destroy();
    centralEditor = null;
}