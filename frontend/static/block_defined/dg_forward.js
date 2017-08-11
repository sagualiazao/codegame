global.Blockly.Blocks['dg_forward'] = {
    init: function () {
        this.appendDummyInput()
        .appendField('move forward')
        .appendField(new global.Blockly.FieldNumber(0, 0, 100), 'step')
        .appendField('step')
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour(260)
        this.setTooltip('')
        this.setHelpUrl('')
    }
}
global.Blockly.JavaScript['dg_forward'] = function (block) {
    var numberStep = block.getFieldValue('step')
    var code = 'go(' + numberStep + ')#'
    return code
}
