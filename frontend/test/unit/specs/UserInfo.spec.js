import Vue from 'vue'
import ElementUI from 'element-ui'
import UserInfo from '@/components/UserInfo'
import { createVue, destroyVM } from '../util'
Vue.use(ElementUI)

// 测试脚本里面应该包括一个或多个describe块，称为测试套件（test suite）
describe('UserInfo', () => {
    // 每个describe块应该包括一个或多个it块，称为测试用例（test case）
    let vm

    beforeEach(() => {
        // 创建组件实例
        vm = createVue(UserInfo, true)
        vm.$store.state.userNickName = 'Hello'
        vm.$store.state.userEmail = '123@qq.com'
        vm.$store.state.registerDate = '2017-08-06'
    })

    afterEach(() => {
        vm.$store.dispatch('init')
        destroyVM(vm)
    })

    it('should render correct contents', () => {
        expect(vm.$el.querySelector('.user-info h1').textContent).to.equal('个人主页')
        expect(vm.$el.querySelector('.base-info span').textContent).to.equal('昵称')
        expect(vm.$el.querySelector('.game-info span').textContent).to.equal('已完成的关卡数')
        expect(vm.$el.querySelector('.change-name-form h2').textContent).to.equal('修改昵称')
        expect(vm.$el.querySelector('.change-password-form h2').textContent).to.equal('修改密码')
        expect(vm.activeName === 'base-tab')
    })

    it('should set correct data', () => {
        expect(vm.$store.state.userNickName).to.equal('Hello')
        expect(vm.$store.state.userEmail).to.equal('123@qq.com')
        expect(vm.$store.state.registerDate).to.equal('2017-08-06')
        expect(vm.finishedLevel).to.equal('')
        expect(vm.remainedLevel).to.equal('')
        expect(vm.nickname).to.equal('')
    })

    it('active-name,#handleClick', done => {
        setTimeout(_ => {
            const paneList = vm.$el.querySelector('.el-tabs__content').children
            const tabList = vm.$refs.tabs.$refs.nav.$refs.tabs

            expect(tabList[0].classList.contains('is-active')).to.be.true
            expect(paneList[0].style.display).to.not.ok

            tabList[3].click()
            vm.$nextTick(_ => {
                expect(tabList[3].classList.contains('is-active')).to.be.true
                expect(paneList[3].style.display).to.not.ok
                expect(vm.activeName === 'set-account-tab')
                done()
            })
        }, 100)
    })

    it('change nickname', async function () {
        vm.nickname = 'xy'
        await vm.nameSubmit()
        await expect(vm.$store.state.userNickName).to.equal('xy')
    })
})
