/**
 * Created by adamsimon on 11/22/16.
 * This editor is always available using a page's init function:
 * initJOSEditor(sctn, tlbr, eapurl, org_cntnt)
 */

var editors = {};

function initJOSEditor(sctn, tlbr, eapurl, org_cntnt) {
    // console.log('sctn: ' + sctn + ', org_cntnt: ' + org_cntnt);
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
    height: 309,
    tabSpaces: 4,
    uiColor: '#ffff00',
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
    height: 650,
    tabSpaces: 4,
    toolbarRows: 1,
    uiColor: '#ffff00',
    extraPlugins: 'colorbutton',
    removePlugins: 'liststyle,tabletools,scayt,contextmenu'
};

window.onbeforeunload = function () {
    //// console.log('unload called');
    var lngth = Object.keys(editors).length;
    for (var i = 0; i < lngth; i++) {
        var section = Object.keys(editors)[i];
        if (editors[section].section_editor && editors[section].section === 'notes') {
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
        segment_element = document.getElementById(sect2edit + '_original_content');

    // console.log('ck_editor_container: ' + ck_editor_container.id + ', edit_btn.text: ' + $(edit_btn).text());


    if ($(edit_btn).hasClass('j_action_button') || sect2edit.search('story') !== -1) {

        if (sect2edit.search('story') === -1) {
            var data_original_title_string = 'Updates ' + sect2edit;
            var edit_button_html = "<i class = 'fa fa-arrow-circle-up fa-fw'></i>SAVE " + sect2edit.toUpperCase();
            $(edit_btn).removeClass('j_action_button').addClass('j_save_button').html(edit_button_html).attr("data-original-title", data_original_title_string);
            $('#' + sect2edit + '_cancel_btn').show();
            $(segment_element).hide();
        }

        if (editors[sect2edit].section_editor) {
            return;
        }

        editors[sect2edit].section_editor = CKEDITOR.appendTo(
            ck_editor_container,
            ck_config,
            editors[sect2edit].original_content);

        // console.log('started editor; .section_editor: ' + editors[sect2edit].section_editor);

    } else { //Save

        josCKSave(sect2edit);
    }
}

function josCKSave(sect2save) {
    console.log('trying to save');
    if (!editors[sect2save].section_editor) {
        return;
    }

    // Retrieve the editor contents. Ajax send to server.
    var segment_element = document.getElementById(sect2save + '_original_content');
    var new_content = editors[sect2save].section_editor.getData();

    editors[sect2save].original_content = new_content;

    if (sect2save.search('story') === -1) {
        $(segment_element).html(new_content);
        josCKDestroy(sect2save);
    }

    $.ajax({
        type: "POST",
        url: editors[sect2save].editor_ajax_post_url,
        data: {
            'new_content': new_content,
            'section': sect2save
        },
        success: function (serverResponse_data) {
            console.log('successfully posted:  ' + new_content + ' to: ' + sect2save + ' -- ' + serverResponse_data);
            if (editors[sect2save].editor_ajax_post_url.search('help') === -1 || sect2edit.search('story') != -1 ) {
                location.reload();
            }
        }
    });
}


function josCKDestroy(sect2destroy) {
    console.log('editor destroy; section: ' + sect2destroy);

    var segment_element = document.getElementById(sect2destroy + '_original_content');
    var edit_btn = document.getElementById(sect2destroy + '_edit_btn');

    $(segment_element).show();
    $('#' + sect2destroy + '_cancel_btn').hide();
    $(edit_btn)
        .removeClass('j_save_button')
        .addClass('j_action_button')
        .text('EDIT ' + sect2destroy.toUpperCase()).attr("data-original-title", "Activates editor");
    editors[sect2destroy].section_editor.destroy();
    editors[sect2destroy].section_editor = null;

    //// console.log('destroyed editor - .section_editor: ' + editors[sect2destroy].section_editor);
}