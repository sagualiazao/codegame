import BlockBase from '@/components/BlockBase'
import { createVue, destroyVM } from '../util'
import Blockly from '@/blockly'
global.Blockly = Blockly

describe ('BlockBase.vue', () => {
    let vm

    beforeEach(() => {
        vm = createVue(BlockBase, true)
    })

    afterEach(() => {
        destroyVM(vm)
    })

    it('mounted挂载成功', () => {
        expect(vm.direct).to.equal(2)
        expect(vm.functionSet).to.deep.equal({})
        let workspace = vm.workspace.getAllBlocks()
        expect(workspace).to.deep.equal([])
        expect(vm.mapWidth).to.equal(10)
        expect(vm.mapHeight).to.equal(10)
        expect(vm.speed).to.equal(1000)
        expect(vm.haveKey).to.equal(false)
        expect(vm.pic.x).to.equal(vm.mapx)
        expect(vm.pic.y).to.equal(vm.mapy)
        expect(vm.tween).to.not.equal(null)
    })

    it('点击运行按钮正常执行动画', () => {
        // TODO 动画执行成功的测试 争取对各个运行函数更高的覆盖率

    })

    it('点击运行按钮后direct和functionSet恢复默认值', () => {
        vm.direct = 4
        vm.functionSet = {'Run': 'go(5);'}
        let buttonElm = vm.$el.querySelector('.run-button')
        buttonElm.click()
        setTimeout(done => {
            expect(vm.direct).to.equal(2)
            expect(vm.functionSet).to.deep.equal({})
            done()
        }, 100)
    })

    it('点击editor正常切换', () => {
        // TODO 测试router正常切换
    })
})
