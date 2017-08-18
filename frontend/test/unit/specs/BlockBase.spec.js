import BlockBase from '@/components/BlockBase'
import { createVue, destroyVM } from '../util'
import Blockly from '@/blockly'
global.Blockly = Blockly

describe('BlockBase.vue', () => {
    let vm

    beforeEach(() => {
        vm = createVue(BlockBase, true)
        vm.maps = [
            ['6', '1', '0', '2', '0', '1', '0', '1', '0', '1'],
            ['7', '1', '0', '2', '0', '1', '0', '1', '0', '1'],
            ['8', '1', '0', '2', '0', '1', '3', '1', '0', '1'],
            ['0', '1', '0', '2', '0', '1', '0', '1', '0', '1'],
            ['9', '1', '0', '1', '0', '1', '0', '1', '0', '1'],
            ['54', '1', '0', '0', '50', '0', '0', '0', '0', '0'],
            ['0', '1', '0', '1', '0', '1', '0', '1', '0', '1'],
            ['0', '1', '0', '1', '0', '1', '0', '1', '0', '1'],
            ['0', '1', '0', '1', '0', '1', '0', '1', '0', '1'],
            ['0', '1', '0', '1', '0', '1', '0', '1', '0', '1']
        ]
    })

    afterEach(() => {
        destroyVM(vm)
    })
    it('mounted挂载成功', () => {
        expect(vm.functionSet).to.deep.equal({})
        let workspace = vm.workspace.getAllBlocks()
        expect(workspace).to.deep.equal([])
        expect(vm.mapWidth).to.equal(10)
        expect(vm.mapHeight).to.equal(10)
        expect(vm.speed).to.equal(1000)
        expect(vm.haveKey).to.equal(false)
        expect(vm.pic.x).to.equal(vm.mapx)
        expect(vm.pic.y).to.equal(vm.mapy)
        expect(vm.tween).to.not.equal([])
        expect(vm.direct).to.not.equal([])
    })
    
    it('go函数正常运行', () => {
        vm.direct[0] = 2
        vm.go(0, 3)
        expect(vm.player[0].x).to.equal(vm.toScreenX(5))
        expect(vm.player[0].y).to.equal(vm.toScreenY(6))
        vm.direct[0] = 3
        vm.go(0, 2)
        expect(vm.player[0].x).to.equal(vm.toScreenX(5))
        expect(vm.player[0].y).to.equal(vm.toScreenY(8))
        vm.direct[0] = 4
        vm.go(0, 3)
        expect(vm.player[0].x).to.equal(vm.toScreenX(2))
        expect(vm.player[0].y).to.equal(vm.toScreenY(8))
        vm.direct[0] = 1
        vm.go(0, 3)
        expect(vm.player[0].x).to.equal(vm.toScreenX(2))
        expect(vm.player[0].y).to.equal(vm.toScreenY(8))
        // TODO 动画执行成功的测试 争取对各个运行函数更高的覆盖率
    })

    it('点击运行按钮正常执行动画', () => {
        vm.direct[0] = 2
        vm.turn(0, 'right')
        expect(vm.direct[0]).to.equal(3)
        vm.turn(0, 'right')
        expect(vm.direct[0]).to.equal(4)
        vm.turn(0, 'right')
        expect(vm.direct[0]).to.equal(1)
        vm.turn(0, 'right')
        expect(vm.direct[0]).to.equal(2)
        vm.turn(0, 'left')
        expect(vm.direct[0]).to.equal(1)
        vm.turn(0, 'left')
        expect(vm.direct[0]).to.equal(4)
        vm.turn(0, 'left')
        expect(vm.direct[0]).to.equal(3)
        vm.turn(0, 'left')
        expect(vm.direct[0]).to.equal(2)
        // TODO 动画执行成功的测试 争取对各个运行函数更高的覆盖率

    })
    it('fly函数可以运行', () => {
        vm.direct[0] = 2
        vm.go(0, 3)
        vm.fly(0)
        expect(vm.player[0].x).to.equal(vm.toScreenX(5))
        expect(vm.player[0].y).to.equal(vm.toScreenY(6))
        vm.direct[0] = 1
        vm.go(0, 2)
        expect(vm.player[0].x).to.equal(vm.toScreenX(5))
        expect(vm.player[0].y).to.equal(vm.toScreenY(4))
        vm.fly(0)
        expect(vm.player[0].x).to.equal(vm.toScreenX(5))
        expect(vm.player[0].y).to.equal(vm.toScreenY(0))
        vm.direct[0] = 2
        vm.go(0, 1)
        expect(vm.player[0].x).to.equal(vm.toScreenX(6))
        expect(vm.player[0].y).to.equal(vm.toScreenY(0))
    })

    it('say wait函数可以运行', () => {
        let cc = vm.stage.numChildren
        vm.saywords(0, 'hello')
        expect(vm.stage.numChildren).to.equal(cc + 2)
        setTimeout(function () {
            expect(vm.stage.numChildren).to.equal(cc)
        }, 500)
        vm.wait(0, 0.5)
        vm.say(0, 'cc')
        vm.direct[0] = 2
        vm.go(0, 3)
        expect(vm.player[0].x).to.equal(vm.toScreenX(5))
        expect(vm.player[0].y).to.equal(vm.toScreenY(6))
    })
    it('collect drop 位置正确时可以运行', () => {
        vm.direct[1] = 2
        vm.go(1, 1)
        expect(vm.player[1].x).to.equal(vm.toScreenX(1))
        expect(vm.player[1].y).to.equal(vm.toScreenY(0))
        expect(vm.haveKey).to.equal(false)
        expect(vm.maps[1][0]).to.not.equal('0')
        vm.collect(1, 'key')
        expect(vm.player[1].x).to.equal(vm.toScreenX(1))
        expect(vm.player[1].y).to.equal(vm.toScreenY(0))
        expect(vm.haveKey).to.equal(true)
        expect(vm.maps[1][0]).to.equal('0')
        vm.go(1, 1)
        expect(vm.maps[2][0] === '0').to.equal(false)
        expect(vm.maps[4][0] === '0').to.equal(false)
        vm.drop(1, 'key')
        expect(vm.player[1].x).to.equal(vm.toScreenX(2))
        expect(vm.player[1].y).to.equal(vm.toScreenY(0))
        expect(vm.haveKey).to.equal(false)
        expect(vm.maps[2][0] === '0').to.equal(true)
        expect(vm.maps[4][0] === '0').to.equal(true)
    })

    it('collect drop 位置不正确时可以运行', () => {
        vm.direct[1] = 2
        vm.collect(1, 'key')
        expect(vm.player[1].x).to.equal(vm.toScreenX(0))
        expect(vm.player[1].y).to.equal(vm.toScreenY(0))
        expect(vm.haveKey).to.equal(false)
        expect(vm.maps[1][0]).to.not.equal('0')
        vm.go(1, 1)
        expect(vm.player[1].x).to.equal(vm.toScreenX(1))
        expect(vm.player[1].y).to.equal(vm.toScreenY(0))
        vm.collect(1, 'cc')
        expect(vm.player[1].x).to.equal(vm.toScreenX(1))
        expect(vm.player[1].y).to.equal(vm.toScreenY(0))
        expect(vm.haveKey).to.equal(false)
        expect(vm.maps[1][0]).to.not.equal('0')
        vm.collect(1, 'key')
        expect(vm.haveKey).to.equal(true)
        expect(vm.maps[1][0]).to.equal('0')
        vm.go(1, 2)
        expect(vm.maps[2][0] === '0').to.equal(false)
        expect(vm.maps[4][0] === '0').to.equal(false)
        vm.drop(1, 'cc')
        expect(vm.player[1].x).to.equal(vm.toScreenX(3))
        expect(vm.player[1].y).to.equal(vm.toScreenY(0))
        expect(vm.haveKey).to.equal(true)
        expect(vm.maps[2][0] === '0').to.equal(false)
        expect(vm.maps[4][0] === '0').to.equal(false)
        expect(vm.maps[3][0] === '7').to.equal(false)
        vm.drop(1, 'key')
        expect(vm.player[1].x).to.equal(vm.toScreenX(3))
        expect(vm.player[1].y).to.equal(vm.toScreenY(0))
        expect(vm.haveKey).to.equal(false)
        expect(vm.maps[2][0] === '0').to.equal(false)
        expect(vm.maps[4][0] === '0').to.equal(false)
        expect(vm.maps[3][0]).to.equal('7')
        vm.collect(1, 'key')
        expect(vm.haveKey).to.equal(true)
        expect(vm.maps[3][0]).to.equal('0')
        vm.turn(1, 'left')
        vm.turn(1, 'left')
        vm.go(1, 1)
        vm.drop(1, 'key')
        expect(vm.player[1].x).to.equal(vm.toScreenX(2))
        expect(vm.player[1].y).to.equal(vm.toScreenY(0))
        expect(vm.haveKey).to.equal(false)
        expect(vm.maps[2][0] === '0').to.equal(true)
        expect(vm.maps[4][0] === '0').to.equal(true)
    })

})
