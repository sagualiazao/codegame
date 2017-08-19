<template>
<div class="map-square">
    <el-tabs ref="tabs" v-model="activeName" @tab-click="handleClick">
        <el-tab-pane label="地图广场" name="first" class="map-square-tab">
            <div v-for="map in mapList">
                <div class="caption">
                    <p class="mapname">地图名称: {{ map[1] }}</p>
                    <p class="image"><img :src="map[3]" alt="显示错误"></p>
                    <p class="author">地图作者: {{ map[2] }}</p>
                    <p class="remarks">地图说明: {{ map[4] }}</p>
                    <div v-if="map[5] === false">
                        <i class="el-icon-star-off" @click="changeFavor(map, true)" title="点击收藏地图">收藏</i>
                    </div>
                    <div v-else>
                        <i class="el-icon-star-on" @click="changeFavor(map, false)">已收藏</i>
                    </div>
                </div>
            </div>
            <button type="playMap" @click="playClick">试玩</button>
        </el-tab-pane>
        <el-tab-pane label="我发布的地图" name="second" class="published-map-tab">
            <div v-for="map in publishedMapList">
                <div class="caption">
                    <p class="mapname">地图名称: {{ map[1] }}</p>
                    <p class="image"><img :src="map[2]" alt="显示错误"></p>
                    <p class="remarks">地图说明: {{ map[3] }}</p>
                </div>
            </div>
        </el-tab-pane>
        <el-tab-pane label="我收藏的地图" name="third" class="favorite-map-tab">
            <div v-for="map in favoriteMapList">
                <div class="caption">
                    <p class="mapname">地图名称: {{ map[1] }}</p>
                    <p class="image"><img :src="map[3]" alt="显示错误"></p>
                    <p class="author">地图作者: {{ map[2] }}</p>
                    <p class="remarks">地图说明: {{ map[4] }}</p>
                </div>
            </div>
        </el-tab-pane>
    </el-tabs>
</div>
</template>

<script>
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
    mounted () {
        if (this.$store.state.loginStatus === false) {
            alert('请先登录噢!')
            this.$router.push('/')
        }
        this.readMapList()
        this.readFavoriteMapList()
        this.readPublishedMapList()
    },
    methods: {
        handleClick (tab, event) {
        },
        playClick () {
        },
        collect () {
        },
        changeFavor (map, status) {
            map[5] = status
            this.changeFavoriteMap(map[0], status)
        },
        readMapList: async function () {
            let response = await fetch('api/read-map-list', {
                method: 'get',
                mode: 'cors',
                credentials: 'include'
            })
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
            let response = await fetch('api/read-published-map-list', {
                method: 'get',
                mode: 'cors',
                credentials: 'include'
            })
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
            let response = await fetch('api/read-favorite-map-list', {
                method: 'get',
                mode: 'cors',
                credentials: 'include'
            })
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
            let response = await fetch(
                ('api/change-favorite' + '?mapid=' + id + '&status=' + Number(status).toString()),
                {
                    method: 'get',
                    mode: 'cors',
                    credentials: 'include'
                }
            )
            let obj = await response.json()
            if (await obj.status === '1') {
                for (let i = 0; i < this.mapList.length; i++) {
                    if (mapList[i][0] === id) {
                        mapList[i][5] = status
                        break
                    }
                }
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
img {
    width: 300px;
    height: 200px;
}
img {
    opacity: 0.4;
    filter: alpha(opacity = 40); /* For IE8 and earlier */
}
img:hover {
    opacity: 1.0;
    filter: alpha(opacity = 100); /* For IE8 and earlier */
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
