import EditorBase from '@/components/EditorBase'
import { createVue, destroyVM } from '../util'

describe('EditorBase.vue', () => {
    let vm

    beforeEach(() => {
        vm = createVue(EditorBase, true)
    })

    afterEach(() => {
        destroyVM(vm)
    })

    it('getCommandCodeList函数执行成功', () => {
        let initialValue = require('../../../src/assets/js/editor_const_list.js').initialValue
        vm.jsEditor.setValue(initialValue)
        let commandList = vm.getCommandCodeList()
         expect(commandList).to.deep.equal([
             'go(5)',
             'repeat 3 times',
             ' go(4)',
             '    turn("left")',
             '    repeat 4 times',
             '        turn("right")',
             '    repeat-end',
             'repeat-end',
             'drop("key")',
             'function run',
             '    go(5)',
             '    repeat 3 times',
             '        go(3)',
             '    repeat-end',
             'function-end',
             'var x=3',
             'nancy.go(x)'
         ])
    })

    it('isSameFormat函数执行成功', () => {
        expect(vm.isSameFormat(/^\s*\w*\.collect\("\w*"\)\s*$/, '   nancy.collect("key")  ')).to.equal(true)
        expect(vm.isSameFormat(/^\s*\w*\.collect\("\w*"\)\s*$/, '   collect("key")')).to.equal(false)
        expect(vm.isSameFormat(/^\s*\w*\.collect\("\w*"\)\s*$/, 'nancy.hhcollect("key")')).to.equal(false)
        expect(vm.isSameFormat(/^\s*\w*\.collect\("\w*"\)\s*$/, 'nancy.hhcollect("key")hh')).to.equal(false)
        expect(vm.isSameFormat(/^\s*\w*\.collect\("\w*"\)\s*$/, 'hhcollect("key")hh')).to.equal(false)
        expect(vm.isSameFormat(/^\s*\w*\.fly\(\)\s*$/, 'nancy.fly()')).to.equal(true)
        expect(vm.isSameFormat(/^\s*\w*\.fly\(\)\s*$/, 'fly()')).to.equal(false)
        expect(vm.isSameFormat(/^\s*\w*\.fly\(\)\s*$/, 'nancy.')).to.equal(false)
        expect(vm.isSameFormat(/^\s*repeat \w+ times\s*$/, 'repeat 33 times')).to.equal(true)
        expect(vm.isSameFormat(/^\s*repeat \w+ times\s*$/, 'repeat aa times')).to.equal(true)
        expect(vm.isSameFormat(/^\s*repeat \w+ times\s*$/, 'repeataatimes')).to.equal(false)
        expect(vm.isSameFormat( /^\s*repeat-end\s*$/, ' repeat-end ')).to.equal(true)
        expect(vm.isSameFormat( /^\s*repeat-end\s*$/, ' ss repeat -end ')).to.equal(false)
        expect(vm.isSameFormat(/^\s*var\s+\w*\s*=\s*\d*\s*$/, 'var xx=33')).to.equal(true)
        expect(vm.isSameFormat(/^\s*var\s+\w*\s*=\s*\d*\s*$/, 'var xx=3d')).to.equal(false)
        expect(vm.isSameFormat(/^\s*function \w+$/, '   function run')).to.equal(true)
        expect(vm.isSameFormat(/^\s*function \w+$/, 'function   run')).to.equal(false)
    })

    it('indexInCommandLibrary', () => {
        expect(vm.indexInCommandLibrary('  nancy.collect("key")')).to.deep.equal('00')
        expect(vm.indexInCommandLibrary('nancy.collect(key)')).to.equal(false)
        expect(vm.indexInCommandLibrary('nancy.drop("key")')).to.deep.equal('01')
        expect(vm.indexInCommandLibrary('nancy.go(23)')).to.deep.equal('02')
        expect(vm.indexInCommandLibrary('nancy.go(ss)')).to.deep.equal('02')
        expect(vm.indexInCommandLibrary('nancy.go(\'hellp\')')).to.equal(false)
        expect(vm.indexInCommandLibrary('nancy.fly()')).to.deep.equal('03')
        expect(vm.indexInCommandLibrary('fly(hh)')).to.equal(false)
        expect(vm.indexInCommandLibrary('   function-end')).to.deep.equal('04')
        expect(vm.indexInCommandLibrary('  function run')).to.deep.equal('05')
        expect(vm.indexInCommandLibrary('    repeat 23 times')).to.deep.equal('20')
        expect(vm.indexInCommandLibrary('repeat dd times')).to.deep.equal('20')
        expect(vm.indexInCommandLibrary('repeatsstimes')).to.equal(false)
        expect(vm.indexInCommandLibrary('repeat-end')).to.deep.equal('21')
        expect(vm.indexInCommandLibrary('nancy.say("hello")')).to.deep.equal('22')
        expect(vm.indexInCommandLibrary('say(hello)')).to.equal(false)
        expect(vm.indexInCommandLibrary('nancy.turn("left")')).to.deep.equal('23')
        expect(vm.indexInCommandLibrary('nancy.turn("right")')).to.deep.equal('24')
        expect(vm.indexInCommandLibrary('   var xx=33')).to.deep.equal('30')
        expect(vm.indexInCommandLibrary('varxx=dd')).to.equal(false)
        expect(vm.indexInCommandLibrary('var x')).to.equal('31')
        expect(vm.indexInCommandLibrary('varx')).to.equal(false)
        expect(vm.indexInCommandLibrary('nancy.wait(30)')).to.deep.equal('32')
        expect(vm.indexInCommandLibrary('nancy.wait(dd)')).to.deep.equal('32')
        expect(vm.indexInCommandLibrary('wait(\'hha\')')).to.equal(false)
    })

    it('getSafeCode', () => {
        expect(vm.getSafeCode('Nancy.collect("key")')).to.equal('this.collect(0, "key");')
        expect(vm.getSafeCode('Carla.collect("key")')).to.equal('this.collect(1, "key");')
        // expect(vm.getSafeCode('collect("key")')).to.equal(false)
        expect(vm.getSafeCode('Nancy.drop("key")')).to.equal('this.drop(0, "key");')
        expect(vm.getSafeCode('Nancy.fly()')).to.equal('this.fly(0);')
        expect(vm.getSafeCode('Nancy.go(55)')).to.equal('this.go(0, 55);')
        expect(vm.getSafeCode('function-end')).to.equal('\';')
        expect(vm.getSafeCode('function run')).to.equal('this.functionSet[\'run\']=\'')
        expect(vm.getSafeCode('run()')).to.deep.equal('eval(this.functionSet["run"]);')
        expect(vm.getSafeCode('repeat 3 times')).to.equal('for(let i = 0; i < 3; i++) {')
        expect(vm.getSafeCode('repeat-end')).to.equal('}')
        expect(vm.getSafeCode('var x=3')).to.equal('var x=3;')
        expect(vm.getSafeCode('var y')).to.equal('var y;')
        expect(vm.getSafeCode('Nancy.wait(30)')).to.equal('this.wait(0, 30);')
    })
})
