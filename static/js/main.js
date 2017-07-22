/**
 * Created by sean on 7/15/17.
 */

var guestNum = 0;
// 当前的帖子对应的order和总共的数量orderMax
var orderMax=-1;
var order = 0;
var hostId, guestId;
var headPreButton = $('.head-pre-button')[0];
var headNextButton = $('.head-next-button')[0];
var headReloadButton = $('.head-reload-button')[0];

// 设置帖主的相关信息
var hostSet = function (data) {
    $('.comment-host .comment-host-content').text(data[0]['content']);
    $('.comment-host .favor-num').text(data[0]['praise_count']);
    hostId = data[0]['_id']
};

// 设置评论区的相关信息
var guestSet = function (data) {
    guestNum = data.length;
    $('ul').filter('.comment-guest').find('li').remove();
    for (let i = 1; i < guestNum; i++) {
        $('.comment-guest').append('<li class="guest-content-area"><span class="guest-index">' + i + '</span>楼: <div class="guest-content">' + data[i]['content'] + '</div>' +
            '<div class="comment-host-use"><div class="use-guest-comment" data-id="' + data[i]['_id'] + '">评论</div><div class="use-guest-favor" data-id="' + data[i]['_id'] + '">' +
            '<span class="favor-icon">&#9829;</span><span class="favor-num">' + data[i]['praise_count'] + '</span></div><div class="use-share">转发</div></div></li>');
        // guestId.append(data[i]['_id']);
    }
};


//读取页面的order
    window.setInterval(function read_post(){
        $.ajax(
            {
                url: "http://localhost/community",
                type: "POST",
                dataType: "json",
                "Content-Type": "application/json",
                data: JSON.stringify(
                    {
                        "order": order,
                        "username":$.cookie('username')
                    }
                ),
                success: function (data) {
                    if(data===-1)
                    {
                        window.href.location='index.html'
                    }
                    order = data.pop();
                    if(order>orderMax)
                    {
                        orderMax=order;
                    }
                    hostSet(data);
                    guestSet(data);
                }
            }
        )
    },1000);

    // 给上一页、下一页、刷新添加事件
headPreButton.addEventListener('click', function () {
    // 给上一页添加事件的函数
    if (order < orderMax) {
        order++
    } else {
    }
});
headNextButton.addEventListener('click', function () {
    // 给下一页添加事件的函数
    if (order > 0) {
        order--;
    }
});
headReloadButton.addEventListener('click', function () {
    order = 0;
});

//读取页面评论对象的_id,root_id
function get_info() {
    $.ajax(
        {
            url: "http://localhost/get_info",
            type: "POST",
            dataType: "json",
            "Content-Type": "application/json",
            data: JSON.stringify(
                {
                    "username": $.cookie('username')
                }
            )

        }
    )
}
get_info();


$('.use-guest-comment').on('click', null, function (e) {
    commentWriteCover.style.display = 'block';
    commentWriteArea.style.display = 'block';
    commentWriteSubmit.value = '发表评论';
    // 得到被点击的评论的id
    guestId = e
});

// 给评论区的点赞添加事件
$('.use-guest-favor').on('click', function (e) {
    guestId = e.target.parentNode.dataset.id;
    $.ajax(
        {
            url: "http://localhost/praise",
            "Content-Type": "application/json;charset=utf-8",
            type: "POST",
            dataType: "json",
            data: JSON.stringify(
                {
                    "_id": guestId
                }
            )
        }
    )
});

// 给注销登录添加事件
logOut.addEventListener('click', function () {
    $.ajax(
        {
            url: "http://localhost/logout",
            type: "POST",
            dataType: "json",
            "Content-Type": "application/json",
            data: JSON.stringify(
                {
                    "username": $.cookie('username')
                }
            ),
            success: function (result) {
                alert("成功退出");
                window.location.href = "index.html"
            }

        }
    )
});


// 给发布按钮添加事件
headButton.addEventListener('click', function () {
    commentWriteCover.style.display = 'block';
    commentWriteArea.style.display = 'block';
    commentWriteSubmit.value = '发布动态';
});

// 给帖子的评论按钮添加事件
useComment.addEventListener('click', function () {
    commentWriteCover.style.display = 'block';
    commentWriteArea.style.display = 'block';
    commentWriteSubmit.value = '发表评论';
});


// 提交评论或者动态的相关程序
function submitFun(){
    if (wform.submit.value === '发布动态') {
        $.ajax(
            {
                url: "http://localhost/write_post",
                type: "POST",
                dataType: "json",
                "Content-Type": "application/json",
                data: JSON.stringify(
                    {
                        "post": document.getElementById("content").value,
                        "username": $.cookie('username')
                    }
                )
            }
        )
    }
    else if (wform.submit.value === '发表评论') {
        $.ajax(
            {
                url: "http://localhost/comments",
                type: "POST",
                dataType: "json",
                "Content-Type": "application/json",
                data: JSON.stringify(
                    {
                        "comment": document.getElementById("content").value,
                        "_id": guestId,
                        "root_id": hostId,
                        "username": $.cookie('username')
                    }
                ),
                success: function (result) {
                    if (result["result"] === "success") {
                        alert("成功发帖")
                    }
                    else {
                        alert("发帖失败")
                    }

                }
            }
        )
    }
}






