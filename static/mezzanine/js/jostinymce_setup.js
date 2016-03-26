
// Map Django language codes to valid TinyMCE language codes.
// There's an entry for every TinyMCE language that exists,
// so if a Django language code isn't here, we can default to en.

var language_codes = {
    'ar': 'ar',
    'ca': 'ca',
    'cs': 'cs',
    'da': 'da',
    'de': 'de',
    'es': 'es',
    'et': 'et',
    'fa': 'fa',
    'fa_IR': 'fa_IR',
    'fi': 'fi',
    'fr': 'fr_FR',
    'hr_HR': 'hr',
    'hu': 'hu_HU',
    'id_ID': 'id',
    'is_IS': 'is_IS',
    'it': 'it',
    'ja': 'ja',
    'ko': 'ko_KR',
    'lv': 'lv',
    'nb': 'nb_NO',
    'nl': 'nl',
    'pl': 'pl',
    'pt_BR': 'pt_BR',
    'pt_PT': 'pt_PT',
    'ru': 'ru',
    'sk': 'sk',
    'sr': 'sr_Latn',
    'sv': 'sv_SE',
    'tr': 'tr',
    'uk': 'uk_UA',
    'vi': 'vi',
    'zh_CN': 'zh_CN',
    'zh_TW': 'zh_TW'
};

function custom_file_browser(field_name, url, type, win) {
    tinyMCE.activeEditor.windowManager.open({
        title: 'Select ' + type + ' to insert',
        file: window.__filebrowser_url + '?pop=5&type=' + type,
        width: 800,
        height: 500,
        resizable: 'yes',
        scrollbars: 'yes',
        inline: 'yes',
        close_previous: 'no'
    }, {
        window: win,
        input: field_name
    });
    return false;
}

jQuery(function($) {

    if (typeof tinyMCE != 'undefined') {

        tinyMCE.init({ //Modified
            selector: "textarea.mceEditor",
            height: '700px',
            language: language_codes[window.__language_code] || 'en',
            plugins: [
                "advlist lists image charmap print preview",
                "searchreplace visualblocks code fullscreen",
                "insertdatetime textcolor paste"
            ],
            link_list: '/displayable_links.js',
            relative_urls: false,
            convert_urls: false,
            menubar: false,
            statusbar: false,
            toolbar: ("undo redo | bold italic underline strikethrough | charmap | " +
                      "alignleft aligncenter alignright | " + "forecolor backcolor | " +
                      "bullist numlist outdent indent | image visualblocks fullscreen"),
            file_browser_callback: custom_file_browser,
            content_css: window.__tinymce_css
        });

    }

});
