/**
 * Created by adamsimon on 11/22/16.
 * This editor is always available using a page's init function:
 * initJOSEditor(sctn, tlbr, eapurl, org_cntnt)
 */

var editors = {};

function initJOSEditor(sctn, tlbr, eapurl, org_cntnt) {
    editors[sctn] = {
        section: sctn, section_editor: null, toolbar: tlbr,
        editor_ajax_post_url: eapurl, original_content: org_cntnt, present_content: org_cntnt
    };
}

var ck_config_small = {
    toolbar: [
        {'name': 'clipboard', 'items': ['Undo', 'Redo', 'Cut', 'Copy', 'Paste']},
        {'name': 'editing', 'items': ['SelectAll', 'Find']}
    ],
    contentsCss: '/static/ckeditor/ckeditor/contents.css',
    disableNativeSpellChecker: false,
    width: '100%',
    height: 360,
    tabSpaces: 4,
    uiColor: '#28a4c9',
    removePlugins: 'liststyle,tabletools,scayt,contextmenu'
};

var ck_config_large = {
    toolbar: [
        {'name': 'clipboard', 'items': ['Undo', 'Redo', 'Cut', 'Copy', 'Paste']},
        {'name': 'styles', 'items': ['Font', 'FontSize']},
        {'name': 'basicstyles', 'items': ['Bold', 'Italic', 'Underline', 'Strike', '-', 'TextColor', 'BGColor']},
        {'name': 'paragraph', 'items': ['JustifyLeft', 'JustifyCenter', 'JustifyRight', '-', 'NumberedList', 'BulletedList']},
        {'name': 'insert', 'items': ['Image', 'Smiley']},
        {'name': 'editing', 'items': ['SelectAll', 'Find']}
    ],
    contentsCss: '/static/ckeditor/ckeditor/contents.css',
    width: '100%',
    height: 360,
    tabSpaces: 4,
    toolbarRows: 1,
    uiColor: '#28a4c9',
    extraPlugins: 'colorbutton',
    removePlugins: 'liststyle,tabletools,scayt,contextmenu'
};

window.onbeforeunload = function () {
    //// console.log('unload called');
    var lngth = Object.keys(editors).length;
    for (var i = 0; i < lngth; i++) {
        var section = Object.keys(editors)[i];
        if (editors[section].section_editor) {
            console.log('unload called; ckeditor found: ' + section + ' -- trying to save');
            josCKEdit(section);
        } else {
            //// console.log('ckeditor: ' + section + ' -- not found');
        }
    }
};

// editor
function josCKEdit(sect2edit) {
    console.log('editor called; section: ' + sect2edit);

    var ck_config = ck_config_small;
    if (editors[sect2edit].toolbar === 'large') {
        ck_config = ck_config_large;
    }

    var ck_editor_container = document.getElementById(sect2edit + '_editor_container'),
        edit_btn = document.getElementById(sect2edit + '_edit_btn'),
        edit_element = document.getElementById(sect2edit + '_original_content');

    //// console.log('edit_btn: ' + $(edit_btn).text());

    if ($(edit_btn).hasClass('btn-info')) {
        //// console.log('starting editor; editors[sect2edit].section_editor: ' + editors[sect2edit].section_editor);
        if (editors[sect2edit].section_editor) {
            return;
        }

        $(edit_btn).removeClass('btn-info').addClass('btn-success').text('Save').attr("data-original-title", "Saves changes");
        $('#' + sect2edit + '_cancel_btn').show();
        $(edit_element).hide();

        editors[sect2edit].section_editor = CKEDITOR.appendTo(
            ck_editor_container,
            ck_config,
            $(edit_element).html());

    } else { //Save

        //// console.log('trying to save');
        if (!editors[sect2edit].section_editor) {
            return;
        }

        // Retrieve the editor contents. Ajax send to server.

        var new_content = editors[sect2edit].section_editor.getData();
        $(edit_element).html(new_content);
        josCKDestroy(sect2edit);
        $.ajax({
            type: "POST",
            url: editors[sect2edit].editor_ajax_post_url,
            data: {
                'new_content': new_content,
                'section': sect2edit
            },
            success: function (serverResponse_data) {
                console.log('successfully posted:  ' + new_content + ' to: ' + sect2edit + ' -- ' + serverResponse_data);
                if (editors[sect2edit].editor_ajax_post_url.search('help') === -1) {
                    location.reload();
                }
            }
        });
    }
}


function josCKDestroy(sect2destroy) {
    console.log('editor destroy; section: ' + sect2destroy);

    var edit_element = document.getElementById(sect2destroy + '_original_content');
    var edit_btn = document.getElementById(sect2destroy + '_edit_btn');

    $(edit_element).show();
    $('#' + sect2destroy + '_cancel_btn').hide();
    $(edit_btn).removeClass('btn-success').addClass('btn-info').text('Edit ' + sect2destroy).attr("data-original-title", "Activates editor");
    editors[sect2destroy].section_editor.destroy();
    editors[sect2destroy].section_editor = null;

    //// console.log('destroyed editor - .section_editor: ' + editors[sect2destroy].section_editor);
}