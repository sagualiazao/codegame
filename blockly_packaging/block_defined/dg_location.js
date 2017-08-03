Blockly.Blocks['dg_location'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("set position")
        .appendField("x")
        .appendField(new Blockly.FieldNumber(0, -240, 240), "x")
        .appendField("y")
        .appendField(new Blockly.FieldNumber(0, -240, 240), "NAME");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(300);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};
Blockly.JavaScript['dg_location'] = function(block) {
  var number_x = block.getFieldValue('x');
  var number_name = block.getFieldValue('NAME');
  // TODO: Assemble JavaScript into code variable.
  var code = '...;\n';
  return code;
};
