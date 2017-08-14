<template>
<div class="edit-map">
    <div id="map1">
        <el-tabs ref="tabs" v-model="activeName" type="card" @tab-click="handleClick">
            <el-tab-pane label="制作地图" name="map-editor">
                <map-editor></map-editor>
            </el-tab-pane>
            <el-tab-pane label="我做的地图" name="my-map">
                <div class="published">
                    <h2>已发布</h2>
                    <img src="../assets/pc5.jpg">
                    <img src="../assets/pc8.jpg">
                    <img src="../assets/pc10.jpg">
                </div>
                <div class="unpublished">
                    <h2>未发布</h2>
                    <img src="../assets/pc13.jpg">
                    <img src="../assets/pc14.jpg">
                    <img src="../assets/pc15.jpg">
                    <img src="../assets/pc16.jpg">
                    <img src="../assets/pc17.jpg">
                    <img src="../assets/pc18.jpg">
                    <button type="publish-map" @click="publishClick">发布地图</button>
                </div>
            </el-tab-pane>
        </el-tabs>
    </div>
</div>
</template>


<script>
import MapEditor from './MapEditor'

export default {
    name: 'edit-map',
    data: function () {
        return {
            activeName: 'map-editor',
            activeIndex: 'published',
            msg: '看到这行字，说明它正常了'
        }
    },
    components: {
        MapEditor
    },
    methods: {
        handleClick (tab, event) {
        },
        saveClick () {
            // 这里保存地图
        },
        publishClick () {
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
