import Vue from 'vue'
import MainPage from '@/components/MainPage'
import { createVue, destroyVM } from '../util'

describe('MainPage.vue', () => {
    let vm
    // 在每个测试之前执行的
    beforeEach(() => {
        // 创建组件实例
        vm = createVue(MainPage, true)
    })

    afterEach(() => {
        // 清理组件
        destroyVM(vm)
    })

    it('should render correct button content', () => {
        expect(vm.$el.querySelector('#start-game').textContent).to.equal('开始游戏')
    })

    it('should render correct text content', () => {
        expect(vm.$el.querySelector('#game-wordintro').textContent).to.equal('让孩子在游戏中走进编程世界，没有压力，开启头脑风暴')
        expect(vm.$el.querySelector('#intro1').textContent).to.equal('description1')
        expect(vm.$el.querySelector('#intro2').textContent).to.equal('description2')
        expect(vm.$el.querySelector('#intro3').textContent).to.equal('description3')
        expect(vm.$el.querySelector('#intro4').textContent).to.equal('description4')
    })
})
