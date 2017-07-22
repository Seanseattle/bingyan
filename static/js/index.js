var logOut = $('.head-logout a')[0];
var bodyLi = $('.body-list li');
var headButton = $('.head-button')[0];
var useComment = $('.use-comment')[0];
var commentWriteCover = $('.comment-write-cover')[0];
var commentWriteArea = $('.comment-write-area')[0];
var commentWriteClose = $('.comment-write-close')[0];
var commentWriteSubmit = $('.comment-write-submit')[0];
var commentGuest = $('.comment-guest');
var favor = $('.use-favor')[0];
var favorNum = $('.use-favor .favor-num')[0];

// 给关闭评论按钮添加事件
commentWriteClose.addEventListener('click', function () {
  commentWriteCover.style.display = 'none'
  commentWriteArea.style.display = 'none'
})
// 左边栏点击样式的实现
var showLi = function (i) {
  for (var j = 0; j < bodyLi.length; j ++) {
    let _j = j
    bodyLi[_j].className = 'li-hover-none'
  }
  bodyLi[i].className = 'li-hover'
}
for (var i = 0; i < bodyLi.length; i ++) {
  let _i = i
  bodyLi[_i].addEventListener('click', function (e) {
    switch (e.target.innerText) {
      case '推荐': showLi (0)
        break
      case '吐槽': showLi (1)
        break
      case '生活': showLi (2)
        break
      case '待定': showLi (3)
        break
      default:
        break
    }
  })
}
// 帖子点赞数量的变化
favor.addEventListener('click', function () {
  favorNum.innerHTML = parseInt(favorNum.innerHTML) + 1
    // 传点赞评论的id。。。。。。。。。。。
})