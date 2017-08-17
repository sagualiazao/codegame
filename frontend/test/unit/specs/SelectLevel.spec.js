import SelectLevel from '@/components/SelectLevel'
import { createVue, destroyVM } from '../util'

describe('SelectLevel.vue', () => {
    let vm
    beforeEach(() => {
        vm = createVue(SelectLevel, true)
    })

    afterEach(() => {
        vm.$store.dispatch('init')
        destroyVM(vm)
    })

    it('按钮内容渲染成功', () => {
        expect(vm.$el.querySelector('#continue-play').textContent).to.equal('继续游戏')
    })
})
