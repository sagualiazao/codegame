<template>
<div class="edit-map">
    <div id="map1">
        <el-tabs ref="tabs" v-model="activeName" type="card" @tab-click="handleClick">
            <el-tab-pane :label="$store.state._const.EDIT_MAP" name="map-editor">
                <map-editor></map-editor>
            </el-tab-pane>
            <el-tab-pane :label="$store.state._const.MY_DISIGNED_MAPS" name="my-map">
                <div v-for="map in myMapList">
                    <div class="map-picture">
                        <a @click="enterMap(map[0])"><img :src="map[2]" :alt="$store.state._const.WRONG_DISPLAY"></a>
                        <div class="caption">
                            <p class="mapname">
                                {{ $store.state._const.MAP_NAME }}: {{ map[1] }}
                            </p>
                            <p class="remarks">
                                {{ $store.state._const.MAP_REMARKS }}: {{ map[3] }}
                            </p>
                            <div v-if="map[4] === true">
                                <i class="el-icon-circle-check" @click="publishClick(map, false)" :title="$store.state._const.CLICK_TO_CANCEL_PUBLISH">
                                    {{ $store.state._const.MAP_PUBLISHED }}
                                </i>
                                <i class="el-icon-delete" @click="deleteClick(map)">
                                    {{ $store.state._const.DELETE_MAP }}
                                </i>
                            </div>
                            <div v-else>
                                <i class="el-icon-upload" @click="publishClick(map, true)" title="$store.state._const.CLICK_TO_PUBLISH">
                                    {{ $store.state._const.MAP_UNPUBLISHED }}
                                </i>
                                <i class="el-icon-delete" @click="deleteClick(map)">
                                    {{ $store.state._const.DELETE_MAP }}
                                </i>
                            </div>
                        </div>
                    </div>
                </div>
            </el-tab-pane>
        </el-tabs>
    </div>
</div>
</template>


<script>
/**
* EditMap 组件中完成制作地图的功能
*
* @class EditMap
*/
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import store from '@/assets/js/store.js'
import MapEditor from './MapEditor'
import { simpleGet, simplePost, readMap } from '@/assets/js/util.js'

