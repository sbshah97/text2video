var upload_text;
var user_id;
var file;

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
            console.log(file);
            if (file) {
                document.getElementById('upload_form').submit();
                upload_complete();
                return;
            }
            // _data = {
            //     id: user_id,
            //     text: $('#textarea').val()
            // }
            // console.log("ad", _data);
            // $.ajax({
            //     type: 'POST',
            //     url: '/try',
            //     success: function (result) {
            //         if (result == 'Success')
            //             upload_complete()
            //     },
            //     error: function (err) {
            //         console.log(err);
            //     },
            //     data: _data
            // })
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

function register() {
    _data = {
        username: $('#username').val(),
        password: $('#password').val()
    }
    console.log("ad",  _data);
    $.ajax({
        type: 'POST',
        url: '/user_register',
        success: function(result) {
            console.log("ad",  result);
            window.location='login.html';
        },
        error: function(err) {
            console.log(err);
        },
        data: _data
    })
}


function login() {
    _data = {
        username: $('#username').val(),
        password: $('#password').val()
    }
    console.log("ad", _data);
    $.ajax({
        type: 'POST',
        url: '/user_login',
        success: function (result) {
            if (result != 'Fail')
                window.location = 'main.html?id='+result;
        },
        error: function (err) {
            console.log(err);
        },
        data: _data
    })
}


function getVideos() {
    _data = {
        id: user_id
    }
    console.log(_data);
    $.ajax({
        type: 'POST',
        url: '/get_videos',
        success: function (result) {
            console.log(result);
            r = JSON.parse(result);
            console.log(r)
            if (r.length <= 0) {
                console.log("as")
                $('.video-list').html('No videos!!! <a class="link" href="try.html?user_id=' + user_id + '">Try it Out!!!</a>');
                return;
            }
            for(i in r){
                video = r[i]
                console.log(video['time'])
                date = new Date(video['time'])
                console.log(date)
                $('.video-list').append(`
                    <a href="/fetch_video?v=${video['video_file']}" target="_blank">
                        <li>
                            <time>
                                <i class="material-icons">play_circle_outline</i>
                                ${date.toString()}
                            </time>
                            <a id="summary-link" href="${video['summary_file']}" target="_blank">Summary</a>
                            <a id="question-link" href="${video['q_file']}" target="_blank">Questionnaire</a>
                        </li>
                    </a>
                `);
            }
        },
        error: function (err) {
            console.log(err);
        },
        data: _data
    })
}