
// 这是一个示例

Blockly.Blocks['dg_changecolor'] = {
    init: function() {
    this.appendDummyInput()
        .appendField("set  color")
        .appendField(new Blockly.FieldDropdown([["blue","BLUE"], ["red","RED"], ["green","GREEN"]]), "color");
    this.setPreviousStatement(true, null)
    this.setNextStatement(true, null)
    this.setColour(65)
    this.setTooltip('')
    this.setHelpUrl('')
  }
}

// 你可以修改 TODO以后的部分 但注意一定要返回一个code变量  否则模块将不收运行按钮的控制

Blockly.JavaScript['dg_changecolor'] = function(block) {
    let dropdown_color = block.getFieldValue('color')
    // TODO: Assemble JavaScript into code variable.
    let code = ""
    if (dropdown_color == 'RED') {
        code="document.getElementById('game-circle').style.backgroundColor = 'red'\n"
    }
    else if (dropdown_color == 'BLUE') {
        code = "document.getElementById('game-circle').style.backgroundColor = 'blue'\n"
    }
    else {
        // 这是一个使用第三方js文件中函数的示例  原则就是把你想调用的函数或者程序code每一行后加一个'\n'
        // 这个code值最终会在你按下按钮的同时  触发run_program.js 中的 runCode() 函数
        // 通过eval()进行解析 然后运行
        // 在该文件中不用引入第三方js 只是传一个字符串而已
        // 只要在HTML 中按照我标注的 引入第三方js脚本即可
        // 同时这个code值会写入到屏幕下方的编辑区中，具体实现方法不必理会
        code = "test()\n"
    }
    return code
}
