import EditorBase from '@/components/EditorBase'
import { createVue, destroyVM } from '../util'

describe('editor', () => {
    let vm
    afterEach(() => {
        destroyVM(vm)
    })

    it('mounted挂载成功', () => {
        vm = createVue(EditorBase, true)
        expect(vm.jsEditor.getValue()).to.equal('go(5)')
        expect(vm.direct).to.equal(2)
        // TODO 测试pre是否成功转换
    })

    it('cleanWorkspace函数执行成功', () => {
        vm = createVue(EditorBase, true)
        vm.cleanWorkspace()
        expect(vm.jsEditor.getValue()).to.equal('')
    })

    it('getCommandCodeList函数执行成功', () => {
        vm = createVue(EditorBase, true)
        vm.jsEditor.setValue([
            'go(3);  go(5)    ',
            '                 ',
            '     turn(left);;',
            'go(5)            '
        ].join('\n'))
        let commandList = vm.getCommandCodeList()
        expect(commandList).to.deep.equal(['go(3)', 'go(5)', 'turn(left)', 'go(5)'])
    })

    it('getTypeOfCode函数执行成功', () => {
        vm = createVue(EditorBase, true)
        let type = vm.getTypeOfCode('turn(right)')
        expect(type).to.equal(1)
        type = vm.getTypeOfCode('turn(left)')
        expect(type).to.equal(2)
        type = vm.getTypeOfCode('turn(1)')
        expect(type).to.equal(0)
        type = vm.getTypeOfCode('go(5)')
        expect(type).to.equal(3)
        type = vm.getTypeOfCode('go(4')
        expect(type).to.equal(0)
        type = vm.getTypeOfCode('4)')
        expect(type).to.equal(0)
        type = vm.getTypeOfCode('go(string1)')
        expect(type).to.equal(0)
        type = vm.getTypeOfCode('xxxxx')
        expect(type).to.equal(0)
    })

    it('tinyEditorRun函数运行成功', () => {
        // TODO 编写测试程序
    })

    it('点击run按钮正常运行', () => {
        // TODO 编写测试程序
    })

    it('点击clean按钮正常清空', () => {
        // TODO 编写测试程序
    })
})
