/**
 * @license Copyright (c) 2003-2016, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:

    config.skin = 'moonocolor, ' +
        'https://joinourstory.com/static/ckeditor/skins/moonocolor/';
    config.toolbar = [
        {'name': 'clipboard', 'items': ['Undo', 'Redo', 'Cut', 'Copy', 'Paste']},
        {'name': 'styles', 'items': ['Font', 'FontSize']},
        {'name': 'basicstyles', 'items': ['Bold', 'Italic', 'Underline', 'Strike', '-', 'TextColor', 'BGColor']},
        {
            'name': 'paragraph',
            'items': ['JustifyLeft', 'JustifyCenter', 'JustifyRight']
        },
        {'name': 'insert', 'items': ['Image', 'Smiley']},
        {'name': 'editing', 'items': ['SelectAll', 'Find']}
    ];
    config.width = '100%';
    config.height = 650;
    config.tabSpaces = 4;
    config.toolbarRows = 1;
    config.fontSize_sizes = '14/14px;18/18px;24/24px;32/32px;42/42px;54/54px;';
    config.toolbarCanCollapse = false;
    config.removePlugins = 'liststyle, contextmenu,tabletools';
};
