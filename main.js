const inner = document.getElementById("content");
let output = ""
let globalDB
config = {
	locateFile: filename => `./dist/sql-wasm.wasm`
}
initSqlJs(config).then(function (SQL) {
	const xhr = new XMLHttpRequest();
	xhr.open('GET', 'https://raw.githubusercontent.com/xiaoWangSec/jable-spider/master/AV.db', true);
	xhr.responseType = 'arraybuffer';

	xhr.onload = e => {
		const uInt8Array = new Uint8Array(xhr.response);
		const db = new SQL.Database(uInt8Array);
		const contents = db.exec("SELECT * FROM AVdb ORDER BY random() limit 10");
		for (i in contents[0]['values']) {
			output += '<a href='+ contents[0]['values'][i][2] +'><img src="' + contents[0]['values'][i][3] + '"/></a>' + "\n";
		}
		inner.innerHTML = output;
	};
	xhr.send();

});


