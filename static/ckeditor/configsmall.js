/**
 * @license Copyright (c) 2003-2016, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */


CKEDITOR.config.toolbar_Basic = [['Bold', 'Italic', 'Underline',
    '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', '-', 'Undo', 'Redo']];
CKEDITOR.config.toolbar = 'Basic';

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:

    config.skin = 'moonocolor, ' +
        'https://joinourstory.com/static/ckeditor/skins/moonocolor/';
    config.toolbar = [
        {'name': 'clipboard', 'items': ['Undo', 'Redo', 'Cut', 'Copy', 'Paste']}
    ];
    config.width = '100%';
    config.height = 175;
    config.tabSpaces = 4;
    config.toolbarRows = 1;
    config.toolbarCanCollapse = false;
    config.removePlugins = 'liststyle, contextmenu,tabletools';
};
