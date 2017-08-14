// 引入要测试的组件
import MenuBarLogged from '@/components/MenuBarLogged'
// 使用element的引入element
import Vue from 'vue'
import ElementUI from 'element-ui'
Vue.use(ElementUI)
// 引入util的封装
import { createVue, destroyVM } from '../util'

describe('menubar-unlogged', () => {
    let vm

    beforeEach(() => {
        vm = createVue(MenuBarLogged, true)
    })

    afterEach(() => {
        destroyVM(vm)
    })

    it('点击按钮注销', () => {
        let buttonElm = vm.$el.querySelector('.signout-button')
        buttonElm.click()
        expect(vm.$store.state.currentMenbar).to.equal('menu-bar-unlogged')
        expect(vm.$store.state.loginStatus).to.equal(false)
    })
})
