<template>
<div class="edit-map">
    <div id="map1">
        <el-tabs ref="tabs" v-model="activeName" type="card" @tab-click="handleClick">
            <el-tab-pane label="制作地图" name="map-editor">
                <map-editor></map-editor>
            </el-tab-pane>
            <el-tab-pane label="我做的地图" name="my-map">
                <div v-for="map in myMapList">
                    <div class="caption">
                        <p class="mapname">地图名称: {{ map[1] }}</p>
                        <p class="image"><img :src="map[2]" alt="显示错误"></p>
                        <p class="remarks">地图说明: {{ map[3] }}</p>
                        <p class="published-status">发布状态: {{ map[4] }}</p>
                        <hr>
                    </div>
                </div>
            </el-tab-pane>
        </el-tabs>
    </div>
</div>
</template>


<script>
import MapEditor from './MapEditor'
import { simpleGet } from '@/assets/js/util.js'

export default {
    name: 'edit-map',
    data: function () {
        return {
            activeName: 'map-editor',
            myMapList: null
        }
    },
    components: {
        MapEditor
    },
    mounted: async function () {
        if (this.$store.state.loginStatus === false) {
            await this.$store.dispatch('signin')
            if (await this.$store.state.loginStatus === false) {
                alert('请先登录噢!')
                this.$router.push('/')
            } else {
                this.readMyMapList()
            }
        } else {
            this.readMyMapList()
        }
    },
    methods: {
        handleClick: function (tab, event) {},
        publishClick: function () {},
        readMyMapList: async function () {
            let response = await simpleGet('api/read-my-map-list')
            let obj = await response.json()
            if (await obj.status === '1') {
                if (obj.number > 0) {
                    let list = JSON.parse(obj.data)
                    this.myMapList = list
                    // 返回一个数组对象, for map in mapList
                    // map[0]: id 地图id
                    // map[1]: name 地图名称
                    // map[2]: img 地图缩略图
                    // map[3]: remarks 地图说明
                    // map[4]: favorite 收藏发布状态
                }
            } else if (await obj.status === '0') {
                alert('读取失败!')
            }
        },
        changePublishStatus: async function (id, status) {
            // 取消地图发布状态
            let jsonObj = {
                'mapid': id,
                'status': Number(status).toString()
            }
            let response = await simplePost('api/change-publish', jsonObj)
            let obj = await response.json()
            if (await obj.status === '1') {
                // TODO: 刷新组件视图
            }
        },
        deleteMap: async function (id) {
            // 删除地图
            let jsonObj = {
                'mapid': id
            }
            let response = await simplePost('api/delete-map', jsonObj)
            let obj = await response.json()
            if (await obj.status === '1') {
                // TODO: 刷新组件视图
            }
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
    font-weight: normal;
}
h2 {
    color:#808000;
}
.published img, .unpublished img {
    width: 400px;
    height: 300px;
}
#map1 {
    margin-top: 20px;
}
button {
    display: inline-block;
    margin-top: 30px;
    margin-bottom: 10px;
    padding: 10px 20px;
    font-size: 14px;
    cursor: pointer;
    text-align: center;
    text-decoration: none;
    outline: none;
    color: white;
    background-color: #8FBC8F;
    border: none;
    border-radius: 15px;
    box-shadow: 5px 5px  5px #333;
}
button:hover {
    background-color: #D19275;
}
button:active {
    background-color: #D19275;
    box-shadow: 3px 5px #333;
    transform: translateY(4px);
}
</style>
