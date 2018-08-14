// 默认进入大厅频道
let current_room = '大厅';

let e = function (sel) {
    return document.querySelector(sel)
};

let join_room = function (room) {
    clear_board();
    current_room = room;
    console.log('切换房间', current_room);
    let data = {
        room: room,
    };
    socket.emit('join', data);
};

let clear_board = function () {
    e("#id_chat_area").value = ''
};

let __main = function () {
    // 初始化 websocket 的方法
    let namespace = '/chatroom';
    let url = `ws://${document.domain}:${location.port}${namespace}`;
    // 一开始是 polling 然后升级成 websocket
    // 所以强制一开始就是 websocket
    console.log('connect url', url);
    socket = io.connect(url, {
        transports: ['websocket']
    });
    // on 函数用来绑定事件, connect 是连接到后端 websocket 成功的时候发生的
    socket.on('connect', function () {
        console.log('connect')
    });

    // 注册 2 个 websocket 消息,
    // 分别是有人加入聊天室的消息和收到别人发送了新消息的消息
    // 这个消息是后端发到前端后, 自动触发的
    let chatArea = e('#id_chat_area');

    socket.on('status', function (data) {
        chatArea.value += `< ${data.message} >\n`
    });

    socket.on('message', function (data) {
        chatArea.value += (data.message + '\n')
    });

    // 加入默认频道
    join_room(current_room);

    // 给 input 绑定一个 回车键发送消息 的事件
    // keypress 事件是在用户按键的时候发生的
    let input = e('#id_input_text');
    input.addEventListener('keypress', function (event) {
        // console.log('keypress', event)
        if (event.key == 'Enter') {
            // 得到用户输入的消息
            message = input.value;
            // 发送消息给后端
            let data = {
                room: current_room,
                message: message,
            };
            socket.emit('send', data, function () {
                // 清空用户输入
                input.value = ''
            })

        }
    });

    // 这是切换频道的事件
    e('body').addEventListener('click', function (event) {
        let self = event.target;
        if (self.classList.contains('gua-room')) {
            console.log('chanel', self.text);
            // 离开频道
            socket.emit('leave', {}, function () {
                console.log("leave room");
                current_room = self.text;
                // 加入房间
                join_room(current_room)
            })
        }
    })
};

__main()