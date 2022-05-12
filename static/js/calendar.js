$(document).ready(buildCalendar);

var today = new Date(); // @param 전역 변수, 오늘 날짜 / 내 컴퓨터 로컬을 기준으로 today에 Date 객체를 넣어줌
var date = new Date();  // @param 전역 변수, today의 Date를 세어주는 역할
var monthEventMap, monthCustomMap;

function prevCalendar() {
    today = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());
    buildCalendar();
}

function nextCalendar() {
    today = new Date(today.getFullYear(), today.getMonth() + 1, today.getDate());
    buildCalendar();
}

function buildCalendar() {

    let doMonth = new Date(today.getFullYear(), today.getMonth(), 1);
    let lastDate = new Date(today.getFullYear(), today.getMonth() + 1, 0);

    let tbCalendar = document.querySelector(".scriptCalendar > tbody");

    document.getElementById("calYear").innerText = today.getFullYear();                       // @param YYYY월
    document.getElementById("calMonth").innerText = autoLeftPad((today.getMonth() + 1), 2);   // @param MM월

    makeMonthMap();

    while (tbCalendar.rows.length > 0) {
        tbCalendar.deleteRow(tbCalendar.rows.length - 1);
    }

    let row = tbCalendar.insertRow();

    let dom = 1;

    let daysLength = (Math.ceil((doMonth.getDay() + lastDate.getDate()) / 7) * 7) - doMonth.getDay();

    for (let day = 1 - doMonth.getDay(); daysLength >= day; day++) {

        let column = row.insertCell();
        // @param 평일( 전월일과 익월일의 데이터 제외 )
        if (Math.sign(day) == 1 && lastDate.getDate() >= day) {
            // @param 평일 날짜 데이터 삽입
            column.innerText = autoLeftPad(day, 2);

            // @param 일요일인 경우
            if (dom % 7 == 1) {
                column.style.color = "#FF4D4D";
            }
            // @param 토요일인 경우
            if (dom % 7 == 0) {
                column.style.color = "#8A2BE2";
                row = tbCalendar.insertRow();   // @param 토요일이 지나면 다시 가로 행을 한줄 추가한다.
            }
        }
        // @param 평일 전월일과 익월일의 데이터 날짜변경
        else {
            let exceptDay = new Date(doMonth.getFullYear(), doMonth.getMonth(), day);
            column.innerText = autoLeftPad(exceptDay.getDate(), 2);
            column.style.color = "#937DDB";
        }

        // @brief   전월, 명월 음영처리
        // @details 현재년과 선택 년도가 같은경우
        if (today.getFullYear() == date.getFullYear()) {
            // @details 현재월과 선택월이 같은경우
            if (today.getMonth() == date.getMonth()) {
                // @details 현재일보다 이전인 경우이면서 현재월에 포함되는 일인경우
                if (date.getDate() > day && Math.sign(day) == 1) {
                    setPossibleDay(column);
                }
                // @details 현재일보다 이후이면서 현재월에 포함되는 일인경우
                else if (date.getDate() < day && lastDate.getDate() >= day) {
                    setPossibleDay(column);
                }
                // @details 현재일인 경우
                else if (date.getDate() == day) {
                    setPossibleDay(column);
                }
                // @details 현재월보다 이전인경우
            } else if (today.getMonth() < date.getMonth()) {
                if (Math.sign(day) == 1 && day <= lastDate.getDate()) {
                    setPossibleDay(column);
                }
            }
            // @details 현재월보다 이후인경우
            else {
                if (Math.sign(day) == 1 && day <= lastDate.getDate()) {
                    setPossibleDay(column);
                }
            }
        }
        // @details 선택한년도가 현재년도보다 작은경우
        else if (today.getFullYear() < date.getFullYear()) {
            if (Math.sign(day) == 1 && day <= lastDate.getDate()) {
                setPossibleDay(column);
            }
        }
        // @details 선택한년도가 현재년도보다 큰경우
        else {
            if (Math.sign(day) == 1 && day <= lastDate.getDate()) {
                setPossibleDay(column);
            }
        }
        dom++;
    }
}

function calendarChoiceDay(column) {
    column.style.backgroundColor = "#FF9999";
    column.setAttribute('data-toggle', 'modal');
    column.setAttribute('data-target', '#myModal');

    $('.modal-body').empty()
    let key = makeMonthMapKey(column);

    let custom = monthCustomMap.get(key);
    if (monthCustomMap.has(key) && custom['custom_sales_flag'] == 'closed') {
        let custom_name = custom['custom_name']
        $('#reservation-flag').text('금일은 휴무 입니다.')
        let tempHtml = `<div class="wrap-modal">
                            <div class="kind">휴무 사유 :</div>
                            <div id="modal-category">${custom_name}</div>
                        </div>
                        `;
        $('.modal-body').append(tempHtml);
        return;
    }

    if (!monthEventMap.has(key)) {
        $('.modal-body').text('등록된 일정이 없습니다.')
        return;
    }

    let event = monthEventMap.get(key);
    let event_category = event['event_category']
    let event_name = event['event_name']
    let event_info = event['event_info']
    let tempHtml = `<div class="wrap-modal">
                        <div class="kind">카테고리 : </div>
                        <div id="modal-category">${event_category}</div>
                    </div>
                    <div class="wrap-modal">
                        <div class="kind">이벤트명 : </div>
                        <div id="modal-event-name">${event_name}</div>
                    </div>
                    <div class="wrap-modal">
                        <div class="kind">이벤트 설명 : </div>
                        <div id="modal-event-info">${event_info}</div>
                    </div>`;
    $('.modal-body').append(tempHtml)
}

function autoLeftPad(num, digit) {
    if (String(num).length < digit) {
        num = new Array(digit - String(num).length + 1).join("0") + num;
    }
    return num;
}

function makeMonthMap() {
    let month = parseInt($('#calMonth').text());
    let year = $('#calYear').text();
    let cafe_id = new URLSearchParams(location.search).get('id');
    $.ajax({
        type: 'GET',
        url: '/api/event/' + cafe_id,
        async: false,
        data: {
            'year': year,
            'month': month,
        },
        success: (response) => {
            monthEventMap = new Map();
            monthCustomMap = new Map();
            let events = response['month_event_list'];
            if (events !== undefined)
                events.forEach((event) => {
                    let date = new Date(event['date']).toISOString().substring(0, 10)
                    monthEventMap.set(date, event)
                })
            let customs = response['month_custom_list'];
            if (customs !== undefined)
                customs.forEach((custom) => {
                    let date = new Date(custom['date']).toISOString().substring(0, 10)
                    monthCustomMap.set(date, custom)
                })
        }
    })
}

function makeMonthMapKey(column) {
    let day = column.innerText;
    let month = $('#calMonth').text();
    let year = $('#calYear').text();
    return year + '-' + month + '-' + day;
}

function getAreaColor(column) {
    let key = makeMonthMapKey(column);
    let color;
    if(monthEventMap.has(key)){
        color = 'skyblue'
    }else if(monthCustomMap.has(key) && monthCustomMap.get(key)['custom_sales_flag']=='closed'){
        color = '#FF9999'
    }else{
        color = '#E6E6FA'
    }
    return color;
}

function setPossibleDay(column) {
    let color = getAreaColor(column)
    column.style.backgroundColor = color;
    column.style.cursor = "pointer";

    column.addEventListener('mouseover', () => {
        column.style.backgroundColor = "mediumpurple";
    });
    column.addEventListener('mouseout', () => {
        column.style.backgroundColor = color;
    });

    column.onclick = function () {
        calendarChoiceDay(this);
    }
}
