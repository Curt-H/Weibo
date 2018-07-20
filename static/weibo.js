//API to Back End
var apiWeiboAll = function (callback) {
    var path = '/api/weibo/all'
    ajax('GET', path, '', callback)
}

var apiCommentAll = function (callback) {
    var path = '/api/comment/all'
    ajax('GET', path, '', callback)
}

var apiWeiboAdd = function (form, callback) {
    var path = '/api/weibo/add'
    ajax('POST', path, form, callback)
}

var apiCommentAdd = function (form, callback) {
    var path = '/api/comment/add'
    ajax('POST', path, form, callback)
}

var apiWeiboDelete = function (weibo_id, callback) {
    var path = `/api/weibo/delete?id=${weibo_id}`
    ajax('GET', path, '', callback)
}

var apiCommentDelete = function (comment_id, callback) {
    var path = `/api/comment/delete?id=${comment_id}`
    ajax('GET', path, '', callback)
}

var apiWeiboUpdate = function (form, callback) {
    var path = '/api/weibo/update'
    ajax('POST', path, form, callback)
}

var apiCommentUpdate = function (form, callback) {
    var path = '/api/comment/update'
    ajax('POST', path, form, callback)
}


//All Template Used
var weiboTemplate = function (weibo) {
    // TODO DOM
    var t = `
        <div class="weibo-cell" data-id="${weibo.id}">
            <span class="weibo-user">${weibo.username}发表了微博:</span>
            <br>
            <span class="weibo-title">${weibo.content}</span>
            <button class="weibo-delete">删除</button>
            <button class="weibo-edit">编辑</button>
            <hr class="weibo-cell-end">
            <input class='input-comment'>
            <button class='button-add-comment'>添加评论</button>
            <hr>
            <hr>
        </div>
    `
    return t
}

var commentTemplate = function (comment) {
    // TODO DOM
    var t = `
    <div class="comment-cell" data-id="${comment.id}" data-weiboId="${comment.weibo_id}">
    <span class="comment-user"> [评论] ${comment.username}:</span>
    <br>
    <span class="comment-title">${comment.content}</span>
    <button class="comment-delete">删除</button>
    <button class="comment-edit">编辑</button>
    <hr class="comment-cell-end">
    </div>
    `
    return t
}

var weiboUpdateTemplate = function (title) {
    // TODO DOM
    var t = `
        <div class="weibo-update-form">
            <input class="weibo-update-input" value="${title}">
            <button class="weibo-update">更新</button>
        </div>
    `
    return t
}

var commentUpdateTemplate = function (title) {
    var t = `
        <div class="comment-update-form">
            <input class="comment-update-input" value="${title}">
            <button class="comment-update">更新</button>
        </div>
    `
    return t
}

//All Function used to Insert HTML
var insertWeibo = function (weibo) {
    var weiboCell = weiboTemplate(weibo)
    // 插入 weibo-list
    var weiboList = e('#id-weibo-list')
    weiboList.insertAdjacentHTML('beforeend', weiboCell)
}

var insertComment = function (comment) {
    var commentCell = commentTemplate(comment)
    var weiboList = document.querySelectorAll(".weibo-cell")
    for (var i = 0; i < weiboList.length; i++) {
        if (comment.weibo_id == weiboList[i].dataset["id"]) {
            log('加载评论', comment.content, '微博ID', comment.weibo_id)
            insertPoint = e(".weibo-cell-end", weiboList[i])
            insertPoint.insertAdjacentHTML('beforeend', commentCell)
        }
    }
}

var insertUpdateForm = function (title, weiboCell) {
    var updateForm = weiboUpdateTemplate(title)
    var insertPoint = e('.weibo-cell-end', weiboCell)
    insertPoint.insertAdjacentHTML('beforebegin', updateForm)
}

var insertUpdateCommentForm = function (title, commentCell) {
    var updateForm = commentUpdateTemplate(title)
    log(commentCell)
    var insertPoint = e('.comment-edit', commentCell)
    insertPoint.insertAdjacentHTML('afterend', updateForm)
}

var loadComments = function () {
    apiCommentAll(function (comments) {
        log('load all comments', comments)
        for (var i = 0; i < comments.length; i++) {
            var comment = comments[i]
            insertComment(comment)
        }
    })
}

var loadWeibos = function () {
    apiWeiboAll(function (weibos) {
        log('load all weibos', weibos)
        for (var i = 0; i < weibos.length; i++) {
            var weibo = weibos[i]
            insertWeibo(weibo)
        }
        loadComments()
    })
}


