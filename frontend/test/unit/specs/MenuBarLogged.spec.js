import MenuBarLogged from '@/components/MenuBarLogged'
import Vue from 'vue'
import ElementUI from 'element-ui'
Vue.use(ElementUI)
import { createVue, destroyVM } from '../util'
import Mock from 'mockjs'
import 'whatwg-fetch'

Mock.mock(
    'api/logout',
    'post',
    {
        status: '1'
    }
)

Mock.mock(
    'api/pay',
    'get',
    {
        status: '1',
        url: 'test'
    }
)

describe('MenuBarLogged.vue', function () {
    let vm

    beforeEach(function () {
        vm = createVue(MenuBarLogged, true)
        vm.$store.dispatch('init')
        vm.$store.commit('changeMenu', 'menu-bar-logged')
        vm.$store.commit('changeLoginStatus', true)
    })

    afterEach(function () {
        destroyVM(vm)
    })

    it('挂载成功', function () {
        expect(vm.$store.state.currentMenbar).to.equal('menu-bar-logged')
        expect(vm.$store.state.loginStatus).to.equal(true)
    })

    it('#signout()', function () {
        vm.$store.dispatch('signout')
        expect(vm.$store.state.currentMenbar).to.equal('menu-bar-unlogged')
        expect(vm.$store.state.loginStatus).to.equal(false)
    })

    it('#pay()', function () {
        vm.pay()
    })
})
