$(document).ready(() => {
    // showCafeManagement();
    makeDatepicker();
})

function showCafeManagement() {
    $.ajax({
        type: 'GET',
        url: '/api/cafe/management',
        data: {},
        success: function (response) {
            let cafe_id = response['cafe_id'];
            let user_id = response['user_id'];
            let start_date = response['start_date'];
            let end_date = response['end_date'];
            let event_category = response['event_category'];

            // todo eventsDB가 들어오면 추가로 완성할 예정
        }
    });
}

function regCustomDay(id) {
    let cafe_idx = id
    let custom_name = $('#input_custom_date_name').val()
    let custom_start_date = $('#startDate').val()
    let custom_end_date = $('#endDate').val()
    let custom_sales_flag = $('input[name=custom_sales_flag]:checked').val()
        if (custom_sales_flag == "closed") {
            // $("input[name=input_cost]").attr("readonly".true);
        }
    let cost = $('#input_custom_cost').val()
    let custom_cost = 0
    if (cost !== "") {
        custom_cost = parseInt(cost)
    }

    $.ajax({
        type: "POST",
        url: "/user/api/cafe/regCustomSchedule",
        data: {
            "cafe_idx_give": cafe_idx,
            "custom_name": custom_name,
            "custom_start_date": custom_start_date,
            "custom_end_date": custom_end_date,
            "custom_sales_flag": custom_sales_flag,
            "custom_cost": custom_cost
        },
        success: function (response) {
            alert("리뷰를 등록했습니다.")
            window.location.replace("/user/cafe/manage?id=" + cafe_idx)
        }
    });
}

function makeDatepicker() {
    $.datepicker.setDefaults($.datepicker.regional['ko']);
    $("#startDate").datepicker({
        nextText: '다음 달',
        prevText: '이전 달',
        dayNames: ['일요일', '월요일', '화요일', '수요일', '목요일', '금요일', '토요일'],
        dayNamesMin: ['일', '월', '화', '수', '목', '금', '토'],
        monthNamesShort: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
        monthNames: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
        dateFormat: "yy-mm-dd",
        onClose: function (selectedDate) {
            $("#endDate").datepicker("option", "minDate", selectedDate);
        }

    });
    $("#endDate").datepicker({
        nextText: '다음 달',
        prevText: '이전 달',
        dayNames: ['일요일', '월요일', '화요일', '수요일', '목요일', '금요일', '토요일'],
        dayNamesMin: ['일', '월', '화', '수', '목', '금', '토'],
        monthNamesShort: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
        monthNames: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
        dateFormat: "yy-mm-dd",
        onClose: function (selectedDate) {
            $("#startDate").datepicker("option", "maxDate", selectedDate);
        }

    });


    $(function () {
        $("#startDate, #endDate").datepicker();
    });
}


