//显示所有weibo的API
let apiWeiboAll = function (callback) {
    let path = '/api/weibo/all';
    ajax('GET', path, '', callback)
};

//显示所有评论的API
let apiCommentAll = function (callback) {
    let path = '/api/comment/all';
    ajax('GET', path, '', callback)
};

//发表微博的API
let apiWeiboAdd = function (form, callback) {
    let path = '/api/weibo/add';
    ajax('POST', path, form, callback)
};

//发表评论的API
let apiCommentAdd = function (form, callback) {
    let path = '/api/comment/add';
    ajax('POST', path, form, callback)
};

//删除微博的API
let apiWeiboDelete = function (weibo_id, callback) {
    let path = '/api/weibo/delete?id=${weibo_id}';
    ajax('GET', path, '', callback)
};

//删除评论的API
let apiCommentDelete = function (comment_id, callback) {
    let path = '/api/comment/delete?id=${comment_id}';
    ajax('GET', path, '', callback)
};

//更新微博的API
let apiWeiboUpdate = function (form, callback) {
    let path = '/api/weibo/update';
    ajax('POST', path, form, callback)
};

//更新评论的API
let apiCommentUpdate = function (form, callback) {
    let path = '/api/comment/update';
    ajax('POST', path, form, callback)
};

//以下是各种模板
let weiboTemplate = function (weibo) {
//微博的模板
    let t = `
        <div class="weibo-cell pure-form" data-id="${weibo.id}">
            <span class="weibo-user pure-u-3-5">${weibo.writer}发表了微博:</span>
            <span class="btn-small">
                <button class="weibo-delete link-style pure-button pure-u-1-8">删除</button>
                <button class="weibo-edit link-style pure-button pure-u-1-8">编辑</button>
            </span>
            <span class="weibo-title">${weibo.content}</span>
            <hr class="weibo-cell-end">
            <input class='input-comment pure-u-3-5'>
            <button class="button-add-comment link-style pure-button pure-u-1-5">添加评论</button>
        </div>
    `;
    return t
};

//评论块的模板
let commentTemplate = function (comment) {
    // TODO DOM
    let t = `
    <div class="comment-cell" data-id="${comment.id}" data-weiboId="${comment.weibo_id}">
        <span class="comment-user"> [评论] ${comment.writer}:</span>
        <br>
        <span class="comment-title">${comment.content}</span>
        <button class="comment-delete">删除</button>
        <button class="comment-edit">编辑</button>
        <hr class="comment-cell-end">
    </div>
    `;
    return t
};

//更新微薄的文本输入框
let weiboUpdateTemplate = function (title) {
    // TODO DOM
    let t = `
        <div class="weibo-update-form">
            <input class="weibo-update-input" value="${title}">
            <button class="weibo-update">更新</button>
        </div>
    `;
    return t
};

//更新评论的输入框
let commentUpdateTemplate = function (title) {
    let t = `
        <div class="comment-update-form">
            <input class="comment-update-input" value="${title}">
            <button class="comment-update">更新</button>
        </div>
    `;
    return t
};

//All Function used to Insert HTML
let insertWeibo = function (weibo) {
    let weiboCell = weiboTemplate(weibo);
    // 插入 weibo-list
    let weiboList = e('#id-weibo-list');
    weiboList.insertAdjacentHTML('afterbegin', weiboCell)
};

let insertComment = function (comment) {
    let commentCell = commentTemplate(comment);
    let weiboList = document.querySelectorAll(".weibo-cell");
    for (let i = 0; i < weiboList.length; i++) {
        if (comment.weibo_id == weiboList[i].dataset["id"]) {
            log('加载评论', comment.content, '微博ID', comment.weibo_id);
            let insertPoint = e(".weibo-cell-end", weiboList[i]);
            insertPoint.insertAdjacentHTML('beforeend', commentCell)
        }
    }
};

let insertUpdateForm = function (title, weiboCell) {
    let updateForm = weiboUpdateTemplate(title);
    let insertPoint = e('.weibo-cell-end', weiboCell);
    insertPoint.insertAdjacentHTML('beforebegin', updateForm)
};

let insertUpdateCommentForm = function (title, commentCell) {
    let updateForm = commentUpdateTemplate(title);
    log(commentCell);
    let insertPoint = e('.comment-edit', commentCell);
    insertPoint.insertAdjacentHTML('afterend', updateForm)
};

let loadComments = function () {
    apiCommentAll(function (comments) {
        log('load all comments', comments);
        for (let i = 0; i < comments.length; i++) {
            let comment = comments[i];
            insertComment(comment)
        }
    })
};

let loadWeibos = function () {
    apiWeiboAll(function (weibos) {
        log('load all weibos', weibos);
        for (let i = 0; i < weibos.length; i++) {
            let weibo = weibos[i];
            insertWeibo(weibo)
        }
        loadComments()
    })
};


