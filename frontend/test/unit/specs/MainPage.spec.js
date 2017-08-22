import Vue from 'vue'
import ElementUI from 'element-ui'
import MainPage from '@/components/MainPage'
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

describe('MainPage.vue', function () {
    let vm

    beforeEach(async function () {
        vm = createVue(MainPage, true)
        vm.$store.dispatch('init')
        await vm.$store.dispatch('signin')
    })

    afterEach(function () {
        destroyVM(vm)
    })

    it('挂载成功', function () {
        expect(vm.$store.state.loginStatus).to.equal(true)
    })
})
