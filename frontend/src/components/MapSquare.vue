<template>
<div class="map-square">
    <el-tabs ref="tabs" v-model="activeName" @tab-click="handleClick">
        <el-tab-pane label="地图广场" name="first" class="map-square-tab">
            <div v-for="(map, index) in mapList">
                <div class="map-picture">
                    <a href="#BlockBase"><img :src="map[3]" class="image" alt="显示错误">
                    <span class="tips">点击图片进入此游戏</span></a>
                    <div class="caption">
                        <span class="mapname">地图名: {{ map[1] }}</span>
                        <span class="author">作者: {{ map[2] }}</span><br>
                        <span class="remarks">说明: {{ map[4] }}</span>
                        <div v-if="map[5] === false">
                            <i class="el-icon-star-off" @click="changeFavor(map, true)" title="点击收藏地图">收藏</i>
                        </div>
                        <div v-else>
                            <i class="el-icon-star-on" @click="changeFavor(map, false)" title="点击取消收藏">已收藏</i>
                        </div>
                    </div>
                    <hr>
                </div>
            </div>
            <button type="playMap" @click="playClick">试玩</button>
        </el-tab-pane>
        <el-tab-pane label="我发布的地图" name="second" class="published-map-tab">
            <div v-for="map in publishedMapList">
                <div class="map-picture">
                    <a href="#BlockBase"><img :src="map[2]" class="image" alt="显示错误"></a>
                    <div class="caption">
                        <span class="mapname">地图名: {{ map[1] }}</span><br>
                        <span class="remarks">说明: {{ map[3] }}</span>
                    </div>
                </div>
            </div>
        </el-tab-pane>
        <el-tab-pane label="我收藏的地图" name="third" class="favorite-map-tab">
            <div v-for="map in favoriteMapList">
                <div class="map-picture">
                    <a href="#BlockBase"><img :src="map[3]" class="image" alt="显示错误"></a>
                    <div class="caption">
                        <span class="mapname">地图名: {{ map[1] }}</span>
                        <span class="author">作者: {{ map[2] }}</span><br>
                        <span class="remarks">说明: {{ map[4] }}</span>
                        <i class="el-icon-star-on" @click="changeFavor(map, false)" title="点击取消收藏">已收藏</i>
                    </div>
                </div>
            </div>
        </el-tab-pane>
    </el-tabs>
</div>
</template>

<script>
import { simpleGet, simplePost } from '@/assets/js/util.js'

export default {
    name: 'map-square',
    data: function () {
        return {
            activeName: 'first',
            mapList: null,
            publishedMapList: null,
            favoriteMapList: null
        }
    },
    mounted: async function () {
        if (this.$store.state.loginStatus === false) {
            await this.$store.dispatch('signin')
            if (await this.$store.state.loginStatus === false) {
                alert('请先登录噢!')
                this.$router.push('/')
            } else {
                this.readMapList()
                this.readFavoriteMapList()
                this.readPublishedMapList()
            }
        } else {
            this.readMapList()
            this.readFavoriteMapList()
            this.readPublishedMapList()
        }
        this.readMapList()
        this.readFavoriteMapList()
        this.readPublishedMapList()
    },
    compute: {

    },
    methods: {
        handleClick (tab, event) {
        },
        playClick () {
        },
        changeFavor (map, status) {
            map[5] = status
            this.changeFavoriteMap(map[0], status)
        },
        readMapList: async function () {
            let response = await simpleGet('api/read-map-list')
            let obj = await response.json()
            if (await obj.status === '1') {
                let list = JSON.parse(obj.data)
                this.mapList = list
                // 返回一个数组对象, for map in mapList
                // map[0]: id 地图id
                // map[1]: name 地图名称
                // map[2]: author 地图作者
                // map[3]: img 地图缩略图
                // map[4]: remarks 地图说明
                // map[5]: favorite 收藏状态
            } else if (await obj.status === '0') {
                alert('读取失败!')
            }
        },
        readPublishedMapList: async function () {
            let response = await simpleGet('api/read-published-map-list')
            let obj = await response.json()
            if (await obj.status === '1') {
                let list = JSON.parse(obj.data)
                this.publishedMapList = list
                // 返回一个数组对象, for map in mapList
                // map[0]: id 地图id
                // map[1]: name 地图名称
                // map[2]: img 地图缩略图
                // map[3]: remarks 地图说明
                // map[4]: published 发布状态
            } else if (await obj.status === '0') {
                alert('读取失败!')
            }
        },
        readFavoriteMapList: async function () {
            let response = await simpleGet('api/read-favorite-map-list')
            let obj = await response.json()
            if (await obj.status === '1') {
                let list = JSON.parse(obj.data)
                this.favoriteMapList = list
                // 返回一个数组对象, for map in mapList
                // map[0]: id 地图id
                // map[1]: name 地图名称
                // map[2]: author 地图作者
                // map[3]: img 地图缩略图
                // map[4]: remarks 地图说明
            } else if (await obj.status === '0') {
                alert('读取失败!')
            }
        },
        changeFavoriteMap: async function (id, status) {
            let jsonObj = {
                'mapid': id,
                'status': Number(status).toString()
            }
            let response = await simplePost('api/change-favorite', jsonObj)
            let obj = await response.json()
            if (await obj.status === '1') {
                // TODO: 更改按钮显示状态
            }
            this.readMapList()
            this.readFavoriteMapList()
        },
        cancelPublishStatus: async function (id) {
            // 取消地图发布状态
            let jsonObj = {
                'mapid': id,
                'status': '0'
            }
            let response = await simplePost('api/change-publish', jsonObj)
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
.el-icon-star-on {
    color: orange;
}
div.map-picture {
    border: ridge 2px #ADD8E6;
    text-align: center;
    width: auto;
    height: auto;
    float: left;
    margin: 3px;
    display: block;
    box-sizing: border-box;
    transition: all .4s ease-in-out;
    overflow: hidden;
}
.caption {
    text-align: center;
    font-weight: normal;
    width: 150px;
    font-size: 12px;
    margin: 10px 5px 10px 5px;
  }
  .map-picture a {
      display: block;
  }
  .map-picture a span {
      display: none;
      transform: scale(1);
  }
  .map-picture a:hover span {
      display: block;
      text-align: center;
      width: 80%;
      vertical-align: center;
      position: absolute;
      overflow: hidden;
  }
img {
    width: auto;
    height: auto;
    display: block;
    margin: 3px;
}
img {
    opacity: 0.4;
    filter: alpha(opacity = 40); /* For IE8 and earlier */
    transition: all 0.5s;
}
img:hover {
    opacity: 1.0;
    filter: alpha(opacity = 100); /* For IE8 and earlier */
    transform: scale(1.1);
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
