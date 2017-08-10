global.Blockly.Blocks['dg_turn_direction'] = {
    init: function () {
        this.appendDummyInput()
        .appendField('turn')
        .appendField(new global.Blockly.FieldDropdown([['rigth', 'Right'], ['left', 'Left']]), 'direction')
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour(260)
        this.setTooltip('')
        this.setHelpUrl('')
    }
}
global.Blockly.JavaScript['dg_turn_direction'] = function (block) {
    let dropdownDirection = block.getFieldValue('direction')
    let code
    if (dropdownDirection === 'Right') {
        code = 'turn(right)#'
    } else if (dropdownDirection === 'Left') {
        code = 'turn(left)#'
    }
    return code
}
