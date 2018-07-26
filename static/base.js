// log函数, 用于打印日志信息
var log = console.log.bind(console)

// 选择器, 用于在父元素下寻找对应元素
var e = function(selector, parent=document) {
    return parent.querySelector(selector)
}

/*
 ajax 函数
*/
var ajax = function(method, path, data, responseCallback) {
    // 初始化
    var r = new XMLHttpRequest()
    // 设置请求方法和请求地址
    r.open(method, path, true)
    // 设置发送的数据的格式为 application/json
    // 这个不是必须的
    r.setRequestHeader('Content-Type', 'application/json')
    // 注册响应函数
    r.onreadystatechange = function() {
        if(r.readyState === 4) {
            // r.response 存的就是服务器发过来的放在 HTTP BODY 中的数据
            log('load ajax response', r.response)
            var json = JSON.parse(r.response)

            //处理后端发过来的状态码
            log('>>>>>>>>',json.error)
            if (json.error == '权限不足'){
                alert('权限不足')
            } else {
                responseCallback(json)
            }
        }
    }
    // 把数据转换为 json 格式字符串
    data = JSON.stringify(data)
    // 发送请求
    r.send(data)
}
