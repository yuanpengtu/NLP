jQuery(function ($) {
    let input = $('#form-field-input');
    let output = $('#form-field-output');

    autosize($('textarea[class*=autosize]'));
    // $(".knob").knob();


    $(document).one('ajaxloadstart.page', function (e) {
        autosize.destroy('textarea[class*=autosize]');
    });

    $('#submit').on("click", function () {
        if (input.val() === "") {
            swal({
                title: '请输入文本',
                type: 'info',
                confirmButtonColor: '#3085d6',
                confirmButtonText: '确定',
            }).then(function () {
                window.location.href = "/";
            });
        } else {
            let data = new FormData();
            data.append("input", input.val());
            $.ajax({
                url: "/sentiment_analysis",
                type: "POST",
                data: data,
                processData: false,
                contentType: false,
                success: function (return_data) {
                    swal({
                        title: '分析成功',
                        type: 'success',
                        confirmButtonColor: '#3085d6',
                        confirmButtonText: '确定',
                    }).then(function () {
                        // do nothing
                    });
                    // console.log(return_data);
                    let msg = JSON.parse(return_data);
                    output.val(msg['message']);
                }
            });
        }
    });

    $('#reset').on("click", function () {
        input.val("");
        output.val("");
    });

});