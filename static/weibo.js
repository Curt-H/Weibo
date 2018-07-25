//API to Back End
const apiWeiboAll = function (callback) {
    const path = '/api/weibo/all';
    ajax('GET', path, '', callback)
};

const apiCommentAll = function (callback) {
    const path = '/api/comment/all';
    ajax('GET', path, '', callback)
};

const apiWeiboAdd = function (form, callback) {
    let path = '/api/weibo/add';
    ajax('POST', path, form, callback)
};

const apiCommentAdd = function (form, callback) {
    const path = '/api/comment/add';
    ajax('POST', path, form, callback)
};

const apiWeiboDelete = function (weibo_id, callback) {
    const path = `/api/weibo/delete?id=${weibo_id}`;
    ajax('GET', path, '', callback)
};

const apiCommentDelete = function (comment_id, callback) {
    const path = `/api/comment/delete?id=${comment_id}`;
    ajax('GET', path, '', callback)
};

const apiWeiboUpdate = function (form, callback) {
    const path = '/api/weibo/update';
    ajax('POST', path, form, callback)
};

const apiCommentUpdate = function (form, callback) {
    const path = '/api/comment/update';
    ajax('POST', path, form, callback)
};


//All Template Used
const weiboTemplate = function (weibo) {
    // Weibo DOM
    const t = `
        <div class="weibo-cell pure-form" data-id="${weibo.id}">
            <span class="weibo-user">${weibo.username}发表了微博:</span>
            <span class="weibo-title">${weibo.content}</span>
            <button class="weibo-delete link-style pure-button pure-u-1-5">删除</button>
            <button class="weibo-edit link-style pure-button pure-u-1-5">编辑</button>
            <hr class="weibo-cell-end">
            <input class='input-comment pure-u-3-5'>
            <button class="button-add-comment link-style pure-button pure-u-1-5">添加评论</button>
        </div>
    `;
    return t
};

const commentTemplate = function (comment) {
    // TODO DOM
    const t = `
    <div class="comment-cell" data-id="${comment.id}" data-weiboId="${comment.weibo_id}">
    <span class="comment-user"> [评论] ${comment.username}:</span>
    <br>
    <span class="comment-title">${comment.content}</span>
    <button class="comment-delete">删除</button>
    <button class="comment-edit">编辑</button>
    <hr class="comment-cell-end">
    </div>
    `;
    return t
};

const weiboUpdateTemplate = function (title) {
    // TODO DOM
    const t = `
        <div class="weibo-update-form">
            <input class="weibo-update-input" value="${title}">
            <button class="weibo-update">更新</button>
        </div>
    `;
    return t
};

const commentUpdateTemplate = function (title) {
    const t = `
        <div class="comment-update-form">
            <input class="comment-update-input" value="${title}">
            <button class="comment-update">更新</button>
        </div>
    `;
    return t
};

//All Function used to Insert HTML
const insertWeibo = function (weibo) {
    const weiboCell = weiboTemplate(weibo);
    // 插入 weibo-list
    const weiboList = e('#id-weibo-list');
    weiboList.insertAdjacentHTML('beforeend', weiboCell)
};

const insertComment = function (comment) {
    const commentCell = commentTemplate(comment);
    const weiboList = document.querySelectorAll(".weibo-cell");
    for (let i = 0; i < weiboList.length; i++) {
        if (comment.weibo_id == weiboList[i].dataset["id"]) {
            log('加载评论', comment.content, '微博ID', comment.weibo_id);
            let insertPoint = e(".weibo-cell-end", weiboList[i]);
            insertPoint.insertAdjacentHTML('beforeend', commentCell)
        }
    }
};

const insertUpdateForm = function (title, weiboCell) {
    const updateForm = weiboUpdateTemplate(title);
    const insertPoint = e('.weibo-cell-end', weiboCell);
    insertPoint.insertAdjacentHTML('beforebegin', updateForm)
};

const insertUpdateCommentForm = function (title, commentCell) {
    const updateForm = commentUpdateTemplate(title);
    log(commentCell);
    const insertPoint = e('.comment-edit', commentCell);
    insertPoint.insertAdjacentHTML('afterend', updateForm)
};

const loadComments = function () {
    apiCommentAll(function (comments) {
        log('load all comments', comments);
        for (let i = 0; i < comments.length; i++) {
            const comment = comments[i];
            insertComment(comment)
        }
    })
};

const loadWeibos = function () {
    apiWeiboAll(function (weibos) {
        log('load all weibos', weibos);
        for (let i = 0; i < weibos.length; i++) {
            const weibo = weibos[i];
            insertWeibo(weibo)
        }
        loadComments()
    })
};


