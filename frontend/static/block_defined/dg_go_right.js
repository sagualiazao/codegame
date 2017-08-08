Blockly.Blocks['dg_go_right'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("go right")
        .appendField(new Blockly.FieldNumber(0, 0, 100), "step")
        .appendField("step")
    this.setPreviousStatement(true, null)
    this.setNextStatement(true, null)
    this.setColour(300)
 this.setTooltip("")
 this.setHelpUrl("")
  }
}
Blockly.JavaScript['dg_go_right'] = function(block) {
  var number_step = block.getFieldValue('step')
  // TODO: Assemble JavaScript into code variable.
  var code = number_step+',1,'
  return code
};
