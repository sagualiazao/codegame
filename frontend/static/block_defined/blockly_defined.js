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
        .appendField(new global.Blockly.FieldDropdown([['right', 'Right'], ['left', 'Left']]), 'direction')
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
        this.appendValueInput('time').setCheck(null)
        this.appendDummyInput().appendField('times')
        this.appendStatementInput('statementsName').setCheck(null)
        this.setInputsInline(true)
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

global.Blockly.Blocks['dg_var'] = {
    init: function() {
        this.appendDummyInput().appendField('var').appendField(new global.Blockly.FieldTextInput('x'), 'variableName')
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour(345)
        this.setTooltip('')
        this.setHelpUrl('')
    }
}

global.Blockly.Blocks['dg_var_set'] = {
    init: function() {
        this.appendDummyInput().appendField('var').appendField(new global.Blockly.FieldTextInput('x'), 'variableName').appendField('=')
        this.appendValueInput('value').setCheck('Number')
        this.setInputsInline(true)
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour(345)
        this.setTooltip('')
        this.setHelpUrl('')
    }
}

global.Blockly.Blocks['dg_value_set'] = {
    init: function() {
        this.appendDummyInput().appendField('set').appendField(new global.Blockly.FieldTextInput('x'), 'variableName').appendField('=')
        this.appendValueInput('value').setCheck('Number')
        this.setInputsInline(true)
        this.setPreviousStatement(true, null)
        this.setNextStatement(true, null)
        this.setColour(345)
        this.setTooltip('')
        this.setHelpUrl('')
    }
}

global.Blockly.Blocks['dg_get_value'] = {
    init: function() {
        this.appendDummyInput().appendField(new global.Blockly.FieldTextInput('x'), 'variableName')
        this.setOutput(true, 'Number')
        this.setColour(345)
        this.setTooltip('')
        this.setHelpUrl('')
    }
}

global.Blockly.JavaScript['dg_get_value'] = function(block) {
    var textVariableName = block.getFieldValue('variableName')
    var code = '' + textVariableName
    return code
}

global.Blockly.JavaScript['dg_var'] = function(block) {
    var textVariablename = block.getFieldValue('variableName')
    var code = 'var ' + textVariablename + ';\n'
    return code
}

global.Blockly.JavaScript['dg_var_set'] = function(block) {
    var textVariablename = block.getFieldValue('variableName')
    var value = global.Blockly.JavaScript.valueToCode(block, 'value', global.Blockly.JavaScript.ORDER_ATOMIC)
    var code = 'var ' + textVariablename + '=' + value + ';\n'
    return code
}

global.Blockly.JavaScript['dg_value_set'] = function(block) {
    var textVariablename = block.getFieldValue('variableName')
    var value = global.Blockly.JavaScript.valueToCode(block, 'value', global.Blockly.JavaScript.ORDER_ATOMIC)
    var code = textVariablename + '=' + value + ';\n'
    return code
}

global.Blockly.JavaScript['dg_for'] = function (block) {
    var timesNumber = global.Blockly.JavaScript.valueToCode(block, 'time', Blockly.JavaScript.ORDER_ATOMIC)
    var statementsName = global.Blockly.JavaScript.statementToCode(block, 'statementsName')
    var code = 'repeat ' + timesNumber + ' times:\n' + statementsName + 'repeat-end \n'
    return code
}

global.Blockly.JavaScript['dg_fly'] = function (block) {
    var code = 'fly();\n'
    return code
}

global.Blockly.JavaScript['dg_forward'] = function (block) {
    var valueName = global.Blockly.JavaScript
    .valueToCode(block, 'NAME', global.Blockly.JavaScript.ORDER_ATOMIC)
    var code = 'go(' + valueName + ');\n'
    return code
}

global.Blockly.JavaScript['dg_turn_direction'] = function (block) {
    var dropdownDirection = block.getFieldValue('direction')
    var code
    if (dropdownDirection === 'Right') {
        code = 'turn("right");\n'
    } else {
        code = 'turn("left");\n'
    }
    return code
}

global.Blockly.JavaScript['dg_say'] = function (block) {
    var textMessage = block.getFieldValue('message')
    var code = 'say("' + textMessage + '");\n'
    return code
}

global.Blockly.JavaScript['dg_collect'] = function (block) {
    var textName = block.getFieldValue('name')
    // TODO: Assemble JavaScript into code variable.
    var code = 'collect("' + textName + '");\n'
    return code
}

global.Blockly.JavaScript['dg_drop'] = function (block) {
    var textMessage = block.getFieldValue('message')
    // TODO: Assemble JavaScript into code variable.
    var code = 'drop("' + textMessage + '");\n'
    return code
}

global.Blockly.JavaScript['dg_wait'] = function (block) {
    var valueName = global.Blockly.JavaScript
    .valueToCode(block, 'NAME', global.Blockly.JavaScript.ORDER_ATOMIC)
    // TODO: Assemble JavaScript into code variable.
    var code = 'wait("' + valueName + '");\n'
    return code
}

global.Blockly.JavaScript['dg_function'] = function (block) {
    var functionName = block.getFieldValue('functionName')
    var statementsName = global.Blockly.JavaScript.statementToCode(block, 'NAME')
    var code = 'function ' + functionName + ':\n' + statementsName + 'function-end\n'
    return code
}

global.Blockly.JavaScript['dg_function_call'] = function (block) {
    var textFunctonName = block.getFieldValue('functonName')
    code = textFunctonName + '();\n'
    return code
}

global.Blockly.JavaScript['dg_object'] = function (block) {
    var characterName = block.getFieldValue('characterName')
    var statementsName = global.Blockly.JavaScript.statementToCode(block, 'functionName')
    var codeList = statementsName.split('\n')
    var code = ''
    for (var i = 0; i < codeList.length - 1; i++) {
        codeList[i] = characterName + '.' + codeList[i].replace(/\s*/g, '')
        code += codeList[i] + '\n'
    }
    return code
}
