const { exec } = require('child_process');
const { describe, it, expect } = require("vitest")


const testCase1 = ()=>{
  return new Promise((resolve,reject)=>{
    exec('pcRPAToolCli.exe ' + data, (error, stdout, stderr) => {
      resolve(stdout)
    });
  })
}

describe("用例1", () => {
  it("测试是否能够清空云文档", async () => {
    const result = await testCase1()
    expect(result).toEqual("no error")
  })
})