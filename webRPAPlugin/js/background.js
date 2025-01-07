console.log("background.js loaded")

console.log(chrome)

const allResourceTypes = Object.values(chrome.declarativeNetRequest.ResourceType);


// // import rules from './rules';
const rules = [
    {
        "id": 1,
        "priority": 1,
        "action": {
            "type": "modifyHeaders",
            "responseHeaders": [
                {
                    "header": "content-security-policy",
                    "operation": "remove"
                },
                {
                    "header": "content-security-policy-report-only",
                    "operation": "remove"
                },
                {
                    "header": "Content-Security-Policy",
                    "operation": "remove"
                },{
                    "header": "X-Zptest",
                    "operation": "set",
                    "value": "zptest"
                }
    
            ],
            
        },
        condition: {
            resourceTypes: ['csp_report', 'font', 'image', 'main_frame', 'media', 'object', 'other', 'ping', 'script', 'stylesheet', 'sub_frame', 'webbundle', 'websocket', 'webtransport', 'xmlhttprequest'],
          }
    }
]
chrome.declarativeNetRequest.updateDynamicRules({
  removeRuleIds: rules.map((rule) => rule.id), // remove existing rules
  addRules: rules
});