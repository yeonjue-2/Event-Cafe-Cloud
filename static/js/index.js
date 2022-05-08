function toggle_heart(cafe_id, type) {
            console.log(cafe_id, type)
            let $a_heart = $(`#${cafe_id} a[aria-label='${type}']`)
            let $i_heart = $a_heart.find("i")
            let full_icons = {"heart": "fa-heart", "bookmark": "fa-bookmark"};
            let empty_icons = {"heart": "fa-heart-o", "bookmark": "fa-bookmark-o"};
            if ($i_heart.hasClass(full_icons[type])) {
                $.ajax({
                    type: "POST",
                    url: "/update_heart",
                    data: {
                        cafe_id_give: cafe_id,
                        type_give: type,
                        action_give: "unheart"
                    },
                    success: function (response) {
                        console.log("unheart")
                        $i_heart.addClass(empty_icons[type]).removeClass(full_icons[type])
                        $a_heart.find("span.heart-num").text(num2str(response["count"]))
                    }
                })
            } else {
                $.ajax({
                    type: "POST",
                    url: "/update_heart",
                    data: {
                        cafe_id_give: cafe_id,
                        type_give: type,
                        action_give: "heart"
                    },
                    success: function (response) {
                        console.log("heart")
                        $i_heart.addClass(full_icons[type]).removeClass(empty_icons[type])
                        $a_heart.find("span.heart-num").text(num2str(response["count"]))
                    }
                })

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
                url: "/main",
                data: {},
                success: function (response) {
                    let cafes = response['cafes']
                    for (let i = 0; i < cafes.length; i++) {
                        let cafe = cafes[i]
                        let cafe_image = cafes[i]['cafe_image']
                        let cafe_name = cafes[i]['cafe_name']
                        let address = cafes[i]['address']
                        let class_heart = cafes['heart_by_me'] ? "fa-heart": "fa-heart-o"
                        let count_heart = cafes['count_heart']
                        let class_bookmark = cafes['bookmark_by_me'] ? "fa-bookmark": "fa-bookmark-o"


                        let temp_html = `<div class="card" id="${cafe["_id"]}" style="width: 18rem; border-radius: 10px;">
                                            <img class="card-img-top" src="..." alt="Card image cap">
                                            <div class="card-body">
                                                <h3 class="card-title">${cafe_name}</h3>
                                                <p class="card-text">${address}</p>
                                                <nav class="level is-mobile">
                                                    <div class="level-left">
                                                        <a class="level-item is-sparta" aria-label="heart" style="color:#F5C0BE" onclick="toggle_heart('${cafe["_id"]}', 'heart')">
                                                            <span class="icon is-small"><i class="fa ${class_heart}"
                                                                                           aria-hidden="true"></i></span>&nbsp;<span
                                                                class="heart-num">${num2str(count_heart)}</span>
                                                        </a>
                                                        <a class="level-item is-sparta" aria-label="bookmark" onclick="toggle_heart('${cafe["_id"]}', 'bookmark')">
                                                            <span class="icon is-small"><i class="fa ${class_bookmark}"
                                                                                           aria-hidden="true"></i></span>&nbsp;<span
                                                                class="heart-num"></span>
                                                        </a>                                                        
                                                    </div>
                                                </nav>
                                                <div class="btn-style">
                                                    <button type="button" class="btn btn-outline-secondary" style="float: right;">
                                                    <a href="#" style="color: dimgrey">둘러보기</a></button>
                                                </div>
                                          </div>`
                        $('#cards-box').append(temp_html)
                    }
                }
            })
        }