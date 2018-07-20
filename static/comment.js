
var apiCommentAll = function(callback) {
    var path = '/api/comment/all'
    ajax('GET', path, '', callback)
}




}

var loadComments = function () {
    apiCommentAll(function (comments) {
        log('Load Comments')
        for (var i = 1; i < comments.length; i++) {
            var comment = comments[i]
            insertComment(weibo)
        }
    })
}

// var commentEvents = function () {
//     bindEventCommentAdd()
//     bindEventCommentEdit()
//     bindEventCommentDel()
//     bindEventCommentUpdate()
// }


var __main = function () {
    // commentEvents()
    loadComments()
}

__main()
