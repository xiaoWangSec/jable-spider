var inner = document.getElementById("content");
var freshBtn = document.getElementById("fresh");
var output = ""
var db
config = {
	locateFile: filename => `./dist/sql-wasm.wasm`
}
initSqlJs(config).then(function (SQL) {
	const xhr = new XMLHttpRequest();
	xhr.open('GET', 'https://raw.githubusercontent.com/xiaoWangSec/jable-spider/master/AV.db', true);
	xhr.responseType = 'arraybuffer';

	xhr.onload = e => {
		const uInt8Array = new Uint8Array(xhr.response);
		db = new SQL.Database(uInt8Array);

		fr();
		getCount();

	};
	xhr.send();

});

function getCount() {
	const all = db.exec("SELECT COUNT(*) FROM AVdb");
	document.getElementById("totle").innerText = all[0]['values'][0];
}

function fr() {
	const contents = db.exec("SELECT * FROM AVdb ORDER BY random() limit 10");
	for (i in contents[0]['values']) {
		output += '<a href='+ contents[0]['values'][i][2] +' target="_blank"><img alt="'+ contents[0]['values'][i][0] +'"title="'+ contents[0]['values'][i][0] + '" src="' + contents[0]['values'][i][3] + '"/></a>' + "\n";
	}
	inner.innerHTML = output;
}
freshBtn.addEventListener("click", fr, true);

