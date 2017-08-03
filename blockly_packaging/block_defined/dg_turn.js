Blockly.Blocks['dg_turn'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("turn")
        .appendField(new Blockly.FieldDropdown([["rigth","Right"], ["left","Left"]]), "direction");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(300);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};
Blockly.JavaScript['dg_turn'] = function(block) {
  var dropdown_direction = block.getFieldValue('direction');
  // TODO: Assemble JavaScript into code variable.
  var code = '...;\n';
  return code;
};
