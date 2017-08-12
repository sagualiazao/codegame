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
        .appendField(new global.Blockly.FieldTextInput('coins'), 'name')
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

global.Blockly.Blocks['dg_for'] = {
    init: function () {
        this.appendDummyInput().appendField('repeat')
        .appendField(new global.Blockly.FieldNumber(0, 0, 10), 'times').appendField('times')
        this.appendStatementInput('statementsName').setCheck(null)
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour(120)
        this.setTooltip('')
        this.setHelpUrl('')
    }
}

global.Blockly.Blocks['dg_drop'] = {
    init: function () {
        this.appendDummyInput().appendField('drop').appendField(new global.Blockly.FieldTextInput('coins'), 'message')
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour(260)
        this.setTooltip('')
        this.setHelpUrl('')
    }
}

global.Blockly.Blocks['dg_function_call'] = {
    init: function () {
        this.appendDummyInput().appendField('call function')
        .appendField(new global.Blockly.FieldTextInput('functionName'), 'functonName')
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour(230)
        this.setTooltip('')
        this.setHelpUrl('')
    }
}


global.Blockly.JavaScript['dg_for'] = function (block) {
    var timesNumber = block.getFieldValue('times')
    var statementsName = global.Blockly.JavaScript.statementToCode(block, 'statementsName')
    // TODO: Assemble JavaScript into code variable.
    var code = ''
    for(var i = 0; i < parseInt(timesNumber); i++ ) {
        code = code + statementsName
    }
    return code
}

global.Blockly.JavaScript['dg_fly'] = function (block) {
    // TODO: Assemble JavaScript into code variable.
    var code = 'this.fly();'
    return code
}

global.Blockly.JavaScript['dg_forward'] = function (block) {
    var valueName = global.Blockly.JavaScript
    .valueToCode(block, 'NAME', global.Blockly.JavaScript.ORDER_ATOMIC)
    var code = 'this.go(' + valueName + ');'
    return code
}

global.Blockly.JavaScript['dg_turn_direction'] = function (block) {
    var dropdownDirection = block.getFieldValue('direction')
    var code
    if (dropdownDirection === 'Right') {
        code = 'this.turn(\'right\');'
    } else {
        code = 'this.turn(\'left\');'
    }
    return code
}

global.Blockly.JavaScript['dg_say'] = function (block) {
    var textMessage = block.getFieldValue('message')
    var code = 'this.say(\'' + textMessage + '\');'
    return code
}

global.Blockly.JavaScript['dg_collect'] = function (block) {
    var textName = block.getFieldValue('name')
    // TODO: Assemble JavaScript into code variable.
    var code = 'this.collect(\'' + textName + '\');'
    return code
}

global.Blockly.JavaScript['dg_drop'] = function (block) {
    var textMessage = block.getFieldValue('message')
    // TODO: Assemble JavaScript into code variable.
    var code = 'this.drop(\'' + textMessage + '\');'
    return code
}

global.Blockly.JavaScript['dg_wait'] = function (block) {
    var valueName = global.Blockly.JavaScript
    .valueToCode(block, 'NAME', global.Blockly.JavaScript.ORDER_ATOMIC)
    // TODO: Assemble JavaScript into code variable.
    var code = 'this.wait(\'' + valueName + '\');'
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
    var code = 'this.functionSet[\'' + functionName + '\'] = "' + statementsName + '";'
    return code
}

global.Blockly.JavaScript['dg_function_call'] = function (block) {
    var textFunctonName = block.getFieldValue('functonName')
    // TODO: Assemble JavaScript into code variable.
    code = [
        'let m = this.functionSet[\'' + textFunctonName + '\'];',
        'eval(m);'
    ].join('\n')
    return code
}
