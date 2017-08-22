import Vue from 'vue'
import ElementUI from 'element-ui'
import MapSquare from '@/components/MapSquare'
import { createVue, destroyVM } from '../util'
Vue.use(ElementUI)
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
    'api/read-map-list',
    'get',
    {
        status: '1',
        data: '{[1, "map one", "tom", "imgimg", "no remarks", false]}'
    }
)

Mock.mock(
    'api/read-published-map-list',
    'get',
    {
        status: '1',
        data: '{[1, "map one", "imgimg", "no remarks", true]}'
    }
)

Mock.mock(
    'api/read-favorite-map-list',
    'get',
    {
        status: '1',
        data: '{[1, "map one", "tom", "imgimg", "no remarks"]}'
    }
)

Mock.mock(
    'api/change-favorite',
    'post',
    function (request) {
        let obj = request.body
        return {
            mapid: obj.id,
            status: obj.status
        }
    }
)

Mock.mock(
    'api/change-publish',
    'post',
    {
        status: '1'
    }
)

describe('MapSquare.vue', function () {
    let vm

    beforeEach(async function () {
        vm = createVue(MapSquare, true)
        vm.$store.dispatch('init')
        await vm.$store.dispatch('signin')
        await vm.init()
    })

    afterEach(function () {
        destroyVM(vm)
    })

    it('挂载成功', function () {
        expect(vm.activeName).to.equal('first')
        expect(vm.mapList).to.equal(null)
        expect(vm.publishedMapList).to.equal(null)
        expect(vm.favoriteMapList).to.equal(null)
        expect(vm.currentPages).to.equal(1)
    })

    it('#changeFavoriteMap()', async function () {
        vm.changeFavoriteMap(1, true)
    })

    it('#cancelPublishedStatus()', async function () {
        vm.cancelPublishStatus(1)
    })
})
