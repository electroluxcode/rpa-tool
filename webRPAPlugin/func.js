let rpa_tool_port;
const getValue = async (key) => {
	return new Promise((resolve, reject) => {
		chrome.storage.sync.get([key], function (items) {
			resolve(items[key]);
		});
	});
};
const setValue = async (Value) => {
	return new Promise((resolve, reject) => {
		chrome.storage.sync.set(Value, function () {
			resolve(Value);
		});
	});
};

const openWebSocket = async (port) => {
    console.log('openWebSocket ws://127.0.0.1', port);
    const socket = io('ws://127.0.0.1:'+ port);

    // 接收消息并展示
    socket.on('rpa_tool_message', function(data) {
        console.log(data);
    });

    
    // 发送消息
    function sendMessage(message) {
        socket.emit('rpa_tool_message', {message});
    }

    document.getElementById('messageButton').addEventListener('click', ()=>{
        const message = document.getElementById('messageInput').value;
        sendMessage(message);
    });
}


const main = async () => {
    // 端口号
	const portValue = (await getValue("rpa_tool_port")) 
	document.querySelector("#port").value = portValue ?? 5000;
	document.querySelector("#port").addEventListener("change", async (e) => {
		await setValue({
			rpa_tool_port: e.target.value,
		});
	});

    // 是否打开
	const isOpenValue = await getValue("rpa_tool_isOpen");
	document.querySelector("#isOpen").checked = isOpenValue
    document.querySelector("#isOpen").addEventListener("change", async (e) => {
		console.log("isOpenValue", e.target);
        await setValue({
			rpa_tool_isOpen: e.target.checked
		});
	});

    if(isOpenValue){
        openWebSocket(portValue);
    }

    const includeValue = (await getValue("rpa_tool_include")) 
	document.querySelector("#include").value = includeValue ?? "";

	document.querySelector("#include").addEventListener("change", async (e) => {
		await setValue({
			rpa_tool_include: e.target.value,
		});
	});
};

main();
