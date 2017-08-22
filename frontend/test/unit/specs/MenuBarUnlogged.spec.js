import MenuBarUnlogged from '@/components/MenuBarUnlogged'
import SigninForm from '@/components/SigninForm'
import SignupForm from '@/components/SignupForm'
import ResetPasswordForm from '@/components/ResetPasswordForm'
import Vue from 'vue'
import ElementUI from 'element-ui'
Vue.use(ElementUI)
import { createVue, destroyVM } from '../util'

describe('menubar-unlogged', () => {
    let vm

    beforeEach(() => {
        vm = createVue(MenuBarUnlogged, true)
        vm.$store.dispatch('init')
    })

    afterEach(() => {
        destroyVM(vm)
    })

    it('挂载成功', () => {
        expect(vm.activeIndex).to.equal('main-page')
    })

    it('#signupChange()', function () {
        vm.signupChange()
        expect(vm.$store.state.signupDialog).to.equal(true)
    })

    it('#signinChange()', function () {
        vm.signinChange()
        expect(vm.$store.state.signinDialog).to.equal(true)
    })
})
