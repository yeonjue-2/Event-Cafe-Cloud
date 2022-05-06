function is_id(asValue) {
    let regExp = /^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{2,10}$/;
    return regExp.test(asValue);
}

function check_dup() {
    let userId = $('#input-userId').val()
    if (userId == "") {
        $('#help-id').text("아이디를 입력해주세요!").removeClass("is-safe").addClass("is-danger")
        $('#input-userId').focus()
        return;
    }
    if (!is_id(userId)) {
        $('#help-id').text("아이디 형식을 확인해주세요!").removeClass("is-safe").addClass("is-danger")
        $('#input-userId').focus()
        return;
    }
    $('#help-id').addClass("is-loading")
    $.ajax({
        type: "POST",
        url: "/auth/api/join/double_check",
        data: {user_id_give: userId},
        success: function (response) {
            if (response["checkResult"]) {
                $("#help-id").text("이미 가입된 아이디입니다.").removeClass("is-safe").addClass("is-danger")
                $("#input-userId").focus()
            } else {
                $("#help-id").text("사용할 수 있는 아이디입니다.").removeClass("is-danger").addClass("is-safe")
            }
        }
    });
}

function is_password(asValue) {
    let regExp = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
    return regExp.test(asValue);
}

function join() {
    let user_id = $('#input-userId').val()
    let user_pw = $('#input-userPw').val()
    let user_pw2 = $('#input-userPw2').val()
    let user_email = $('#input-userMail').val()
    let user_nickname = $('#input-nickname').val()
    let user_img = $('#file')[0].files[0]

    if ($('#help-id').hasClass("is-danger")) {
        alert("아이디를 확인해주세요!")
        return;
    } else if (!$('#help-id').hasClass("is-safe")) {
        alert("아이디 중복확인을 해주세요!")
        return;
    }

    if (user_pw == "") {
        $('#help-password').text("비밀번호를 입력하세요").removeClass("is-safe").addClass("is-danger")
        $('#input-userPw').focus()
        return;
    } else if (!is_password(user_pw)) {
        $('#help-password').text("비밀번호 형식을 확인해주세요").removeClass("is-safe").addClass("is-danger")
        $('#input-userPw').focus()
        return;
    } else {
        $('#help-password').text("사용할 수 있는 비밀번호입니다").removeClass("is-safe").addClass("is-danger")
    }
    if (user_pw2 != user_pw) {
        $('#help-password2').text("비밀번호가 일치하지 않습니다.")
        $('#input-userPw2').focus()
        return;
    }

    let form_data = new FormData()

    form_data.append("user_id_give", user_id)
    form_data.append("user_pw_give", user_pw)
    form_data.append("user_email_give", user_email)
    form_data.append("user_nickname_give", user_nickname)
    form_data.append("user_profile_give", user_img)

    $.ajax({
        type: "POST",
        url: "/auth/api/join",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            alert("가입되었습니다!")
            window.location.replace("/auth/")
        }
    });
}