var upload_text;

function init() {

}

function upload() {
    upload_text = $('textarea').val;
    
    setTimeout(() => {
        $('#textarea-parent').css({
            'height': '64px',
            'overflow': 'hidden'
        });
        $('.progress-bar').css({
            'display': ''
        });
        setTimeout(() => {
            $('#textarea-parent .input').css('display', 'none');
            $('#textarea-parent .progress-bar').css('display', '');
            $('.progress-bar').css({
                'opacity': 1
            });
            $('.progress-bar span').css({
                'width': '50%',
                'display': '',
                'opacity': 1
            });
            setTimeout(() => {
                upload_complete();
            }, 600);
        }, 610);
        
    }, 16);
}

function upload_complete() {
    $('.progress-bar span').css('width', '100%');
    $('.textarea').css('height', '40%');
    setTimeout(() => {
        $('.progress-bar').css({
            'opacity': 0
        });
        $('.textarea .after-upload').css({
            'display': ''
        });
        setTimeout(() => {
            $('.textarea .after-upload').css({
                'opacity': 1
            });
        }, 310);
    }, 310);
}