// All Function used to Bind Event
var bindEventWeiboAdd = function () {
    var b = e('#id-button-add')
    b.addEventListener('click', function () {
        var input = e('#id-input-weibo')
        var title = input.value
        input.value = ""
        log('click add', title)
        var form = {
            content: title
        }
        apiWeiboAdd(form, function (weibo) {
            // 收到返回的数据, 插入到页面中
            insertWeibo(weibo)
        })
    })
}

var bindEventCommentAdd = function () {
    var b = e('#id-weibo-list')
    b.addEventListener('click', function (btn) {
        self = btn.target
        if (self.classList.contains('button-add-comment')) {
            var weiboCell = self.closest('.weibo-cell')
            var input = e('.input-comment', weiboCell)
            var content = input.value
            input.value = ""
            log('click add', content)
            var form = {
                weibo_id: weiboCell.dataset['id'],
                content: content
            }
            apiCommentAdd(form, function (comment) {
                // 收到返回的数据, 插入到页面中
                insertComment(comment)
            })
        }
    })
}

var bindEventWeiboDelete = function () {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function (event) {
        log(event)
        var self = event.target
        log(self.classList)
        if (self.classList.contains('weibo-delete')) {
            log('点到了删除按钮')
            weiboId = self.parentElement.dataset['id']
            apiWeiboDelete(weiboId, function (r) {
                log('apiWeiboDelete', r.message)
                self.parentElement.remove()
                alert(r.message)
            })
        }
    })
}

var bindEventCommentDelete = function () {
    var b = e('#id-weibo-list')
    b.addEventListener('click', function (btn) {
        var self = btn.target
        if (self.classList.contains('comment-delete')) {
            log('点到了删除按钮')
            commnetId = self.parentElement.dataset['id']
            apiCommentDelete(commnetId, function (r) {
                log('apiWeiboDelete', r.message)
                self.parentElement.remove()
                alert(r.message)
            })
        }
    })
}

var bindEventWeiboEdit = function () {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function (event) {
        // self is the one clicked
        var self = event.target
        log(self.classList)
        if (self.classList.contains('weibo-edit')) {
            log('点到了编辑按钮')
            weiboCell = self.closest('.weibo-cell')
            weiboId = weiboCell.dataset['id']
            var weiboSpan = e('.weibo-title', weiboCell)
            var title = weiboSpan.innerText
            insertUpdateForm(title, weiboCell)
        }
    })
}

var bindEventCommentEdit = function () {
    var b = e('#id-weibo-list')
    b.addEventListener('click', function (btn) {
        var self = btn.target
        if (self.classList.contains('comment-edit')) {
            log('点到了编辑按钮')
            commentCell = self.closest('.comment-cell')
            commentId = commentCell.dataset['id']
            var commentSpan = e('.comment-title', commentCell)
            var title = commentSpan.innerText
            insertUpdateCommentForm(title, commentCell)
        }
    })
}

var bindEventWeiboUpdate = function () {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function (event) {
        var self = event.target
        log(self.classList)
        if (self.classList.contains('weibo-update')) {
            log('点到了更新按钮')
            weiboCell = self.closest('.weibo-cell')
            weiboId = weiboCell.dataset['id']
            log('update weibo id', weiboId)
            input = e('.weibo-update-input', weiboCell)
            title = input.value
            var form = {
                id: weiboId,
                content: title,
            }

            apiWeiboUpdate(form, function (weibo) {
                // 收到返回的数据, 插入到页面中
                var weiboSpan = e('.weibo-title', weiboCell)
                weiboSpan.innerText = weibo.content

                var updateForm = e('.weibo-update-form', weiboCell)
                updateForm.remove()
            })
        }
    })
}

var bindEventCommentUpdate = function () {
    var b = e('#id-weibo-list')
    b.addEventListener('click', function (btn) {
        var self = btn.target
        if (self.classList.contains('comment-update')) {
            log('点到了更新按钮')
            commentCell = self.closest('.comment-cell')
            commentId = commentCell.dataset['id']
            input = e('.comment-update-input', commentCell)
            title = input.value
            var form = {
                id: commentId,
                content: title,
            }

            apiCommentUpdate(form, function (comment) {
                // 收到返回的数据, 插入到页面中
                var commentSpan = e('.comment-title', commentCell)
                commentSpan.innerText = comment.content

                var updateForm = e('.comment-update-form', commentCell)
                updateForm.remove()
            })
        }
    })
}


// Main Function
var bindWeiboEvents = function () {
    bindEventWeiboAdd()
    bindEventWeiboDelete()
    bindEventWeiboEdit()
    bindEventWeiboUpdate()
}

var bindCommentEvents = function () {
    bindEventCommentAdd()
    bindEventCommentDelete()
    bindEventCommentEdit()
    bindEventCommentUpdate()
}

var __main = function () {
    bindWeiboEvents()
    bindCommentEvents()
    loadWeibos()
}

__main()
