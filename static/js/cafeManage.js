$(document).ready(()=>{
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

function regCustomDay(idx) {
    let cafe_idx = idx
    let custom_name = $('#input_custom_date_name').val()
    let custom_start_date = $('#datepicker1').val()
    let custom_end_date = $('#datepicker2').val()
    let custom_sales_flag = $('input[name=custom_sales_flag]:checked').val()
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
            window.location.replace("/user/cafe/manage/" + cafe_idx)
        }
    });
}

function makeDatepicker() {
    $.datepicker.setDefaults({
        dateFormat: 'yy-mm-dd',
        prevText: '이전 달',
        nextText: '다음 달',
        monthNames: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
        monthNamesShort: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
        dayNames: ['일', '월', '화', '수', '목', '금', '토'],
        dayNamesShort: ['일', '월', '화', '수', '목', '금', '토'],
        dayNamesMin: ['일', '월', '화', '수', '목', '금', '토'],
        showMonthAfterYear: true,
        yearSuffix: '년'
    });

    $(function () {
        $("#datepicker1, #datepicker2").datepicker();
    });
}


