$(document).ready(showCafeDetail);

let id = new URLSearchParams(location.search).get('id');


function showCafeDetail() {
    let id = new URLSearchParams(location.search).get('id');
    $.ajax({
        type: 'GET',
        url: '/api/cafe/detail/' + id,
        success: (response) => {
            let cafe_name = response['cafes']['cafe_name'];
            let cafe_info = response['cafes']['cafe_detail_info'];
            let address = response['cafes']['address'];
            let cafe_image = response['cafes']['cafe_image'];
            let reviews = response['reviews']
            let x = response['cafes']['cafe_x'];
            let y = response['cafes']['cafe_y'];
            let cafe_notice = response['cafes']['cafe_notice'];
            $('#address').text(address);
            $('.cafe-img').html(`<img src="../static/cafe_pics/${cafe_image}">`);
            $('#cafe-name').text(cafe_name);
            $('#info').text(cafe_info);
            $('#notice').text(cafe_notice);
            kakaoMapAPI(y, x);
            let scoreSum = 0;
            for (let i = 0; i < reviews.length; i++) {
                let user_id = reviews[i]['user_id']
                let cafe_rating = reviews[i]['cafe_rating']
                let cafe_review = reviews[i]['cafe_review']
                let create_date = reviews[i]['create_date']
                scoreSum += parseInt(cafe_rating);
                let temp_html = `<div class="card" >
                                    <div class="card-body">
                                         <div class="nicknameAndId">${user_id} ${cafe_rating}<div class="create-time">${create_date}</div></div>
                                         <div class="reviewContent">${cafe_review}</div>
                                    </div>
                                 </div>`
                $('#review').append(temp_html)
            }
            let rating = 0;
            if (reviews.length != 0) {
                rating = (scoreSum / reviews.length).toFixed(1);
                if (rating % 1 < 0.5) {
                    rating = Math.floor(rating);
                } else {
                    rating = Math.ceil(rating);
                }
            }
            $('.number-rating').text(rating.toFixed(1));
            $('#star').css('width', `${rating * 20}%`);
        }
    });
}

function kakaoMapAPI(x, y) {
    let container = document.getElementById('map');
    let options = { //지도를 생성할 때 필요한 기본 옵션
        center: new kakao.maps.LatLng(x, y), //지도의 중심좌표.
        level: 3 //지도의 레벨(확대, 축소 정도)
    };

    let map = new kakao.maps.Map(container, options);
    new kakao.maps.Marker({
        position: new kakao.maps.LatLng(x, y), // 마커의 좌표
        map: map // 마커를 표시할 지도 객체
    })
}

function regReview() {
    let id = new URLSearchParams(location.search).get('id');
    let cafe_rating = $('input[name=rating]:checked').val();
    let cafe_review = $('#input-cafe-review').val();

    $.ajax({
        type: "POST",
        url: "/api/cafe/regReview",
        data: {
            "cafe_idx_give": id,
            "cafe_rating_give": cafe_rating,
            "cafe_review_give": cafe_review,
        },
        success: function (response) {
            console.log(response);
            alert("리뷰를 등록했습니다.")
            window.location.replace("/cafe/detail?id=" + id)
        },
        error: (request, status, error) => {
            if (error == 'CONFLICT') {
                alert('이미 리뷰를 작성하였습니다.')
                window.location.replace("/cafe/detail?id=" + id)
            }
        }
    });
}

function goEventReg() {
    let id = new URLSearchParams(location.search).get('id');
    window.location.replace("/cafe/eventRegister?id=" + id)
}


