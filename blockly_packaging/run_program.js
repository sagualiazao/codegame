// 运行按钮的响应函数
// 不要修改这个文件中的内容

function runCode() {
    window.LoopTrap = 1000
    Blockly.JavaScript.INFINITE_LOOP_TRAP =
    'if (--window.LoopTrap == 0) throw "Infinite loop.";\n'
    let code = Blockly.JavaScript.workspaceToCode(workspace)
    Blockly.JavaScript.INFINITE_LOOP_TRAP = null
    try {
        eval(code)
    }catch (e) {
        alert(e)
    }
}