// All Function used to Bind Event
let bindEventWeiboAdd = function () {
    let b = e('#id-button-add');
    b.addEventListener('click', function () {
        let input = e('#id-input-weibo');
        let title = input.value;
        input.value = "";
        log('click add', title);
        let form = {
            content: title
        };
        apiWeiboAdd(form, function (weibo) {
            // 收到返回的数据, 插入到页面中
            insertWeibo(weibo)
        })
    })
};

let bindEventCommentAdd = function () {
    let b = e('#id-weibo-list');
    b.addEventListener('click', function (btn) {
        self = btn.target;
        if (self.classList.contains('button-add-comment')) {
            let weiboCell = self.closest('.weibo-cell');
            let input = e('.input-comment', weiboCell);
            let content = input.value;
            input.value = "";
            log('click add', content);
            let form = {
                weibo_id: weiboCell.dataset['id'],
                content: content
            };
            apiCommentAdd(form, function (comment) {
                // 收到返回的数据, 插入到页面中
                insertComment(comment)
            })
        }
    })
};

let bindEventWeiboDelete = function () {
    let weiboList = e('#id-weibo-list');
    weiboList.addEventListener('click', function (event) {
        log(event);
        let self = event.target;
        log(self.classList);
        if (self.classList.contains('weibo-delete')) {
            log('点到了删除按钮');
            let weiboId = self.parentElement.dataset['id'];
            apiWeiboDelete(weiboId, function (r) {
                log('apiWeiboDelete', r.message);
                self.parentElement.remove();
                alert(r.message)
            })
        }
    })
};

let bindEventCommentDelete = function () {
    let b = e('#id-weibo-list');
    b.addEventListener('click', function (btn) {
        let self = btn.target;
        if (self.classList.contains('comment-delete')) {
            log('点到了删除按钮');
            let commnetId = self.parentElement.dataset['id'];
            apiCommentDelete(commnetId, function (r) {
                log('apiWeiboDelete', r.message);
                self.parentElement.remove();
                alert(r.message)
            })
        }
    })
};

let bindEventWeiboEdit = function () {
    let weiboList = e('#id-weibo-list');
    weiboList.addEventListener('click', function (event) {
        // self is the one clicked
        let self = event.target;
        log(self.classList);
        if (self.classList.contains('weibo-edit')) {
            log('点到了编辑按钮');
            let weiboCell = self.closest('.weibo-cell');
            let weiboId = weiboCell.dataset['id'];
            let weiboSpan = e('.weibo-title', weiboCell);
            let title = weiboSpan.innerText;
            insertUpdateForm(title, weiboCell)
        }
    })
};

let bindEventCommentEdit = function () {
    let b = e('#id-weibo-list');
    b.addEventListener('click', function (btn) {
        let self = btn.target;
        if (self.classList.contains('comment-edit')) {
            log('点到了编辑按钮');
            let commentCell = self.closest('.comment-cell');
            let commentId = commentCell.dataset['id'];
            let commentSpan = e('.comment-title', commentCell);
            let title = commentSpan.innerText;
            insertUpdateCommentForm(title, commentCell)
        }
    })
};

let bindEventWeiboUpdate = function () {
    let weiboList = e('#id-weibo-list');
    weiboList.addEventListener('click', function (event) {
        let self = event.target;
        log(self.classList);
        if (self.classList.contains('weibo-update')) {
            log('点到了更新按钮');
            let weiboCell = self.closest('.weibo-cell');
            let weiboId = weiboCell.dataset['id'];
            log('update weibo id', weiboId);
            let input = e('.weibo-update-input', weiboCell);
            let title = input.value;
            let form = {
                id: weiboId,
                content: title,
            };

            apiWeiboUpdate(form, function (weibo) {
                // 收到返回的数据, 插入到页面中
                let weiboSpan = e('.weibo-title', weiboCell);
                weiboSpan.innerText = weibo.content;

                let updateForm = e('.weibo-update-form', weiboCell);
                updateForm.remove()
            })
        }
    })
};

let bindEventCommentUpdate = function () {
    let b = e('#id-weibo-list');
    b.addEventListener('click', function (btn) {
        let self = btn.target;
        if (self.classList.contains('comment-update')) {
            log('点到了更新按钮');
            let commentCell = self.closest('.comment-cell');
            let commentId = commentCell.dataset['id'];
            let input = e('.comment-update-input', commentCell);
            let title = input.value;
            let form = {
                id: commentId,
                content: title,
            };

            apiCommentUpdate(form, function (comment) {
                // 收到返回的数据, 插入到页面中
                let commentSpan = e('.comment-title', commentCell);
                commentSpan.innerText = comment.content;

                let updateForm = e('.comment-update-form', commentCell);
                updateForm.remove()
            })
        }
    })
};


// Main Function
let bindWeiboEvents = function () {
    bindEventWeiboAdd();
    bindEventWeiboDelete();
    bindEventWeiboEdit();
    bindEventWeiboUpdate()
};

let bindCommentEvents = function () {
    bindEventCommentAdd();
    bindEventCommentDelete();
    bindEventCommentEdit();
    bindEventCommentUpdate()
};

let __main = function () {
    bindWeiboEvents();
    bindCommentEvents();
    loadWeibos()
};

__main();
