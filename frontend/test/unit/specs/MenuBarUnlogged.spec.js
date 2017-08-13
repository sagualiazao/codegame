// 引入要测试的组件
import MenuBarUnlogged from '@/components/MenuBarUnlogged'
// 引入子组件
import SigninForm from '@/components/SigninForm'
import SignupForm from '@/components/SignupForm'
import ResetPasswordForm from '@/components/ResetPasswordForm'
// 使用element的引入element
import Vue from 'vue'
import ElementUI from 'element-ui'
Vue.use(ElementUI)
// 引入util的封装
import { createVue, destroyVM } from '../util'
// 一个大的测试单元
describe('menubar-unlogged', () => {
    let vm
    // 在每个测试之前执行的
    beforeEach(() => {
        // 创建组件实例
        vm = createVue(MenuBarUnlogged, true)
    })

    afterEach(() => {
        // 清理组件
        destroyVM(vm)
    })

    it('mounted挂载成功', () => {
        // 使用vm.xxx访问xxx属性
        expect(vm.activeIndex).to.equal('main-page')
        // 使用vm.$store访问vuex
        expect(vm.$store.state.signinDialog).to.equal(false)
    })
})
