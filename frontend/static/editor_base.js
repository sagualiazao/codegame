function TinyEditor () {
	ace.require('ace/ext/language_tools')
    this.init()
}

let buffer = {

	//-- 缓存编辑器元素

	//-- 缓存编辑器  通过ace将对应的<pre>转换为可编辑的区域
	jsEditor : ace.edit('js-editor'),

	//-- 编辑器配置 是否自动补全等等
	setOptions:{
		enableBasicAutocompletion: true,
		enableSnippets: true,
		enableLiveAutocompletion: true
	},

    // 给编辑器设置主题样式
    setTheme: 'ace/theme/monokai',
}

TinyEditor.prototype = {
	init : function(){
		var self = this

		//-- 初始化设置编辑器样式
		buffer.jsEditor.session.setMode('ace/mode/javascript')
		buffer.jsEditor.setTheme(buffer.setTheme)
		buffer.jsEditor.setOptions(buffer.setOptions)
		buffer.jsEditor.moveCursorTo(0,0)
		buffer.jsEditor.resize(true)

		//-- ctrl+enter运行 快捷键
		document.onkeydown= function(e) { e=e||window.event
			kc=e.keyCode||e.charCode
			if ((kc == 13&&e.ctrlKey)) {
				self.run()
			}
		}

	},

	//-- 运行
	run:function(){
		var js = buffer.jsEditor.getValue()
        try {
            eval(js)
        }catch (e) {
            alert(e)
        }
	}

}