// All Function used to Bind Event
const bindEventWeiboAdd = function () {
    const b = e('#id-button-add');
    b.addEventListener('click', function () {
        const input = e('#id-input-weibo');
        const title = input.value;
        input.value = "";
        log('click add', title);
        const form = {
            content: title
        };
        apiWeiboAdd(form, function (weibo) {
            // 收到返回的数据, 插入到页面中
            insertWeibo(weibo)
        })
    })
};

const bindEventCommentAdd = function () {
    const b = e('#id-weibo-list');
    b.addEventListener('click', function (btn) {
        self = btn.target;
        if (self.classList.contains('button-add-comment')) {
            const weiboCell = self.closest('.weibo-cell');
            const input = e('.input-comment', weiboCell);
            const content = input.value;
            input.value = "";
            log('click add', content);
            const form = {
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

const bindEventWeiboDelete = function () {
    const weiboList = e('#id-weibo-list');
    weiboList.addEventListener('click', function (event) {
        log(event);
        const self = event.target;
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

const bindEventCommentDelete = function () {
    const b = e('#id-weibo-list');
    b.addEventListener('click', function (btn) {
        const self = btn.target;
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

const bindEventWeiboEdit = function () {
    const weiboList = e('#id-weibo-list');
    weiboList.addEventListener('click', function (event) {
        // self is the one clicked
        const self = event.target;
        log(self.classList);
        if (self.classList.contains('weibo-edit')) {
            log('点到了编辑按钮');
            let weiboCell = self.closest('.weibo-cell');
            let weiboId = weiboCell.dataset['id'];
            const weiboSpan = e('.weibo-title', weiboCell);
            const title = weiboSpan.innerText;
            insertUpdateForm(title, weiboCell)
        }
    })
};

const bindEventCommentEdit = function () {
    const b = e('#id-weibo-list');
    b.addEventListener('click', function (btn) {
        const self = btn.target;
        if (self.classList.contains('comment-edit')) {
            log('点到了编辑按钮');
            let commentCell = self.closest('.comment-cell');
            let commentId = commentCell.dataset['id'];
            const commentSpan = e('.comment-title', commentCell);
            const title = commentSpan.innerText;
            insertUpdateCommentForm(title, commentCell)
        }
    })
};

const bindEventWeiboUpdate = function () {
    const weiboList = e('#id-weibo-list');
    weiboList.addEventListener('click', function (event) {
        const self = event.target;
        log(self.classList);
        if (self.classList.contains('weibo-update')) {
            log('点到了更新按钮');
            let weiboCell = self.closest('.weibo-cell');
            let weiboId = weiboCell.dataset['id'];
            log('update weibo id', weiboId);
            let input = e('.weibo-update-input', weiboCell);
            let title = input.value;
            const form = {
                id: weiboId,
                content: title,
            };

            apiWeiboUpdate(form, function (weibo) {
                // 收到返回的数据, 插入到页面中
                const weiboSpan = e('.weibo-title', weiboCell);
                weiboSpan.innerText = weibo.content;

                const updateForm = e('.weibo-update-form', weiboCell);
                updateForm.remove()
            })
        }
    })
};

const bindEventCommentUpdate = function () {
    const b = e('#id-weibo-list');
    b.addEventListener('click', function (btn) {
        const self = btn.target;
        if (self.classList.contains('comment-update')) {
            log('点到了更新按钮');
            let commentCell = self.closest('.comment-cell');
            let commentId = commentCell.dataset['id'];
            let input = e('.comment-update-input', commentCell);
            let title = input.value;
            const form = {
                id: commentId,
                content: title,
            };

            apiCommentUpdate(form, function (comment) {
                // 收到返回的数据, 插入到页面中
                const commentSpan = e('.comment-title', commentCell);
                commentSpan.innerText = comment.content;

                const updateForm = e('.comment-update-form', commentCell);
                updateForm.remove()
            })
        }
    })
};


// Main Function
const bindWeiboEvents = function () {
    bindEventWeiboAdd();
    bindEventWeiboDelete();
    bindEventWeiboEdit();
    bindEventWeiboUpdate()
};

const bindCommentEvents = function () {
    bindEventCommentAdd();
    bindEventCommentDelete();
    bindEventCommentEdit();
    bindEventCommentUpdate()
};

const __main = function () {
    bindWeiboEvents();
    bindCommentEvents();
    loadWeibos()
};

__main();
