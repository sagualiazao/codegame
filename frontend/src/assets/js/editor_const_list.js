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

/**
* Editor需要的字符串常量
*
* @class editorConstData
*/
let editorConstData = {
    /**
    *用于测试的editor初始值
    *
    * @property initialValue
    * @type {String}
    */
    initialValue
}

module.exports = editorConstData
