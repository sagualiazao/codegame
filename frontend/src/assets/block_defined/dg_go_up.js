global.Blockly.Blocks['dg_go_up'] = {
    init: function () {
        this.appendDummyInput()
        .appendField('go up')
        .appendField(new global.Blockly.FieldNumber(0, 0, 100), 'step')
        .appendField('step')
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour(300)
        this.setTooltip('')
        this.setHelpUrl('')
    }
}
global.Blockly.JavaScript['dg_go_up'] = function (block) {
    let numberStep = block.getFieldValue('step')
    let code = numberStep + ',4#'
    return code
}