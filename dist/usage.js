const { exec } = require('child_process');

const data =  [
  {
    "cmdType": "Click",
    "cmdParam": {
        "x": 100,
        "y": 100,
        "clicks": 2
    }
},
]

  const normalJsonStr = JSON.stringify(data)
  const escapedJsonStr = (normalJsonStr).replaceAll("\"", "\\\"").replaceAll("\\\\", "\\")
  console.log("'" +escapedJsonStr+ "'");
  
  exec('pcRPAToolCli.exe ' + escapedJsonStr, (error, stdout, stderr) => {
    if (error) {
      console.error(`执行的错误: ${error}`);
      return;
    }
    console.log(`标准输出: ${stdout}`);
    if (stderr) {
      console.error(`标准错误输出: ${stderr}`);
    }
  });