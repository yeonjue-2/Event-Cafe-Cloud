$(document).ready(showCafeDetail);
function showCafeDetail(){
    let id = new URLSearchParams(location.search).get('id');
    $.ajax({
        type:'GET',
        url:'/api/cafe/detail/'+id,
        success:(response)=>{
            let cafe_id = response['cafe_id'];
            let cafe_name = response['cafe_name'];
            let cafe_info = response['cafe_info'];
            let address = response['address'];
            let cafe_image = response['cafe_image'];
            // let reviews = response['reviews'];
            let x = response['x'];
            let y = response['y'];
            $('#cafe-name').text(cafe_name);
            $('#info').text(cafe_info);
            kakaoMapAPI(x,y);
        }

    })
}
function kakaoMapAPI(x, y) {
    let container = document.getElementById('map');
    let options = { //지도를 생성할 때 필요한 기본 옵션
        center: new kakao.maps.LatLng(x, y), //지도의 중심좌표.
        level: 3 //지도의 레벨(확대, 축소 정도)
    };
    new kakao.maps.Map(container, options);
}

