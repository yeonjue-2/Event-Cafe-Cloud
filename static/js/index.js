
function toggle_heart(cafe_idx, type) {
    if ($.cookie("jwt_token") === undefined) {
        alert("로그인 후 이용해주세요")
        return
    }
    let $a_heart = $(`#${cafe_idx} a[aria-label='${type}']`);
    let $i_heart = $a_heart.find("i");
    let full_icons = {"heart": "fa-heart", "bookmark": "fa-bookmark"};
    let empty_icons = {"heart": "fa-heart-o", "bookmark": "fa-bookmark-o"};

    if ($i_heart.hasClass(full_icons[type])) {
        $.ajax({
            type: "POST",
            url: "/update_heart",
            data: {
                cafe_idx_give: cafe_idx,
                type_give: type,
                action_give: "unheart"
            },
            success: function (response) {
                $i_heart.addClass(empty_icons[type]).removeClass(full_icons[type])
                $a_heart.find("span.heart-num").text(num2str(response["count"]))
            }
        })
    } else {
        $.ajax({
            type: "POST",
            url: "/update_heart",
            data: {
                cafe_idx_give: cafe_idx,
                type_give: type,
                action_give: "heart"
            },
            success: function (response) {
                $i_heart.addClass(full_icons[type]).removeClass(empty_icons[type])
                $a_heart.find("span.heart-num").text(num2str(response["count"]))
            }
        });
    }
}

function num2str(count) {
    if (count > 10000) {
        return parseInt(count / 1000) + "k"
    }
    if (count > 500) {
        return parseInt(count / 100) / 10 + "k"
    }
    if (count == 0) {
        return ""
    }
    return count
}

function listing() {

    $("#cards-box").empty()
    $.ajax({
        type: "GET",
        url: `/listing`,
        data: {},
        success: function (response) {
            let cafes = response['cafes']
            for (let i = 0; i < cafes.length; i++) {
                let cafe_id = cafes[i]['cafe_id']
                let cafe_image = cafes[i]['cafe_image']
                let cafe_name = cafes[i]['cafe_name']
                let cafe_short_info = cafes[i]['cafe_short_info']
                let class_heart = cafes[i]['heart_by_me'] ? "fa-heart" : "fa-heart-o"
                let count_heart = cafes[i]['count_heart']
                let class_bookmark = cafes[i]['bookmark_by_me'] ? "fa-bookmark" : "fa-bookmark-o"

                let temp_html = `<div class="card" id="${cafe_id}" style="width: 18rem; border-radius: 10px;">
                                        <img class="card-img-top" src="../static/cafe_pics/${cafe_image}" alt="Card image cap">
                                        <div class="card-body">
                                            <h3 class="card-title">${cafe_name}&nbsp;&nbsp;<a class="level-item is-sparta" aria-label="bookmark" onclick="toggle_heart('${cafe_id}', 'bookmark')" style="color: dodgerblue">
                                                <span class="icon is-small"><i class="fa ${class_bookmark}" aria-hidden="true"></i></span></a>
                                            </h3>
                                            <p class="card-text">${cafe_short_info}</p>
                                            <nav class="level is-mobile">
                                                <div class="level-left">
                                                        <a class="level-item is-sparta" aria-label="heart" style="color:#F5C0BE" onclick="toggle_heart('${cafe_id}', 'heart')">
                                                            <span class="icon is-small"><i class="fa ${class_heart}" aria-hidden="true"></i>
                                                            </span>&nbsp;<span class="heart-num">${num2str(count_heart)}</span>
                                                        </a>                                                                                                                                                                                                                                                                  
                                                </div>
                                            </nav>
                                            <div class="btn-style">
                                                <button type="button" class="btn btn-outline-secondary" style="float: right; margin-bottom: 10px;">
                                                <a href="/cafe/detail?id=${cafe_id}" style="color: dimgrey">둘러보기</a></button>
                                            </div>
                                 </div>`
                $('#cards-box').append(temp_html)
            }
        }
    })
}

function listing_event(event_category) {

    $("#cards-box").empty()
    $.ajax({
        type: "GET",
        url: `/event_cafe/listing_event?event_category_give=${event_category}`,
        data: {},
        success: function (response) {
            let cafes = response['cafes']
            for (let i = 0; i < cafes.length; i++) {
                let cafe_id = cafes[i]['cafe_id']
                let cafe_image = cafes[i]['cafe_image']
                let cafe_name = cafes[i]['cafe_name']
                let cafe_short_info = cafes[i]['cafe_short_info']
                let class_heart = cafes[i]['heart_by_me'] ? "fa-heart" : "fa-heart-o"
                let count_heart = cafes[i]['count_heart']
                let class_bookmark = cafes[i]['bookmark_by_me'] ? "fa-bookmark" : "fa-bookmark-o"

                let temp_html = `<div class="card" id="${cafe_id}" style="width: 18rem; border-radius: 10px;">
                                        <img class="card-img-top" src="../static/cafe_pics/${cafe_image}" alt="Card image cap">
                                        <div class="card-body">
                                            <h3 class="card-title">${cafe_name}&nbsp;&nbsp;<a class="level-item is-sparta" aria-label="bookmark" onclick="toggle_heart('${cafe_id}', 'bookmark')" style="color: dodgerblue">
                                                <span class="icon is-small"><i class="fa ${class_bookmark}" aria-hidden="true"></i></span></a>
                                            </h3>
                                            <p class="card-text">${cafe_short_info}</p>
                                            <nav class="level is-mobile">
                                                <div class="level-left">
                                                        <a class="level-item is-sparta" aria-label="heart" style="color:#F5C0BE" onclick="toggle_heart('${cafe_id}', 'heart')">
                                                            <span class="icon is-small"><i class="fa ${class_heart}" aria-hidden="true"></i>
                                                            </span>&nbsp;<span class="heart-num">${num2str(count_heart)}</span>
                                                        </a>
                                                </div>
                                            </nav>
                                            <div class="btn-style">
                                                <button type="button" class="btn btn-outline-secondary" style="float: right; margin-bottom: 10px;">
                                                <a href="/cafe/detail?id=${cafe_id}" style="color: dimgrey">둘러보기</a></button>
                                            </div>
                                 </div>`
                $('#cards-box').append(temp_html)
            }
        }
    })
}


