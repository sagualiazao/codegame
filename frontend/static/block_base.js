// 运行按钮的响应函数
// 不要修改这个文件中的内容
function BlockEditor () {
    this.init()
}


// let workspace = Blockly.inject('block-area',
// {toolbox: document.getElementById('tool-box'),
// grid: {
//     spacing: 20,
//     length: 3,
//     colour: '#ccc',
//     snap: true,
//     trashcan: true
// },
// zoom: {
//     controls: true,
//     wheel: true,
//     startScale: 1.0,
//     maxScale: 3,
//     minScale: 0.3,
//     scaleSpeed: 1.2,
//     trashcan: true
// }
// })

BlockEditor.prototype = {
    init: function () {

    }
    runCode: function () {
        alert("enter the run function")
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
}
