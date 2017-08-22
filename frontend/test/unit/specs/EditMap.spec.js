// import Vue from 'vue'
// import ElementUI from 'element-ui'
// import EditMap from '@/components/EditMap'
// import { createVue, destroyVM } from '../util'
// Vue.use(ElementUI)
// import Mock from 'mockjs'
// import 'whatwg-fetch'

// Mock.mock(
//     'api/login',
//     'get',
//     function (request) {
//         let date = new Date(null)
//         date = date.toLocaleString()
//         return {
//             status: '1',
//             email: 'tom@123.com',
//             id: 1,
//             nickname: 'tom',
//             gameProgress: 13,
//             hasPaied: false,
//             createdAt: date
//         }
//     }
// )

// Mock.mock(
//     'api/read-my-map-list',
//     'get',
//     {
//         status: '1',
//         data: '{[1, "map one", "imgimg", "no remarks", false]}'
//     }
// )

// Mock.mock(
//     'api/change-publish',
//     'post',
//     function (request) {
//         let obj = request.body
//         let mapId = obj.mapid
//         return {
//             status: '1',
//             msg: mapId
//         }
//     }
// )

// Mock.mock(
//     'api/delete-map',
//     'post',
//     function (request) {
//         let obj = request.body
//         let mapId = obj.mapid
//         return {
//             status: '1',
//             msg: mapId
//         }
//     }
// )

// describe('EditMap', function () {
//     let vm

//     beforeEach(async function () {
//         vm = createVue(EditMap, true)
//         vm.$store.dispatch('init')
//         await vm.$store.dispatch('signin')
//         await vm.init()
//     })

//     afterEach(function () {
//         destroyVM(vm)
//     })

//     it('挂载成功', function () {
//         expect(vm.activeName).to.equal('map-editor')
//         expect(vm.myMapList).to.equal(null)
//     })
// })
