// let toolBoxText = [
//     '<xml>',
//     '   <category name="Action">',
//     '       <block type="dg_go_up">',
//     '           <field name="step">0</field>',
//     '       </block>',
//     '       <block type="dg_go_down">',
//     '           <field name="step">0</field>',
//     '       </block>',
//     '       <block type="dg_go_left">',
//     '           <field name="step">0</field>',
//     '       </block>',
//     '       <block type="dg_go_right">',
//     '           <field name="step">0</field>',
//     '       </block>',
//     '   </category>',
//     '   <category name="Control">',
//     '       <block type="controls_if"></block>',
//     '   </category>',
//     '</xml>'].join('\n')

let toolBoxTextTemp = [
    '<xml>',
    '    <category name="Action">',
    '        <block type="dg_forward">',
    '           <value name="NAME">',
    '               <shadow type="math_number">',
    '                   <field name="NUM">3</field>',
    '               </shadow>',
    '           </value>',
    '        </block>',
    '        <block type="dg_turn_direction">',
    '            <field name="direction">Right</field>',
    '        </block>',
    '    </category>',
    '</xml>'
].join('\n')

module.exports = toolBoxTextTemp
