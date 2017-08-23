import SelectLevel from '@/components/SelectLevel'
import Vue from 'vue'
import ElementUI from 'element-ui'
Vue.use(ElementUI)
import { createVue, destroyVM } from '../util'
import Mock from 'mockjs'
import 'whatwg-fetch'

Mock.mock(
    'api/login',
    'get',
    function (request) {
        let date = new Date(null)
        date = date.toLocaleString()
        return {
            status: '1',
            email: 'tom@123.com',
            id: 1,
            nickname: 'tom',
            gameProgress: 13,
            hasPaied: false,
            createdAt: date
        }
    }
)

Mock.mock(
    /api\/read-map/,
    'get',
    function (request) {
        let url = request.url
        let str = url.split('?')[1]
        let mapid = parseInt(str.split('=')[1])
        return {
            status: '1',
            msg: ('msg: ' + mapid.toString()),
            id: mapid,
            map: '111111',
            name: 'new map',
            tips: 'new tips',
            codes: 'new codes',
            mode: '[]',
            author: 'author'
        }
    }
)

describe('SelectLevel.vue', function () {
    let vm
    beforeEach(async function () {
        vm = createVue(SelectLevel, true)
        vm.$store.dispatch('init')
        await vm.$store.dispatch('signin')
    })

    afterEach(function () {
        destroyVM(vm)
    })

    it('挂载成功', function () {
        expect(vm.selectLevelDialog).to.equal(false)
        expect(vm.$store.state.userGameProgress).to.equal(13)
    })

    it('选择之前玩过关卡', async function () {
        await vm.selectLevel(1)
        await expect(vm.$store.state.mapId).to.equal(1)
    })

    it('选择未解锁关卡', async function () {
        await vm.selectLevel(15)
        await expect(vm.$store.state.mapId).to.equal(1)
    })

    it('showDialog', function () {
        vm.showDialog()
        expect(vm.selectLevelDialog).to.equal(true)
    })
})
