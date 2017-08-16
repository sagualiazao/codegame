let commandCodeLibrary = [
    // abcdefg
    [/^\s*collect\("\w*"\)\s*$/, /^\s*drop\("\w*"\)\s*$/, /^\s*go\(\w*\)\s*$/, /^\s*fly\(\)\s*$/, /^\s*function-end\s*$/, /^\s*function \w+$/],
    // hijklmn
    [/^\s*nancy.\S+\s*$/],
    // opqrstu
    [/^\s*repeat \w+ times\s*$/, /^\s*repeat-end\s*$/, /^\s*say\("\w*"\)\s*$/, /^\s*turn\("left"\)\s*$/, /^\s*turn\("right"\)\s*$/],
    // vwxyz
    [/^\s*var\s+\w*\s*=\s*\d*\s*$/, /^\s*var\s+\w*\s*/, /^\s*wait\(\w*\)\s*$/],
    // 定义的变量  放进来一个带等于号的 一个不带等于号的
    [],
    // 定义的函数  放进带（）的函数 不处理含参的函数
    []
    // 面向对象的放进正常的里面  手动处理 不受用户支配
]
let whiteListConstData = {
    commandCodeLibrary,
    init: function () {
        this.commandCodeLibrary[5] = []
        this.commandCodeLibrary[4] = []
    },
    formatFunction00: function (code) {
        code = code.replace('collect', 'this.collect')
        return code + ';'
    },
    formatFunction01: function (code) {
        code = code.replace('drop', 'this.drop')
        return code + ';'
    },
    formatFunction02: function (code) {
        code = code.replace('go', 'this.go')
        return code + ';'
    },
    formatFunction03: function (code) {
        code = code.replace('fly', 'this.fly')
        return code + ';'
    },
    formatFunction04: function (code) {
        code = code.replace('function-end', '\'')
        return code + ';'
    },
    formatFunction05: function (code) {
        // TODO 处理重复的情况
        let functionName = code.replace('function', '') + '\\(\\)'
        functionName = functionName.replace(/\s*/g, '')
        let regExpString = '^\\s*' + functionName + '\\s*$'
        this.commandCodeLibrary[5].push(new RegExp(regExpString))
        code = code.replace('function ', 'this.functionSet[\'')
        return code + '\']=\''
    },
    formatFunction10: function (code) {
        code = code.replace('nancy.', 'this.nancy')
        return code + ';'
    },
    formatFunction20: function (code) {
        code = code.replace('repeat ', 'for(let i = 0; i < ')
        code = code.replace(' times', '; i++) {')
        return code
    },
    formatFunction21: function (code) {
        code = code.replace('repeat-end', '}')
        return code
    },
    formatFunction22: function (code) {
        code = code.replace('say', 'this.say')
        return code + ';'
    },
    formatFunction23: function (code) {
        code = code.replace('turn', 'this.turn')
        return code + ';'
    },
    formatFunction24: function (code) {
        code = code.replace('turn', 'this.turn')
        return code + ';'
    },
    formatFunction30: function (code) {
        // TODO 处理重复的情况
        'var x = 3'
        let temp = code.replace('var', '')
        temp = temp.replace(/=\s*\d*\s*/, '')
        let variable = temp.replace(/\s*/g, '')
        let regExpString = '^\\s*' + variable + '\\s*$'
        let regExp = new RegExp(regExpString)
        this.commandCodeLibrary[4].push(regExp)
        regExpString = '^\\s*' + variable + '\\s*=\\d+\\s*$'
        regExp = new RegExp(regExpString)
        this.commandCodeLibrary[4].push(regExp)
        return code + ';'
    },
    formatFunction31: function (code) {
        let temp = code.replace('var', '')
        let variable = temp.replace(/\s*/g, '')
        let regExpString = '^\\s*' + variable + '\\s*$'
        let regExp = new RegExp(regExpString)
        this.commandCodeLibrary[4].push(regExp)
        regExpString = '^\\s*' + variable + '\\s*=\\d+\\s*$'
        regExp = new RegExp(regExpString)
        this.commandCodeLibrary[4].push(regExp)
        return code + ';'
    },
    formatFunction32: function (code) {
        code = code.replace('wait', 'this.wait')
        return code + ';'
    },
    formatFunction4: function (code) {
        return code + ';'
    },
    formatFunction5: function (code) {
        let functionName = code.replace('()', '')
        functionName = functionName.replace(/\s*/g, '')
        code = 'eval(this.functionSet["' + functionName + '"]);'
        return code
    }
}

module.exports = whiteListConstData
