global.Blockly.Blocks['dg_forward'] = {
    init: function () {
        this.appendDummyInput().appendField('move forward')
        this.appendValueInput('NAME').setCheck('Number')
        this.appendDummyInput().appendField('step')
        this.setInputsInline(true)
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour(260)
        this.setTooltip('')
        this.setHelpUrl('')
    }
}

global.Blockly.Blocks['dg_turn_direction'] = {
    init: function () {
        this.appendDummyInput().appendField('turn')
        .appendField(new global.Blockly.FieldDropdown([['rigth', 'Right'], ['left', 'Left']]), 'direction')
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour(260)
        this.setTooltip('')
        this.setHelpUrl('')
    }
}

global.Blockly.Blocks['dg_say'] = {
    init: function () {
        this.appendDummyInput().appendField('say')
        .appendField(new global.Blockly.FieldTextInput('robot'), 'message')
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour(260)
        this.setTooltip('')
        this.setHelpUrl('')
    }
}

global.Blockly.Blocks['dg_collect'] = {
    init: function () {
        this.appendDummyInput().appendField('collect')
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour(260)
        this.setTooltip('')
        this.setHelpUrl('')
    }
}

global.Blockly.Blocks['dg_wait'] = {
    init: function () {
        this.appendValueInput('NAME').setCheck(null).appendField('wait')
        this.appendDummyInput().appendField('second')
        this.setInputsInline(true)
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour(120)
        this.setTooltip('')
        this.setHelpUrl('')
    }
}

global.Blockly.Blocks['dg_object'] = {
    init: function () {
        this.appendDummyInput().appendField('character')
        .appendField(new global.Blockly.FieldTextInput('robot'), 'characterName')
        this.appendStatementInput('functionName').setCheck(null)
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour(230)
        this.setTooltip('')
        this.setHelpUrl('')
    }
}

global.Blockly.Blocks['dg_function'] = {
    init: function () {
        this.appendDummyInput().appendField('function')
        .appendField(new global.Blockly.FieldTextInput('Run'), 'functionName')
        this.appendStatementInput('NAME').setCheck(null)
        this.setColour(230)
        this.setTooltip('')
        this.setHelpUrl('')
    }
}

global.Blockly.Blocks['dg_fly'] = {
    init: function () {
        this.appendDummyInput().setAlign(global.Blockly.ALIGN_CENTRE).appendField('gate    fly ')
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour(260)
        this.setTooltip('')
        this.setHelpUrl('')
    }
}
global.Blockly.JavaScript['dg_fly'] = function (block) {
    // TODO: Assemble JavaScript into code variable.
    var code = 'fly()#'
    return code
}

global.Blockly.JavaScript['dg_forward'] = function (block) {
    var valueName = global.Blockly.JavaScript
    .valueToCode(block, 'NAME', global.Blockly.JavaScript.ORDER_ATOMIC)
    var code = 'go(' + valueName + ')#'
    return code
}

global.Blockly.JavaScript['dg_turn_direction'] = function (block) {
    var dropdownDirection = block.getFieldValue('direction')
    var code
    if (dropdownDirection === 'Right') {
        code = 'turn(right)#'
    } else {
        code = 'turn(left)#'
    }
    return code
}

global.Blockly.JavaScript['dg_say'] = function (block) {
    var textMessage = block.getFieldValue('message')
    // TODO: Assemble JavaScript into code variable.
    var code = '...\n'
    return code
}

global.Blockly.JavaScript['dg_collect'] = function (block) {
    // TODO: Assemble JavaScript into code variable.
    var code = '...\n'
    return code
}

global.Blockly.JavaScript['dg_wait'] = function (block) {
    var valueName = global.Blockly.JavaScript
    .valueToCode(block, 'NAME', global.Blockly.JavaScript.ORDER_ATOMIC)
    // TODO: Assemble JavaScript into code variable.
    var code = '...\n'
    return code
}

global.Blockly.JavaScript['dg_object'] = function (block) {
    var characterName = block.getFieldValue('characterName')
    var statementsName = global.Blockly.JavaScript.statementToCode(block, 'functionName')
    // TODO: Assemble JavaScript into code variable.
    var code = characterName + '(' + statementsName + ')\n'
    return code
}

global.Blockly.JavaScript['dg_function'] = function (block) {
    var functionName = block.getFieldValue('functionName')
    var statementsName = global.Blockly.JavaScript.statementToCode(block, 'NAME')
    // TODO: Assemble JavaScript into code variable.
    var code = '...\n'
    return code
}
