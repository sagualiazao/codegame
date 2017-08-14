<template>
<div class="map-square">
    <el-tabs v-model="activeName" @tab-click="handleClick">
        <el-tab-pane label="地图广场" name="first">
            <img src="../assets/pc7.jpg">
            <img src="../assets/pc8.jpg">
            <img src="../assets/pc9.jpg">
            <img src="../assets/pc1.jpg">
            <img src="../assets/pc2.jpg">
            <img src="../assets/pc3.jpg">
            <img src="../assets/pc4.jpg">
            <img src="../assets/pc5.jpg">
            <img src="../assets/pc6.jpg">
            <img src="../assets/pc10.jpg">
            <img src="../assets/pc11.jpg">
            <img src="../assets/pc12.jpg">
            <button type="playMap" @click="playClick">试玩</button>
            <h1>这是地图广场</h1>
        </el-tab-pane>
        <el-tab-pane label="我发布的地图" name="second">
            <img src="../assets/pc5.jpg">
            <img src="../assets/pc8.jpg">
            <img src="../assets/pc10.jpg">
            <h1>这是我发布的地图</h1>
        </el-tab-pane>
        <el-tab-pane label="我收藏的地图" name="third">
            <img src="../assets/pc1.jpg">
            <img src="../assets/pc2.jpg">
            <img src="../assets/pc3.jpg">
            <img src="../assets/pc4.jpg">
            <h1>这是我收藏的地图</h1>
        </el-tab-pane>
    </el-tabs>
</div>
</template>

<script>
export default {
    name: 'map-square',
    data: function () {
        return {
            msg: '看到这行字，说明它正常了',
            activeName: 'first'
        }
    },
    methods: {
        handleClick (tab, event) {
        },
        playClick () {
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
    font-weight: normal;
}
img {
    width: 300px;
    height: 200px;
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
