/**
 * Created by adamsimon on 6/12/16.
 */


var currentEditor;

function activateCKEdit(section) {

    currentEditor = CKEDITOR.replace(section, {
        toolbar: [
            {'name': 'clipboard', 'items': ['Undo', 'Redo', 'Cut', 'Copy', 'Paste']},
            {'name': 'styles', 'items': ['Font', 'FontSize']},
            {'name': 'basicstyles', 'items': ['Bold', 'Italic', 'Underline', 'Strike', '-', 'TextColor', 'BGColor']},
            {
                'name': 'paragraph',
                'items': ['JustifyLeft', 'JustifyCenter', 'JustifyRight', '-', 'NumberedList', 'BulletedList']
            },
            {'name': 'insert', 'items': ['Image', 'Smiley']},
            {'name': 'editing', 'items': ['SelectAll', 'Find']}
        ],
        contentsCss: '/static/ckeditor/ckeditor/contents.css',
        disableNativeSpellChecker: false,
        width: '95%',
        tabSpaces: 4,
        uiColor: '#28a4c9',
        removePlugins: 'liststyle,tabletools,scayt,contextmenu',
        extraPlugins: 'colorbutton'
    });

}


function handleCKEdit(el) {
    var elstrid = '#' + el.id;
    var pos = elstrid.search("_");
    var section = elstrid.slice(pos + 1);
    var acttxt = elstrid.slice(1, pos);
    // alert(section);

    switch (acttxt) {

        case "edit":
            $("#editing_side_panel").addClass('hidden');
            $("#editing_side_panel_hint").removeClass('hidden');
            $('.edit_section_button').hide();
            $('.joshint').show();
            $('#save_' + section).show();
            $('#discard_' + section).show();
            $('.edit_border_class').removeClass('edit_border');
            $('#border_' + section).addClass('edit_border_active');
            activateCKEdit(section);
            break;

        case "save":

            var data = currentEditor.editable().getData();
            // alert(data);
            $('#' + section + '_holder').val(data);
            var save_confirm = $.confirm({
                cancelButton: 'Save changes',
                cancelButtonClass: 'btn-default',
                confirmButton: 'Cancel',
                confirmButtonClass: 'btn-warning',
                content: 'Do you want to save recent changes?',
                confirm: function () {
                    save_confirm.close()
                },
                cancel: function () {
                    $('#hint').hide();
                    $('#' + section + '_form').submit();
                }
            });
            break;

        case "discard":

            var discard_confirm = $.confirm({
                cancelButton: 'Discard changes',
                cancelButtonClass: 'btn-default',
                confirmButton: 'Cancel',
                confirmButtonClass: 'btn-warning',
                content: 'Do you want to discard recent changes?',
                confirm: function () {
                    discard_confirm.close()
                },
                cancel: function () {
                    location.reload();

                }
            });
            break;

    }
}