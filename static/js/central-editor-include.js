/**
 * Created by adamsimon on 11/22/16.
 * This loads one big editor into the center of the window.
 */

var cntrlEditor;

window.onbeforeunload = function () {
    if (cntrlEditor) {
        console.log('unload called and cntrlEditor found');
        cntrlCKEdit(section);
    }
};

// editor
function cntrlCKEdit(template_section, template, upload_url) {                 //// parameter upload_url
    console.log('cntrlEditor called; section: ' + template_section);

    var cntrl_container = document.getElementById('cntrl_editor_container'),
        cntrl_title = document.getElementById('cntrl_editor_title'),
        cntrl_orig_elmnt = document.getElementById('original_content_' + template_section),

        cntrl_edit_btn = document.getElementById('edit_btn_' + template_section),
        cntrl_save_btn = document.getElementById('save_btn_central'),
        cntrl_cancel_btn = document.getElementById('cancel_btn_central');

    if ($(cntrl_edit_btn).hasClass('btn-info')) {
        console.log('starting cntrlEditor; section: ' + template_section);

        if (cntrlEditor) {
            return;
        }

        $('.edit_btn_central').hide();
        $(cntrl_edit_btn).show();
        $(cntrl_cancel_btn).show();
        $(cntrl_title).text(template_section).show();
        $(cntrl_orig_elmnt).hide();

        cntrlEditor = CKEDITOR.appendTo(
            cntrl_container,
            ck_config_large,
            $(cntrl_orig_elmnt).text());

    } else { //Save

        if (!cntrlEditor) {
            return;
        }

        // Retrieve the editor contents. Ajax send to server.
        var cntrl_new_content = cntrlEditor.editable.getText();
        $(edit_element).html(cntrl_new_content);
        cntrlCKDestroy(template_section);
        $.ajax({
            type: "POST",
            url: upload_url,
            data: {
                'cntrl_new_content': template_section,
                'template_section': template_section,
                'template': template
            },
            success: function (serverResponse_data) {
                console.log('successfully posted:  ' + template_section + ' to: ' + template_section + ' -- ' + serverResponse_data);
                location.reload();
            }
        });
    }
}

function cntrlCKDestroy(template_section) {
    console.log('editor destroy; section: ' + template_section);

    var cntrl_title = document.getElementById('cntrl_editor_title'),
        cntrl_edit_btn = document.getElementById('edit_btn_' + template_section),
        cntrl_orig_elmnt = document.getElementById('original_content_' + template_section);

    if (!cntrlEditor) {
        return;
    }

    $(cntrl_orig_elmnt).show();
    $(cntrl_title).hide().text(' ');
    $(cntrl_cancel_btn).hide();
    $('.edit_btn_central').show();
    cntrlEditor.destroy();
    cntrlEditor = null;
}