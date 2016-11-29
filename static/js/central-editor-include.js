/**
 * Created by adamsimon on 11/22/16.
 * This loads an editor into the center of the window.
 */

var cntrlEditor;

var edit_bucket = document.getElementById('edit_bucket'),
    cntrl_editor_container = document.getElementById('cntrl_editor_container'),
    cntrl_title = document.getElementById('cntrl_editor_title');
    // cntrl_save_btn = document.getElementById('save_btn_central'),
    // cntrl_cancel_btn = document.getElementById('cancel_btn_central');

window.onbeforeunload = function () {
    if (cntrlEditor) {
        preventDefault();
        console.log('unload called and cntrlEditor found');
        alert('Please save or discard your edits');
    }
};

// editor
function cntrlCKEditStart(cntrl_section2edit) {
    console.log('start called; cntrl_section2edit: ' + cntrl_section2edit);

    var cntrl_orig_elmnt = document.getElementById('original_content_' + cntrl_section2edit);

    var orig_text = $(cntrl_orig_elmnt).text();

    if (cntrlEditor) {
        return;
    }

    $('.edit_btn_central').hide();
    $('.template_row').hide();
    $('#edit_mode_button').hide();
    $('#background_image').css({opacity: 0.1});

    cntrlEditor = CKEDITOR.appendTo(
        cntrl_editor_container, ck_config_small, orig_text);

    $(cntrl_title).text('Editing ' + cntrl_section2edit);
    $(edit_bucket).show();

}

function cntrlCKEditSave(sw_template, upload_url) {

    if (!cntrlEditor) {
        return;
    }

    var cntrl_sect2save = $(cntrl_title).text().split(' ')[1];

    console.log('save called; cntrl_sect2save: ' + cntrl_sect2save);
    console.log('cntrlEditor: ' + cntrlEditor);

    // Retrieve the editor contents, then ajax to server.
    var html_new = cntrlEditor.getData();
    var cntrl_new_content = $(html_new).text();

    $.ajax({
        type: "POST",
        url: upload_url,
        data: {
            'cntrl_new_content': cntrl_new_content,
            'template_section': cntrl_sect2save,
            'sw_template': sw_template
        },

        success: function (serverResponse_data) {
            console.log('successfully posted:  ' + cntrl_new_content + ' -- ' + serverResponse_data);

            cntrlCKDestroy();
            location.reload();
        }
    });
}

function cntrlCKDestroy() {

    var cntrl_sect2destroy = $(cntrl_title).text().split(' ')[1];

    console.log('destroy called; cntrl_sect2destroy: ' + cntrl_sect2destroy);

    if (!cntrlEditor) {
        return;
    }

    $('.edit_btn_central').show();
    $('.template_row').show();
    $('#edit_mode_button').show();
    $('#background_image').css({opacity: 1});

    $(cntrl_title).text(' ');
    $(edit_bucket).hide();

    cntrlEditor.destroy();
    cntrlEditor = null;
}