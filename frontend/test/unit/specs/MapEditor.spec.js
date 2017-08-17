import MapEditor from '@/components/MapEditor'
import { createVue, destroyVM } from '../util'
describe('MapEditor.vue', () => {
    let vm

    beforeEach(() => {
        vm = createVue(MapEditor, true)
    })

    afterEach(() => {
        destroyVM(vm)
    })

    it('mounted挂载成功', () => {
        expect(vm.mapWidth).to.equal(10)
        expect(vm.mapHeight).to.equal(10)
        expect(vm.div).to.equal(64)
        expect(vm.bias).to.equal(30)
        expect(vm.stage).to.not.equal(null)
        expect(vm.mapContainer).to.not.equal(null)
        expect(vm.maps).to.not.equal([])
        expect(vm.items).to.equal(4)
        expect(vm.stage.numChildren).to.equal(5)
        expect(vm.randomColor).to.not.equal(0)
    })

    it('坐标函数执行成功', () => {
        expect(vm.toMapX(200)).to.equal(3)
        expect(vm.toMapY(200)).to.equal(3)
    })

    it('mousedown事件监听成功', () => {
        
        // TODO 动画执行成功的测试 争取对各个运行函数更高的覆盖率

    })

    // it('点击运行按钮后direct和functionSet恢复默认值', () => {
    //     vm.direct = 4
    //     vm.functionSet = {'Run': 'go(5);'}
    //     let buttonElm = vm.$el.querySelector('.run-button')
    //     buttonElm.click()
    //     setTimeout(done => {
    //         expect(vm.direct).to.equal(2)
    //         expect(vm.functionSet).to.deep.equal({})
    //         done()
    //     }, 100)
    // })

    it('点击editor正常切换', () => {
        // TODO 测试router正常切换
    })
})