export default {
    name: 'edit-map',
    store: store,
    data: function () {
        return {
            /**
            *激活的界面
            *
            * @property activeName
            * @type {String}
            * @default 'map-editor'
            */
            activeName: 'map-editor',
            /**
            *我的地图列表
            *
            * @property myMapList
            * @type {Object}
            * @default null
            */
            myMapList: null
        }
    },
    components: {
        MapEditor
    },
    /**
    *vue组件的mounted函数, 判断登录状态, 调用初始化函数
    *
    *@method mounted
    */
    mounted: async function () {
        if (this.$store.state.loginStatus === false) {
            await this.$store.dispatch('signin')
            if (await this.$store.state.loginStatus === false) {
                alert(this.$store.state._const.LOGIN_FIRST)
                this.$router.push('/')
            } else {
                this.init()
            }
        } else {
            this.init()
        }
    },
    methods: {
        /**
        *初始化函数, 调用readMyMapList函数
        *
        *@method init
        */
        init: function () {
            this.readMyMapList()
        },
        /**
        *切换标签页
        * @method handleClick
        * @param {Object} tab 标签页
        * @param {Event} event 事件
        */
        handleClick: function (tab, event) {},
        /**
        *点击发布按钮的相应函数
        * @method publishClick
        * @param {Object} map
        * @param {Boolean} status
        */
        publishClick: function (map, status) {
            map[4] = status
            this.changePublishStatus(map[0], status)
        },
        /**
        *点击删除按钮的相应函数
        * @method deleteClick
        * @param {Object} map
        */
        deleteClick (map) {
            this.confirmDelete(map[0])
        },
        /**
        *进入地图游戏界面
        * @method enterMap
        * @param {Number} id
        */
        enterMap: async function (id) {
            this.$store.commit('changeLevelMode', false)
            this.$store.commit('changeGameID', id)
            let response = await readMap(false, id)
            let obj = await response.json()
            if (await obj.status === '1') {
                this.$store.commit('changeMap', obj)
                this.$router.push('/BlockBase')
            }
        },
        /**
        *读取数据库地图列表
        * @method readMyMapList
        */
        readMyMapList: async function () {
            let response = await simpleGet('api/read-my-map-list')
            let obj = await response.json()
            if (await obj.status === '1') {
                if (obj.number > 0) {
                    let list = JSON.parse(obj.data)
                    this.myMapList = list
                    // 返回mapmap一个数组对象, for map in mapList
                    // map[0]: id 地图id
                    // map[1]: name 地图名称
                    // map[2]: img 地图缩略图
                    // map[3]: remarks 地图说明
                    // map[4]: favorite 收藏发布状态
                }
            } else if (await obj.status === '0') {
                alert(this.$store.state._const.LOAD_FAILURE)
            }
        },
        /**
        *更改发布状态
        * @method changePublishStatus
        * @param {Number} id
        * @param {Boolean} status
        */
        changePublishStatus: async function (id, status) {
            let jsonObj = {
                'mapid': id,
                'status': Number(status).toString()
            }
            let response = await simplePost('api/change-publish', jsonObj)
            let obj = await response.json()
            if (await obj.status === '1') {
                this.readMyMapList()
            }
        },
        /**
        *删除地图
        * @method deleteMap
        * @param {Number} id
        */
        deleteMap: async function (id) {
            let jsonObj = {
                'mapid': id
            }
            let response = await simplePost('api/delete-map', jsonObj)
            let obj = await response.json()
            if (await obj.status === '1') {
                this.readMyMapList()
            }
        },
        /**
        *删除地图提示确认的响应函数
        * @method confirmDelete
        * @param {Number} id
        */
        confirmDelete: function (id) {
            let successMsg = this.$store.state._const.DELETE_SUCCESS
            let failureMsg = this.$store.state._const.DELETE_FAILURE
            let deleteMap = this.deleteMap
            this.$confirm(
                this.$store.state._const.DELETE_CONFIRM_INFORMATION,
                this.$store.state._const.TIPS,
                {
                    confirmButtonText: this.$store.state._const.CONFIRM,
                    cancelButtonText: this.$store.state._const.CANCEL,
                    type: 'warning'
                }).then(() => {
                    deleteMap(id)
                    this.$message({
                        type: 'success',
                        message: successMsg
                    })
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: failureMsg
                    })
                })
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
div.map-picture {
    border: 1px solid #BFBFBF;
    text-align: center;
    float: left;
    width: 20%;
    height: auto;
    margin: 2%;
    display: block;
    /*box-sizing: border-box;*/
    overflow: hidden;
}
div.map-picture:hover {
    border: 1px solid #777;
}
.caption {
    text-align: center;
    font-weight: normal;
    width: 100%;
    font-size: 0.7em;
    margin: 10px 5px 10px 5px;
  }
  .map-picture a {
      display: block;
  }
  /*.map-picture a p {
      display: none;
      transform: scale(1);
  }*/
.map-picture img {
    width: 80%;
    height: auto;
    display: block;
    margin: 10%;
}
img {
    opacity: 0.8;
    filter: alpha(opacity = 40); /* For IE8 and earlier */
    transition: all 0.5s;
}
img:hover {
    opacity: 1.0;
    filter: alpha(opacity = 100); /* For IE8 and earlier */
    transform: scale(1.2);
    /*border: 1px solid #333333;*/
    /*box-shadow: 0 0 2px 1px rgba(0, 140, 186, 0.5);*/
    overflow: hidden;
}
@media only screen and (max-width: 700px){
    .map-picture {
        width: 49.99999%;
        margin: 6px 0;
    }
}
.el-icon-upload {
    float: left;
    color: #2E8B57;
}
.el-icon-circle-check {
    float: left;
    color:#FFA07A;
    cursor: pointer;
}
.el-icon-delete {
    float: right;
    margin-right: 2px;
    color: #4169E1;
    cursor: pointer;
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
