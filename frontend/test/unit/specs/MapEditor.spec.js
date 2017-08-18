import MapEditor from '@/components/MapEditor'
import { createVue, destroyVM } from '../util'
import Vue from 'vue'
import ElementUI from 'element-ui'
import 'yuki-createjs'
Vue.use(ElementUI)

describe('MapEditor.vue', () => {
    let vm

    beforeEach(() => {
        vm = createVue(MapEditor, true)
        vm.init()
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
        expect(vm.items).to.equal(5)
        expect(vm.stage.numChildren).to.equal(7)
        expect(vm.randomColor).to.not.equal(0)
    })

    it('坐标函数执行成功', () => {
        expect(vm.toMapX(0)).to.equal(0)
        expect(vm.toMapY(200)).to.equal(3)
    })

    it('addPic函数执行', () => {
        let ox = vm.stage.x + vm.canvasWidth - vm.div - vm.bias
        let cc = vm.stage.numChildren
        vm.addPic(3, ox, vm.bias + vm.div * 3)
        expect(vm.stage.numChildren).to.equal(cc + 1)
        cc = vm.stage.numChildren
        vm.addPic(4, ox, vm.bias + vm.div * 4)
        expect(vm.stage.numChildren).to.equal(cc + 1)
        vm.havePlayer = true
        cc = vm.stage.numChildren
        vm.addPic(3, ox, vm.bias + vm.div * 3)
        expect(vm.stage.numChildren).to.equal(cc)
        vm.haveFlag = true
        cc = vm.stage.numChildren
        vm.addPic(4, ox, vm.bias + vm.div * 4)
        expect(vm.stage.numChildren).to.equal(cc)
        cc = vm.stage.numChildren
        vm.addPic(1, ox, vm.bias + vm.div * 1)
        expect(vm.stage.numChildren).to.equal(cc + 1)
        cc = vm.stage.numChildren
        vm.addPic(1, ox, vm.bias + vm.div * 1)
        expect(vm.stage.numChildren).to.equal(cc + 1)

    })

    it('remove函数对非传送门执行成功', () => {
        function create (i, x, y) {
            var con = new createjs.Container()
            var bitmap = new createjs.Bitmap('../../static/map/' + i + '.png')
            con.x = x
            con.y = y
            con.name = i
            con.addChild(bitmap)
            vm.stage.addChild(con)
            return con
        }
        vm.maps[2][2] = create (1, 0, 0)
        vm.remove(2, 2)
        expect(vm.maps[2][2]).to.equal(0)
        vm.maps[2][2] = 0
        vm.remove(2, 2)
        expect(vm.maps[2][2]).to.equal(0)
        vm.maps[2][2] = create (2, 0, 0)
        vm.remove(2, 2)
        expect(vm.maps[2][2]).to.equal(0)
        vm.maps[2][2] = create (3, 0, 0)
        vm.remove(2, 2)
        expect(vm.maps[2][2]).to.equal(0)
        expect(vm.havePlayer).to.equal(false)
        vm.maps[2][2] = create (4, 0, 0)
        vm.remove(2, 2)
        expect(vm.maps[2][2]).to.equal(0)
        expect(vm.haveFlag).to.equal(false)
        vm.maps[2][2] = create (5, 0, 0)
        vm.remove(2, 2)
        expect(vm.maps[2][2]).to.equal(0)
        expect(vm.haveFlag).to.equal(false)
    })
})
