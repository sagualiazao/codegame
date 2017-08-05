Blockly.Blocks['dg_start'] = {
  init: function() {
    this.appendDummyInput();
    this.appendDummyInput()
        .appendField("             start            ");
    this.appendDummyInput();
    this.setNextStatement(true, null);
    this.setColour(20);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};
Blockly.JavaScript['dg_start'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = '...;\n';
  return code;
};
