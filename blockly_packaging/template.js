// 将block挂载到div上 并设计blockly布局
// 不要修改这个文件中的内容

let workspace = Blockly.inject('block-area',
{toolbox: document.getElementById('tool-box'),
grid: {
    spacing: 20,
    length: 3,
    colour: '#ccc',
    snap: true,
    trashcan: true
},
zoom: {
    controls: true,
    wheel: true,
    startScale: 1.0,
    maxScale: 3,
    minScale: 0.3,
    scaleSpeed: 1.2,
    trashcan: true
}
})


function myUpdateFunction(event) {
    let code = Blockly.JavaScript.workspaceToCode(workspace)
    document.getElementById('code-area').value = code
}
workspace.addChangeListener(myUpdateFunction)

// How to create a response to an action
// function myfunction() {
//     alert('you press the button')
// }
// workspace.registerButtonCallback('myFirstButtonPressed', myFunction)
