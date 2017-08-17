let initialValue = [
    'go(5)',
    'repeat 3 times: go(4)',
    '    turn("left")',
    '    repeat 4 times:',
    '        turn("right")',
    '    repeat-end',
    '                  ',
    '                     ',
    'repeat-end',
    'drop("key");',
    'function run:',
    '    go(5)',
    '    repeat 3 times:',
    '        go(3)',
    '    repeat-end',
    'function-end',
    'var x=3',
    'nancy.go(x)'
].join('\n')

let editorConstData = {
    initialValue
}

module.exports = editorConstData
