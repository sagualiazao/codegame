Blockly.Blocks['dg_go_up'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("go up")
        .appendField(new Blockly.FieldNumber(0, 0, 100), "step")
        .appendField("step")
    this.setPreviousStatement(true, null)
    this.setNextStatement(true, null)
    this.setColour(300)
 this.setTooltip("")
 this.setHelpUrl("")
  }
};
Blockly.JavaScript['dg_go_up'] = function(block) {
  var number_step = block.getFieldValue('step')
  // TODO: Assemble JavaScript into code variable.
  var code = 'this.length = '+number_step+' ; this.direct = 4#'
  return code
};
