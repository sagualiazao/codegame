Blockly.Blocks['dg_forward'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("move forward")
        .appendField(new Blockly.FieldNumber(0, 0, 100), "step")
        .appendField("step");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(300);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};
Blockly.JavaScript['dg_forward'] = function(block) {
  var number_step = block.getFieldValue('step');
  // TODO: Assemble JavaScript into code variable.
  var code = '...;\n';
  return code;
};
