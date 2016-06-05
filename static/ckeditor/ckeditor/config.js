/**
 * Copyright (c) 2003-2015, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
    config.skin = ['moono'];
    config.toolbar = [
        {'name': 'styles', 'items': ['Font', 'FontSize']},
        {'name':'clipboard', 'items': ['Undo', 'Redo', 'Cut', 'Copy', 'Paste']},
        {'name': 'basicstyles', 'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Smiley']},
        {'name': 'colors', 'items': ['TextColor', 'BGColor']},
        {'name': 'paragraph', 'items': ['NumberedList', 'BulletedList', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight']},
        {'name': 'editing', 'items': ['Find']}
    ];
    config.contentsCss = ['/static/ckeditor/ckeditor/contents.css'];
    config.disableNativeSpellChecker = False;
    config.tabSpaces = 4;
    config.removePlugins = 'elementspath, liststyle,tabletools,scayt,menubutton,contextmenu';
};