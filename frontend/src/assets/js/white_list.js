let commandCodeLibrary = [
    // abcdefg
    [/^\s*\w*\.?collect\("\w*"\)\s*$/, /^\s*\w*\.?drop\("\w*"\)\s*$/, /^\s*\w*\.?go\(\w*\)\s*$/, /^\s*\w*\.?fly\(\)\s*$/, /^\s*function-end\s*$/, /^\s*function \w+$/],
    // hijklmn
    [],
    // opqrstu
    [/^\s*repeat \w+ times\s*$/, /^\s*repeat-end\s*$/, /^\s*\w*\.?say\("\w*"\)\s*$/, /^\s*\w*\.?turn\("left"\)\s*$/, /^\s*\w*\.?turn\("right"\)\s*$/],
    // vwxyz
    [/^\s*var\s+[A-Za-z]\w*\s*=\s*(\d+|[A-Za-z]\w*)\s*$/, /^\s*var\s+[A-Za-z]\w*\s*/, /^\s*\w*\.?wait\(\w*\)\s*$/],
    // 定义的变量  放进来一个带等于号的 一个不带等于号的 和一个对应的正则表达式字符串
    [],
    // 定义的函数  放进带（）的正则表达式和相应的字符串（不处理含参的函数）
    []
    // 面向对象的放进正常的里面  手动处理 不受用户支配
]
/**
* 代码白名单
*
* @class whiteListConstData
*/
let whiteListConstData = {
    /**
    *安全代码库
    *
    * @property commandCodeLibrary
    * @type {List}
    */
    commandCodeLibrary,
    /**
    *白名单初始化函数
    *
    * @method init
    */
    init: function () {
        this.commandCodeLibrary = [
            [/^\s*\w*\.?collect\("\w*"\)\s*$/, /^\s*\w*\.?drop\("\w*"\)\s*$/, /^\s*\w*\.?go\(\w*\)\s*$/, /^\s*\w*\.?fly\(\)\s*$/, /^\s*function-end\s*$/, /^\s*function \w+$/],
            [],
            [/^\s*repeat \w+ times\s*$/, /^\s*repeat-end\s*$/, /^\s*\w*\.?say\("\w*"\)\s*$/, /^\s*\w*\.?turn\("left"\)\s*$/, /^\s*\w*\.?turn\("right"\)\s*$/],
            [/^\s*var\s+[A-Za-z]\w*\s*=\s*(\d+|[A-Za-z]\w*)\s*$/, /^\s*var\s+[A-Za-z]\w*\s*/, /^\s*\w*\.?wait\(\w*\)\s*$/],
            [],
            []
        ]
    },
    /**
    *白名单清空变量和函数列表的函数
    *
    * @method clean
    */
    clean: function () {
        this.commandCodeLibrary[4] = ''
        this.commandCodeLibrary[5] = ''
    },
    /**
    *根据输入的角色姓名获取角色的对应序号
    *
    * @method indexOfCharacter
    * @return {Number} 如果角色姓名为 Nancy 返回 0; Carla 1; 不存在 2；
    */
    indexOfCharacter: function (name) {
        if (name === 'Nancy') {
            return 0
        } else if (name === 'Carla') {
            return 1
        } else {
            return 2
        }
    },
    /**
    *将用户输入的Name.xxx()转换为名字序号作为参数的字符串
    *
    * @method formateTheName
    * @param {String} code 要转换的代码
    * @return {String} 名字序号作为参数的字符串
    */
    formateTheName: function (code) {
        let typeOfCharacter = 0
        let indexOfDot = code.indexOf('.')
        if (indexOfDot !== -1) {
            let codeList = code.split('.')
            codeList[0] = codeList[0].replace(/\s*/g, '')
            let typeOfCharacter = this.indexOfCharacter(codeList[0])
            if (typeOfCharacter === 2) {
                return false
            }
            code = codeList[1].replace('(', '(' + typeOfCharacter + ', ')
        } else {
            code = code.replace('(', '(' + typeOfCharacter + ', ')
        }
        return code
    },
    /**
    *转换对应代码库位置[0, 0]的代码
    *
    * @method formatFunction00
    * @param {String} code 要转换的代码
    * @return {String} 安全可执行代码
    */
    formatFunction00: function (code) {
        code = this.formateTheName(code)
        if (code !== false) {
            code = code.replace('collect', 'this.collect') + ';'
        }
        return code
    },
    /**
    *转换对应代码库位置[0, 1]的代码
    *
    * @method formatFunction01
    * @param {String} code 要转换的代码
    * @return {String} 安全可执行代码
    */
    formatFunction01: function (code) {
        code = this.formateTheName(code)
        if (code !== false) {
            code = code.replace('drop', 'this.drop') + ';'
        }
        return code
    },
    /**
    *转换对应代码库位置[0, 2]的代码
    *
    * @method formatFunction02
    * @param {String} code 要转换的代码
    * @return {String} 安全可执行代码
    */
    formatFunction02: function (code) {
        code = this.formateTheName(code)
        if (code !== false) {
            code = code.replace('go', 'this.go') + ';'
        }
        return code
    },
    /**
    *转换对应代码库位置[0, 3]的代码
    *
    * @method formatFunction03
    * @param {String} code 要转换的代码
    * @return {String} 安全可执行代码
    */
    formatFunction03: function (code) {
        code = this.formateTheName(code)
        if (code !== false) {
            code = code.replace('fly', 'this.fly') + ';'
            code = code.replace(', ', '')
        }
        return code
    },
    /**
    *转换对应代码库位置[0, 4]的代码
    *
    * @method formatFunction04
    * @param {String} code 要转换的代码
    * @return {String} 安全可执行代码
    */
    formatFunction04: function (code) {
        code = code.replace('function-end', '\'')
        return code + ';'
    },
    /**
    *转换对应代码库位置[0, 5]的代码
    *
    * @method formatFunction05
    * @param {String} code 要转换的代码
    * @return {String} 安全可执行代码
    */
    formatFunction05: function (code) {
        let functionName = code.replace('function', '') + '\\(\\)'
        functionName = functionName.replace(/\s*/g, '')
        let regExpString = '^\\s*' + functionName + '\\s*$'
        // 处理重复定义函数的情况
        if (this.commandCodeLibrary[5].indexOf(regExpString) !== -1) {
            return false
        }
        this.commandCodeLibrary[5].push(new RegExp(regExpString))
        this.commandCodeLibrary[5].push(regExpString)
        code = code.replace('function ', 'this.functionSet[\'') + '\']=\''
        return code
    },
    /**
    *转换对应代码库位置[2, 0]的代码
    *
    * @method formatFunction20
    * @param {String} code 要转换的代码
    * @return {String} 安全可执行代码
    */
    formatFunction20: function (code) {
        code = code.replace('repeat ', 'for(let i = 0; i < ')
        code = code.replace(' times', '; i++) {')
        return code
    },
    /**
    *转换对应代码库位置[2, 1]的代码
    *
    * @method formatFunction21
    * @param {String} code 要转换的代码
    * @return {String} 安全可执行代码
    */
    formatFunction21: function (code) {
        code = code.replace('repeat-end', '}')
        return code
    },
    /**
    *转换对应代码库位置[2, 2]的代码
    *
    * @method formatFunction22
    * @param {String} code 要转换的代码
    * @return {String} 安全可执行代码
    */
    formatFunction22: function (code) {
        code = this.formateTheName(code)
        if (code !== false) {
            code = code.replace('say', 'this.say') + ';'
        }
        return code
    },
    /**
    *转换对应代码库位置[2, 3]的代码
    *
    * @method formatFunction23
    * @param {String} code 要转换的代码
    * @return {String} 安全可执行代码
    */
    formatFunction23: function (code) {
        code = this.formateTheName(code)
        if (code !== false) {
            code = code.replace('turn', 'this.turn') + ';'
        }
        return code
    },
    /**
    *转换对应代码库位置[2, 4]的代码
    *
    * @method formatFunction24
    * @param {String} code 要转换的代码
    * @return {String} 安全可执行代码
    */
    formatFunction24: function (code) {
        code = this.formateTheName(code)
        if (code !== false) {
            code = code.replace('turn', 'this.turn') + ';'
        }
        return code
    },
    /**
    *转换对应代码库位置[3, 0]的代码
    *
    * @method formatFunction30
    * @param {String} code 要转换的代码
    * @return {String} 安全可执行代码
    */
    formatFunction30: function (code) {
        'var x = 3'
        let temp = code.replace('var', '')
        temp = temp.replace(/=\s*(\d+|[A-Za-z]\w*)\s*/, '')
        let variable = temp.replace(/\s*/g, '')
        let regExpString = '^\\s*' + variable + '\\s*$'
        // 处理重复定义变量的情况
        if (this.commandCodeLibrary[4].indexOf(regExpString) === -1) {
            this.commandCodeLibrary[4].push(regExpString)
            let regExp = new RegExp(regExpString)
            this.commandCodeLibrary[4].push(regExp)
            regExpString = '^\\s*' + variable + '\\s*=\\s*(\\d+|[A-Za-z]\\w*)\\s*$'
            regExp = new RegExp(regExpString)
            this.commandCodeLibrary[4].push(regExp)
        }
        return code + ';'
    },
    /**
    *转换对应代码库位置[3, 1]的代码
    *
    * @method formatFunction31
    * @param {String} code 要转换的代码
    * @return {String} 安全可执行代码
    */
    formatFunction31: function (code) {
        let temp = code.replace('var', '')
        let variable = temp.replace(/\s*/g, '')
        let regExpString = '^\\s*' + variable + '\\s*$'
        // 处理重复定义变量的情况
        if (this.commandCodeLibrary[4].indexOf(regExpString) === -1) {
            this.commandCodeLibrary[4].push(regExpString)
            let regExp = new RegExp(regExpString)
            this.commandCodeLibrary[4].push(regExp)
            regExpString = '^\\s*' + variable + '\\s*=\\s*(\\d+|[A-Za-z]\\w*)\\s*$'
            regExp = new RegExp(regExpString)
            this.commandCodeLibrary[4].push(regExp)
        }
        return code + ';'
    },
    /**
    *转换对应代码库位置[3, 2]的代码
    *
    * @method formatFunction32
    * @param {String} code 要转换的代码
    * @return {String} 安全可执行代码
    */
    formatFunction32: function (code) {
        code = this.formateTheName(code)
        if (code !== false) {
            code = code.replace('wait', 'this.wait') + ';'
        }
        return code
    },
    /**
    *转换对应代码库位置[4, x]的代码
    *
    * @method formatFunction4
    * @param {String} code 要转换的代码
    * @return {String} 安全可执行代码
    */
    formatFunction4: function (code) {
        return code + ';'
    },
    /**
    *转换对应代码库位置[5, x]的代码
    *
    * @method formatFunction5
    * @param {String} code 要转换的代码
    * @return {String} 安全可执行代码
    */
    formatFunction5: function (code) {
        let functionName = code.replace('()', '')
        functionName = functionName.replace(/\s*/g, '')
        code = 'eval(this.functionSet["' + functionName + '"]);'
        return code
    }
}

module.exports = whiteListConstData
