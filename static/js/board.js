    $(document).ready(function () {
        post_listing();
    });

     function post_listing() {

        $.ajax({
            type: "GET",
            url: "/api/post",
            data: {},
            success: function (response) {
                $("#post_box").empty();

                for (let i = 0; i < response.length; i++) {
                    let post_title = response[i]['post_title']
                    let user_nickname = response[i]['user_nickname']
                    let post_view = response[i]['post_view']
                    let create_date = response[i]['create_date']
                    let post_num = response[i]['post_num']

                    let temp_html = `<tr onclick="readPost(${post_num})" id="${post_num}" >
                                        <th>${post_num}</th>
                                        <th>${post_title}</th>
                                        <th>${user_nickname}</th>
                                        <th>${post_view}</th>
                                        <th>${create_date}</th>
                                    </tr>`
                    $('#post_box').append(temp_html)
                }
            }
        })
     }
     // 게시글 상세 조회 및 조회수 ++

    function readPost(target_id) {
        $.ajax({
            type: "POST",
            url: `api/post/detail`,
            data: {target_id : target_id },
            success: function (response) {

                let title = response['user']['post_title']
                let content = response['user']['post_content']
                let reg_id = response['user']['user_id']
                let user_id = response['user_id']

                $('#editBtn').css('display','none')
                $('#saveBtn').css('display','none')

                if (user_id == reg_id) {
                    $('#modal-title').html(title);
                    $('#modal-content').attr("readonly", true)
                    $('#modal-content').val(content);
                    $('#articleModal').modal('show');
                    $('#editBtn').css('display','')
                    $('#delBtn').css('display','')
                } else {
                    $('#modal-title').html(title);
                    $('#modal-content').attr("readonly", true)
                    $('#modal-content').val(content);
                    $('#articleModal').modal('show');
                    $('#editBtn').css('display','none')
                    $('#delBtn').css('display','none')
                }

                $('#articleModal').attr('post_num',target_id );
                post_listing()

            }
        })
    }



    function posting() {
        let post_title = $("#textarea-title").val()
        let post_content = $("#textarea-content").val()
            if (post_title == '') {
                (alert("제목을 입력해주세요"))
                return
            }
            if (post_content ==''){
                (alert("내용을 입력해주세요"))
                return
            }

        $.ajax({
            type: "POST",
            url: "/api/post",
            data: {post_title, post_content},
            success: function (response) {
                    if (response["result"] == "success") {
                        alert("게시글이 작성되었습니다");
                        window.location.reload();
                    } else {
                        alert("로그인 후 이용해주세요!")
                    }
                }
            })
    }


     // 글작성자가 글수정 저장 버튼 클릭시
    function post_edit_save() {
        let edit_content = $("#modal-content").val();
        let post_num = $('#articleModal').attr('post_num')

        $.ajax({
            type: "PUT",
            url: "api/post",
            data: {"edit_content":edit_content,"post_num":post_num},
            success: function (response) {
                if (response["result"] == "success") {
                    alert("게시글이 수정되었습니다");
                    window.location.reload();
                } else {
                    alert("서버 오류!");
                }
            }
        })
    }



    function post_edit(){

        $('#modal-content').attr("readonly",false)
        $('#saveBtn').css('display','')

    }

    function post_delete() {
        let post_num = $('#articleModal').attr('post_num')

        $.ajax({
            type: "DELETE",
            url: 'api/post'+ '?' + $.param({"post_num": post_num }),
            success: function (response) {
                if (response["result"] == "success") {
                    alert("게시글이 삭제되었습니다");
                    window.location.href = '/post'
                    post_listing()
                } else if (response["result"] == "fail"){
                    alert("본인의 게시물이 아닙니다");
                } else {
                    alert("로그인 정보가 필요합니다");
                }
            }
        })
    }

