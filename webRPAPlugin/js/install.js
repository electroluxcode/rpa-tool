// console.log("install.js loaded");

// chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
// 	console.log("收藏消息:", {
// 		request,
// 		sender,
// 	});
// 	// console.log(sender.tab ?"from a content script:" + sender.tab.url :"from the extension");
// 	if (request.cmd == "test") alert(request.value);
// 	sendResponse("我收到了你的消息！");
// });
// setTimeout(() => {
// 	console.log("document", document.body);
// 	console.log("io", io);
// }, 1000);


// let script = document.createElement('script');
// script.innerHTML = `
//   let meta = document.createElement('meta');
//   meta.httpEquiv = 'Content-Security-Policy';
//   meta.content = 'default-src *; script-src *; connect-src *; img-src *; style-src *;';
//   document.getElementsByTagName('head')[0].appendChild(meta);
// `;
// document.documentElement.appendChild(script);

console.log("install.js loaded", chrome);
// chrome.webRequest.onHeadersReceived.addListener(
//     function(details) {
//       for (let i = 0; i < details.responseHeaders.length; ++i) {
//         if (details.responseHeaders[i].name.toLowerCase() === 'content-security-policy') {
//           details.responseHeaders.splice(i, 1);
//           break;
//         }
//       }
//       return { responseHeaders: details.responseHeaders };
//     },
//     {
//       urls: ["*:*"], // 你想要绕过CSP策略的域名
//       types: ["main_frame", "sub_frame"]
//     },
//     ["blocking", "responseHeaders"]
// );
const openWebSocket = async (port) => {
    console.log('openWebSocket ws://127.0.0.1', port);
    const socket = io('ws://127.0.0.1:'+ port);

    // 接收消息并展示
    socket.on('rpa_tool_message', function(data) {
        console.log(data);
        if(data?.message=="exit" || data?.user){
            return
        }
        try{
            const script = document.createElement("script")
            script.innerHTML=data.message
            document.body.appendChild(script)
        }catch(e){
            console.log(e)
        }
       
        
    });
    socket.on('connection', function() {
        console.log("rpa_tool连接成功");
    });

}

const getValue = async (key) => {
	return new Promise((resolve, reject) => {
		chrome.storage.sync.get([key], function (items) {
			resolve(items[key]);
		});
	});
};

const main = async () => {
	const rpa_tool_port = await getValue("rpa_tool_port");
	const isOpenValue = await getValue("rpa_tool_isOpen");
    const rpa_tool_include = await getValue("rpa_tool_include");
    console.log({
        rpa_tool_port,
        isOpenValue,
        rpa_tool_include
    })
    if(!isOpenValue) return;
    if(rpa_tool_include){
        const a = new RegExp(rpa_tool_include); 
        const isValiate = a.test(window.location.href)
        if(!isValiate) return;
    }
    openWebSocket(rpa_tool_port)

}

main()