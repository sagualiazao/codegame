// The path is relative to the project root.
import BlockBase from '@/components/BlockBase'

describe('BlockBase.vue', () => {
    it('expect the direct to be 2', () => {
        // Extend the component to get the constructor, which we can then initialize directly.
        expect(typeof BlockBase.data).to.equal('function')
        const defaultData = BlockBase.data()
        expect(defaultData.direct).to.equal(2)
    })
})
