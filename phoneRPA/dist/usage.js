const { exec } = require('child_process');
 
const data =  [
  {
            "cmdType": "Back",
            "cmdParam":0,
            "cmdCound":0
        },
        {
            "cmdType": "ClickPosition",
            "cmdParam":{
                "x":460,
                "y":450
            },
            "cmdCound":1
        },
 
]

const normalJsonStr = JSON.stringify(data)
const escapedJsonStr = (normalJsonStr).replaceAll("\"", "\\\"").replaceAll("\\\\", "\\")
console.log("'" +escapedJsonStr+ "'");

exec('phoneRPAToolCli.exe ' + escapedJsonStr, (error, stdout, stderr) => {
  if (error) {
    console.error(`执行的错误: ${error}`);
    return;
  }
  console.log(`标准输出: ${stdout}`);
  if (stderr) {
    console.error(`标准错误输出: ${stderr}`);
  }
});