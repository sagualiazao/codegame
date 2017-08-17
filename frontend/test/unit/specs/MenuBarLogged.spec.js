// 引入要测试的组件
import MenuBarLogged from '@/components/MenuBarLogged'
// 使用element的引入element
import Vue from 'vue'
import ElementUI from 'element-ui'
Vue.use(ElementUI)
// 引入util的封装
import { createVue, destroyVM } from '../util'

import Mock from 'mockjs'
import 'whatwg-fetch'

import { cbcDecrypt } from '@/assets/js/util'

Mock.mock(
    'api/logout',
    'post',
    {
        status: '1'
    }
)

describe('MenuBarLogged.vue', () => {
    let vm

    beforeEach(() => {
        vm = createVue(MenuBarLogged, true)
    })

    afterEach(() => {
        vm.$store.dispatch('init')
        destroyVM(vm)
    })

    it('点击按钮注销', () => {
        vm.$store.dispatch('signout')
        expect(vm.$store.state.currentMenbar).to.equal('menu-bar-unlogged')
        expect(vm.$store.state.loginStatus).to.equal(false)
    })
})
